import boto3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf(results, output_dir="reports"):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate file name with date
    current_date = datetime.now().strftime("%Y-%m-%d")
    output_file = os.path.join(output_dir, f"{current_date}_report_data.pdf")
    
    c = canvas.Canvas(output_file, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    # Write results to PDF
    y = 750
    for key, value in results.items():
        c.drawString(100, y, f"{key}: {value}")
        y -= 20
    
    c.save()
    print(f"PDF saved at {output_file}")
    return output_file

def upload_to_s3(file_path, bucket_name, s3_key):
    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                      aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
    s3.upload_file(file_path, bucket_name, s3_key)
    print(f"File {file_path} uploaded to S3 bucket {bucket_name} as {s3_key}")
