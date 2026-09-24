"""Draw two conceptual FACE animations, inspired by the supplied FFDP figures.

These are explanatory schematics, not experiment plots or FFDP cone constraints.
Run with Pillow and imageio-ffmpeg installed. Outputs: GIF, MP4, and PNG poster.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import math
import random
import subprocess
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
SIZE = (720, 340)
FPS = 15
COUNT = 120
COLORS = ['#527ca1', '#bd7c49', '#499074']
INK, MUTED = '#213e34', '#66786f'
FONT = next((p for p in [Path('C:/Windows/Fonts/segoeui.ttf'), Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')] if p.exists()), None)
if FONT is None:
    raise FileNotFoundError('Install Segoe UI or DejaVu Sans to reproduce the figures.')

class Frame:
    def __init__(self):
        self.image = Image.new('RGB', (SIZE[0]*2, SIZE[1]*2), 'white')
        self.draw = ImageDraw.Draw(self.image)
    def text(self, xy, text, size=17, fill=MUTED, anchor='mm'):
        self.draw.text(tuple(v*2 for v in xy), text, font=ImageFont.truetype(str(FONT), size*2), fill=fill, anchor=anchor)
    def line(self, points, fill, width=2):
        self.draw.line([(x*2,y*2) for x,y in points], fill=fill, width=width*2, joint='curve')
    def polygon(self, points, fill):
        self.draw.polygon([(x*2,y*2) for x,y in points], fill=fill)
    def circle(self, x, y, r, fill):
        self.draw.ellipse(((x-r)*2,(y-r)*2,(x+r)*2,(y+r)*2),fill=fill)
    def arrow(self, start, end, fill, width=3):
        self.line([start,end],fill,width)
        dx,dy=end[0]-start[0],end[1]-start[1]
        norm=math.hypot(dx,dy)
        if norm < 1: return
        ux,uy=dx/norm,dy/norm
        self.polygon([end,(end[0]-11*ux+5*uy,end[1]-11*uy-5*ux),(end[0]-11*ux-5*uy,end[1]-11*uy+5*ux)],fill)
    def finish(self):
        return self.image.resize(SIZE, Image.Resampling.LANCZOS)

rng=random.Random(47)
# A shared illustrative interaction distribution under three contact transforms.
samples=[(rng.gauss(0,1),rng.gauss(0,1)) for _ in range(52)]
centers=[(112,161),(227,154),(172,242)]
angles=[-.35,.4,-.8]
def factorization(t):
    f=Frame()
    f.text((178,30),'Physical forces',21,INK)
    f.text((556,30),'Shared interaction',21,INK)
    for j,(label,color) in enumerate(zip(['Smooth','Rough','Tilted'],COLORS)):
        x=92+j*85
        f.circle(x-26,64,4,color)
        f.text((x+5,64),label,13)
    f.arrow((323,177),(391,177),'#a2b2a4',2)
    f.text((357,203),'encode',13)
    # Rest, flow from measured forces into normalized coordinates, then hold.
    phase=max(0,min(1,(t-0.13)/0.50))
    blend=phase*phase*(3-2*phase)
    for i,(u,v) in enumerate(samples):
        for j,color in enumerate(COLORS):
            c,s=math.cos(angles[j]),math.sin(angles[j])
            ox,oy=centers[j]
            x=ox+27*u*c-11*v*s
            y=oy+27*u*s+11*v*c
            f.circle(x,y,2.5,['#dee7ec','#eee2d8','#dcebe4'][j])
            # Tiny, fixed offsets keep all three colors visible at convergence.
            target_x=556+23*u+(j-1)*2
            target_y=183+21*v+(j-1)*2
            px=x+(target_x-x)*blend
            py=y+(target_y-y)*blend-22*math.sin(math.pi*blend)
            f.circle(px,py,2.7,color)
    f.text((360,307),'Different surfaces. The same interaction pattern.',17,INK)
    return f.finish()

def wiping(t):
    f=Frame()
    f.text((182,30),'Rough surface',21,INK)
    f.text((539,30),'Smooth, curved surface',21,INK)
    f.line([(360,67),(360,280)],'#e6ebe4',1)
    # Move in the same direction on each surface; hold briefly at each end.
    phase=t*2*math.pi
    local_x=168-70*math.cos(phase)
    direction=1 if math.sin(phase)>=0 else -1
    for j in range(2):
        offset=12+j*356
        def height(x): return 185 if j==0 else 185+23*math.sin((x-70)/85)
        def slope(x): return 0 if j==0 else 23/85*math.cos((x-70)/85)
        surface=[(offset+x,height(x)) for x in range(28,318,3)]
        f.polygon(surface+[(offset+315,282),(offset+28,282)],'#edf1e9')
        f.line(surface,'#9bab95',2)
        if j==0:
            for x in range(35,310,14): f.line([(offset+x,193),(offset+x+5,199)],'#bdc9b7',1)
        x=offset+local_x; y=height(local_x)
        a=math.atan(slope(local_x)); tx,ty=math.cos(a),math.sin(a)
        nx,ny=-ty,tx
        # The tool follows the surface; normal loading stays fixed, tangential
        # force follows the surface-dependent friction scale (rho=1).
        mu=.85 if j==0 else .30
        force_x=62*(nx+direction*mu*tx)
        force_y=62*(ny+direction*mu*ty)
        f.arrow((x,y),(x+force_x,y+force_y),'#3c8666',4)
        trail=[(offset+k,height(k)-2) for k in range(98,int(local_x)+1,2)]
        if len(trail)>1: f.line(trail,'#9abfa2',3)
        # Small wiping pad and handle, aligned to the local contact surface.
        points=[(x+u*tx+v*nx,y+u*ty+v*ny) for u,v in [(-14,-2),(14,-2),(14,-13),(-14,-13)]]
        f.polygon(points,INK)
        f.line([(x-9*nx,y-9*ny),(x-42*nx,y-42*ny)],INK,5)
        f.arrow((x-46*nx,y-46*ny),(x-46*nx+direction*30*tx,y-46*ny+direction*30*ty),'#acb9b0',2)
    f.circle(196,310,4,'#3c8666')
    f.text((375,310),'Contact force adapts as the tool moves.',17,INK)
    return f.finish()

def export(name, draw_frame, poster_index):
    images=ROOT/'static/images'
    videos=ROOT/'static/videos'
    frames=[draw_frame(i/(COUNT-1)) for i in range(COUNT)]
    frames[poster_index].save(images/f'{name}.png')
    palette=frames[0].quantize(colors=128)
    indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(images/f'{name}.gif',save_all=True,append_images=indexed[1:],duration=[70,60,70]*40,loop=0,optimize=True,disposal=2)
    with TemporaryDirectory() as temp:
        for i,im in enumerate(frames): im.save(Path(temp)/f'{i:03d}.png')
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-y','-framerate',str(FPS),'-i',str(Path(temp)/'%03d.png'),'-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(videos/f'{name}.mp4')],check=True)
    print(f'Created {name}: GIF, MP4, poster (8-second loop).')

if __name__=='__main__':
    export('method-factorization',factorization,92)
    export('method-wiping',wiping,35)
