from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import os


def create_pdf_with_graphs_and_data_for_sample(sample_path, pdf_file, graph, data):
    # Create the full path for the PDF file
    full_pdf_path = os.path.join(sample_path, pdf_file)

    # Create a PDF document
    document = SimpleDocTemplate(
        full_pdf_path,
        pagesize=letter
    )

    # Content list to store paragraphs, images, and spacers
    content = []

    # Styles for paragraphs
    styles = getSampleStyleSheet()

    # Add sample_name as title
    title_style = styles["Title"]
    content.append(Paragraph(pdf_file, title_style))

    # Add graph to content
    # Assuming the graph is saved as a PNG file
    #content.append(Image(f"{graph}.png"))

    # Add spacer
    content.append(Spacer(1, 12))

    # Add data lines to content
    for line in data:
        content.append(Paragraph(line, styles["Normal"]))

    # Save content to PDF
    document.build(content)
    print(f"PDF saved to {full_pdf_path}")

def create_pdf_with_graphs_and_data_for_section(pdf_file, graph, data):
    # Create a PDF document
    document = SimpleDocTemplate(
        pdf_file,
        pagesize=letter
    )

    # Content list to store paragraphs, images, and spacers
    content = []

    # Styles for paragraphs
    styles = getSampleStyleSheet()

    # Add sample_name as title
    title_style = styles["Title"]
    content.append(Paragraph(pdf_file, title_style))

    # Add graph to content
    # Assuming the graph is saved as a PNG file
    #content.append(Image(f"{graph}.png"))

    # Add spacer
    content.append(Spacer(1, 12))

    # Add data lines to content
    for line in data:
        content.append(Paragraph(line, styles["Normal"]))

    # Save content to PDF
    document.build(content)
    print(f"PDF saved to {pdf_file}")


# Example graphs and data (replace with your actual data)
sample_name = "Sample Name"
graphs = ["Graph1", "Graph2"]  # List of graph file names
data = [
    "Line 1: Lorem ipsum dolor sit amet.",
    "Line 2: Consectetur adipiscing elit.",
    "Line 3: Maecenas tincidunt finibus felis."
]


