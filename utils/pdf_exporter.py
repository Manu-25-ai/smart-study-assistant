import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER


# ── Colour palette (mirrors the app UI) ──────────────────────────────────────
PURPLE      = colors.HexColor("#7C6AF7")
TEAL        = colors.HexColor("#4ECDC4")
DARK_BG     = colors.HexColor("#13131C")
CARD_BORDER = colors.HexColor("#22223A")
TEXT_MAIN   = colors.HexColor("#1A1A2E")
TEXT_MUTED  = colors.HexColor("#5A5A70")
WHITE       = colors.white


def _styles():
    base = getSampleStyleSheet()

    title = ParagraphStyle(
        "NoteTitle",
        parent=base["Title"],
        fontSize=24,
        textColor=PURPLE,
        spaceAfter=4,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    )
    subtitle = ParagraphStyle(
        "NoteSubtitle",
        parent=base["Normal"],
        fontSize=10,
        textColor=TEXT_MUTED,
        spaceAfter=2,
        alignment=TA_CENTER,
    )
    section_head = ParagraphStyle(
        "SectionHead",
        parent=base["Heading2"],
        fontSize=12,
        textColor=PURPLE,
        fontName="Helvetica-Bold",
        spaceBefore=14,
        spaceAfter=6,
        borderPad=0,
    )
    body = ParagraphStyle(
        "NoteBody",
        parent=base["Normal"],
        fontSize=10,
        textColor=TEXT_MAIN,
        leading=16,
        spaceAfter=4,
    )
    lang_badge = ParagraphStyle(
        "LangBadge",
        parent=base["Normal"],
        fontSize=9,
        textColor=TEAL,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    return {
        "title": title,
        "subtitle": subtitle,
        "section_head": section_head,
        "body": body,
        "lang_badge": lang_badge,
    }


def generate_pdf(notes: str, transcript: str, language: str = "unknown") -> bytes:
    """
    Generates a styled PDF from the raw notes string returned by generate_notes().
    Returns PDF as bytes (ready for st.download_button).
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    s = _styles()
    story = []

    # ── Header ──
    story.append(Paragraph("NoteFlow AI", s["title"]))
    story.append(Paragraph("AI-Generated Video Notes", s["subtitle"]))

    lang_display = language.upper() if language != "unknown" else "Auto-detected"
    story.append(Paragraph(f"Language detected: {lang_display}", s["lang_badge"]))
    story.append(HRFlowable(width="100%", thickness=1, color=PURPLE, spaceAfter=10))

    # ── Notes section ──
    story.append(Paragraph("Generated Notes", s["section_head"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=CARD_BORDER, spaceAfter=6))

    # Split notes into lines and render each, preserving structure
    for line in notes.splitlines():
        line = line.strip()
        if not line:
            story.append(Spacer(1, 4))
            continue

        # Section headers (lines ending with : or all caps short lines)
        if line.endswith(":") or (line.isupper() and len(line) < 60):
            story.append(Spacer(1, 6))
            story.append(Paragraph(line, s["section_head"]))
            story.append(HRFlowable(width="100%", thickness=0.4, color=CARD_BORDER, spaceAfter=4))
        else:
            # Escape special XML chars for ReportLab
            safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(safe, s["body"]))

    # ── Transcript section ──
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=PURPLE, spaceAfter=6))
    story.append(Paragraph("Full Transcript", s["section_head"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=CARD_BORDER, spaceAfter=6))

    transcript_style = ParagraphStyle(
        "Transcript",
        fontSize=8.5,
        textColor=TEXT_MUTED,
        leading=13,
        spaceAfter=3,
    )
    safe_transcript = transcript.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    story.append(Paragraph(safe_transcript, transcript_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()