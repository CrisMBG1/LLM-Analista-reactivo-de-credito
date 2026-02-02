from pypdf import PdfReader

class PDFProcessor:
    @staticmethod
    def extract_text_from_pdf(filepath):
        """
        Extracts text from a PDF file.
        """
        try:
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            return f"Error extracting PDF text: {str(e)}"
