"""Safari rejects relative URI actions in served PDFs; downloads stay portable."""
from types import SimpleNamespace
import pymupdf
import pytest
from tenderpack.panel.server import _handler


def pdf_bytes():
    with pymupdf.open() as doc:
        page = doc.new_page()
        page.insert_text((20, 30), 'A3 requirement and supporting detail')
        for i, uri in enumerate(['a3_detail.html#R-1', '../a3_detail.html#I-1', 'https://example.com/reference']):
            page.insert_link({'kind': pymupdf.LINK_URI, 'from': pymupdf.Rect(20, 40+i*20, 180, 55+i*20), 'uri': uri})
        return doc.tobytes()


def uris(data):
    with pymupdf.open(stream=data, filetype='pdf') as doc:
        return [doc.xref_get_key(link['xref'], 'A/URI')[1] for page in doc for link in page.get_links()]


def serve(path, sub):
    panel = SimpleNamespace(url='http://127.0.0.1:54321/t/test-token/', safe_file=lambda area, rel: path)
    handler = _handler(panel).__new__(_handler(panel))
    handler._send = lambda status, data, ctype, headers, **kw: (data, headers)
    return handler._file(sub)


@pytest.mark.parametrize('area,rel', [('out', 'a3/a3.pdf'), ('runs', 'demo/candidate/out/a3/candidate/a3.pdf')])
def test_pdf_view_resolves_relative_detail_links_without_changing_files(tmp_path, area, rel):
    path = tmp_path/'a3.pdf'; original = pdf_bytes(); path.write_bytes(original)
    data, headers = serve(path, f'file/{area}/{rel}')
    base = 'http://127.0.0.1:54321/t/test-token/file/' + area + '/' + rel.rsplit('/', 1)[0]
    assert uris(data) == [base+'/a3_detail.html#R-1', base.rsplit('/', 1)[0]+'/a3_detail.html#I-1', 'https://example.com/reference']
    assert path.read_bytes() == original
    assert headers['Content-Disposition'].startswith('inline')
    with pymupdf.open(stream=data, filetype='pdf') as doc:
        assert len(doc) == 1 and 'A3 requirement and supporting detail' in doc[0].get_text()


@pytest.mark.parametrize('sub', ['download/out/a3/a3.pdf', 'file/sources/tender.pdf', 'file/runs/demo/candidate/input/ADD-03.pdf'])
def test_downloads_and_tender_source_pdfs_stay_byte_identical(tmp_path, sub):
    path = tmp_path/'a3.pdf'; original = pdf_bytes(); path.write_bytes(original)
    assert serve(path, sub)[0] == original
