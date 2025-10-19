"""
PDF report generation utility for the Startup Idea Validator.
"""

import os
import time
from fpdf import FPDF
import re

from config import OUTPUT_DIR


def sanitize_filename(text):
    """Convert text to a valid filename."""
    # Extract first few words to create a name
    words = re.sub(r'[^\w\s]', '', text).split()[:5]
    name = '_'.join(words).lower()
    
    # Ensure filename is valid
    name = re.sub(r'[^\w\-_\.]', '_', name)
    
    return name


def create_pdf_report(startup_idea, report_content):
    """
    Create a PDF report from the markdown content.
    
    Args:
        startup_idea (str): The original startup idea
        report_content (str): The report content in markdown format
        
    Returns:
        str: Path to the created PDF file
    """
    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # Set font
    pdf.set_font("Arial", size=12)
    
    # Extract title from report content or use default
    title_match = re.search(r"# STARTUP IDEA VALIDATOR: (.*)", report_content)
    if title_match:
        title = title_match.group(1)
    else:
        title = "Startup Idea Validation Report"
    
    # Create filename based on title and timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{sanitize_filename(title)}_{timestamp}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Set title
    pdf.set_font("Arial", "B", size=16)
    pdf.cell(200, 10, txt=title, ln=True, align="C")
    pdf.ln(10)
    
    # Add content - this is a simple implementation that doesn't handle markdown formatting
    # For a production system, use a proper markdown to PDF converter
    pdf.set_font("Arial", size=12)
    
    # Process content by sections
    sections = re.split(r'#{1,3} ', report_content)
    
    for section in sections:
        if not section.strip():
            continue
            
        # Get section title
        lines = section.split('\n', 1)
        if len(lines) > 0:
            section_title = lines[0].strip()
            pdf.set_font("Arial", "B", size=14)
            pdf.cell(200, 10, txt=section_title, ln=True)
            pdf.ln(5)
            
            # Add section content if available
            if len(lines) > 1:
                section_content = lines[1].strip()
                pdf.set_font("Arial", size=12)
                
                # Simple paragraph handling
                paragraphs = section_content.split('\n\n')
                for paragraph in paragraphs:
                    # Remove markdown formatting
                    clean_paragraph = re.sub(r'\*\*(.*?)\*\*', r'\1', paragraph)  # Bold
                    clean_paragraph = re.sub(r'\*(.*?)\*', r'\1', clean_paragraph)  # Italic
                    
                    pdf.multi_cell(0, 10, txt=clean_paragraph)
                    pdf.ln(5)
            
            pdf.ln(10)
    
    # Save PDF
    pdf.output(filepath)
    
    return filepath