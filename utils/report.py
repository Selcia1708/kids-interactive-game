"""
PDF Progress Report Generator  —  requires:  pip install reportlab
"""
from io import BytesIO
from datetime import datetime

def generate_pdf_report(child_name, age, avatar, stars, xp,
                        skill_scores, badges,
                        sessions=None, achievements=None):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor, white, black, Color
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                        Table, TableStyle, HRFlowable,
                                        KeepTogether)
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
        from reportlab.pdfgen import canvas as pdfcanvas

        # ── Colour Palette ───────────────────────────────────────────────────
        DARK_BG   = HexColor("#0f0c29")
        MID_BG    = HexColor("#302b63")
        ACCENT1   = HexColor("#f093fb")   # pink
        ACCENT2   = HexColor("#4facfe")   # blue
        ACCENT3   = HexColor("#43e97b")   # green
        GOLD      = HexColor("#f6d365")
        LIGHT_TXT = HexColor("#ffffff")
        BODY_TXT  = HexColor("#2d2d2d")
        MUTED     = HexColor("#888888")
        ROW_ALT   = HexColor("#f5f0ff")
        ROW_NORM  = HexColor("#ffffff")
        BORDER    = HexColor("#e0d6f5")
        HEADER_BG = HexColor("#302b63")
        SECTION_LINE = HexColor("#c9b8f0")

        buf = BytesIO()

        # ── Page size & margins ──────────────────────────────────────────────
        W, H = A4   # 595 x 842 pts
        LM = RM = 2.0 * cm
        TM = 2.5 * cm
        BM = 2.0 * cm

        # ── Paragraph styles ─────────────────────────────────────────────────
        base = getSampleStyleSheet()["Normal"]

        def sty(name, **kw):
            return ParagraphStyle(name, parent=base, **kw)

        cover_title = sty("CT",
            fontSize=28, textColor=LIGHT_TXT, alignment=TA_CENTER,
            fontName="Helvetica-Bold", spaceAfter=6, leading=34)

        cover_sub = sty("CS",
            fontSize=13, textColor=HexColor("#d0c8f0"), alignment=TA_CENTER,
            spaceAfter=4, leading=18)

        cover_date = sty("CD",
            fontSize=10, textColor=HexColor("#a090d0"), alignment=TA_CENTER,
            spaceAfter=0)

        section_heading = sty("SH",
            fontSize=13, textColor=MID_BG, fontName="Helvetica-Bold",
            spaceBefore=18, spaceAfter=8, leading=18)

        body = sty("BD",
            fontSize=10, textColor=BODY_TXT, spaceAfter=4, leading=15)

        rec_style = sty("RC",
            fontSize=10, textColor=BODY_TXT, spaceAfter=6,
            leading=15, leftIndent=8)

        footer_style = sty("FT",
            fontSize=8, textColor=MUTED, alignment=TA_CENTER, leading=12)

        kpi_label = sty("KL",
            fontSize=8, textColor=MUTED, alignment=TA_CENTER,
            fontName="Helvetica", leading=12)

        kpi_value = sty("KV",
            fontSize=22, textColor=MID_BG, alignment=TA_CENTER,
            fontName="Helvetica-Bold", leading=26)

        table_header_sty = sty("TH",
            fontSize=10, textColor=LIGHT_TXT, fontName="Helvetica-Bold",
            alignment=TA_CENTER, leading=14)

        table_cell_sty = sty("TC",
            fontSize=9, textColor=BODY_TXT, alignment=TA_CENTER, leading=13)

        # ── Helper: section divider ──────────────────────────────────────────
        def section_div(label):
            return [
                Spacer(1, 0.3 * cm),
                Paragraph(label.upper(), section_heading),
                HRFlowable(width="100%", thickness=1.5,
                           color=SECTION_LINE, spaceAfter=8),
            ]

        # ── Helper: styled table ─────────────────────────────────────────────
        def styled_table(data, col_widths, hdr_bg=HEADER_BG):
            t = Table(data, colWidths=col_widths, repeatRows=1)
            row_count = len(data)
            style_cmds = [
                # Header
                ("BACKGROUND",  (0, 0), (-1, 0), hdr_bg),
                ("TEXTCOLOR",   (0, 0), (-1, 0), LIGHT_TXT),
                ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE",    (0, 0), (-1, 0), 10),
                ("ALIGN",       (0, 0), (-1, 0), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("TOPPADDING",    (0, 0), (-1, 0), 10),
                # Body rows
                ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE",    (0, 1), (-1, -1), 9),
                ("ALIGN",       (0, 1), (-1, -1), "CENTER"),
                ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING",  (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
                # Grid
                ("GRID",        (0, 0), (-1, -1), 0.5, BORDER),
                ("LINEBELOW",   (0, 0), (-1, 0),  1.5, hdr_bg),
            ]
            # Alternating row colours
            for r in range(1, row_count):
                bg = ROW_ALT if r % 2 == 0 else ROW_NORM
                style_cmds.append(("BACKGROUND", (0, r), (-1, r), bg))

            t.setStyle(TableStyle(style_cmds))
            return t

        # ── Cover banner (drawn on canvas) ───────────────────────────────────
        class CoverPage(BaseDocTemplate):
            def __init__(self, filename, **kwargs):
                super().__init__(filename, **kwargs)
                frame = Frame(LM, BM, W - LM - RM, H - TM - BM,
                              id="normal", leftPadding=0, rightPadding=0,
                              topPadding=0, bottomPadding=0)
                template = PageTemplate(id="main", frames=[frame],
                                        onPage=self._draw_page)
                self.addPageTemplates([template])

            def _draw_page(self, canv, doc):
                canv.saveState()
                # Dark header banner
                banner_h = 7.0 * cm
                canv.setFillColor(DARK_BG)
                canv.rect(0, H - banner_h, W, banner_h, fill=1, stroke=0)
                # Accent strip at bottom of banner
                canv.setFillColor(ACCENT1)
                canv.rect(0, H - banner_h - 6, W, 6, fill=1, stroke=0)
                # Footer bar
                canv.setFillColor(HexColor("#f5f0ff"))
                canv.rect(0, 0, W, BM - 0.3 * cm, fill=1, stroke=0)
                canv.setFont("Helvetica", 8)
                canv.setFillColor(MUTED)
                canv.drawCentredString(W / 2, 0.5 * cm,
                    f"Kids Learning Universe  |  Confidential Progress Report  |  {datetime.now().strftime('%B %Y')}")
                canv.restoreState()

        doc = CoverPage(buf, pagesize=A4,
                        leftMargin=LM, rightMargin=RM,
                        topMargin=TM, bottomMargin=BM)

        story = []

        # ════════════════════════════════════════════════════════════════════
        # COVER / HEADER
        # ════════════════════════════════════════════════════════════════════
        story += [
            Spacer(1, 1.2 * cm),   # push content below banner
            Paragraph("Kids Learning Universe", cover_title),
            Paragraph("Parent Progress Report", cover_sub),
            Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y  at  %H:%M')}", cover_date),
            Spacer(1, 2.2 * cm),
        ]

        # ════════════════════════════════════════════════════════════════════
        # EXPLORER PROFILE CARD
        # ════════════════════════════════════════════════════════════════════
        story += section_div("Explorer Profile")

        AVATAR_NAMES = {
            "🧑‍🚀": "Astronaut",
            "🧙":   "Wizard",
            "🦸":   "Superhero",
            "🧜":   "Mermaid",
        }
        avatar_name = AVATAR_NAMES.get(avatar, avatar)

        # ── Leaderboard rank lookup ──────────────────────────────────────────
        rank_display = "N/A"
        rank_out_of  = "N/A"
        try:
            from database.db import get_leaderboard
            board = get_leaderboard(100)
            rank_out_of = str(len(board))
            for idx, entry in enumerate(board, start=1):
                if entry["name"].strip().lower() == child_name.strip().lower():
                    rank_display = f"#{idx}"
                    break
            else:
                rank_display = "Unranked"
        except Exception:
            rank_display = "N/A"
            rank_out_of  = "N/A"

        profile_data = [
            ["Field", "Details"],
            ["Name",        child_name],
            ["Age",         f"{age} years old"],
            ["Avatar",      avatar_name],
            ["Leaderboard Rank", f"{rank_display}  out of {rank_out_of} explorers"],
            ["Report Date", datetime.now().strftime("%B %d, %Y")],
        ]
        story.append(styled_table(profile_data,
                                  [5 * cm, W - LM - RM - 5 * cm]))
        story.append(Spacer(1, 0.4 * cm))

        # ════════════════════════════════════════════════════════════════════
        # KPI SUMMARY ROW
        # ════════════════════════════════════════════════════════════════════
        story += section_div("Achievement Summary")

        active_worlds = len([v for v in skill_scores.values() if v > 0])
        kpi_items = [
            ("Stars Earned",  str(stars)),
            ("XP Points",     str(xp)),
            ("Badges",        str(len(badges))),
            ("Worlds Active", str(active_worlds)),
        ]

        kpi_row_labels = [[Paragraph(lbl, kpi_label) for lbl, _ in kpi_items]]
        kpi_row_values = [[Paragraph(val, kpi_value) for _, val in kpi_items]]

        kpi_table = Table(
            kpi_row_labels + kpi_row_values,
            colWidths=[(W - LM - RM) / 4] * 4
        )
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#f9f5ff")),
            ("BACKGROUND",    (0, 0), (-1, 0),  HexColor("#ede8fc")),
            ("GRID",          (0, 0), (-1, -1), 0.5, BORDER),
            ("TOPPADDING",    (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LINEABOVE",     (0, 0), (-1, 0),  2, ACCENT1),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 0.4 * cm))

        # ════════════════════════════════════════════════════════════════════
        # SKILL BREAKDOWN
        # ════════════════════════════════════════════════════════════════════
        story += section_div("Skill Breakdown")

        skill_colors = {
            "phonics":    "#f093fb",
            "math":       "#4facfe",
            "logic":      "#a18cd1",
            "science":    "#43e97b",
            "creativity": "#fa709a",
        }

        skill_rows = [["Subject", "Score", "Level", "Status"]]
        for skill, val in skill_scores.items():
            level_str  = "Advanced"     if val >= 70 else "Intermediate" if val >= 40 else "Beginner"
            status_str = "Excellent"    if val >= 80 else "Good"         if val >= 50 else "Growing"
            skill_rows.append([
                skill.capitalize(),
                f"{val}%",
                level_str,
                status_str,
            ])

        col_w = (W - LM - RM) / 4
        skill_table = styled_table(skill_rows,
                                   [col_w * 1.2, col_w * 0.8, col_w, col_w],
                                   hdr_bg=HexColor("#4facfe"))

        # Colour-code score cells
        for r_idx, (skill, val) in enumerate(skill_scores.items(), start=1):
            clr = HexColor(skill_colors.get(skill, "#888888"))
            skill_table._argW  # touch to ensure style list accessible
            skill_table.setStyle(TableStyle([
                ("TEXTCOLOR", (1, r_idx), (1, r_idx), clr),
                ("FONTNAME",  (1, r_idx), (1, r_idx), "Helvetica-Bold"),
                ("FONTSIZE",  (1, r_idx), (1, r_idx), 11),
            ]))

        story.append(skill_table)
        story.append(Spacer(1, 0.4 * cm))

        # ════════════════════════════════════════════════════════════════════
        # BADGES
        # ════════════════════════════════════════════════════════════════════
        story += section_div("Badges Earned")

        if badges:
            # Strip emoji from badge names for clean PDF rendering
            import re
            clean_badges = [re.sub(r'[^\x00-\x7F]', '', b).strip() for b in badges]
            clean_badges = [b for b in clean_badges if b]  # remove empty

            cols_per_row = 3
            col_w_b = (W - LM - RM) / cols_per_row
            for i in range(0, len(clean_badges), cols_per_row):
                chunk = clean_badges[i:i + cols_per_row]
                while len(chunk) < cols_per_row:
                    chunk.append("")
                bt = Table([chunk], colWidths=[col_w_b] * cols_per_row)
                bt.setStyle(TableStyle([
                    ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#fff8e1")),
                    ("TEXTCOLOR",     (0, 0), (-1, -1), MID_BG),
                    ("FONTNAME",      (0, 0), (-1, -1), "Helvetica-Bold"),
                    ("FONTSIZE",      (0, 0), (-1, -1), 10),
                    ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID",          (0, 0), (-1, -1), 0.5, HexColor("#f6d365")),
                    ("TOPPADDING",    (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("LINEABOVE",     (0, 0), (-1, 0),  2, GOLD),
                ]))
                story += [bt, Spacer(1, 0.2 * cm)]
        else:
            story.append(Paragraph("No badges earned yet — keep exploring!", body))

        story.append(Spacer(1, 0.2 * cm))

        # ════════════════════════════════════════════════════════════════════
        # SESSION HISTORY
        # ════════════════════════════════════════════════════════════════════
        if sessions:
            story += section_div("Recent Session History")
            sess_rows = [["World", "Score", "Duration", "Date"]]
            for s in sessions[:10]:
                mins = s.get("duration_s", 0) // 60
                secs = s.get("duration_s", 0) % 60
                sess_rows.append([
                    s.get("world", "—").capitalize(),
                    str(s.get("score", 0)),
                    f"{mins}m {secs}s",
                    str(s.get("played_at", "—"))[:10],
                ])
            cw = (W - LM - RM) / 4
            story.append(styled_table(sess_rows,
                                      [cw * 1.3, cw * 0.7, cw, cw],
                                      hdr_bg=HexColor("#43e97b")))
            story.append(Spacer(1, 0.4 * cm))

        # ════════════════════════════════════════════════════════════════════
        # RECOMMENDATIONS
        # ════════════════════════════════════════════════════════════════════
        story += section_div("Parent Recommendations")

        level_labels = {
            0:  ("Not Started",   HexColor("#f87171")),
            40: ("Early Stage",   HexColor("#fb923c")),
            70: ("Developing",    HexColor("#facc15")),
            80: ("Nearly Mastered", HexColor("#4ade80")),
        }

        rec_rows = [["Subject", "Status", "Recommendation"]]
        for skill, val in skill_scores.items():
            if val == 0:
                status = "Not Started"
                rec    = "Encourage your child to explore this world!"
            elif val < 40:
                status = f"Early Stage ({val}%)"
                rec    = "More practice sessions would help build confidence."
            elif val < 70:
                status = f"Developing ({val}%)"
                rec    = "Good progress! Keep the momentum going."
            elif val < 80:
                status = f"Advanced ({val}%)"
                rec    = "Almost there — try the hardest challenges!"
            else:
                status = f"Mastered ({val}%)"
                rec    = "Outstanding! Explore bonus challenges."
            rec_rows.append([skill.capitalize(), status, rec])

        cw2 = W - LM - RM
        rec_table = styled_table(rec_rows,
                                  [cw2 * 0.2, cw2 * 0.25, cw2 * 0.55],
                                  hdr_bg=HexColor("#a18cd1"))
        # Left-align the recommendation column
        rec_table.setStyle(TableStyle([
            ("ALIGN",  (2, 1), (2, -1), "LEFT"),
            ("FONTNAME", (2, 1), (2, -1), "Helvetica"),
        ]))
        story.append(rec_table)

        # ════════════════════════════════════════════════════════════════════
        # FOOTER SPACER
        # ════════════════════════════════════════════════════════════════════
        story += [
            Spacer(1, 1.0 * cm),
            HRFlowable(width="100%", thickness=1, color=SECTION_LINE,
                       spaceAfter=6),
            Paragraph(
                "This report was automatically generated by Kids Learning Universe. "
                "All progress data reflects the child's activity within the app.",
                footer_style
            ),
        ]

        doc.build(story)
        return buf.getvalue()

    except ImportError as e:
        print(f"PDF generation failed: {e}")
        return None
    except Exception as e:
        print(f"PDF generation error: {e}")
        return None