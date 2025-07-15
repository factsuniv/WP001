#!/usr/bin/env python3
"""
Generate PDF document of the Revolutionary THPU White Paper
"""

import requests
import json
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, black, blue, gray
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics.charts.textlabels import Label
from datetime import datetime
import os

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

def create_performance_chart():
    """Create a performance comparison chart"""
    drawing = Drawing(500, 200)
    
    # Create horizontal bar chart
    chart = HorizontalBarChart()
    chart.x = 50
    chart.y = 50
    chart.height = 100
    chart.width = 400
    
    # Data: [CPU, GPU, THPU]
    chart.data = [
        [1, 10, 1000],  # Energy Efficiency
        [1, 100, 10000],  # Throughput
    ]
    
    chart.categoryAxis.categoryNames = ['CPU', 'GPU', 'THPU']
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 10000
    
    # Add labels
    chart.bars[0].fillColor = Color(0.2, 0.4, 0.8, 1)
    chart.bars[1].fillColor = Color(0.8, 0.2, 0.4, 1)
    
    drawing.add(chart)
    
    # Add title
    title = Label()
    title.setText("THPU Performance Comparison")
    title.x = 250
    title.y = 170
    title.textAnchor = 'middle'
    drawing.add(title)
    
    return drawing

def generate_pdf():
    """Generate the PDF document"""
    
    # Fetch data
    print("Fetching white paper data...")
    data = fetch_whitepaper_data()
    if not data:
        print("Failed to fetch white paper data")
        return
    
    # Create PDF
    filename = "/app/THPU_Revolutionary_White_Paper.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        textColor=blue,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=black,
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=blue,
        spaceAfter=12,
        spaceBefore=20
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=black,
        spaceAfter=8,
        spaceBefore=12
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=black,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leftIndent=0,
        rightIndent=0
    )
    
    abstract_style = ParagraphStyle(
        'CustomAbstract',
        parent=styles['Normal'],
        fontSize=10,
        textColor=black,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leftIndent=36,
        rightIndent=36,
        borderWidth=1,
        borderColor=gray,
        borderPadding=12
    )
    
    # Build content
    content = []
    
    # Title page
    content.append(Paragraph(data['title'], title_style))
    content.append(Spacer(1, 30))
    
    # Authors
    for author in data['authors']:
        content.append(Paragraph(f"<b>{author['name']}</b>", subtitle_style))
        content.append(Paragraph(author['affiliation'], subtitle_style))
        content.append(Spacer(1, 12))
    
    content.append(Spacer(1, 30))
    content.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
    
    # Keywords
    content.append(Spacer(1, 30))
    keywords_text = ", ".join(data['keywords'])
    content.append(Paragraph(f"<b>Keywords:</b> {keywords_text}", body_style))
    
    content.append(PageBreak())
    
    # Abstract
    content.append(Paragraph("Abstract", heading_style))
    content.append(Paragraph(data['abstract'], abstract_style))
    content.append(Spacer(1, 30))
    
    # Performance metrics
    content.append(Paragraph("Key Performance Achievements", heading_style))
    metrics = [
        ("Energy Efficiency Improvement", "1000x over traditional CPUs"),
        ("Throughput Increase", "100x for AI workloads"),
        ("Latency Reduction", "10x for inference tasks"),
        ("Adaptability", "Infinite through neuromorphic learning")
    ]
    
    for metric, value in metrics:
        content.append(Paragraph(f"• <b>{metric}:</b> {value}", body_style))
    
    content.append(PageBreak())
    
    # Table of Contents
    content.append(Paragraph("Table of Contents", heading_style))
    for i, section in enumerate(data['sections']):
        content.append(Paragraph(f"{i+1}. {section['title']}", body_style))
    
    content.append(PageBreak())
    
    # Sections
    for section in data['sections']:
        content.append(Paragraph(section['title'], heading_style))
        
        # Process section content
        section_content = section['content']
        paragraphs = section_content.split('\n\n')
        
        for para in paragraphs:
            if para.strip():
                # Handle different formatting
                if para.startswith('**') and para.endswith('**'):
                    # Bold subheading
                    content.append(Paragraph(para.replace('**', '').strip(), subheading_style))
                elif para.startswith('*') and para.endswith('*'):
                    # Italic subheading
                    content.append(Paragraph(f"<i>{para.replace('*', '').strip()}</i>", subheading_style))
                elif para.startswith('- '):
                    # Bullet point
                    content.append(Paragraph(f"• {para[2:].strip()}", body_style))
                else:
                    # Regular paragraph
                    content.append(Paragraph(para.strip(), body_style))
        
        # Add figures if any
        for figure in section.get('figures', []):
            content.append(Spacer(1, 20))
            content.append(Paragraph(f"<b>{figure['title']}</b>", subheading_style))
            content.append(Paragraph(figure['caption'], body_style))
            content.append(Spacer(1, 20))
        
        content.append(PageBreak())
    
    # References
    content.append(Paragraph("References", heading_style))
    for i, ref in enumerate(data['references']):
        ref_text = f"[{i+1}] {ref['title']} by {', '.join(ref['authors'])} ({ref['year']}). <i>{ref['journal']}</i>"
        if ref.get('doi'):
            ref_text += f". DOI: {ref['doi']}"
        content.append(Paragraph(ref_text, body_style))
    
    # Build PDF
    print("Building PDF...")
    doc.build(content)
    print(f"PDF generated successfully: {filename}")
    
    return filename

if __name__ == "__main__":
    generate_pdf()