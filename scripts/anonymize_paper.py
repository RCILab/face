"""Create an anonymous web copy; never alter the supplied source manuscript.

The reviewed rectangles apply only to the supplied eight-page manuscript.
They remove author/affiliation blocks, the project URL and acknowledgements.
PDF text is actually redacted (not covered with white rectangles).
"""
from pathlib import Path
import hashlib
import pymupdf

SOURCE_SHA256 = '52b5f3bab99f5a1c80f1e3f3cd87adde5d2813095f0ecd78d5065f2df7dc9fb2'

def anonymize_paper(source, destination):
    source, destination = Path(source), Path(destination)
    assert source.resolve() != destination.resolve(), 'Keep the source unchanged'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA256, 'Re-audit redaction regions for a new manuscript'
    doc = pymupdf.open(source)
    regions = [(0, (54, 101, 558, 127)), (0, (53, 693, 300, 734))]
    first = doc[0]
    for phrase in ['Videos and additional materials can be found on', 'the project page:']:
        for rect in first.search_for(phrase):
            if phrase == 'the project page:': rect.x1 = 300
            regions.append((0, tuple(rect)))
    for page in doc:
        for block in page.get_text('blocks'):
            if block[4].startswith('Acknowledgements'):
                regions.append((page.number, tuple(block[:4])))
        # The supplied manuscript has one external project-page link.
        for link in list(page.get_links()):
            if link.get('uri'): page.delete_link(link)
    for page_number, bounds in regions:
        doc[page_number].add_redact_annot(pymupdf.Rect(bounds), fill=(1, 1, 1))
    for page_number in set(page for page, _ in regions):
        doc[page_number].apply_redactions(images=0, graphics=0)
    doc.set_metadata({})
    doc.del_xml_metadata()
    doc.scrub(metadata=True, xml_metadata=True, attached_files=True, embedded_files=True, javascript=True)
    # Rewrite the file, eliminating obsolete content streams and metadata.
    doc.save(destination, garbage=4, deflate=True, clean=True, no_new_id=True)
    doc.close()
    return {'path': 'static/pdfs/face-paper.pdf', 'source': source.name,
            'sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
            'transform': 'Anonymous copy: author and affiliation blocks, project URL, acknowledgement block, external project link and PDF metadata removed with permanent redaction.',
            'redactions': [{'page': page + 1, 'rectangle': list(rect)} for page, rect in regions]}

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    anonymize_paper(root.parent / 'materials/_2026__ICRA___FACE.pdf', root / 'static/pdfs/face-paper.pdf')
