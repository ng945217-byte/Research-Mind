"""
RESEARCHMINDAI - Document Report Generator
"""
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from models.report import ReportFormat

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Compiles research and document analysis data into PDF, DOCX, PPTX, and MD files."""

    def generate(
        self,
        file_path: str,
        title: str,
        data: Dict[str, Any],
        source_type: str,  # "research" | "document"
        fmt: ReportFormat,
        options: Dict[str, bool]
    ) -> bool:
        """Entrypoint for report generation."""
        logger.info(f"Generating report: {file_path} (Format: {fmt.value})")

        if fmt == ReportFormat.PDF:
            return self._generate_pdf(file_path, title, data, source_type, options)
        elif fmt == ReportFormat.DOCX:
            return self._generate_docx(file_path, title, data, source_type, options)
        elif fmt == ReportFormat.PPTX:
            return self._generate_pptx(file_path, title, data, source_type, options)
        elif fmt == ReportFormat.MARKDOWN:
            return self._generate_markdown(file_path, title, data, source_type, options)

        return False

    def _generate_pdf(
        self,
        file_path: str,
        title: str,
        data: Dict[str, Any],
        source_type: str,
        options: Dict[str, bool]
    ) -> bool:
        """Generate PDF report using ReportLab."""
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors

        # Setup doc template
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
        )

        styles = getSampleStyleSheet()
        
        # Define custom professional styles
        title_style = ParagraphStyle(
            "CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            textColor=colors.HexColor("#3b2a50"),  # Dark purple theme
            spaceAfter=15
        )
        
        subtitle_style = ParagraphStyle(
            "CoverSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#7c6e8f"),
            spaceAfter=30
        )
        
        h1_style = ParagraphStyle(
            "Header1",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#3b2a50"),
            spaceBefore=15,
            spaceAfter=10,
            keepWithNext=True
        )

        h2_style = ParagraphStyle(
            "Header2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#aa3bff"),
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True
        )

        body_style = ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14.5,
            textColor=colors.HexColor("#2d2c30"),
            spaceAfter=8
        )

        meta_label_style = ParagraphStyle(
            "MetaLabel",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=colors.HexColor("#5b4a70")
        )

        meta_val_style = ParagraphStyle(
            "MetaValue",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#2d2c30")
        )

        story = []

        # ─── 1. Cover Page ────────────────────────────────────────────────────
        story.append(Spacer(1, 100))
        story.append(Paragraph(title, title_style))
        report_sub = "AI-Generated Intelligence Summary" if source_type == "research" else "AI Document Analysis & Insights Report"
        story.append(Paragraph(report_sub, subtitle_style))
        story.append(Spacer(1, 30))

        # Metadata Table
        created_str = datetime.now().strftime("%B %d, %Y - %H:%M")
        meta_data = [
            [Paragraph("Generated On:", meta_label_style), Paragraph(created_str, meta_val_style)],
            [Paragraph("Source Type:", meta_label_style), Paragraph(source_type.upper(), meta_val_style)]
        ]
        
        if source_type == "research":
            meta_data.append([Paragraph("Research Mode:", meta_label_style), Paragraph(data.get("mode", "quick").upper(), meta_val_style)])
            meta_data.append([Paragraph("Confidence Score:", meta_label_style), Paragraph(f"{int(data.get('confidence_score', 0.0) * 100)}%", meta_val_style)])
        else:
            meta_data.append([Paragraph("Original File:", meta_label_style), Paragraph(data.get("filename", "Unknown"), meta_val_style)])
            meta_data.append([Paragraph("Word Count:", meta_label_style), Paragraph(str(data.get("word_count", 0)), meta_val_style)])

        meta_table = Table(meta_data, colWidths=[120, 300])
        meta_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#e5e4e7")),
        ]))
        story.append(meta_table)
        story.append(PageBreak())

        # ─── 2. Executive Summary ─────────────────────────────────────────────
        story.append(Paragraph("Executive Summary", h1_style))
        story.append(Paragraph(data.get("summary") or "No executive summary available.", body_style))
        story.append(Spacer(1, 10))

        # ─── 3. Deep Content (Deep Research or Doc Analysis) ──────────────────
        if data.get("deep_summary"):
            story.append(Paragraph("Detailed Analysis", h1_style))
            story.append(Paragraph(data.get("deep_summary"), body_style))
            story.append(Spacer(1, 10))

        # Perspectives (for Deep Research)
        if source_type == "research" and data.get("mode") == "deep":
            if data.get("technical_analysis"):
                story.append(Paragraph("Technical Deep-Dive", h1_style))
                story.append(Paragraph(data.get("technical_analysis"), body_style))
                story.append(Spacer(1, 10))
                
            if data.get("beginner_explanation"):
                story.append(Paragraph("Simplified Explanation (ELI5)", h1_style))
                story.append(Paragraph(data.get("beginner_explanation"), body_style))
                story.append(Spacer(1, 10))
                
            if data.get("expert_explanation"):
                story.append(Paragraph("Expert Commentary", h1_style))
                story.append(Paragraph(data.get("expert_explanation"), body_style))
                story.append(Spacer(1, 10))
                
            if data.get("future_predictions") and options.get("include_timeline"):
                story.append(Paragraph("Future Predictions & Outlook", h1_style))
                story.append(Paragraph(data.get("future_predictions"), body_style))
                story.append(Spacer(1, 10))

        # Topics & Entities (for Documents)
        if source_type == "document":
            if data.get("topics"):
                story.append(Paragraph("Extracted Topics", h1_style))
                for t in data.get("topics", []):
                    topic_text = f"<b>{t.get('topic')}</b> (Weight: {t.get('weight', 1.0)}): Keywords: {', '.join(t.get('keywords', []))}"
                    story.append(Paragraph(f"&bull; {topic_text}", body_style))
                story.append(Spacer(1, 10))

            if data.get("entities"):
                story.append(Paragraph("Key Entities & Mentions", h1_style))
                entities_list = [f"<b>{e.get('text')}</b> ({e.get('label')})" for e in data.get("entities", [])]
                story.append(Paragraph(", ".join(entities_list), body_style))
                story.append(Spacer(1, 10))

        # ─── 4. Timeline Section ──────────────────────────────────────────────
        if options.get("include_timeline") and data.get("timeline"):
            story.append(Paragraph("Chronological Timeline", h1_style))
            timeline_data = [[
                Paragraph("<b>Date</b>", meta_label_style),
                Paragraph("<b>Event</b>", meta_label_style),
                Paragraph("<b>Significance</b>", meta_label_style)
            ]]
            for ev in data.get("timeline", []):
                timeline_data.append([
                    Paragraph(ev.get("date", ""), meta_val_style),
                    Paragraph(ev.get("event", ""), meta_val_style),
                    Paragraph(ev.get("significance", ""), meta_val_style)
                ])
                
            timeline_table = Table(timeline_data, colWidths=[80, 180, 240])
            timeline_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f4f3ec")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#d5d4d7")),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(timeline_table)
            story.append(Spacer(1, 15))

        # ─── 5. Contradictions Log ───────────────────────────────────────────
        if data.get("contradictions"):
            story.append(Paragraph("Factual Contradictions Log", h1_style))
            for idx, c in enumerate(data.get("contradictions", [])):
                sev_color = "#e53e3e" if c.get("severity") == "high" else "#dd6b20" if c.get("severity") == "medium" else "#4a5568"
                c_data = [
                    [Paragraph(f"<b>Conflict {idx+1} [Severity: <font color='{sev_color}'>{c.get('severity').upper()}</font>]</b>", meta_label_style), ""],
                    [Paragraph("<b>Claim A:</b>", meta_label_style), Paragraph(c.get("claim_a"), meta_val_style)],
                    [Paragraph("<b>Source A:</b>", meta_label_style), Paragraph(c.get("source_a") or "Unspecified", meta_val_style)],
                    [Paragraph("<b>Claim B:</b>", meta_label_style), Paragraph(c.get("claim_b"), meta_val_style)],
                    [Paragraph("<b>Source B:</b>", meta_label_style), Paragraph(c.get("source_b") or "Unspecified", meta_val_style)],
                ]
                c_table = Table(c_data, colWidths=[100, 400])
                c_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('SPAN', (0,0), (1,0)),
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#fff5f5")),
                    ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#fed7d7")),
                    ('TOPPADDING', (0,0), (-1,-1), 5),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ]))
                story.append(KeepTogether([c_table, Spacer(1, 10)]))
            story.append(Spacer(1, 10))

        # ─── 6. Sources Reference ─────────────────────────────────────────────
        if options.get("include_sources") and data.get("sources"):
            story.append(Paragraph("References & Sources", h1_style))
            for idx, src in enumerate(data.get("sources", [])):
                src_title = src.get("title") or "Source URL"
                src_url = src.get("url") or "#"
                src_type = src.get("source_type", "web").upper()
                snippet = src.get("snippet", "")
                
                src_link = f"<a href='{src_url}'><font color='#aa3bff'><b>{idx+1}. {src_title}</b></font></a> [{src_type}]"
                story.append(Paragraph(src_link, body_style))
                if snippet:
                    story.append(Paragraph(f"<i>Context: {snippet[:200]}...</i>", ParagraphStyle("Snip", parent=body_style, textColor=colors.HexColor("#718096"), leftIndent=15)))
                story.append(Spacer(1, 5))

        # Build PDF Document
        doc.build(story)
        return True

    def _generate_docx(
        self,
        file_path: str,
        title: str,
        data: Dict[str, Any],
        source_type: str,
        options: Dict[str, bool]
    ) -> bool:
        """Generate DOCX file using python-docx."""
        import docx
        from docx.shared import Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH

        doc = docx.Document()

        # Document Header / Title
        doc_title = doc.add_paragraph()
        doc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_run = doc_title.add_run(title)
        title_run.font.name = 'Arial'
        title_run.font.size = Pt(24)
        title_run.font.bold = True
        title_run.font.color.rgb = RGBColor(59, 42, 80) # Primary purple

        # Subtitle
        doc_subtitle = doc.add_paragraph()
        doc_subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sub_run = doc_subtitle.add_run("AI-Generated Intelligence Summary" if source_type == "research" else "AI Document Analysis & Insights Report")
        sub_run.font.size = Pt(12)
        sub_run.font.italic = True
        sub_run.font.color.rgb = RGBColor(124, 110, 143)

        doc.add_paragraph(f"Generated On: {datetime.now().strftime('%B %d, %Y - %H:%M')}")
        doc.add_paragraph().paragraph_format.space_after = Pt(20)

        # 1. Executive Summary
        doc.add_heading("Executive Summary", level=1)
        doc.add_paragraph(data.get("summary") or "No summary available.")

        # 2. Deep summary
        if data.get("deep_summary"):
            doc.add_heading("Detailed Analysis", level=1)
            doc.add_paragraph(data.get("deep_summary"))

        # Deep Research Details
        if source_type == "research" and data.get("mode") == "deep":
            if data.get("technical_analysis"):
                doc.add_heading("Technical Deep-Dive", level=1)
                doc.add_paragraph(data.get("technical_analysis"))
            if data.get("beginner_explanation"):
                doc.add_heading("Simplified Explanation (ELI5)", level=1)
                doc.add_paragraph(data.get("beginner_explanation"))
            if data.get("expert_explanation"):
                doc.add_heading("Expert Commentary", level=1)
                doc.add_paragraph(data.get("expert_explanation"))
            if data.get("future_predictions"):
                doc.add_heading("Future Predictions & Outlook", level=1)
                doc.add_paragraph(data.get("future_predictions"))

        # Document Topics/Entities
        if source_type == "document":
            if data.get("topics"):
                doc.add_heading("Extracted Topics", level=1)
                for t in data.get("topics", []):
                    doc.add_paragraph(f"• {t.get('topic')} (Weight: {t.get('weight', 1.0)}): Keywords: {', '.join(t.get('keywords', []))}")
            if data.get("entities"):
                doc.add_heading("Key Entities", level=1)
                entities_str = ", ".join([f"{e.get('text')} ({e.get('label')})" for e in data.get("entities", [])])
                doc.add_paragraph(entities_str)

        # 3. Timeline
        if options.get("include_timeline") and data.get("timeline"):
            doc.add_heading("Chronological Timeline", level=1)
            table = doc.add_table(rows=1, cols=3)
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = 'Date'
            hdr_cells[1].text = 'Event'
            hdr_cells[2].text = 'Significance'
            for ev in data.get("timeline", []):
                row_cells = table.add_row().cells
                row_cells[0].text = ev.get("date", "")
                row_cells[1].text = ev.get("event", "")
                row_cells[2].text = ev.get("significance", "")

        # 4. Contradictions
        if data.get("contradictions"):
            doc.add_heading("Factual Contradictions Log", level=1)
            for idx, c in enumerate(data.get("contradictions", [])):
                p = doc.add_paragraph()
                p.add_run(f"Conflict {idx+1} [Severity: {c.get('severity').upper()}]\n").bold = True
                p.add_run(f"Claim A: ").bold = True
                p.add_run(f"{c.get('claim_a')} ({c.get('source_a') or 'Source A'})\n")
                p.add_run(f"Claim B: ").bold = True
                p.add_run(f"{c.get('claim_b')} ({c.get('source_b') or 'Source B'})\n")

        # 5. References
        if options.get("include_sources") and data.get("sources"):
            doc.add_heading("References & Sources", level=1)
            for idx, src in enumerate(data.get("sources", [])):
                p = doc.add_paragraph()
                p.add_run(f"{idx+1}. {src.get('title') or 'Source'}\n").bold = True
                p.add_run(f"URL: {src.get('url') or 'N/A'}\n")
                if src.get("snippet"):
                    p.add_run(f"Context: {src.get('snippet')[:150]}...").italic = True

        doc.save(file_path)
        return True

    def _generate_pptx(
        self,
        file_path: str,
        title: str,
        data: Dict[str, Any],
        source_type: str,
        options: Dict[str, bool]
    ) -> bool:
        """Generate PowerPoint slide deck using python-pptx."""
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor

        prs = Presentation()

        # Slide Layout Types
        blank_layout = prs.slide_layouts[6]
        
        # Helper to set background color
        def set_slide_bg(slide, rgb_tuple):
            background = slide.background
            fill = background.fill
            fill.solid()
            fill.fore_color.rgb = RGBColor(*rgb_tuple)

        # ─── Slide 1: Title Slide ─────────────────────────────────────────────
        slide1 = prs.slides.add_slide(blank_layout)
        set_slide_bg(slide1, (59, 42, 80)) # Dark purple background
        
        txBox = slide1.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(3))
        tf = txBox.text_frame
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(40)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        p2 = tf.add_paragraph()
        p2.text = "AI-Generated Summary Deck" if source_type == "research" else "AI Document Intelligence Slides"
        p2.font.size = Pt(20)
        p2.font.color.rgb = RGBColor(200, 180, 220)

        # ─── Slide 2: Executive Summary ───────────────────────────────────────
        slide2 = prs.slides.add_slide(blank_layout)
        set_slide_bg(slide2, (255, 255, 255))
        
        # Title
        txBox = slide2.shapes.add_textbox(Inches(0.75), Inches(0.5), Inches(8.5), Inches(0.8))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = "Executive Summary"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(59, 42, 80)
        
        # Content
        txBox = slide2.shapes.add_textbox(Inches(0.75), Inches(1.5), Inches(8.5), Inches(4.5))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = data.get("summary") or "No executive summary available."
        p.font.size = Pt(16)
        p.font.color.rgb = RGBColor(40, 40, 40)

        # ─── Slide 3: Perspectives or Detailed Content ────────────────────────
        if data.get("deep_summary") or data.get("technical_analysis"):
            slide3 = prs.slides.add_slide(blank_layout)
            set_slide_bg(slide3, (255, 255, 255))
            
            txBox = slide3.shapes.add_textbox(Inches(0.75), Inches(0.5), Inches(8.5), Inches(0.8))
            tf = txBox.text_frame
            p = tf.paragraphs[0]
            p.text = "Technical Deep-Dive" if data.get("technical_analysis") else "Detailed Analysis"
            p.font.size = Pt(28)
            p.font.bold = True
            p.font.color.rgb = RGBColor(59, 42, 80)
            
            txBox = slide3.shapes.add_textbox(Inches(0.75), Inches(1.5), Inches(8.5), Inches(4.5))
            tf = txBox.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = data.get("technical_analysis") or data.get("deep_summary") or ""
            p.font.size = Pt(15)
            p.font.color.rgb = RGBColor(40, 40, 40)

        # ─── Slide 4: Timeline Slide ──────────────────────────────────────────
        if data.get("timeline"):
            slide4 = prs.slides.add_slide(blank_layout)
            set_slide_bg(slide4, (255, 255, 255))
            
            txBox = slide4.shapes.add_textbox(Inches(0.75), Inches(0.5), Inches(8.5), Inches(0.8))
            tf = txBox.text_frame
            p = tf.paragraphs[0]
            p.text = "Chronological Milestones"
            p.font.size = Pt(28)
            p.font.bold = True
            p.font.color.rgb = RGBColor(59, 42, 80)
            
            # Content
            txBox = slide4.shapes.add_textbox(Inches(0.75), Inches(1.5), Inches(8.5), Inches(4.5))
            tf = txBox.text_frame
            tf.word_wrap = True
            
            for ev in data.get("timeline", [])[:5]: # Cap at 5 for slides
                p = tf.add_paragraph()
                p.text = f"• {ev.get('date')}: {ev.get('event')}"
                p.font.size = Pt(16)
                p.font.bold = True
                p.font.color.rgb = RGBColor(50, 50, 50)
                
                p_sig = tf.add_paragraph()
                p_sig.text = f"  Significance: {ev.get('significance')}"
                p_sig.font.size = Pt(14)
                p_sig.font.color.rgb = RGBColor(100, 100, 100)

        # ─── Slide 5: References & Sources ────────────────────────────────────
        if data.get("sources"):
            slide5 = prs.slides.add_slide(blank_layout)
            set_slide_bg(slide5, (255, 255, 255))
            
            txBox = slide5.shapes.add_textbox(Inches(0.75), Inches(0.5), Inches(8.5), Inches(0.8))
            tf = txBox.text_frame
            p = tf.paragraphs[0]
            p.text = "References & Core Sources"
            p.font.size = Pt(28)
            p.font.bold = True
            p.font.color.rgb = RGBColor(59, 42, 80)
            
            txBox = slide5.shapes.add_textbox(Inches(0.75), Inches(1.5), Inches(8.5), Inches(4.5))
            tf = txBox.text_frame
            tf.word_wrap = True
            
            for idx, src in enumerate(data.get("sources", [])[:6]):
                p = tf.add_paragraph()
                p.text = f"{idx+1}. {src.get('title')} ({src.get('source_type', 'web').upper()})"
                p.font.size = Pt(14)
                p.font.color.rgb = RGBColor(80, 80, 80)

        prs.save(file_path)
        return True

    def _generate_markdown(
        self,
        file_path: str,
        title: str,
        data: Dict[str, Any],
        source_type: str,
        options: Dict[str, bool]
    ) -> bool:
        """Generate standard Markdown file."""
        lines = []
        lines.append(f"# {title}")
        lines.append(f"*AI-Generated Report - Compiled on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        lines.append("")
        
        # 1. Summary
        lines.append("## Executive Summary")
        lines.append(data.get("summary") or "No summary available.")
        lines.append("")

        # 2. Detailed summary
        if data.get("deep_summary"):
            lines.append("## Detailed Analysis")
            lines.append(data.get("deep_summary"))
            lines.append("")

        # Deep Research Details
        if source_type == "research" and data.get("mode") == "deep":
            if data.get("technical_analysis"):
                lines.append("## Technical Deep-Dive")
                lines.append(data.get("technical_analysis"))
                lines.append("")
            if data.get("beginner_explanation"):
                lines.append("## Simplified Explanation (ELI5)")
                lines.append(data.get("beginner_explanation"))
                lines.append("")
            if data.get("expert_explanation"):
                lines.append("## Expert Commentary")
                lines.append(data.get("expert_explanation"))
                lines.append("")
            if data.get("future_predictions"):
                lines.append("## Future Predictions & Outlook")
                lines.append(data.get("future_predictions"))
                lines.append("")

        # Document Topics/Entities
        if source_type == "document":
            if data.get("topics"):
                lines.append("## Extracted Topics")
                for t in data.get("topics", []):
                    lines.append(f"- **{t.get('topic')}** (Weight: {t.get('weight', 1.0)}): Keywords: {', '.join(t.get('keywords', []))}")
                lines.append("")
            if data.get("entities"):
                lines.append("## Key Entities")
                entities_str = ", ".join([f"{e.get('text')} ({e.get('label')})" for e in data.get("entities", [])])
                lines.append(entities_str)
                lines.append("")

        # 3. Timeline
        if options.get("include_timeline") and data.get("timeline"):
            lines.append("## Chronological Timeline")
            lines.append("| Date | Event | Significance |")
            lines.append("| --- | --- | --- |")
            for ev in data.get("timeline", []):
                lines.append(f"| {ev.get('date')} | {ev.get('event')} | {ev.get('significance')} |")
            lines.append("")

        # 4. Contradictions
        if data.get("contradictions"):
            lines.append("## Contradictions & Factual Conflicts")
            for idx, c in enumerate(data.get("contradictions", [])):
                lines.append(f"### Conflict {idx+1} [Severity: {c.get('severity').upper()}]")
                lines.append(f"- **Claim A:** {c.get('claim_a')}")
                lines.append(f"  - *Source A:* {c.get('source_a') or 'Unspecified'}")
                lines.append(f"- **Claim B:** {c.get('claim_b')}")
                lines.append(f"  - *Source B:* {c.get('source_b') or 'Unspecified'}")
                lines.append("")

        # 5. References
        if options.get("include_sources") and data.get("sources"):
            lines.append("## References & Sources")
            for idx, src in enumerate(data.get("sources", [])):
                lines.append(f"{idx+1}. **[{src.get('title')}]({src.get('url') or '#'})** [{src.get('source_type', 'web').upper()}]")
                if src.get("snippet"):
                    lines.append(f"   > *Snippet:* {src.get('snippet')[:200]}...")
                lines.append("")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
            
        return True

report_generator = ReportGenerator()
