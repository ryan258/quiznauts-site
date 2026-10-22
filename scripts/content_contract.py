"""Offline content and URL contracts. Ownership and factual review stay human."""
from pathlib import Path
import json
import re
from urllib.parse import urlsplit


def read_json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise ValueError(f"Cannot read {path}: {error}") from error


def http_url_error(value, policy, base=False):
    if not isinstance(value, str) or not value or any(c.isspace() or ord(c) < 32 for c in value):
        return "use a nonempty HTTP(S) URL without whitespace"
    try:
        url = urlsplit(value)
        host = url.hostname or ""
        port = url.port  # Validate malformed ports even when no request is made.
    except ValueError:
        return "malformed URL or port"
    if url.scheme not in policy["schemes"] or not url.netloc or url.username is not None or url.password is not None:
        return "use HTTP(S) with a public domain and no embedded credentials"
    if len(host) > 253 or not re.fullmatch(policy["host_pattern"], host) or re.search(policy["blocked_host_pattern"], host):
        return "use a real public domain, not a local, reserved or numeric host"
    if port is not None and not 1 <= port <= 65535:
        return "port must be between 1 and 65535"
    if base and (url.query or url.fragment):
        return "the site base URL cannot have a query or fragment"
    return ""


def destination_errors(platforms, policy):
    if not isinstance(platforms, list):
        return ["Properties must contain a platforms list."]
    errors, seen = [], set()
    for platform in platforms:
        if not isinstance(platform, dict) or not isinstance(platform.get("id"), str):
            errors.append("Every platform needs an id.")
            continue
        identity = platform["id"]
        if not identity or identity in seen:
            errors.append("Platform IDs must be nonempty and unique: " + identity)
        seen.add(identity)
        value = platform.get("url")
        if value == "":
            continue
        problem = http_url_error(value, policy)
        if problem:
            errors.append(f"{identity} destination: {problem}.")
    return errors


def mission_catalog(root):
    registry = read_json(root / "data/missions.json")
    if not isinstance(registry, dict) or not registry:
        raise ValueError("data/missions.json must map mission IDs to data names.")
    catalog = {}
    for identity, name in registry.items():
        if not isinstance(identity, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identity):
            raise ValueError("Invalid mission ID in data/missions.json.")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", name):
            raise ValueError("Mission data names must be simple names inside data/.")
        mission = read_json(root / "data" / (name + ".json"))
        if not isinstance(mission, dict) or mission.get("id") != identity:
            raise ValueError("Mission data identity does not match registry: " + identity)
        catalog[identity] = mission
    return catalog


def validate_mission(mission, policy):
    errors = []
    identity = mission.get("id", "unknown")
    for key in ("title", "intro"):
        if not isinstance(mission.get(key), str) or not mission[key].strip():
            errors.append(f"{identity}: missing {key}.")
    questions = mission.get("questions")
    if not isinstance(questions, list) or not questions:
        return errors + [f"{identity}: questions must be a nonempty list."]
    seen = set()
    for row in questions:
        if not isinstance(row, dict):
            errors.append(f"{identity}: each question must be an object.")
            continue
        qid = row.get("id")
        if not isinstance(qid, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", qid) or qid in seen:
            errors.append(f"{identity}: question IDs must be valid and unique.")
        else:
            seen.add(qid)
        for key in ("prompt", "explanation"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                errors.append(f"{identity}/{qid}: missing {key}.")
        choices = row.get("choices")
        if not isinstance(choices, list) or len(choices) != 3 or not all(isinstance(c, dict) for c in choices):
            errors.append(f"{identity}/{qid}: expected three choices.")
        elif [c.get("id") for c in choices] != ["A", "B", "C"] or any(not isinstance(c.get("text"), str) or not c["text"].strip() for c in choices) or len({c["text"].strip().casefold() for c in choices}) != 3:
            errors.append(f"{identity}/{qid}: choices must be distinct nonempty A/B/C values.")
        if row.get("answer") not in ("A", "B", "C"):
            errors.append(f"{identity}/{qid}: invalid answer.")
        source = row.get("source")
        if not isinstance(source, dict) or not isinstance(source.get("title"), str) or not source["title"].strip() or http_url_error(source.get("url"), policy) or not source.get("url", "").startswith("https://"):
            errors.append(f"{identity}/{qid}: source needs a title and public HTTPS URL.")
    return errors


def content_errors(root):
    policy = read_json(root / "data/url_policy.json")
    properties = read_json(root / "data/properties.json")
    if not isinstance(properties, dict):
        raise ValueError("data/properties.json must be an object with a platforms list.")
    errors = destination_errors(properties.get("platforms"), policy)
    for mission in mission_catalog(root).values():
        errors.extend(validate_mission(mission, policy))
    # This is the deliberately small website sample, not a compiler bank.
    sample = read_json(root / "data/quick_mission.json")
    if not isinstance(sample, dict) or sample.get("id") != "first-contact" or not isinstance(sample.get("questions"), list) or len(sample["questions"]) != 3:
        errors.append("First Contact must remain the recorded three-question sample.")
    return errors
