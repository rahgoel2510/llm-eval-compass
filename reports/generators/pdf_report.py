"""PDF report generator. Writes markdown; PDF conversion requires weasyprint."""

from reports.generators.markdown_report import MarkdownReportGenerator


class PDFReportGenerator:
    """Generate a PDF report. Currently outputs markdown with a TODO for PDF conversion."""

    def __init__(self):
        self._md_generator = MarkdownReportGenerator()

    def generate(self, results: dict, output_path: str) -> str:
        md_path = output_path.replace(".pdf", ".md")
        self._md_generator.generate(results, md_path)

        # TODO: Convert markdown to PDF using weasyprint.
        # Install with: pip install weasyprint
        # Example:
        #   from weasyprint import HTML
        #   HTML(string=html_content).write_pdf(output_path)

        return md_path
