# Quiznauts marketing artwork

Edition 1.0, October 22, 2026. Fourteen composed campaign assets accompany the local Hugo site. Each has a self-contained SVG master, a full-resolution PNG upload export and a lossless WebP copy. They use the current v1.4 Atomic Advertising character geometry, including the viewer-right temple patch, white forehead and eye surrounds, one simple helmet collar, round paws and oval feet. No new image-generation call was used for this kit.

The working campaign voice is “Come for the cow. Leave knowing more.” This is local campaign copy, not evidence of an approved public tagline or a launched account. There are no invented handles, URLs, audiences, upload dates, subscriber counts, fixed schedules or endorsements in the art.

## Inventory

| File stem | Pixels | Intended use |
| --- | ---: | --- |
| `quiznauts-avatar` | 1024 × 1024 | Shared profile avatar; circular crop friendly |
| `quiznauts-youtube-banner` | 2560 × 1440 | Channel banner with a conservative center guide |
| `quiznauts-youtube-thumbnail` | 3840 × 2160 | Editable evergreen video invitation |
| `quiznauts-youtube-end-card` | 1920 × 1080 | End-card background; open placement panel |
| `quiznauts-open-graph` | 1200 × 630 | Site metadata and link previews |
| `quiznauts-brand-square` | 1080 × 1080 | Introductory brand post |
| `quiznauts-feed-portrait` | 1080 × 1350 | Portrait feed introduction |
| `quiznauts-vertical-invitation` | 1080 × 1920 | Vertical still for short-form properties |
| `quiznauts-question-card` | 1080 × 1080 | First Contact ocean question |
| `quiznauts-explanation-card` | 1080 × 1080 | Answer, short explanation and source credit |
| `quiznauts-wide-profile-header` | 1500 × 500 | Wide profile header for testing in X/Bluesky |
| `quiznauts-facebook-cover` | 1640 × 624 | Community cover for testing in Facebook |
| `quiznauts-pinterest-poster` | 1000 × 1500 | Tall curiosity poster |
| `quiznauts-video-watermark` | 300 × 300 | Transparent Q-orbit corner mark |

Sources are in `static/marketing/svg/`; upload exports are in `static/marketing/png/` and web copies in `static/marketing/webp/`. The gallery uses WebP previews and offers all three formats. `data/marketing.json` owns titles, dimensions, alt text, usage notes and suggested safe rectangles. The `/media/` page reads that data. These are fourteen different compositions, rather than one design clipped to many shapes.

## Verified requirements and production choices

Official primary sources were checked October 22, 2026. Platform guidance can change. “Production choice” means a useful editable master size; it does not assert an official minimum, recommended size or verified upload/crop result.

- YouTube recommends a 2560 × 1440 banner. Its minimum is 2048 × 1152; at that minimum its text/logo safe area is 1235 × 338, with cropping by device. This kit centers a slightly conservative 1540 × 420 guide at `(510,510)` on its larger canvas. The banner PNG is approximately 0.21 MB, below the 6 MB limit. [YouTube branding guidance](https://support.google.com/youtube/answer/10456525?hl=en).
- YouTube’s current thumbnail recommendation is 3840 × 2160 for video. The shipped thumbnail follows that size, 16:9, and is approximately 0.51 MB. Account verification and the actual content/upload flow remain separate. [YouTube thumbnail guidance](https://support.google.com/youtube/answer/72431?hl=en).
- YouTube accepts static profile PNGs up to 15 MB and renders the image at 98 × 98. The kit’s 1024-square avatar is our production choice. Its 300-square watermark exceeds the official 150-square minimum and is under the 1 MB limit. Watermarks have audience-designation restrictions; the art does not determine a video’s designation. [YouTube branding guidance](https://support.google.com/youtube/answer/10456525?hl=en).
- Pinterest’s official creative guidance recommends 2:3 or 1000 × 1500 for standard image creative. The tall poster follows that ratio and size. This does not establish a verified Pin, account, destination or campaign. [Pinterest creative guidance](https://business.pinterest.com/en-gb/creative-best-practices/), [Pinterest product specifications](https://help.pinterest.com/en/business/article/pinterest-product-specs).
- Other export sizes and all non-YouTube safe rectangles are production choices. The vertical guide is conservative for our layout, not a measured guarantee against each service’s controls, subtitles, search labels or future UI. The end-card panel is a suggested working space; actual clickable elements must be positioned and checked in Studio. Open Graph crops, profile-photo overlaps and live upload acceptance have not been verified.

No account has been created, modified, connected or published through this work. Do not add a guessed domain to a graphic. Add real destinations to the site’s property registry once they exist, then use the verified destination in the post composer.

## Accessible use

Reading copy uses ink/teal on cream, cream on teal, or teal on mustard. Orange and unsupported low-contrast pairs remain decorative. The mascot stays unchanged; backgrounds keep its shape distinct. Primary copy avoids sitting behind the illustration. All fourteen exports are static; there is no animation, strobe, countdown or autoplay.

A graphic is an image of text. Repeat the question, choices, answer or campaign sentence in the accompanying post’s readable text. Use the `alt` description from `data/marketing.json` as a starting point. For paired question/explanation posts, keep both cards together and include the source link. Platform compression, a tiny feed preview and a nominal safe rectangle do not prove readable final text. Check the actual platform preview, circular crop and smallest useful size before saving. No browser, live social composer, screen reader or assistive-technology verification was performed for this kit.

The ocean pair is tied to question `fc-ocean-pacific` in `data/quick_mission.json`. It asks about ocean-basin area, gives Pacific as answer B, and credits NOAA. The generator checks the expected question and explanation before reproducing the pair. If this question changes, review and update the paired art and caption together. [NOAA source](https://oceanservice.noaa.gov/facts/biggestocean.html).

## Editing and recovery

Hugo serves the saved static files; generating artwork is optional. The checkout has no commits yet. Source copy and placement live in `scripts/generate-art.py`. The script reuses unchanged canonical brand SVG geometry. It outlines headlines with locally installed Futura Condensed Extra Bold and body copy with Avenir Next Demi Bold through macOS CoreText, then uses AppKit for native PNG rendering. It fails if those named fonts are unavailable. The generator is safe to import and renders the complete SVG/PNG batch into a temporary folder before replacing saved masters; `./qn art` makes a source checkpoint before starting. The SVG exports need no fonts, external links or embedded raster images; no font files are shipped.

On macOS with Python 3, Swift, cwebp and those fonts already present, regenerate the complete asset set with a local backup first:

```sh
./qn art
```

This command is a local artwork authoring helper, not a Hugo build dependency or a cross-platform font installer. Keep the current exports if the authoring fonts/runtime are unavailable. Edit the Python strings to revise copy; outlined SVG letters themselves are editable vector shapes rather than live text. Export PNGs at the dimensions listed above after changes, then run `./qn images` to refresh WebPs and download kits if using the lower-level generator directly. `./qn art` completes those steps for you. The generator retains WebP paths in the inventory; the local gate rejects stale copies.

## Local evidence

- All 14 SVGs parse, have unique IDs within each file, and contain no `script`, `foreignObject`, `image`, live `text` or external `href`.
- All 14 PNG headers match manifest dimensions; all are below 0.51 MB.
- Native render review covered the full contact sheet and detailed avatar, banner, vertical, question, square, feed and tall-poster views. Overlap found between mascot feet and footer copy during review was corrected before the final exports.
- Review does not establish platform upload acceptance, device crops, readable final compressed text, clickable end-screen placement, account ownership or public readiness.

## Lossless web copies

Ryan selected preservation of the original designs on October 22. All 22 source PNGs have full-size WebP derivatives: eight mascots under `static/brand/webp/mascot/` and fourteen campaign images under `static/marketing/webp/`. The mascots and video watermark retain transparency. The other thirteen keep their deliberate cream/teal compositions. White fur, helmet areas and internal panels are never removed by color matching.

The 22 PNGs total 3,200,449 bytes; WebPs total 992,174 bytes, a 69.0% reduction. Marketing gallery image bytes fall from 2,270,085 to 682,548 (69.9%). This is a byte comparison of full-size assets, not a browser-load timing or an additional reduction to the SVG-based homepage. PNG originals, SVG masters and the PNG Open Graph image remain for upload compatibility and recovery. Both ZIPs include WebPs; retaining both formats increases download-kit size.

The optional local encoder is `cwebp` from libwebp, already installed for this conversion. Regenerate with:

```sh
./qn images
```

This uses lossless encoding, `-z 9 -exact -metadata none`, without resizing or flattening alpha. It adds no build/runtime package and makes no provider call. `docs/image-optimization.json` records encoder version, options, dimensions, byte sizes and source/export SHA-256 hashes. `./qn check` reads the saved receipt and VP8L headers with the standard library to reject missing, stale or dimension-mismatched derivatives. Pixel and alpha equivalence were checked separately during this migration; header/hash checks alone are not a recurring pixel decoder.

After regenerating SVG/PNG campaign art, run `./qn images`, then `./qn check`. Ordinary Hugo build and preview commands use the saved WebPs and do not run the encoder. Browser screenshot evidence stays in PNG because it records a browser capture rather than a public image asset.
