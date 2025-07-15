#!/usr/bin/env python3
"""
Generate Simple PDF of the Revolutionary THPU White Paper
"""

import requests
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, blue
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from datetime import datetime

# Backend URL
BACKEND_URL = "https://9ff8b068-b843-42e4-987f-d68282246334.preview.emergentagent.com/api"

def fetch_whitepaper_data():
    """Fetch the white paper data from the backend API"""
    try:
        response = requests.get(f"{BACKEND_URL}/whitepaper", timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching whitepaper: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception fetching whitepaper: {e}")
        return None

def generate_simple_pdf():
    """Generate a simple PDF document"""
    
    # Fetch data
    print("Fetching white paper data...")
    data = fetch_whitepaper_data()
    if not data:
        print("Failed to fetch white paper data")
        return
    
    # Create PDF
    filename = "/app/THPU_White_Paper_Simple.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create simple styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=18,
        textColor=black,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    author_style = ParagraphStyle(
        'Author',
        parent=styles['Normal'],
        fontSize=14,
        textColor=black,
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=black,
        spaceAfter=12,
        spaceBefore=20
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        textColor=black,
        spaceAfter=12,
        alignment=TA_JUSTIFY
    )
    
    # Build content
    content = []
    
    # Title
    content.append(Paragraph(data['title'], title_style))
    content.append(Spacer(1, 30))
    
    # Authors
    for author in data['authors']:
        content.append(Paragraph(author['name'], author_style))
        content.append(Paragraph(author['affiliation'], author_style))
    
    content.append(Spacer(1, 30))
    content.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", author_style))
    
    # Keywords
    content.append(Spacer(1, 30))
    keywords_text = "Keywords: " + ", ".join(data['keywords'])
    content.append(Paragraph(keywords_text, body_style))
    
    content.append(PageBreak())
    
    # Abstract
    content.append(Paragraph("Abstract", heading_style))
    content.append(Paragraph(data['abstract'], body_style))
    content.append(Spacer(1, 30))
    
    # Key Performance Metrics
    content.append(Paragraph("Key Performance Achievements", heading_style))
    content.append(Paragraph("• Energy Efficiency: 1000x improvement over traditional CPUs", body_style))
    content.append(Paragraph("• Throughput: 100x increase for AI workloads", body_style))
    content.append(Paragraph("• Latency: 10x reduction for inference tasks", body_style))
    content.append(Paragraph("• Adaptability: Infinite through neuromorphic learning", body_style))
    
    content.append(PageBreak())
    
    # Table of Contents
    content.append(Paragraph("Table of Contents", heading_style))
    for i, section in enumerate(data['sections']):
        content.append(Paragraph(f"{i+1}. {section['title']}", body_style))
    
    content.append(PageBreak())
    
    # Sections
    for section in data['sections']:
        content.append(Paragraph(section['title'], heading_style))
        
        # Process content - split into paragraphs and clean up
        section_content = section['content']
        paragraphs = [p.strip() for p in section_content.split('\n\n') if p.strip()]
        
        for para in paragraphs:
            # Remove special formatting markers for simple PDF
            clean_para = para.replace('**', '').replace('*', '').replace('```', '')
            
            # Skip very short paragraphs (likely formatting artifacts)
            if len(clean_para) > 20:
                content.append(Paragraph(clean_para, body_style))
        
        content.append(Spacer(1, 20))
    
    # References
    content.append(PageBreak())
    content.append(Paragraph("References", heading_style))
    
    for i, ref in enumerate(data['references']):
        ref_text = f"[{i+1}] {ref['title']} by {', '.join(ref['authors'])} ({ref['year']}). {ref['journal']}"
        if ref.get('doi'):
            ref_text += f". DOI: {ref['doi']}"
        content.append(Paragraph(ref_text, body_style))
    
    # Footer
    content.append(Spacer(1, 30))
    content.append(Paragraph("© 2024 FactsUniv. All rights reserved.", author_style))
    
    # Build PDF
    print("Building simple PDF...")
    doc.build(content)
    print(f"Simple PDF generated successfully: {filename}")
    
    return filename

if __name__ == "__main__":
    generate_simple_pdf()