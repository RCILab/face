# FACE project page

Website for **Contact-Aware Imitation Learning Through Contact Factorization**.

Live page: https://rcilab.khu.ac.kr/face/

A static HTML/CSS/JavaScript site, with no build step, CDN, analytics, or runtime dependencies. GitHub Pages serves the root of `master`.

## Editing

- `index.html`: paper text, figures, experiments, and quantitative results.
- `static/css/face.css`: responsive layout and visual design.
- `static/js/face.js`: preview playback, video chapter links, and citation copy.
- `static/js/method-demo.js`: lightweight SVG decoder animation. Three selectable contact conditions illustrate Eqs. (6)-(7) with a fixed action; illustrative values are not experimental measurements. The loop pauses offscreen, supports manual pause/selection, and starts paused with reduced motion enabled.
- `MEDIA_TODO.md`: individual clip placeholders, source references, and replacement instructions (Korean).
- `static/pdfs/face-paper.pdf`: the supplied anonymous manuscript.
- `static/videos/face-final.mp4`: the final video with its original streams, remuxed for progressive playback.

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
python -m pip install pymupdf imageio-ffmpeg
python scripts/prepare_assets.py --paper "../_2026__ICRA___FACE (2).pdf" --video "../ICRA27_3998_VI_i-2.mp4"
```

The extraction script records the paper crop coordinates and video timestamps. It never modifies the source files. The full video is stream-copied, while only the short hero loop is re-encoded.

## Verification

```sh
python -m pip install playwright RangeHTTPServer
python scripts/check_site.py
```

The browser check uses an installed Microsoft Edge. It checks relative assets and anchors, responsive overflow at 1440/768/390/320 px, video playback and chapter seeking, reduced motion, preview pause/resume, citation copy, and a JavaScript-disabled fallback. Screenshots are saved outside the repository in `../working/`.

## Reference and attribution

The information flow was inspired by [CAMP-MPPI](https://rcilab.khu.ac.kr/CAMP-MPPI/) ([source](https://github.com/RCILab/CAMP-MPPI), reference revision `3173bb5`). A separate reference checkout is kept alongside this repository in `../reference-camp-mppi/`.

The original repository was generated from the [RCI paper page template](https://github.com/RCILab/RCI_paper_page_template), based on the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template) and [Nerfies](https://nerfies.github.io/). The draft replaces the sample content and front-end assets with a FACE-specific page.

Website license: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/), retained from the original template. This website notice does not assign a new license to the research manuscript or video.
