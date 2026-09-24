"""Extract website assets from the supplied paper and final video.

Usage: python scripts/prepare_assets.py --paper PATH --video PATH
Requires: pymupdf, Pillow, imageio-ffmpeg. No build tools are needed to serve the site.
"""
import argparse
from pathlib import Path
import shutil
import subprocess

import imageio_ffmpeg
import pymupdf

parser = argparse.ArgumentParser()
parser.add_argument('--paper', type=Path, required=True)
parser.add_argument('--video', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
for folder in ('images', 'videos', 'pdfs'):
    (root / 'static' / folder).mkdir(parents=True, exist_ok=True)
shutil.copyfile(args.paper, root / 'static/pdfs/face-paper.pdf')
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

def run(*options):
    subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', *map(str, options)], check=True)

# Preserve the final video streams; move the MP4 index to the front for web playback.
run('-i', args.video, '-map', '0', '-c', 'copy', '-movflags', '+faststart', root / 'static/videos/face-final.mp4')
# Include all six original Success overlays, then hold that frame for one second.
run('-ss', '48', '-t', '10.2', '-i', args.video, '-an', '-vf', 'scale=960:-2,tpad=stop_mode=clone:stop_duration=1', '-r', '30', '-c:v', 'libx264', '-crf', '25', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', root / 'static/videos/hero-loop.mp4')
# Standalone experiment clips retain their original outcomes and method labels.
for name, start, duration in [('cup-comparison', '47', '11.2'), ('egg-comparison', '81.5', '15.7')]:
    run('-ss', start, '-t', duration, '-i', args.video, '-an', '-vf', 'tpad=stop_mode=clone:stop_duration=1', '-r', '30', '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', root / f'static/videos/{name}.mp4')
for name, second in [('hero', 53), ('video', 0.5), ('demonstration', 30), ('geometry', 54), ('eggs', 90), ('wiping', 150)]:
    run('-ss', second, '-i', args.video, '-frames:v', '1', '-q:v', '2', root / f'static/images/{name}.jpg')

doc = pymupdf.open(args.paper)
# Page indexes are zero based; crop rectangles are PDF points, excluding captions.
figures = {
    'overview': (0, (312, 144, 560, 268)),
    'architecture': (1, (82, 49, 538, 226)),
    'hardware': (4, (55, 50, 548, 187)),
    'failure-modes': (4, (54, 245, 300, 324)),
    'contact-estimation': (5, (56, 51, 552, 285)),
    'rollouts': (6, (54, 298, 299, 546)),
}
for name, (page, rect) in figures.items():
    doc[page].get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=pymupdf.Rect(rect)).save(root / f'static/images/{name}.png')
print('Prepared paper, final video, hero and experiment clips, posters, and six paper figures.')
