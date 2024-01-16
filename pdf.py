from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image,Table,TableStyle

import os
import pandas as pd



def create_pdf_with_graphs_and_data_for_sample(sample_path, pdf_file, data,sample_stats_dict):
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

    # Add sample_name as title with adjusted style
    title_style = styles["Title"]
    title_style.fontSize = 16  # Adjust the font size
    title_style.spaceAfter = 20  # Adjust the space after the title
    content.append(Paragraph(pdf_file, title_style))

    # Add spacer
    content.append(Spacer(1, 12))

    # Convert dictionary to a list of tuples (key, value)
    data_tuples = [(key, value) for key, value in data.items()]

    # Create a DataFrame from the list of tuples
    df = pd.DataFrame(data_tuples, columns=['Key', 'Value'])

    # Remove rows with null values (if any)
    df = df.dropna()

    exclude_columns = ['Polymer Density Solution 1 ID','Solvent Density Solution 1 ID']
    df_cleaned = df.drop(columns=exclude_columns, errors='ignore')

    # Convert cleaned DataFrame to a list of lists
    data_list = [df_cleaned.columns.tolist()] + df_cleaned.values.tolist()

    # Create a table
    table = Table(data_list)

    # Add style to the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Add table to content
    content.append(table)

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


