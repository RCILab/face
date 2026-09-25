"""Rebuild FACE web media exclusively from the supplied PDF, PPTX and full video.

Requires pymupdf, Pillow, imageio-ffmpeg. Originals are never modified.
Run from any directory: python scripts/prepare_assets.py
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile
import xml.etree.ElementTree as ET

import imageio_ffmpeg
import pymupdf
from anonymize_paper import anonymize_paper
from prepare_full_video import prepare_full_video

ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT.parent / 'materials'
# name, embedded media number, slide, output width (no crop, retiming or overlays)
CLIPS = [('cup-nominal', 19, 3, 720),
 ('cup-vertical', 18, 3, 720),
 ('cup-horizontal', 17, 3, 720),
 ('cup-pvc', 16, 3, 720),
 ('cup-plastic', 15, 3, 720),
 ('cup-wet', 14, 3, 720),
 ('compare-nominal-face', 20, 5, 480),
 ('compare-wet-face', 21, 5, 480),
 ('compare-wrinkled-face', 22, 5, 480),
 ('compare-wrinkled-vision', 23, 5, 480),
 ('compare-nominal-vision', 24, 5, 480),
 ('compare-wet-vision', 25, 5, 480),
 ('compare-wet-observation', 26, 5, 480),
 ('compare-wrinkled-observation', 27, 5, 480),
 ('compare-nominal-observation', 28, 5, 480),
 ('compare-wet-direct', 29, 5, 480),
 ('compare-wrinkled-direct', 30, 5, 480),
 ('compare-nominal-direct', 31, 5, 480),
 ('compare-nominal-analytic', 32, 5, 480),
 ('compare-wet-analytic', 33, 5, 480),
 ('compare-wrinkled-analytic', 34, 5, 480),
 ('egg-direct', 35, 6, 342),
 ('egg-observation', 36, 6, 342),
 ('egg-analytic', 37, 6, 342),
 ('egg-vision', 38, 6, 342),
 ('egg-face', 39, 6, 342),
 ('wiping-unseen-direct', 41, 10, 960),
 ('wiping-nominal-direct', 42, 10, 960),
 ('wiping-wet-direct', 43, 10, 960),
 ('wiping-soapy-direct', 44, 10, 960),
 ('wiping-unseen', 45, 11, 960),
 ('wiping-nominal', 46, 11, 960),
 ('wiping-wet', 47, 11, 960),
 ('wiping-soapy', 48, 11, 960)]
FIGURES = {'architecture': (2, (82, 49, 538, 226)),
           'contact-estimation': (6, (56, 51, 552, 285))}

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--paper', type=Path, default=MATERIALS / '_2026__ICRA___FACE.pdf')
    parser.add_argument('--slides', type=Path, default=MATERIALS / 'FACE (2).pptx')
    parser.add_argument('--video', type=Path, default=MATERIALS / 'ICRA27_3998_VI_i-2.mp4')
    args = parser.parse_args()
    for folder in ['videos', 'images', 'pdfs']:
        (ROOT / 'static' / folder).mkdir(parents=True, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    def run(*args):
        subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', *map(str, args)], check=True)
    manifest = {'sources': {args.paper.name: sha(args.paper), args.slides.name: sha(args.slides)},
                'videos': [], 'images': [], 'slides': []}
    with tempfile.TemporaryDirectory(prefix='face-source-') as tmp, zipfile.ZipFile(args.slides) as z:
        for name in z.namelist():
            if re.fullmatch(r'ppt/media/media\d+\.[mM][pP]4', name):
                Path(tmp, Path(name).name).write_bytes(z.read(name))
        ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
        for i in range(1, 13):
            xml = ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
            rels = ET.fromstring(z.read(f'ppt/slides/_rels/slide{i}.xml.rels'))
            manifest['slides'].append({'slide': i, 'text': ' | '.join(x.text or '' for x in xml.findall('.//a:t', ns)),
                'embedded_media': sorted(set(r.attrib['Target'] for r in rels if r.attrib['Type'].endswith('/media')))})
        def encode(spec):
            name, number, slide, width = spec
            src = Path(tmp, f'media{number}.mp4' if number != 13 else 'media13.MP4')
            out = ROOT / f'static/videos/{name}.mp4'
            run('-threads', '2', '-i', src, '-map', '0:v:0', '-an', '-map_metadata', '-1', '-map_metadata:s:v', '-1', '-map_chapters', '-1', '-write_tmcd', '0',
                '-vf', f'scale={width}:-2,setsar=1', '-r', '30',
                '-c:v', 'libx264', '-threads', '2', '-crf', '23', '-preset', 'fast',
                '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out)
            poster = ROOT / f'static/images/{name}.jpg'
            run('-ss', '7', '-i', out, '-frames:v', '1', '-q:v', '2', poster)
            info = subprocess.run([ffmpeg, '-hide_banner', '-i', str(out)], capture_output=True, text=True).stderr
            timestamp = re.search(r'Duration: ([\d:.]+)', info)[1]
            h, m, s = map(float, timestamp.split(':'))
            print(f'{name}: {timestamp}', flush=True)
            return {'path': str(out.relative_to(ROOT)), 'source': args.slides.name,
                    'member': f'ppt/media/{src.name}', 'slide': slide,
                    'source_sha256': sha(src), 'sha256': sha(out),
                    'duration': h * 3600 + m * 60 + s,
                    'transform': f'Full source duration; H.264, width {width}, 30 fps, no audio track; no crop or retiming. Existing source speed labels retained.',
                    'poster': str(poster.relative_to(ROOT)), 'poster_time': 7, 'poster_sha256': sha(poster)}
        with ThreadPoolExecutor(max_workers=3) as pool:
            manifest['videos'] = list(pool.map(encode, CLIPS))
    full_video = prepare_full_video(args.video, ROOT)
    manifest['sources'][args.video.name] = full_video['source_sha256']
    manifest['videos'].append(full_video)
    manifest['paper'] = anonymize_paper(args.paper, ROOT / 'static/pdfs/face-paper.pdf')
    doc = pymupdf.open(args.paper)
    for name, (page, rect) in FIGURES.items():
        out = ROOT / f'static/images/{name}.png'
        doc[page - 1].get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=pymupdf.Rect(rect)).save(out)
        manifest['images'].append({'path': str(out.relative_to(ROOT)), 'source': args.paper.name,
            'page': page, 'crop_pdf_points': list(rect), 'sha256': sha(out), 'transform': 'Crop excludes paper caption; original diagram retained.'})
    (ROOT / 'scripts/media-manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f'Prepared {len(CLIPS)} videos, posters, {len(FIGURES)} paper images and the supplied PDF.')

if __name__ == '__main__':
    main()
