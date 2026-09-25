"""Prepare the supplied full video with no audio, preserving the video stream."""
from pathlib import Path
import hashlib
import re
import subprocess
import imageio_ffmpeg

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def prepare_full_video(source, root):
    source, root = Path(source), Path(root)
    out = root / 'static/videos/face-full.mp4'
    poster = root / 'static/images/face-full.jpg'
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
        '-map', '0:v:0', '-an', '-c:v', 'copy', '-map_metadata', '-1',
        '-map_metadata:s', '-1', '-map_chapters', '-1', '-movflags', '+faststart', str(out)], check=True)
    subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-ss', '15', '-i', str(out),
        '-frames:v', '1', '-q:v', '2', str(poster)], check=True)
    info = subprocess.run([ffmpeg, '-hide_banner', '-i', str(out)], capture_output=True, text=True).stderr
    h, m, s = map(float, re.search(r'Duration: ([\d:.]+)', info)[1].split(':'))
    return {'path': str(out.relative_to(root)), 'source': source.name,
        'source_sha256': sha(source), 'sha256': sha(out), 'duration': h*3600+m*60+s,
        'transform': 'Full supplied video; video stream copied without crop, retiming or re-encoding; no audio track. Source metadata removed; MP4 faststart enabled.',
        'poster': str(poster.relative_to(root)), 'poster_time': 15, 'poster_sha256': sha(poster)}
