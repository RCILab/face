"""Browser smoke checks. Requires Playwright, RangeHTTPServer, and Microsoft Edge.

Run: python scripts/check_site.py
Screenshots are written outside the repository, to ../working/.
"""
from functools import partial
from http.server import ThreadingHTTPServer
from RangeHTTPServer import RangeRequestHandler
from pathlib import Path
from threading import Thread
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
artifacts = root.parent / 'working'
artifacts.mkdir(exist_ok=True)

class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for attr in ('src', 'href', 'poster'):
            if attrs.get(attr):
                self.links.append(attrs[attr])

doc = Document()
doc.feed((root / 'index.html').read_text(encoding='utf-8'))
assert len(doc.ids) == len(set(doc.ids)), 'Duplicate element IDs'
for link in doc.links:
    url = urlsplit(link)
    if url.scheme or url.netloc:
        continue
    if url.path:
        assert (root / unquote(url.path)).is_file(), f'Missing asset: {link}'
    elif url.fragment:
        assert url.fragment in doc.ids, f'Missing anchor: {link}'

class QuietHandler(RangeRequestHandler):
    def log_message(self, *args):
        pass
    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass  # Browsers cancel pending media ranges when seeking or closing.

server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(root.parent)))
server.daemon_threads = True
Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}/{root.name}/'
errors = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
        context.grant_permissions(['clipboard-read', 'clipboard-write'])
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('response', lambda response: errors.append(f'{response.status} {response.url}') if response.status >= 400 else None)
        page.goto(url, wait_until='networkidle')
        assert page.title().startswith('FACE')
        assert page.locator('#hero-video').evaluate('(v) => v.paused'), 'Reduced motion must disable autoplay'
        page.locator('#motion-toggle').click()
        page.wait_for_function("!document.querySelector('#hero-video').paused")
        page.locator('#motion-toggle').click()
        page.wait_for_function("document.querySelector('#hero-video').paused")
        page.locator('#hero-video').evaluate('(v) => v.currentTime = 5')
        page.screenshot(path=str(artifacts / 'desktop-hero.png'))
        page.locator('#method').screenshot(path=str(artifacts / 'desktop-method.png'))
        # Decoder illustration follows Eqs. (6)-(7), not a prerecorded visual.
        page.locator('#method-demo').scroll_into_view_if_needed()
        assert page.locator('#demo-toggle').inner_text() == 'Play animation'
        page.locator('[data-condition="1"]').click()
        assert page.locator('#demo-friction').inner_text() == '0.85'
        assert page.locator('#demo-force').inner_text() == '3.4 N'
        flat_motion = page.locator('#demo-motion').get_attribute('d')
        page.locator('[data-condition="2"]').click()
        assert page.locator('#demo-force').inner_text() == '3.4 N'
        assert page.locator('#demo-motion').get_attribute('d') != flat_motion
        assert 'rotate(-24.00)' in page.locator('#demo-surface').get_attribute('transform')
        page.locator('#method-demo').screenshot(path=str(artifacts / 'method-animation-desktop.png'))
        page.locator('#demo-toggle').click()
        page.wait_for_function("document.querySelector('[data-condition=\"0\"]').getAttribute('aria-pressed') === 'true'", timeout=9000)
        page.locator('#demo-toggle').click()
        stopped = page.locator('#demo-surface').get_attribute('transform')
        page.wait_for_timeout(300)
        assert page.locator('#demo-surface').get_attribute('transform') == stopped
        page.locator('[data-video-time="84"]').click()
        page.wait_for_function("document.querySelector('#main-video').currentTime >= 84 && !document.querySelector('#main-video').paused")
        duration = page.locator('#main-video').evaluate('(v) => v.duration')
        assert 172 < duration < 174, duration
        page.locator('#main-video').evaluate('(v) => v.pause()')
        page.locator('summary').click()
        assert page.locator('details').evaluate('(d) => d.open')
        page.locator('#copy-citation').click()
        assert page.evaluate('navigator.clipboard.readText()').startswith('@misc{face,')
        page.locator('summary').click()
        for width in (1440, 768, 390, 320):
            page.set_viewport_size({'width': width, 'height': 1000})
            page.evaluate('window.scrollTo(0, 0)')
            page.wait_for_timeout(150)
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), f'Overflow at {width}px'
            if width in (1440, 390):
                page.screenshot(path=str(artifacts / f'page-{width}.png'), full_page=True)
            if width == 390:
                page.locator('#method-demo').screenshot(path=str(artifacts / 'method-animation-mobile.png'))
        # Ensure every image has loaded, including the lazily loaded detail figures.
        page.locator('summary').click()
        page.locator('details').scroll_into_view_if_needed()
        page.wait_for_function('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
        assert not errors, errors
        no_js = browser.new_context(java_script_enabled=False, viewport={'width':390,'height':844})
        plain = no_js.new_page()
        plain.goto(url)
        assert plain.locator('#main-video').get_attribute('controls') is not None
        assert plain.locator('[data-video-time="84"]').get_attribute('href').endswith('#t=84')
        assert plain.locator('#copy-citation').is_hidden()
        assert plain.locator('#demo-toggle').is_hidden()
        assert plain.locator('.demo-scene').is_visible()
        browser.close()
    print(json.dumps({'status':'passed', 'widths':[1440,768,390,320], 'video_duration':duration, 'javascript_errors':errors, 'checks':['local assets and anchors','video playback and seek','reduced motion','pause/resume','clipboard','details','no JavaScript fallback'], 'screenshots':str(artifacts)}, indent=2))
finally:
    server.shutdown()
