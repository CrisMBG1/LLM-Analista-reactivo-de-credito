from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import re

class PDFReportGenerator:
    @staticmethod
    def create_pdf(filename, markdown_content):
        """
        Generates a PDF file from the markdown content.
        Since converting MD to PDF perfectly is hard without complex libraries,
        we will do a basic conversion of headers and paragraphs.
        """
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Custom Styles
        title_style = styles['Heading1']
        title_style.alignment = 1 # Center
        
        h2_style = styles['Heading2']
        h2_style.textColor = colors.darkblue
        
        normal_style = styles['BodyText']
        
        # Add Title
        story.append(Paragraph("Dictamen Final de Crédito", title_style))
        story.append(Spacer(1, 24))

        # Process text line by line (Simplified Markdown Parser)
        lines = markdown_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('# '):
                # H1
                text = line.replace('# ', '')
                story.append(Spacer(1, 12))
                story.append(Paragraph(text, styles['Heading1']))
                story.append(Spacer(1, 6))
            elif line.startswith('## '):
                # H2
                text = line.replace('## ', '')
                story.append(Spacer(1, 12))
                story.append(Paragraph(text, h2_style))
                story.append(Spacer(1, 6))
            elif line.startswith('### '):
                # H3
                text = line.replace('### ', '')
                story.append(Paragraph(text, styles['Heading3']))
            elif line.startswith('- ') or line.startswith('* '):
                # Bullet
                text = line[2:]
                bullet_style = ParagraphStyle('Bullet', parent=normal_style, leftIndent=20)
                story.append(Paragraph(f"• {text}", bullet_style))
            else:
                # Normal Text
                story.append(Paragraph(line, normal_style))
            
            # Small space between paragraphs (optional)
            # story.append(Spacer(1, 2))

        try:
            doc.build(story)
            return True
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
