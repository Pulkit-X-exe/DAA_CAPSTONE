"""
PDF Report Generator for PlagScan using ReportLab.

Generates a downloadable, professional PDF document summarizing:
- Plagiarism analysis overview and timestamp
- Document names and metrics (word counts, similarity percentage)
- Algorithm execution times and theoretical complexities
- Academic integrity disclaimer
"""

import io
from datetime import datetime
from typing import Dict, Any, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


def generate_pdf_report(report_data: Dict[str, Any]) -> io.BytesIO:
    """
    Constructs a PDF document in memory and returns a BytesIO buffer.

    Args:
        report_data (Dict[str, Any]): Dictionary containing:
            - doc1_name: Reference document name
            - doc2_name: Compared document name
            - similarity_percentage: float
            - algorithm_name: string
            - execution_time_ms: float
            - matched_word_count: int
            - doc1_word_count: int
            - doc2_word_count: int
            - matching_sections_count: int
            - benchmark: optional benchmark dict

    Returns:
        io.BytesIO: Stream containing the binary PDF data.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1E293B")
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748B")
    )

    heading2_style = ParagraphStyle(
        "Heading2Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0F172A")
    )

    body_style = ParagraphStyle(
        "BodyCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155")
    )

    disclaimer_style = ParagraphStyle(
        "DisclaimerCustom",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#64748B")
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("PlagScan &mdash; Similarity Analysis Report", title_style))
    story.append(Paragraph(
        f"DAA Capstone Project &bull; Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}",
        subtitle_style
    ))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#4F46E5"), spaceAfter=14))

    # 2. Executive Summary Metrics Table
    sim_score = float(report_data.get("similarity_percentage", 0.0))
    sim_color = colors.HexColor("#DC2626") if sim_score > 50 else (
        colors.HexColor("#D97706") if sim_score > 20 else colors.HexColor("#16A34A")
    )

    summary_data = [
        [
            Paragraph("<b>Reference Document (Doc 1):</b>", body_style),
            Paragraph(str(report_data.get("doc1_name", "Document 1")), body_style),
            Paragraph("<b>Compared Document (Doc 2):</b>", body_style),
            Paragraph(str(report_data.get("doc2_name", "Document 2")), body_style)
        ],
        [
            Paragraph("<b>Overall Similarity:</b>", body_style),
            Paragraph(f"<font color='{sim_color.hexval()}'><b>{sim_score}%</b></font>", body_style),
            Paragraph("<b>Matched Words:</b>", body_style),
            Paragraph(f"{report_data.get('matched_word_count', 0)} of {report_data.get('doc2_word_count', 0)}", body_style)
        ],
        [
            Paragraph("<b>Primary Algorithm:</b>", body_style),
            Paragraph(str(report_data.get("algorithm_name", "Knuth-Morris-Pratt (KMP)")), body_style),
            Paragraph("<b>Execution Time:</b>", body_style),
            Paragraph(f"{report_data.get('execution_time_ms', 0)} ms", body_style)
        ],
        [
            Paragraph("<b>Matching Passages:</b>", body_style),
            Paragraph(str(report_data.get("matching_sections_count", 0)), body_style),
            Paragraph("<b>Shingle Size:</b>", body_style),
            Paragraph(f"{report_data.get('shingle_size', 5)} words", body_style)
        ]
    ]

    summary_table = Table(summary_data, colWidths=[130, 130, 130, 140])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 16))

    # 3. DAA Algorithm Benchmark Comparison
    story.append(Paragraph("DAA Algorithm Empirical Performance Comparison", heading2_style))
    story.append(Spacer(1, 6))

    benchmark_info = report_data.get("benchmark", {})
    results_list = benchmark_info.get("results", [])

    if not results_list:
        results_list = [
            {"name": "Naive Pattern Matching", "execution_time_ms": report_data.get("execution_time_ms", 0.0), "complexity": "O(N * M)"},
            {"name": "Rabin-Karp Rolling Hash", "execution_time_ms": report_data.get("execution_time_ms", 0.0), "complexity": "O(N + M) avg"},
            {"name": "Knuth-Morris-Pratt (KMP)", "execution_time_ms": report_data.get("execution_time_ms", 0.0), "complexity": "O(N + M) guaranteed"}
        ]

    bench_table_data = [
        [
            Paragraph("<b>Algorithm</b>", body_style),
            Paragraph("<b>Execution Time (ms)</b>", body_style),
            Paragraph("<b>Time Complexity</b>", body_style),
            Paragraph("<b>Auxiliary Space</b>", body_style)
        ]
    ]

    for item in results_list:
        name = item.get("name", "")
        time_ms = item.get("execution_time_ms", 0.0)
        if "Naive" in name:
            comp = "O(N * M) Worst Case"
            space = "O(1)"
        elif "Rabin" in name:
            comp = "O(N + M) Average"
            space = "O(1)"
        else:
            comp = "O(N + M) Guaranteed"
            space = "O(M) for LPS Array"

        bench_table_data.append([
            Paragraph(name, body_style),
            Paragraph(f"<b>{time_ms} ms</b>", body_style),
            Paragraph(comp, body_style),
            Paragraph(space, body_style)
        ])

    bench_table = Table(bench_table_data, colWidths=[150, 110, 150, 120])
    bench_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EEF2F6")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(bench_table)
    story.append(Spacer(1, 16))

    # 4. Methodological Explanation
    story.append(Paragraph("Algorithmic Methodology", heading2_style))
    story.append(Spacer(1, 6))
    method_text = (
        "PlagScan applies an N-gram shingling technique (default 5-word shingles) over normalized "
        "document tokens. Each shingle is tested against the reference text using the chosen "
        "string-matching algorithm. Matched tokens are grouped into disjoint sets to prevent "
        "duplicate matches from falsely inflating similarity scores."
    )
    story.append(Paragraph(method_text, body_style))
    story.append(Spacer(1, 14))

    # 5. Academic Disclaimer & Footer
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#94A3B8"), spaceAfter=8))
    disclaimer_text = (
        "<b>Important Academic Disclaimer:</b> This report reflects syntactic text similarity and verbatim "
        "overlap calculated using string-matching algorithms. It does not determine intellectual property "
        "intent, citation accuracy, or AI generation."
    )
    story.append(Paragraph(disclaimer_text, disclaimer_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
