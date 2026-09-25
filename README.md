# FACE project page

**Contact-Aware Imitation Learning Through Contact Factorization**

A static HTML/CSS/JavaScript research project page. No build step or runtime dependencies.

## Content and layout

The page follows the local `../contact-aware-learning.github.io/` reference: an anonymous centered publication header, dark rounded resource links, a six-condition FACE cup teaser with one shared caption, followed by Abstract, the supplied full video, How FACE works, method comparisons, simultaneous generalization clips, and the contact factor estimation figure with one compact detail table, with restrained typography. Paper figure numbers and paper captions are excluded; the cup teaser has one web-specific caption.

Research framing and the revision plan are preserved in [REVISION_PLAN.md](REVISION_PLAN.md). The governing distinction is intended task behavior versus its contact-dependent physical realization. Policy parameters remain fixed at deployment; contact factors adapt execution. Policies are trained per task/object category, not one policy spanning all demonstrated tasks.

- `index.html`: anonymous project header, research explanation, experiment conditions and method comparisons.
- `static/css/face.css`: responsive layout.
- `static/js/face.js`: accessible condition tabs, viewport playback, persistent manual pauses, explicit muted autoplay on load, reload and condition changes.
- `static/katex/`, `static/js/math.js`: bundled KaTeX 0.16.11 (CSS, JS, woff2 fonts) typesetting the TeX source of `.math` elements; without JavaScript the TeX source stays visible.
- `scripts/media-manifest.json`: every published media asset's source, hash and conversion details.
- [MEDIA_TODO.md](MEDIA_TODO.md): Korean source audit and maintenance notes.

This is an anonymous review page. Do not add author names, affiliations, institutional URLs, contact details or identifying citation metadata. Paper and Code are disabled placeholders; Code includes the GitHub icon. The retained, unlinked PDF is a permanently redacted anonymous derivative; the source manuscript remains unchanged outside this site. No conference acceptance, arXiv link, code release or publication year is inferred. `noindex` remains in place.

## Preview

From this directory:

```sh
python3 -m pip install RangeHTTPServer
python3 -m RangeHTTPServer 8000 --bind 127.0.0.1
```

Open http://localhost:8000/. Range requests allow video seeking. Basic HTML viewing also works without a server.

## Rebuild media

Only these supplied files are used:

- `../materials/_2026__ICRA___FACE.pdf`
- `../materials/FACE (2).pptx`
- `../materials/ICRA27_3998_VI_i-2.mp4`

```sh
python3 -m pip install pymupdf Pillow imageio-ffmpeg
python3 scripts/prepare_assets.py
```

The script extracts 34 selected embedded videos from the PPTX, converts them to H.264 for browser compatibility, and creates posters. Source framing, full duration and existing speed labels are retained; no crop, speed change, outcome overlay, or extra end-frame hold is introduced. All 35 website videos contain no audio track; both preparation scripts explicitly discard audio. The full MP4 preserves its video stream without re-encoding, and appears after Abstract with manual playback. `scripts/anonymize_paper.py` creates the anonymous PDF by permanently removing the author/affiliation blocks, project URL, acknowledgements and PDF metadata. Rebuilding assets retains this anonymization.

The PPTX contains 48 embedded videos across 12 slide XML files. Repeated overview footage and the wet-cup clip inside method slides are not all duplicated on the page. The manifest lists all slides for traceability. Videos are not counted as independent evaluation trials.

## Verification

```sh
python3 -m pip install playwright RangeHTTPServer pymupdf
python3 -m playwright install chromium
python3 scripts/check_site.py --screenshots /tmp/face-check
```

The check launches its own local server. It validates local links and original-source hashes; all 35 video durations, decoding, playback and seeking; layouts at 1440, 960, 768, 390 and 320 px; every comparison tab and keyboard navigation; reload autoplay and manual pauses; anonymous HTML/PDF metadata and the requested section order and simultaneous generalization display; and no-JavaScript access to all conditions. Screenshots are written outside the site.

## Attribution

Layout reference: the local `contact-aware-learning.github.io` checkout, currently containing the [Nerfies](https://nerfies.github.io/) template. Original project-template attribution to the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template) is retained. Website license: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Formula typesetting: [KaTeX](https://katex.org/) 0.16.11, MIT license (`static/katex/LICENSE`). This notice does not assign a new license to the manuscript or experimental media.
