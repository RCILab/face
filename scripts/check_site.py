"""Validate local assets, supplied-source provenance and real browser behavior.

Install playwright and RangeHTTPServer; run `playwright install chromium` once.
Run: python scripts/check_site.py --screenshots /tmp/face-check
"""
import argparse
from contextlib import contextmanager
import hashlib
from html.parser import HTMLParser
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import threading
from urllib.parse import urlsplit, unquote
import zipfile
import re

ROOT = Path(__file__).resolve().parents[1]

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs, self.videos, self.sources = [], [], [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        for key in ['src', 'href', 'poster']:
            if key in attrs: self.refs.append(attrs[key])
        if tag == 'video': self.videos.append(attrs)
        if tag == 'source': self.sources.append(attrs['src'])

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate_assets():
    parser = PageParser()
    html = (ROOT / 'index.html').read_text()
    parser.feed(html)
    assert len(parser.ids) == len(set(parser.ids)), 'Duplicate element IDs'
    for ref in parser.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc: continue
        if url.path: assert (ROOT / unquote(url.path)).is_file(), ref
        elif url.fragment: assert url.fragment in parser.ids, ref
    assert html.count('<figcaption') == 1 and 'Figure ' not in html and 'Anonymous Authors' not in html
    manifest = json.loads((ROOT / 'scripts/media-manifest.json').read_text())
    assert set(parser.sources) == {v['path'] for v in manifest['videos']}
    assert len(parser.sources) == 35
    assert all('controls' in v and 'playsinline' in v and 'poster' in v for v in parser.videos)
    for v in manifest['videos']:
        assert sha(ROOT / v['path']) == v['sha256'], v['path']
        assert sha(ROOT / v['poster']) == v['poster_sha256'], v['poster']
    for v in manifest['images']:
        assert sha(ROOT / v['path']) == v['sha256'], v['path']
    keep = {v['path'] for v in manifest['videos']}
    assert {str(p.relative_to(ROOT)) for p in (ROOT / 'static/videos').iterdir()} == keep
    materials = ROOT.parent / 'materials'
    for filename, digest in manifest['sources'].items():
        assert sha(materials / filename) == digest, filename
    assert sha(ROOT / 'static/pdfs/face-paper.pdf') == manifest['paper']['sha256']
    validate_anonymity(html, materials)
    with zipfile.ZipFile(materials / 'FACE (2).pptx') as z:
        for v in manifest['videos']:
            if 'member' in v:
                assert hashlib.sha256(z.read(v['member'])).hexdigest() == v['source_sha256'], v['member']
            else:
                assert sha(materials / v['source']) == v['source_sha256']
    print('PASS: all local links, anchors, 35 videos, posters, diagrams, and source hashes', flush=True)
    return manifest


def validate_anonymity(html, materials):
    import pymupdf
    source = pymupdf.open(materials / '_2026__ICRA___FACE.pdf')
    anonymous = pymupdf.open(ROOT / 'static/pdfs/face-paper.pdf')
    # Derive identifying strings from the source; never duplicate them in public scripts.
    words = re.findall(r'[A-Za-z]+', source[0].get_text(clip=pymupdf.Rect(54, 101, 558, 127)))
    identities = [' '.join(words[i:i+2]).lower() for i in range(0, len(words), 2)]
    identities += [f'{words[i+1]}, {words[i]}'.lower() for i in range(0, len(words), 2)]
    domains = re.findall(r'(?:https?://|@)([a-zA-Z0-9.-]+)', source[0].get_text())
    identities += [domain.rstrip('.').lower() for domain in domains]
    affiliation = ' '.join(block[4] for block in source[0].get_text('blocks') if 693 < block[1] < 710)
    identities += [re.sub(r'\s+', ' ', part).strip(' ,.').lower() for part in re.split(r'\d+', affiliation) if part.strip()]
    public_texts = [p for p in ROOT.rglob('*') if '.git' not in p.parts and p.suffix in {'.html','.md','.js','.json','.py','.svg','.css'}]
    for path in public_texts:
        text = re.sub(r'\s+', ' ', path.read_text()).lower()
        assert all(identity not in text for identity in identities), f'Identifying content: {path}'
    pdf_text = re.sub(r'\s+', ' ', ' '.join(page.get_text() for page in anonymous)).lower()
    assert all(identity not in pdf_text for identity in identities), 'Identifying PDF text'
    assert 'acknowledgements' not in pdf_text
    assert not anonymous.metadata.get('author') and not anonymous.metadata.get('creator')
    assert not anonymous.get_xml_metadata() and not anonymous.embfile_names()
    assert not any(link.get('uri') for page in anonymous for link in page.get_links())
    assert len(source) == len(anonymous) == 8
    assert 'citation_author' not in html and 'id="BibTeX"' not in html
    order = ['teaser', 'abstract', 'video', 'method', 'experiments', 'generalization', 'estimation']
    assert [html.index(f'id="{name}"') for name in order] == sorted(html.index(f'id="{name}"') for name in order)
    # The only table is the compact estimation-detail table below the wiping section.
    assert html.count('<table') == 1 and html.index('<table') > html.index('id="estimation"')
    assert 'Watch demos' not in html and 'static/videos/teaser-geometry.mp4' not in html
    print('PASS: anonymous page/PDF; cup teaser, abstract, full video, distinct experiments and estimation table', flush=True)

@contextmanager
def server():
    from RangeHTTPServer import RangeRequestHandler
    class Handler(RangeRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT), **kwargs)
        def log_message(self, *args): pass
        def do_GET(self):
            try:
                super().do_GET()
            except (BrokenPipeError, ConnectionResetError):
                pass  # Browsers cancel in-flight range requests when seeking.
    httpd = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try: yield f'http://127.0.0.1:{httpd.server_port}/'
    finally:
        httpd.shutdown()
        httpd.server_close()

def browser_checks(manifest, screenshots):
    from playwright.sync_api import sync_playwright
    screenshots.mkdir(parents=True, exist_ok=True)
    with server() as base, sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('response', lambda r: errors.append(f'{r.status}: {r.url}') if r.status >= 400 else None)
        page.goto(base, wait_until='networkidle')
        # Every TeX source in the estimation tables is typeset by the bundled KaTeX.
        assert page.locator('.math').count() == page.locator('.math > .katex').count() > 0
        assert page.locator('.publication-links button:disabled').count() == 2
        assert page.locator('.publication-links a').count() == 0
        assert page.locator('.publication-links').inner_text().split() == ['Paper', 'Code']
        assert page.locator('.github-icon').count() == 1
        assert page.locator('#teaser video').count() == 6
        assert page.locator('#teaser figcaption').count() == 1
        assert page.locator('#experiments .condition-grid').count() == 0
        assert page.locator('#generalization video:visible').count() == 8
        assert page.locator('#generalization [role="tab"]').count() == 0
        assert page.locator('#full-video').evaluate('(v) => !v.autoplay && !v.loop && !v.classList.contains("research-clip")')
        for width in [1440, 960, 768, 390, 320]:
            page.set_viewport_size({'width': width, 'height': 1000 if width > 500 else 844})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Overflow at {width}'
            page.screenshot(path=str(screenshots / f'face-{width}.png'), full_page=True)
        assert page.locator('#full-video').evaluate('(v) => v.paused')
        print('PASS: five responsive widths and manual full-video playback', flush=True)
        page.set_viewport_size({'width': 1440, 'height': 1000})
        for group, count in [('cup', 3)]:
            for i in range(count):
                tab = page.locator(f'#{group}-tab-{i}')
                tab.click()
                assert page.locator(f'#{group}-panel-{i}').is_visible()
                assert tab.get_attribute('aria-selected') == 'true'
                for j in range(count):
                    assert page.locator(f'#{group}-panel-{j}').is_visible() == (i == j)
            page.locator(f'#{group}-tab-{count-1}').press('Home')
            assert page.locator(f'#{group}-tab-0').evaluate('(e) => e === document.activeElement')
            page.locator(f'#{group}-tab-0').press('ArrowRight')
            assert page.locator(f'#{group}-tab-1').get_attribute('aria-selected') == 'true'
        print('PASS: all comparison conditions and keyboard tab navigation', flush=True)
        # Decode and seek every supplied clip, including panels hidden by the tabs.
        for item in manifest['videos']:
            result = page.evaluate('''async ({path}) => {
              // Isolate decoding from viewport autoplay, which pauses off-screen clips.
              const source = [...document.querySelectorAll('video')].find(v => v.querySelector('source').getAttribute('src') === path);
              const v = source.cloneNode(true);
              v.muted = true;
              v.autoplay = false;
              v.load();
              await new Promise((resolve, reject) => {
                if (v.readyState >= 1) return resolve();
                v.addEventListener('loadedmetadata', resolve, {once: true});
                v.addEventListener('error', () => reject(new Error(path + ': media error')), {once: true});
                setTimeout(() => reject(new Error(path + ': metadata timeout')), 10000);
              });
              await v.play();
              await new Promise(r => setTimeout(r, 160));
              v.pause();
              const advanced = v.currentTime > 0;
              const target = v.duration * .65;
              await new Promise((resolve, reject) => {
                v.addEventListener('seeked', resolve, {once: true});
                v.currentTime = target;
                setTimeout(() => reject(new Error(path + ': seek timeout')), 10000);
              });
              return {duration: v.duration, advanced, seek: Math.abs(v.currentTime - target) < .1, width: v.videoWidth};
            }''', {'path': item['path']})
            assert abs(result['duration'] - item['duration']) < .12, item['path']
            assert result['advanced'] and result['seek'] and result['width'] > 0, item['path']
        print('PASS: all 35 videos decode, play and seek at their recorded durations', flush=True)
        # Fresh page isolates interaction tests from the exhaustive decoder check.
        page.goto(base, wait_until='networkidle')
        page.emulate_media(reduced_motion='no-preference')
        first = page.locator('#teaser video').first
        first.scroll_into_view_if_needed()
        page.wait_for_function('!document.querySelector("#teaser video").paused')
        first.evaluate('(v) => v.pause()')
        page.wait_for_timeout(100)
        page.locator('#egg-marking').scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        first.scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        assert first.evaluate('(v) => v.paused'), 'Manual pause lost after scrolling'
        first.evaluate('(v) => v.play()')
        page.locator('#egg-marking').scroll_into_view_if_needed()
        page.wait_for_function('document.querySelector("#teaser video").paused')
        first.scroll_into_view_if_needed()
        page.wait_for_function('!document.querySelector("#teaser video").paused')
        # Autoplay is explicitly requested, including after a reload with reduced motion.
        page.emulate_media(reduced_motion='reduce')
        page.reload(wait_until='networkidle')
        page.wait_for_function('!document.querySelector("#teaser video").paused')
        # Switching a comparison panel stops the outgoing clips.
        page.locator('#cup-tab-0').click()
        page.locator('#cup-panel-0').scroll_into_view_if_needed()
        page.wait_for_function('[...document.querySelectorAll("#cup-panel-0 video")].some(v => !v.paused)')
        page.locator('#cup-tab-1').click()
        page.wait_for_function('[...document.querySelectorAll("#cup-panel-0 video")].every(v => v.paused)')
        print('PASS: viewport playback, persistent manual pauses, reload autoplay and hidden-panel pauses', flush=True)
        assert not errors, errors
        nojs = browser.new_context(java_script_enabled=False, viewport={'width':390,'height':844})
        fallback = nojs.new_page()
        fallback.goto(base, wait_until='networkidle')
        assert fallback.locator('[data-tab-panel]:visible').count() == 3
        assert fallback.locator('video').count() == 35
        assert fallback.locator('[role="tablist"]:visible').count() == 0
        assert fallback.evaluate('document.documentElement.scrollWidth <= innerWidth')
        fallback.screenshot(path=str(screenshots / 'face-no-js.png'), full_page=True)
        print('PASS: no-JavaScript content and no browser errors', flush=True)
        browser.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--screenshots', type=Path, default=Path('/tmp/face-check'))
    args = parser.parse_args()
    browser_checks(validate_assets(), args.screenshots)
