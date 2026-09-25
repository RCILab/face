# FACE project page

Website for **Contact-Aware Imitation Learning Through Contact Factorization**.

A static HTML/CSS/JavaScript site, with no build step, CDN, analytics, or runtime dependencies. GitHub Pages serves the root of `master`.

## Editing

- `index.html`: teaser, abstract, video, method, experiments, generalization, and contact factor estimation.
- `static/css/face.css`: responsive layout and visual design.
- `static/js/face.js`: cup-condition tabs, viewport playback of research clips, and persistent manual pauses. Native controls remain available.
- `static/js/math.js`, `static/katex/`: bundled KaTeX 0.16.11 (CSS, JS, woff2 fonts, MIT license) typesetting the TeX formulas of the estimation table.
- `static/videos/`: 34 experiment clips extracted from the supplied slides and `face-full.mp4`, the full video with its original stream, remuxed for progressive playback.
- `static/images/`: video posters, and the architecture (`architecture.png`) and contact factor estimation (`contact-estimation.png`) figures cropped from the paper without captions.
- `static/pdfs/face-paper.pdf`: anonymized copy of the supplied manuscript.
- `scripts/prepare_assets.py`, `scripts/prepare_full_video.py`, `scripts/anonymize_paper.py`: rebuild the media and the anonymized PDF from the supplied sources.
- `scripts/media-manifest.json`: source, hash, and conversion details of every published media file.
- `scripts/check_site.py`: asset, anonymity, and browser checks.
- `MEDIA_TODO.md`, `REVISION_PLAN.md`, `COPY_REVIEW.md`: media source audit, page plan, and wording review (Korean and English).

The first draft retains anonymous authors and `noindex`. Publication metadata and author names should be updated when supplied; no acceptance status or release date is assumed.

## Local preview

```sh
python -m pip install RangeHTTPServer
python -m RangeHTTPServer 8000
```

Open http://localhost:8000/. A range-capable preview server supports seeking in the video before the entire file downloads, as GitHub Pages does. The main content, PDF, video, navigation, and expandable results also work without JavaScript.

## Regenerate supplied media

Optional authoring tools (not required to serve the site):

```sh
python -m pip install pymupdf Pillow imageio-ffmpeg
python scripts/prepare_assets.py
```

By default the script reads `../materials/_2026__ICRA___FACE.pdf`, `../materials/FACE (2).pptx`, and `../materials/ICRA27_3998_VI_i-2.mp4` without modifying them. The full video is stream-copied; the clips embedded in the slides are re-encoded. `scripts/media-manifest.json` records each file's source, hash, and paper crop coordinates. Clips are not counted as independent evaluation trials.

## Verification

```sh
python -m pip install playwright RangeHTTPServer
python scripts/check_site.py
```

The browser check uses an installed Microsoft Edge. It checks relative assets and anchors, responsive overflow at 1440/768/390/320 px, all 18 research clips and their durations, video playback and seeking, viewport playback with persistent manual pauses, reduced motion for the hero, GIF animation and pause/resume, citation copy, and a JavaScript-disabled fallback. Screenshots are saved outside the repository in `../working/`.

## Reference and attribution

The layout follows a local checkout of the [Nerfies](https://nerfies.github.io/) template kept alongside this repository in `../contact-aware-learning.github.io/`. The original project template is based on the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template) and Nerfies. The page replaces the sample content and front-end assets with FACE-specific ones.

Website license: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/), retained from the original template. This website notice does not assign a new license to the research manuscript or video.
