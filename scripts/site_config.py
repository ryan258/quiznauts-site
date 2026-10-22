"""Read Hugo's effective config using Hugo's own parser (Python 3.9+)."""
import json
import shutil
import subprocess


def load_config(root):
    binary = shutil.which("hugo")
    if not binary:
        raise SystemExit("Hugo extended is required. See README.md.")
    result = subprocess.run(
        [binary, "config", "--source", str(root), "--format", "json", "--printZero"],
        capture_output=True, text=True, check=True,
    )
    config = json.loads(result.stdout)
    config["baseURL"] = config["baseurl"]
    return config
