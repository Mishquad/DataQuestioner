from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf(results):
    # Generate file name with date
    current_date = datetime.now().strftime("%Y-%m-%d")
    output_file = f"{current_date}_report_data.pdf"
    
    # Create the PDF
    c = canvas.Canvas(output_file, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    # Write results to the PDF
    y = 750  # Starting vertical position
    for key, value in results.items():
        c.drawString(100, y, f"{key}:")
        y -= 20  # Move down for the next line
        
        if isinstance(value, str):
            lines = value.split("\n")
            for line in lines:
                c.drawString(120, y, line)
                y -= 15
        else:
            c.drawString(120, y, str(value))
            y -= 15
        
        y -= 10  # Extra space between sections
    
    c.save()
    print(f"PDF successfully saved locally as {output_file}")
    return output_file
