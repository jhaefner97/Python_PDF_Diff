import fitz

from dataclasses import dataclass, field
from paths import paths
from pathlib import Path
from typing import Iterator


@dataclass
class PdfData:
    document_path: Path
    meta_data: None = None
    text_dict: dict[tuple, tuple] = field(default_factory=dict)

    def build_text_dict(self, page_data: fitz.Page) -> None:
        for block in page_data.get_text("blocks"):
            coords = block[:4]
            text = block[4:-2]
            self.text_dict[text] = coords, page_data.number


class Differ:
    def __init__(self, pdf_file_one: PdfData, pdf_file_two: PdfData):
        self.pdf_file_one = pdf_file_one
        self.pdf_file_two = pdf_file_two

    def compare(self) -> tuple[set, set]:
        pdf_one_diffs = set(self.pdf_file_one.text_dict) - set(self.pdf_file_two.text_dict)
        pdf_two_diffs = set(self.pdf_file_two.text_dict) - set(self.pdf_file_one.text_dict)
        return pdf_one_diffs, pdf_two_diffs

    def annotate_diffs(self) -> None:
        diffed_bookmarks = []
        doc_one_diffs, doc_two_diffs = self.compare()
        diffed_pdf = fitz.Document()
        with fitz.Document(str(self.pdf_file_one.document_path)) as f:
            pages_with_differences = set([self.pdf_file_one.text_dict[diff][1] for diff in doc_one_diffs])
            for page in pages_with_differences:
                diffed_bookmarks.append((1, "DIFF", page+1))
                for diff in doc_one_diffs:
                    coords, page_number = self.pdf_file_one.text_dict[diff]
                    page = f[page_number]
                    page.add_highlight_annot(coords)
                diffed_pdf.insert_pdf(f, from_page=page_number, to_page=page_number)
        diffed_pdf.set_toc(diffed_bookmarks)
        diffed_pdf.save(str(paths.diffed_pdf))


def read_pdf(pdf_doc: Path) -> PdfData:
    with fitz.Document(str(pdf_doc)) as f:
        doc = PdfData(
            document_path=pdf_doc,
        )
        for page in f:
            doc.build_text_dict(page)
    return doc


def iterate_over_incoming_pdf_files() -> Iterator[Path]:
    incoming_files = [file for file in paths.incoming_dir.glob("*") if file.suffix.lower() == ".pdf"]
    assert len(incoming_files), "The program can only process 2 pdf files at a time."
    for pdf_file in incoming_files:
        yield pdf_file
