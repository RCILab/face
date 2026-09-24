"""Extract the condition galleries and remaining chapters of the final video.

Usage: python scripts/prepare_gallery.py --video ../ICRA27_3998_VI_i-2.mp4
Requires imageio-ffmpeg. Crops are views of existing footage, not new trials.
Original timing is retained; selected outcome frames receive a one-second hold.
"""
import argparse
import json
from pathlib import Path
import subprocess
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--video', type=Path, required=True)
args = parser.parse_args()
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

# name, source start (s), source duration (s), crop filter, hold (s), poster offset (s)
CLIPS = [
    ('handheld-demo', 25.5, 16, None, 0, 5),
    ('robot-transfer', 43.7, 3, None, 0, 1),
    ('method-walkthrough', 101.2, 25, None, 0, 4),
    ('cup-baselines', 68, 10.2, None, 1, 5),
    ('cup-nominal', 47, 11.2, 'crop=426:360:0:0', 1, 6),
    ('cup-vertical', 47, 11.2, 'crop=428:360:426:0', 1, 6),
    ('cup-horizontal', 47, 11.2, 'crop=426:360:854:0', 1, 6),
    ('cup-pvc', 47, 11.2, 'crop=426:360:0:360', 1, 6),
    ('cup-plastic', 47, 11.2, 'crop=428:360:426:360', 1, 6),
    ('cup-wet', 47, 11.2, 'crop=426:360:854:360', 1, 6),
    # Remove the montage-wide title at the top; retain the tool, plate, result,
    # and condition labels. Original playback speeds are stated in the cards.
    ('wiping-nominal', 145, 10.6, 'crop=640:260:0:455', 1, 5),
    ('wiping-wet', 145, 10.6, 'crop=640:260:0:95', 1, 5),
    ('wiping-soapy', 145, 10.6, 'crop=640:260:640:95', 1, 5),
    ('wiping-unseen', 145, 10.6, 'crop=640:260:640:455', 1, 5),
    ('wiping-baseline', 132.5, 8.2, None, 1, 3),
    ('surface-preparation', 142, 3, None, 0, 1.5),
]

def run(*options):
    subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', *map(str, options)], check=True)

manifest = []
for name, start, duration, crop, hold, poster in CLIPS:
    filters = [crop] if crop else ['scale=960:-2']
    if hold:
        filters.append(f'tpad=stop_mode=clone:stop_duration={hold}')
    run('-ss', start, '-t', duration, '-i', args.video, '-an', '-vf', ','.join(filters), '-r', '30', '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', ROOT / f'static/videos/{name}.mp4')
    run('-ss', start + poster, '-i', args.video, '-frames:v', '1', '-vf', filters[0], '-q:v', '3', ROOT / f'static/images/{name}.jpg')
    manifest.append({'name': name, 'source_start': start, 'source_end': round(start + duration, 2), 'crop': crop, 'hold_seconds': hold, 'duration': round(duration + hold, 2)})
    print(f'{name}: {start:g}-{start+duration:g}s' + (f', {crop}' if crop else ''), flush=True)
(ROOT / 'scripts/gallery-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
