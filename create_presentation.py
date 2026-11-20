"""
AgriTwinX - Precision Paddy Farming Digital Twin System
Professional Academic PowerPoint Presentation Generator
For Karunya Institute of Technology and Sciences - Final Year B.Tech Project Review
Course Code: 23AI2014 | Student: Aiswarya AV (URK23CS5048) | Supervisor: Mr. K. Martin Victor
"""

import os
from PIL import Image
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ==========================================
# CONSTANTS & THEME PALETTE
# ==========================================
DEEP_GREEN    = RGBColor(27, 67, 50)     # #1B4332 - Headers, major emphasis
DARK_EMERALD  = RGBColor(8, 28, 21)      # #081C15 - Deep contrast
FOREST_GREEN  = RGBColor(45, 106, 79)    # #2D6A4F - Secondary headers, cards
ACCENT_GREEN  = RGBColor(64, 145, 108)   # #40916C - Badges, highlights, borders
MINT_TINT     = RGBColor(216, 243, 220)  # #D8F3DC - Light badge fills
SAGE_BG       = RGBColor(238, 245, 239)  # #EEF5EF - Soft card backgrounds
WARM_BG       = RGBColor(249, 250, 248)  # #F9FAF8 - Overall slide canvas

# Neutral Colors
CARD_WHITE    = RGBColor(255, 255, 255)  # Pure White
TEXT_DARK     = RGBColor(30, 41, 59)     # #1E293B - High readability body text
TEXT_MUTED    = RGBColor(71, 85, 105)    # #475569 - Secondary text, metadata
BORDER_LIGHT  = RGBColor(226, 232, 240)  # #E2E8F0 - Subtle card outline
BORDER_GREEN  = RGBColor(183, 228, 199)  # #B7E4C7 - Green accent border
AMBER_ACCENT  = RGBColor(217, 119, 6)    # #D97706 - Highlights / Warnings
ALERT_BG      = RGBColor(254, 242, 242)  # #FEF2F2 - Placeholder / Alert fill
ALERT_BORDER  = RGBColor(248, 113, 113)  # #F87171 - Placeholder border

FONT_PRIMARY   = "Segoe UI"
FONT_HEADING   = "Segoe UI"

LOGO_BANNER = "extracted_logo_0_1.png"
LOGO_CREST  = "extracted_logo_1_2.png"

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def set_slide_background(slide, color=WARM_BG):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.color.rgb = color
    return bg_shape

def add_header(slide, title, category="FINAL YEAR B.TECH PROJECT REVIEW • 23AI2014"):
    # Header container bar
    header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.15))
    header_box.fill.solid()
    header_box.fill.fore_color.rgb = CARD_WHITE
    header_box.line.color.rgb = BORDER_LIGHT

    # Karunya Emblem Logo on Left
    if os.path.exists(LOGO_CREST):
        add_picture_fit(slide, LOGO_CREST, 0.55, 0.12, 0.95, 0.90)

    # Breadcrumb / Category
    cat_box = slide.shapes.add_textbox(Inches(1.65), Inches(0.18), Inches(11.0), Inches(0.3))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.name = FONT_PRIMARY
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ACCENT_GREEN

    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(1.65), Inches(0.42), Inches(11.0), Inches(0.55))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = DEEP_GREEN

    # Accent divider line beneath header
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(1.14), Inches(12.233), Inches(0.025))
    line.fill.solid()
    line.fill.fore_color.rgb = FOREST_GREEN
    line.line.color.rgb = FOREST_GREEN

def add_footer(slide, slide_num, total_slides=14):
    # Top divider
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(6.92), Inches(12.233), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_LIGHT
    line.line.color.rgb = BORDER_LIGHT

    # Left text
    left_box = slide.shapes.add_textbox(Inches(0.55), Inches(6.98), Inches(7.5), Inches(0.35))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_right = tf_left.margin_bottom = 0
    p_left = tf_left.paragraphs[0]
    p_left.text = "AgriTwinX: Precision Paddy Farming Digital Twin  |  Aiswarya AV (URK23CS5048)  |  Supervisor: Mr. K. Martin Victor"
    p_left.font.name = FONT_PRIMARY
    p_left.font.size = Pt(8.5)
    p_left.font.color.rgb = TEXT_MUTED

    # Center/Dept text
    center_box = slide.shapes.add_textbox(Inches(8.2), Inches(6.98), Inches(3.6), Inches(0.35))
    tf_cen = center_box.text_frame
    tf_cen.word_wrap = True
    tf_cen.margin_left = tf_cen.margin_top = tf_cen.margin_right = tf_cen.margin_bottom = 0
    p_cen = tf_cen.paragraphs[0]
    p_cen.text = "Division of AI & ML | Dept. of CSE | KITS"
    p_cen.font.name = FONT_PRIMARY
    p_cen.font.size = Pt(8.5)
    p_cen.font.color.rgb = TEXT_MUTED

    # Slide pill badge on right
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(12.0), Inches(6.96), Inches(0.80), Inches(0.28))
    badge.fill.solid()
    badge.fill.fore_color.rgb = MINT_TINT
    badge.line.color.rgb = ACCENT_GREEN
    tf_b = badge.text_frame
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    p_b.text = f"{slide_num} / {total_slides}"
    p_b.font.name = FONT_PRIMARY
    p_b.font.size = Pt(8.5)
    p_b.font.bold = True
    p_b.font.color.rgb = DEEP_GREEN

def add_card(slide, left, top, width, height, bg_color=CARD_WHITE, border_color=BORDER_LIGHT):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.0)
    return card

def add_picture_fit(slide, img_path, box_left, box_top, box_width, box_height):
    """
    Embeds an image into a specified bounding box preserving its native aspect ratio
    and centers it within the box without stretching or distortion.
    """
    if not os.path.exists(img_path):
        return None
    with Image.open(img_path) as im:
        img_w, img_h = im.size
    img_aspect = img_w / img_h
    box_aspect = box_width / box_height

    if img_aspect > box_aspect:
        target_w = box_width
        target_h = box_width / img_aspect
        target_left = box_left
        target_top = box_top + (box_height - target_h) / 2.0
    else:
        target_h = box_height
        target_w = box_height * img_aspect
        target_top = box_top
        target_left = box_left + (box_width - target_w) / 2.0

    return slide.shapes.add_picture(
        img_path,
        Inches(target_left),
        Inches(target_top),
        width=Inches(target_w),
        height=Inches(target_h)
    )

def add_formatted_bullet(text_frame, bold_prefix, text_body, pt_size=10, space_after=5, bullet=True):
    p = text_frame.add_paragraph() if len(text_frame.paragraphs[0].text) > 0 else text_frame.paragraphs[0]
    p.font.name = FONT_PRIMARY
    p.font.size = Pt(pt_size)
    p.space_after = Pt(space_after)
    if bullet:
        p.level = 0
    
    r1 = p.add_run()
    r1.text = bold_prefix + (" " if bold_prefix else "")
    r1.font.bold = True
    r1.font.color.rgb = DEEP_GREEN
    
    r2 = p.add_run()
    r2.text = text_body
    r2.font.bold = False
    r2.font.color.rgb = TEXT_DARK

# ==========================================
# SLIDE BUILDERS
# ==========================================

# ------------------------------------------
# SLIDE 1: Title Slide (Official Viva Voce)
# ------------------------------------------
def build_slide_1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, WARM_BG)

    # University Header Container
    u_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(0.30), Inches(12.233), Inches(1.10))
    u_box.fill.solid()
    u_box.fill.fore_color.rgb = CARD_WHITE
    u_box.line.color.rgb = BORDER_GREEN
    u_box.line.width = Pt(1.5)

    tf_u = u_box.text_frame
    tf_u.word_wrap = True
    tf_u.margin_top = Inches(0.08)

    p0 = tf_u.paragraphs[0]
    p0.alignment = PP_ALIGN.CENTER
    p0.text = "DIVISION OF ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING"
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = DEEP_GREEN

    p1 = tf_u.add_paragraph()
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING"
    p1.font.name = FONT_PRIMARY
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = FOREST_GREEN

    p2 = tf_u.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "23AI2014 Project Requirement Specification  •  ODD SEMESTER 2026–2027"
    p2.font.name = FONT_PRIMARY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_MUTED

    p3 = tf_u.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.text = "END SEMESTER VIVA VOCE EXAMINATION"
    p3.font.name = FONT_PRIMARY
    p3.font.size = Pt(11)
    p3.font.bold = True
    p3.font.color.rgb = AMBER_ACCENT

    # Main Project Title Box
    title_card = add_card(slide, 0.55, 1.55, 12.233, 2.10, CARD_WHITE, BORDER_GREEN)
    tf_t = title_card.text_frame
    tf_t.word_wrap = True
    tf_t.margin_top = Inches(0.18)

    pt0 = tf_t.paragraphs[0]
    pt0.alignment = PP_ALIGN.CENTER
    pt0.text = "AgriTwinX"
    pt0.font.name = FONT_HEADING
    pt0.font.size = Pt(36)
    pt0.font.bold = True
    pt0.font.color.rgb = DEEP_GREEN

    pt1 = tf_t.add_paragraph()
    pt1.alignment = PP_ALIGN.CENTER
    pt1.text = "A Precision Paddy Farming Digital Twin System"
    pt1.font.name = FONT_PRIMARY
    pt1.font.size = Pt(18)
    pt1.font.bold = True
    pt1.font.color.rgb = FOREST_GREEN

    pt2 = tf_t.add_paragraph()
    pt2.alignment = PP_ALIGN.CENTER
    pt2.text = "An Explainable, Multi-Modal Cyber-Physical Decision-Support Platform for Rice Cultivation"
    pt2.font.name = FONT_PRIMARY
    pt2.font.size = Pt(11.5)
    pt2.font.italic = True
    pt2.font.color.rgb = TEXT_MUTED

    pt3 = tf_t.add_paragraph()
    pt3.alignment = PP_ALIGN.CENTER
    pt3.text = "UN SDG Addressed: Goal 2 (Zero Hunger - Target 2.4) & Goal 12 (Responsible Consumption & Production)"
    pt3.font.name = FONT_PRIMARY
    pt3.font.size = Pt(10.5)
    pt3.font.bold = True
    pt3.font.color.rgb = AMBER_ACCENT

    # Left Card: Presented By
    p_card = add_card(slide, 0.55, 3.80, 5.95, 1.95, CARD_WHITE, BORDER_LIGHT)
    tf_p = p_card.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = Inches(0.25)
    tf_p.margin_top = Inches(0.15)

    pp0 = tf_p.paragraphs[0]
    pp0.text = "PRESENTED BY"
    pp0.font.name = FONT_PRIMARY
    pp0.font.size = Pt(10)
    pp0.font.bold = True
    pp0.font.color.rgb = ACCENT_GREEN

    pp1 = tf_p.add_paragraph()
    pp1.text = "Aiswarya AV"
    pp1.font.name = FONT_HEADING
    pp1.font.size = Pt(17)
    pp1.font.bold = True
    pp1.font.color.rgb = DEEP_GREEN

    pp2 = tf_p.add_paragraph()
    pp2.text = "Register Number: URK23CS5048"
    pp2.font.name = FONT_PRIMARY
    pp2.font.size = Pt(12)
    pp2.font.bold = True
    pp2.font.color.rgb = FOREST_GREEN

    pp3 = tf_p.add_paragraph()
    pp3.text = "Degree: B.Tech Computer Science and Engineering (AI/AIML)"
    pp3.font.name = FONT_PRIMARY
    pp3.font.size = Pt(10.5)
    pp3.font.color.rgb = TEXT_DARK

    pp4 = tf_p.add_paragraph()
    pp4.text = "Project Type: Individual Project  |  Intended Outcome: Journal Publication"
    pp4.font.name = FONT_PRIMARY
    pp4.font.size = Pt(10)
    pp4.font.italic = True
    pp4.font.color.rgb = TEXT_MUTED

    # Right Card: Supervised By
    s_card = add_card(slide, 6.83, 3.80, 5.95, 1.95, CARD_WHITE, BORDER_LIGHT)
    tf_s = s_card.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = Inches(0.25)
    tf_s.margin_top = Inches(0.15)

    sp0 = tf_s.paragraphs[0]
    sp0.text = "SUPERVISED BY"
    sp0.font.name = FONT_PRIMARY
    sp0.font.size = Pt(10)
    sp0.font.bold = True
    sp0.font.color.rgb = ACCENT_GREEN

    sp1 = tf_s.add_paragraph()
    sp1.text = "Mr. K. Martin Victor"
    sp1.font.name = FONT_HEADING
    sp1.font.size = Pt(17)
    sp1.font.bold = True
    sp1.font.color.rgb = DEEP_GREEN

    sp2 = tf_s.add_paragraph()
    sp2.text = "Assistant Professor"
    sp2.font.name = FONT_PRIMARY
    sp2.font.size = Pt(12)
    sp2.font.bold = True
    sp2.font.color.rgb = FOREST_GREEN

    sp3 = tf_s.add_paragraph()
    sp3.text = "Division of Artificial Intelligence and Machine Learning"
    sp3.font.name = FONT_PRIMARY
    sp3.font.size = Pt(10.5)
    sp3.font.color.rgb = TEXT_DARK

    sp4 = tf_s.add_paragraph()
    sp4.text = "Karunya Institute of Technology and Sciences (Deemed to be University)"
    sp4.font.name = FONT_PRIMARY
    sp4.font.size = Pt(10)
    sp4.font.color.rgb = TEXT_MUTED

    # Bottom Banner: Official Karunya Logo Banner (fit cleanly without distortion)
    if os.path.exists(LOGO_BANNER):
        add_picture_fit(slide, LOGO_BANNER, 2.65, 5.90, 8.0, 1.35)

# ------------------------------------------
# SLIDE 2: Agenda
# ------------------------------------------
def build_slide_2(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "AGENDA", "PRESENTATION ROADMAP & REVIEW STRUCTURE")
    add_footer(slide, 2)

    agenda_items = [
        ("01", "Abstract", "Executive overview, core value proposition & 4 predictive engines"),
        ("02", "Problem Definition & Scope", "Paddy farming challenges, siloed advisory & project objectives"),
        ("03", "Literature Survey", "Empirical study of XAI, EfficientNet, LightGBM & multimodal ML"),
        ("04", "Proposed System", "AgriTwinX modular digital twin framework & algorithmic foundations"),
        ("05", "System Architecture", "End-to-end data flow, Flask backend, thread orchestrator & XAI"),
        ("06", "Implementation", "Module-wise implementation: Vision, Boosting, BiLSTM & XAI hooks"),
        ("07", "Results & Discussion", "Empirical test metrics, confusion matrix, Grad-CAM & SHAP plots"),
        ("08", "Research Gap & Contribution", "Benchmarking against prior literature & novel integration benefits"),
        ("09", "Conclusion & References", "Summary, future scope, IEEE citations & journal publication roadmap")
    ]

    col_w = 3.88
    row_h = 1.65
    start_x = 0.55
    start_y = 1.45
    gap_x = 0.29
    gap_y = 0.20

    for idx, (num, title, desc) in enumerate(agenda_items):
        r = idx // 3
        c = idx % 3
        x = start_x + c * (col_w + gap_x)
        y = start_y + r * (row_h + gap_y)

        card = add_card(slide, x, y, col_w, row_h, CARD_WHITE, BORDER_LIGHT)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.20)
        tf.margin_top = Inches(0.18)
        tf.margin_right = Inches(0.15)

        p0 = tf.paragraphs[0]
        p0.text = f"SECTION {num}"
        p0.font.name = FONT_PRIMARY
        p0.font.size = Pt(9)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_GREEN

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(13.5)
        p1.font.bold = True
        p1.font.color.rgb = DEEP_GREEN
        p1.space_after = Pt(3)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_PRIMARY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED

# ------------------------------------------
# SLIDE 3: Abstract
# ------------------------------------------
def build_slide_3(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "ABSTRACT", "PROJECT OVERVIEW & SYSTEM IDENTITY")
    add_footer(slide, 3)

    # Left Column: Strategic Abstract Summary Card
    left_card = add_card(slide, 0.55, 1.35, 5.20, 4.55, CARD_WHITE, BORDER_GREEN)
    tf_l = left_card.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.25)
    tf_l.margin_top = Inches(0.20)
    tf_l.margin_right = Inches(0.25)

    p0 = tf_l.paragraphs[0]
    p0.text = "Executive Summary"
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = DEEP_GREEN
    p0.space_after = Pt(8)

    add_formatted_bullet(tf_l, "Platform Identity:", "AgriTwinX is an explainable, software-based Cyber-Physical Digital Twin and decision-support platform designed specifically for precision rice (Oryza sativa) farming.", 10, 6)
    add_formatted_bullet(tf_l, "Core Motivation:", "Resolves conventional agricultural fragmentation by uniting disease diagnostics, nutrient management, irrigation scheduling, and yield forecasting into a single cohesive pipeline.", 10, 6)
    add_formatted_bullet(tf_l, "Hardware-Free Philosophy:", "Functions without requiring expensive on-field IoT sensors or specialized robotic actuators, relying on web standards and regional fallbacks to empower resource-constrained smallholders.", 10, 6)
    add_formatted_bullet(tf_l, "Dual-Domain Explainability:", "Embeds Grad-CAM visual heatmaps for leaf pathology and SHAP feature attributions for tabular predictions, building crucial agronomist and farmer trust.", 10, 6)

    # Right Column: The 4 Core Predictive Engines (Cards)
    engines = [
        ("1. Paddy Disease Detection", "Multimodal EfficientNet-B3", "Fuses 224x224 RGB foliar images with variety embeddings and crop age to classify 10 distinct paddy diseases with high macro precision.", "Grad-CAM Saliency Heatmaps"),
        ("2. NPK & Irrigation Advisory", "XGBoost Regressors", "Predicts site-specific soil Nitrogen, Phosphorus, Potassium deficits (kg/ha) and daily volumetric irrigation requirements (mm/day) with regional defaults.", "TreeSHAP Feature Attributions"),
        ("3. Seasonal Yield Prediction", "LightGBM Regressor", "Forecasts seasonal paddy harvest (metric tons/ha) and financial revenue projections using state, season, area, and climatic statistics.", "SHAP Summary & Dependence"),
        ("4. Weather-Based Risk Forecast", "Attention-based BiLSTM", "Processes 168-hour (7-day) sequential meteorological sliding windows (temperature, humidity, rain) to predict next-24-hour disease outbreak risk.", "Temporal Additive Attention")
    ]

    card_h = 1.05
    gap = 0.12
    for idx, (ename, ealgo, edesc, exai) in enumerate(engines):
        y = 1.35 + idx * (card_h + gap)
        ecard = add_card(slide, 5.95, y, 6.83, card_h, CARD_WHITE, BORDER_LIGHT)
        tf_e = ecard.text_frame
        tf_e.word_wrap = True
        tf_e.margin_left = Inches(0.20)
        tf_e.margin_top = Inches(0.10)
        tf_e.margin_right = Inches(0.15)

        pe0 = tf_e.paragraphs[0]
        r_name = pe0.add_run()
        r_name.text = ename + "  "
        r_name.font.name = FONT_HEADING
        r_name.font.size = Pt(11.5)
        r_name.font.bold = True
        r_name.font.color.rgb = DEEP_GREEN

        r_badge = pe0.add_run()
        r_badge.text = f"[{ealgo}]"
        r_badge.font.name = FONT_PRIMARY
        r_badge.font.size = Pt(9.5)
        r_badge.font.bold = True
        r_badge.font.color.rgb = ACCENT_GREEN

        pe1 = tf_e.add_paragraph()
        pe1.text = edesc
        pe1.font.name = FONT_PRIMARY
        pe1.font.size = Pt(9)
        pe1.font.color.rgb = TEXT_DARK
        pe1.space_after = Pt(2)

        pe2 = tf_e.add_paragraph()
        r_xai_lbl = pe2.add_run()
        r_xai_lbl.text = "Explainability Method: "
        r_xai_lbl.font.size = Pt(8.5)
        r_xai_lbl.font.bold = True
        r_xai_lbl.font.color.rgb = AMBER_ACCENT
        r_xai_val = pe2.add_run()
        r_xai_val.text = exai
        r_xai_val.font.size = Pt(8.5)
        r_xai_val.font.color.rgb = TEXT_MUTED

    # Bottom Alert Banner across width
    b_banner = add_card(slide, 0.55, 6.05, 12.233, 0.72, SAGE_BG, BORDER_GREEN)
    tf_bb = b_banner.text_frame
    tf_bb.word_wrap = True
    tf_bb.margin_left = Inches(0.25)
    tf_bb.margin_top = Inches(0.10)
    pbb = tf_bb.paragraphs[0]
    pbb.text = "CORE VALUE PROPOSITION: AgriTwinX delivers end-to-end precision agronomy as a pure software digital twin, empowering smallholders with transparent, verifiable AI recommendations while maintaining complete hardware accessibility."
    pbb.font.name = FONT_PRIMARY
    pbb.font.size = Pt(10)
    pbb.font.bold = True
    pbb.font.color.rgb = DEEP_GREEN

# ------------------------------------------
# SLIDE 4: Problem Definition, Scope & Objectives
# ------------------------------------------
def build_slide_4(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "PROBLEM DEFINITION, SCOPE AND OBJECTIVES", "CHALLENGES IN CONVENTIONAL PADDY FARMING & SYSTEM GOALS")
    add_footer(slide, 4)

    # Left Card: Conventional Farming Challenges
    left_card = add_card(slide, 0.55, 1.35, 5.95, 5.40, CARD_WHITE, BORDER_LIGHT)
    tf_l = left_card.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.25)
    tf_l.margin_top = Inches(0.18)
    tf_l.margin_right = Inches(0.20)

    p0 = tf_l.paragraphs[0]
    p0.text = "Problem Definition & Conventional Challenges"
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(13.5)
    p0.font.bold = True
    p0.font.color.rgb = DEEP_GREEN
    p0.space_after = Pt(8)

    add_formatted_bullet(tf_l, "Subjective & Delayed Diagnosis:", "Smallholders rely on manual foliar inspection. Visual symptoms are easily misidentified or detected too late, leading to catastrophic yield losses (up to 40% from rice blast).", 9.5, 6)
    add_formatted_bullet(tf_l, "Fragmented Decision Silos:", "Existing advisory services isolate disease management, soil fertility, irrigation scheduling, and yield forecasting into separate disconnected tools with no holistic context.", 9.5, 6)
    add_formatted_bullet(tf_l, "Imbalanced Chemical Application:", "Unscientific fertilizer application (chronic excess Nitrogen and deficit Potash) causes severe soil degradation, chemical runoff, and elevated pest vulnerability.", 9.5, 6)
    add_formatted_bullet(tf_l, "The 'Black-Box' Adoption Barrier:", "Prior deep learning solutions output opaque classifications without visual localization or feature attribution, hindering agronomist and farmer trust.", 9.5, 6)
    add_formatted_bullet(tf_l, "Prohibitive IoT Hardware Costs:", "Most digital twin proposals demand complex in-situ sensor networks and robotic equipment, making them inaccessible to low-income smallholder farms.", 9.5, 6)

    # Right Card: Project Scope & Core Engineering Objectives
    right_card = add_card(slide, 6.83, 1.35, 5.95, 5.40, CARD_WHITE, BORDER_GREEN)
    tf_r = right_card.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = Inches(0.25)
    tf_r.margin_top = Inches(0.18)
    tf_r.margin_right = Inches(0.20)

    pr0 = tf_r.paragraphs[0]
    pr0.text = "Project Scope & Engineering Objectives"
    pr0.font.name = FONT_HEADING
    pr0.font.size = Pt(13.5)
    pr0.font.bold = True
    pr0.font.color.rgb = DEEP_GREEN
    pr0.space_after = Pt(8)

    add_formatted_bullet(tf_r, "Project Scope:", "A modular, browser-accessible Flask application providing software-driven precision agriculture for smallholders without requiring on-field physical hardware.", 9.5, 6)
    add_formatted_bullet(tf_r, "Objective 1 – Multimodal Pathology:", "Engineer an EfficientNet-B3 network fusing foliar imagery with cultivar embeddings and plant age to classify 10 rice diseases with >=95% accuracy.", 9.5, 6)
    add_formatted_bullet(tf_r, "Objective 2 – Soil & Water Optimization:", "Construct XGBoost regressors to quantify soil N-P-K macronutrient deficits and compute daily volumetric irrigation depth in mm/day.", 9.5, 6)
    add_formatted_bullet(tf_r, "Objective 3 – Yield & Revenue Forecasting:", "Develop a gradient-boosted LightGBM regressor predicting seasonal yield (t/ha) and financial revenue benchmarked against Minimum Support Prices (MSP).", 9.5, 6)
    add_formatted_bullet(tf_r, "Objective 4 – Weather Disease Proliferation:", "Build a sequence-aware BiLSTM with multi-head attention to model 168-hour temporal weather dynamics for 24-hour outbreak risk prediction.", 9.5, 6)
    add_formatted_bullet(tf_r, "Objective 5 – Verifiable XAI Integration:", "Provide dual-domain interpretability using Grad-CAM heatmaps for vision and TreeSHAP feature attributions for tabular models.", 9.5, 6)

# ------------------------------------------
# SLIDE 5: Literature Survey
# ------------------------------------------
def build_slide_5(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "LITERATURE SURVEY", "PEER-REVIEWED FOUNDATIONS ACROSS RESEARCH DOMAINS")
    add_footer(slide, 5)

    studies = [
        ("Deep Learning & EfficientNet for Rice Disease Detection",
         "Tan & Le (ICML 2019) & Tiwari & Dev (2026)",
         [
             ("EfficientNet Compound Scaling:", "Rethinks CNN scaling by balancing depth, width, and resolution with 12.2M parameters, achieving 81.6% Top-1 ImageNet accuracy with lower FLOPs than ResNet-50."),
             ("Lightweight Hybrid CNNs:", "Tiwari & Dev (2026) demonstrate that lightweight convolutional backbones with neural architecture search provide real-time diagnostic performance for open-field crops."),
             ("Limitation in Literature:", "Most studies rely solely on raw leaf images, neglecting agronomical context such as rice cultivar resistance or crop growth stage.")
         ]),
        ("Multimodal Fusion in Plant Pathology",
         "Vijayan & Chowdhary (Sci. Rep. 2026) & Deepa (Sci. Rep. 2026)",
         [
             ("RiceMultiModalNet:", "Vijayan & Chowdhary (2026) proved that biologically constrained multimodal deep learning fusing leaf imagery with phenological stage improves diagnostic robustness."),
             ("Bilinear Metadata Pooling:", "Deepa (2026) demonstrated that combining foliar visual symptoms with tabular agro-metadata outperforms unimodal CNN classification by mitigating false positives."),
             ("AgriTwinX Alignment:", "Directly inspires AgriTwinX's feature concatenation bottleneck (1536 image features + 16-dim variety embedding + 1-dim crop age).")
         ]),
        ("Explainable AI (XAI) in Precision Agriculture",
         "Michael (J. Agric. Inform. 2026) & Abou Samra & Ali (AgriEngineering 2026)",
         [
             ("The Interpretability Imperative:", "Michael (2026) underscores that XAI is essential for bridging the trust gap between complex AI models and smallholder farmers."),
             ("Dual-Domain XAI Synthesis:", "Abou Samra & Ali (2026) review interpretable remote sensing and highlight Grad-CAM (Selvaraju et al., 2017) and SHAP (Lundberg & Lee, 2017) as complementary standard methods."),
             ("Agronomic Utility:", "Grad-CAM validates whether CNNs focus on true fungal lesions rather than background soil noise; SHAP quantifies exact soil chemical drivers.")
         ]),
        ("Gradient Boosting & Temporal Microclimate Modeling",
         "Olatinwo et al. (Agriculture 2026) & Jahan et al. (Smart Agric. Tech. 2026)",
         [
             ("Interpretable Yield Forecasting:", "Olatinwo et al. (2026) demonstrate that tree ensemble regressors coupled with SHAP explainability deliver high predictive fidelity across heterogeneous rainfed conditions."),
             ("Spatiotemporal Microclimate Dynamics:", "Jahan & Nassiri-Mahallati (2026) show that temporal sequence models effectively capture weather-driven ecophysiological triggers."),
             ("Key Research Gap Identified:", "Existing literature overwhelmingly investigates these predictive tasks as isolated experiments rather than a unified operational digital twin platform.")
         ])
    ]

    col_w = 5.95
    row_h = 2.60
    start_x = 0.55
    start_y = 1.35
    gap_x = 0.33
    gap_y = 0.20

    for idx, (title, citation, points) in enumerate(studies):
        r = idx // 2
        c = idx % 2
        x = start_x + c * (col_w + gap_x)
        y = start_y + r * (row_h + gap_y)

        card = add_card(slide, x, y, col_w, row_h, CARD_WHITE, BORDER_LIGHT)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.20)
        tf.margin_top = Inches(0.12)
        tf.margin_right = Inches(0.18)

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = DEEP_GREEN

        p_cite = tf.add_paragraph()
        p_cite.text = f"Key Sources: {citation}"
        p_cite.font.name = FONT_PRIMARY
        p_cite.font.size = Pt(8.5)
        p_cite.font.bold = True
        p_cite.font.color.rgb = ACCENT_GREEN
        p_cite.space_after = Pt(4)

        for b_prefix, b_body in points:
            add_formatted_bullet(tf, b_prefix, b_body, 8.5, 3)

# ------------------------------------------
# SLIDE 6: Proposed System
# ------------------------------------------
def build_slide_6(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "PROPOSED SYSTEM: AgriTwinX", "OVERALL ARCHITECTURAL SOLUTION & PREDICTIVE MODULES")
    add_footer(slide, 6)

    # Top Overview Text Card
    top_card = add_card(slide, 0.55, 1.35, 12.233, 0.85, SAGE_BG, BORDER_GREEN)
    tf_top = top_card.text_frame
    tf_top.word_wrap = True
    tf_top.margin_left = Inches(0.25)
    tf_top.margin_top = Inches(0.10)
    p_top = tf_top.paragraphs[0]
    p_top.text = "AgriTwinX introduces a modular, software-based digital twin that mirrors real-world paddy field conditions in software. By coupling multimodal deep learning, gradient boosted regressors, and sequence-aware recurrent networks under a unified Flask inference pipeline, the system provides real-time, explainable precision farming recommendations."
    p_top.font.name = FONT_PRIMARY
    p_top.font.size = Pt(10)
    p_top.font.color.rgb = DEEP_GREEN

    modules = [
        ("MODULE 1", "Paddy Disease Detection", "Multimodal EfficientNet-B3",
         "224x224 RGB Leaf Image + Rice Variety Embedding (d=16) + Crop Age (Days)",
         "10 Foliar Disease Classes + Softmax Confidence Distribution",
         "PyTorch 2.2.1, Timm tf_efficientnet_b3",
         "Grad-CAM Visual Saliency Heatmaps on final conv head"),
        
        ("MODULE 2", "NPK & Irrigation Advisory", "XGBoost Regressors",
         "Soil N, P, K (kg/ha), Soil pH, Soil Moisture %, Growth Stage (with regional defaults)",
         "Site-Specific N-P-K Deficits (kg/ha) & Daily Irrigation Requirement (mm/day)",
         "XGBoost 2.0.3, Scikit-Learn 1.4.1",
         "TreeSHAP Feature Attributions quantifying chemical deficit drivers"),
        
        ("MODULE 3", "Seasonal Yield Prediction", "LightGBM Regressor",
         "State, Season, Cultivated Area (Acres), Historical Rainfall (mm), Temperature",
         "Projected Harvest Yield (metric tons/ha) & Net Revenue (MSP ₹21,830/t)",
         "LightGBM 4.3.0, Scikit-Learn",
         "SHAP Summary Plots & Partial Dependence Curves for climate variables"),
        
        ("MODULE 4", "Weather Disease Risk", "Attention-based BiLSTM",
         "168-Hour (7-Day) Temporal Sequence: Temp, Relative Humidity, Rainfall, Wind Speed",
         "Next-24-Hour Disease Proliferation Risk Probability (Low / Moderate / High)",
         "PyTorch 2.2.1 BiLSTM (2 layers, hidden=64)",
         "Multi-Head Additive Temporal Attention highlighting high-risk weather windows")
    ]

    col_w = 2.85
    gap_w = 0.27
    start_x = 0.55
    y_pos = 2.35
    card_h = 4.45

    for idx, (mod_id, mod_name, algo, inputs, outputs, tech, xai) in enumerate(modules):
        x = start_x + idx * (col_w + gap_w)
        mcard = add_card(slide, x, y_pos, col_w, card_h, CARD_WHITE, BORDER_LIGHT)
        tf_m = mcard.text_frame
        tf_m.word_wrap = True
        tf_m.margin_left = Inches(0.15)
        tf_m.margin_top = Inches(0.15)
        tf_m.margin_right = Inches(0.12)

        p_id = tf_m.paragraphs[0]
        p_id.text = mod_id
        p_id.font.name = FONT_PRIMARY
        p_id.font.size = Pt(8.5)
        p_id.font.bold = True
        p_id.font.color.rgb = ACCENT_GREEN

        p_name = tf_m.add_paragraph()
        p_name.text = mod_name
        p_name.font.name = FONT_HEADING
        p_name.font.size = Pt(11.5)
        p_name.font.bold = True
        p_name.font.color.rgb = DEEP_GREEN
        p_name.space_after = Pt(2)

        p_algo = tf_m.add_paragraph()
        p_algo.text = algo
        p_algo.font.name = FONT_PRIMARY
        p_algo.font.size = Pt(9.5)
        p_algo.font.bold = True
        p_algo.font.color.rgb = FOREST_GREEN
        p_algo.space_after = Pt(6)

        add_formatted_bullet(tf_m, "Inputs:", inputs, 8.5, 4, False)
        add_formatted_bullet(tf_m, "Outputs:", outputs, 8.5, 4, False)
        add_formatted_bullet(tf_m, "Engine:", tech, 8.5, 4, False)
        add_formatted_bullet(tf_m, "XAI Layer:", xai, 8.5, 2, False)

# ------------------------------------------
# SLIDE 7: System Architecture (Diagram)
# ------------------------------------------
def build_slide_7(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "SYSTEM ARCHITECTURE", "MODULAR PREDICTIVE INFERENCE PIPELINE & DATA FLOW")
    add_footer(slide, 7)

    # Layer 1: User Inputs Tier
    input_box = add_card(slide, 1.20, 1.35, 10.933, 0.68, SAGE_BG, BORDER_GREEN)
    tf_in = input_box.text_frame
    tf_in.word_wrap = True
    tf_in.margin_top = Inches(0.08)
    pin0 = tf_in.paragraphs[0]
    pin0.alignment = PP_ALIGN.CENTER
    pin0.text = "USER INPUT LAYER (Web / Mobile Browser Interface)"
    pin0.font.name = FONT_HEADING
    pin0.font.size = Pt(10.5)
    pin0.font.bold = True
    pin0.font.color.rgb = DEEP_GREEN

    pin1 = tf_in.add_paragraph()
    pin1.alignment = PP_ALIGN.CENTER
    pin1.text = "Foliar Leaf Photograph (JPEG/PNG)  |  Cultivar Variety (IR-64, ADT45, etc.)  |  Crop Age (Days)  |  Soil N-P-K & pH  |  Location & Season"
    pin1.font.name = FONT_PRIMARY
    pin1.font.size = Pt(9)
    pin1.font.color.rgb = TEXT_DARK

    # Arrow 1 down
    arr1 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(6.45), Inches(2.08), Inches(0.40), Inches(0.18))
    arr1.fill.solid()
    arr1.fill.fore_color.rgb = FOREST_GREEN
    arr1.line.color.rgb = FOREST_GREEN

    # Layer 2: Flask Backend
    flask_box = add_card(slide, 1.20, 2.30, 10.933, 0.72, CARD_WHITE, BORDER_GREEN)
    tf_fl = flask_box.text_frame
    tf_fl.word_wrap = True
    tf_fl.margin_top = Inches(0.08)
    pfl0 = tf_fl.paragraphs[0]
    pfl0.alignment = PP_ALIGN.CENTER
    pfl0.text = "FLASK-BASED APPLICATION & SERVICE BACKEND (Python 3.11 WSGI)"
    pfl0.font.name = FONT_HEADING
    pfl0.font.size = Pt(10.5)
    pfl0.font.bold = True
    pfl0.font.color.rgb = DEEP_GREEN

    pfl1 = tf_fl.add_paragraph()
    pfl1.alignment = PP_ALIGN.CENTER
    pfl1.text = "Input Validation (MIME & Size checks)  •  Regional Soil Defaults Engine (Fallback)  •  Concurrent ThreadPoolExecutor Orchestrator"
    pfl1.font.name = FONT_PRIMARY
    pfl1.font.size = Pt(9)
    pfl1.font.color.rgb = TEXT_DARK

    # Arrow 2 down
    arr2 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(6.45), Inches(3.08), Inches(0.40), Inches(0.18))
    arr2.fill.solid()
    arr2.fill.fore_color.rgb = FOREST_GREEN
    arr2.line.color.rgb = FOREST_GREEN

    # Layer 3: Centralized Inference Pipeline Container (4 Predictive Modules)
    inf_container = add_card(slide, 0.80, 3.30, 11.733, 1.48, CARD_WHITE, BORDER_GREEN)
    tf_ic = inf_container.text_frame
    tf_ic.word_wrap = True
    tf_ic.margin_top = Inches(0.05)
    pic0 = tf_ic.paragraphs[0]
    pic0.alignment = PP_ALIGN.CENTER
    pic0.text = "MODULAR PREDICTIVE INFERENCE PIPELINE (Pre-loaded RAM ModelRegistry)"
    pic0.font.name = FONT_HEADING
    pic0.font.size = Pt(10)
    pic0.font.bold = True
    pic0.font.color.rgb = FOREST_GREEN

    mod_boxes = [
        ("Disease Detection", "Multimodal EfficientNet-B3", "Image + Variety + Age -> 10 Classes"),
        ("NPK & Irrigation", "XGBoost Regressor", "Soil NPK/pH -> Deficits & mm/day"),
        ("Yield Prediction", "LightGBM Regressor", "Agro-Climate -> t/ha & Revenue"),
        ("Weather Risk", "Attention-BiLSTM", "168-hr Weather -> 24-hr Risk Index")
    ]
    sub_w = 2.65
    sub_gap = 0.22
    for idx, (m_title, m_algo, m_desc) in enumerate(mod_boxes):
        sx = 1.05 + idx * (sub_w + sub_gap)
        scard = add_card(slide, sx, 3.65, sub_w, 0.98, SAGE_BG, BORDER_GREEN)
        tf_s = scard.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = Inches(0.10)
        tf_s.margin_top = Inches(0.08)
        ps0 = tf_s.paragraphs[0]
        ps0.alignment = PP_ALIGN.CENTER
        ps0.text = m_title
        ps0.font.name = FONT_HEADING
        ps0.font.size = Pt(9.5)
        ps0.font.bold = True
        ps0.font.color.rgb = DEEP_GREEN

        ps1 = tf_s.add_paragraph()
        ps1.alignment = PP_ALIGN.CENTER
        ps1.text = m_algo
        ps1.font.name = FONT_PRIMARY
        ps1.font.size = Pt(8.5)
        ps1.font.bold = True
        ps1.font.color.rgb = ACCENT_GREEN

        ps2 = tf_s.add_paragraph()
        ps2.alignment = PP_ALIGN.CENTER
        ps2.text = m_desc
        ps2.font.name = FONT_PRIMARY
        ps2.font.size = Pt(8)
        ps2.font.color.rgb = TEXT_DARK

    # Arrow 3 down
    arr3 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(6.45), Inches(4.84), Inches(0.40), Inches(0.18))
    arr3.fill.solid()
    arr3.fill.fore_color.rgb = FOREST_GREEN
    arr3.line.color.rgb = FOREST_GREEN

    # Layer 4: Explainability Layer (XAI Core) - 2 Side-by-Side Cards
    xai_container = add_card(slide, 1.20, 5.06, 10.933, 0.88, CARD_WHITE, BORDER_GREEN)
    tf_xc = xai_container.text_frame
    tf_xc.word_wrap = True
    tf_xc.margin_top = Inches(0.04)
    pxc0 = tf_xc.paragraphs[0]
    pxc0.alignment = PP_ALIGN.CENTER
    pxc0.text = "EXPLAINABILITY LAYER (Dual-Domain XAI Core)"
    pxc0.font.name = FONT_HEADING
    pxc0.font.size = Pt(10)
    pxc0.font.bold = True
    pxc0.font.color.rgb = DEEP_GREEN

    # Sub-card 1: Grad-CAM
    xc1 = add_card(slide, 1.35, 5.38, 5.15, 0.48, SAGE_BG, BORDER_GREEN)
    tf_xc1 = xc1.text_frame
    tf_xc1.word_wrap = True
    tf_xc1.margin_top = Inches(0.04)
    px1_0 = tf_xc1.paragraphs[0]
    px1_0.alignment = PP_ALIGN.CENTER
    px1_0.text = "Grad-CAM Saliency Engine: PyTorch conv_head backward hooks -> 2D lesion heatmaps"
    px1_0.font.name = FONT_PRIMARY
    px1_0.font.size = Pt(8)
    px1_0.font.bold = True
    px1_0.font.color.rgb = DEEP_GREEN

    # Sub-card 2: TreeSHAP
    xc2 = add_card(slide, 6.75, 5.38, 5.15, 0.48, SAGE_BG, BORDER_GREEN)
    tf_xc2 = xc2.text_frame
    tf_xc2.word_wrap = True
    tf_xc2.margin_top = Inches(0.04)
    px2_0 = tf_xc2.paragraphs[0]
    px2_0.alignment = PP_ALIGN.CENTER
    px2_0.text = "TreeSHAP Engine: Exact Shapley feature attributions for soil deficit & yield drivers"
    px2_0.font.name = FONT_PRIMARY
    px2_0.font.size = Pt(8)
    px2_0.font.bold = True
    px2_0.font.color.rgb = DEEP_GREEN

    # Arrow 4 down
    arr4 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(6.45), Inches(5.98), Inches(0.40), Inches(0.16))
    arr4.fill.solid()
    arr4.fill.fore_color.rgb = FOREST_GREEN
    arr4.line.color.rgb = FOREST_GREEN

    # Layer 5: Output & Persistence Layer
    out_box = add_card(slide, 1.20, 6.18, 10.933, 0.65, SAGE_BG, BORDER_GREEN)
    tf_o = out_box.text_frame
    tf_o.word_wrap = True
    tf_o.margin_top = Inches(0.06)
    po0 = tf_o.paragraphs[0]
    po0.alignment = PP_ALIGN.CENTER
    po0.text = "PREDICTION RESULTS & DECISION SUPPORT (UI & Persistence)"
    po0.font.name = FONT_HEADING
    po0.font.size = Pt(10.5)
    po0.font.bold = True
    po0.font.color.rgb = DEEP_GREEN

    po1 = tf_o.add_paragraph()
    po1.alignment = PP_ALIGN.CENTER
    po1.text = "Interactive Diagnostic Cards  •  Visual Grad-CAM Heatmap Overlays  •  Agronomic Treatment Advisory  •  SQLAlchemy Relational Database Audit"
    po1.font.name = FONT_PRIMARY
    po1.font.size = Pt(8.5)
    po1.font.color.rgb = TEXT_DARK

# ------------------------------------------
# SLIDE 8: Implementation
# ------------------------------------------
def build_slide_8(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "SYSTEM IMPLEMENTATION", "MODULE-WISE ENGINEERING ARCHITECTURE & PIPELINE DETAILS")
    add_footer(slide, 8)

    quadrants = [
        ("1. Multimodal Pathology Classification", "MultiModal EfficientNet-B3 (PyTorch 2.2.1)",
         [
             ("Visual Pipeline:", "Input images resized to 224x224 RGB, normalized to ImageNet distribution; augmented with Albumentations (random flip, rotation, affine)."),
             ("Multimodal Fusion:", "Backbone outputs 1536-dim feature vector; rice variety mapped via nn.Embedding(num_classes, 16); crop age standardized. Fused into 1553-dim dense layer."),
             ("Classification Target:", "10 classes: Bacterial Leaf Blight, Brown Spot, Leaf Blast, Neck Blast, Sheath Blight, Tungro, Hispa, Leaf Scald, Narrow Brown Spot, Healthy."),
             ("Grad-CAM Engine:", "Custom backward hook registered on final conv layer (conv_head); gradients pooled across channels and multiplied by forward activation maps.")
         ]),
        ("2. NPK & Irrigation Optimization", "XGBoost Regressors & Regional Fallbacks",
         [
             ("Soil Telemetry:", "Evaluates soil Nitrogen (N), Phosphorus (P), Potassium (K) in kg/ha, pH, and soil moisture % against empirical paddy growth stage demand curves."),
             ("Regional Fallback Engine:", "If laboratory soil tests are unavailable, get_soil_defaults() queries state agro-climatic databases (e.g. Kerala: N=82, P=42, K=36, pH=6.6)."),
             ("Irrigation Depth:", "Calculates daily volumetric irrigation depth in mm/day required to maintain optimal standing water levels for the detected growth stage."),
             ("TreeSHAP Integration:", "Generates exact Shapley values quantifying whether low potash or extreme pH drove the nutrient advisory.")
         ]),
        ("3. Seasonal Paddy Yield Prediction", "LightGBM Regressor & Revenue Projections",
         [
             ("Macro-Agronomic Modeling:", "Trained on historical Indian agricultural production statistics (1997–2020) spanning diverse rainfall and agro-climatic zones."),
             ("Hyperparameters:", "Configured with 500 boosting iterations, learning rate 0.05, num_leaves 31; evaluates state, season, area, rainfall, and temperature."),
             ("Economic Translation:", "Per-hectare yield forecast is scaled by farm acreage and converted into gross financial revenue using government Minimum Support Price (MSP ₹21,830/ton)."),
             ("SHAP Interpretability:", "Computes global summary and dependence plots identifying rainfall and cultivated area as dominant non-linear yield drivers.")
         ]),
        ("4. Weather-Based Risk & Backend Pipeline", "Attention-BiLSTM & Flask Web Framework",
         [
             ("Sequence Modeling:", "BiLSTM with 2 layers (hidden size 64, dropout 0.20) evaluating 168-hour (7-day) sequential sliding windows of hourly temperature, humidity, and rainfall."),
             ("Multi-Head Attention:", "Computes temporal attention scores highlighting specific microclimate intervals with prolonged relative humidity (>85%) and warm temperatures."),
             ("Risk Classification:", "Outputs next-24-hour disease proliferation risk tier (Low, Moderate, High) to preemptively schedule protective bio-fungicide sprays."),
             ("Flask Backend Pipeline:", "Modular blueprints (farmer, auth, admin), ThreadPoolExecutor dispatching parallel model inference (mean latency <3.5s), SQLAlchemy ORM.")
         ])
    ]

    col_w = 5.95
    row_h = 2.60
    start_x = 0.55
    start_y = 1.35
    gap_x = 0.33
    gap_y = 0.20

    for idx, (title, sub, bullets) in enumerate(quadrants):
        r = idx // 2
        c = idx % 2
        x = start_x + c * (col_w + gap_x)
        y = start_y + r * (row_h + gap_y)

        card = add_card(slide, x, y, col_w, row_h, CARD_WHITE, BORDER_LIGHT)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.20)
        tf.margin_top = Inches(0.12)
        tf.margin_right = Inches(0.18)

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = DEEP_GREEN

        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.name = FONT_PRIMARY
        p_sub.font.size = Pt(8.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = ACCENT_GREEN
        p_sub.space_after = Pt(4)

        for b_pref, b_text in bullets:
            add_formatted_bullet(tf, b_pref, b_text, 8.5, 3)

# ------------------------------------------
# SLIDE 9: Technologies Used
# ------------------------------------------
def build_slide_9(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "TECHNOLOGIES USED", "TECHNICAL ECOSYSTEM & VERIFIED SOFTWARE DEPENDENCIES")
    add_footer(slide, 9)

    tech_stacks = [
        ("Programming & Backend", "Core Frameworks & Routing",
         [
             ("Python 3.11.8:", "Core 64-bit runtime providing typing enhancements and performance improvements."),
             ("Flask 3.0.3:", "WSGI microframework handling routing, modular blueprints, and request lifecycles."),
             ("Flask-Login 0.6.3:", "User session authentication, access control decorators, and session caching."),
             ("Flask-Bcrypt 1.0.1:", "Secure Scrypt/Bcrypt password hashing and credential verification."),
             ("Jinja2 3.1.6:", "Modular server-side HTML rendering inheriting from base templates.")
         ]),
        ("Machine Learning & Deep Learning", "Predictive Modeling & Computer Vision",
         [
             ("PyTorch 2.2.1:", "Deep learning framework for tensor computing and backpropagation graph execution."),
             ("Torchvision 0.17.1:", "Computer vision transforms, dataset pipelines, and tensor operations."),
             ("Timm 0.9.16:", "Pre-trained deep learning backbone repository (tf_efficientnet_b3)."),
             ("LightGBM 4.3.0:", "Fast, distributed gradient boosting for seasonal crop yield regression."),
             ("XGBoost 2.0.3:", "Extreme gradient boosting for soil nutrient deficits and irrigation depth."),
             ("Scikit-Learn 1.4.1:", "Regression metrics, preprocessing pipelines, and standard scalers.")
         ]),
        ("Explainable AI (XAI)", "Model Interpretability & Transparency",
         [
             ("Grad-CAM Engine:", "Custom PyTorch hook capturing final convolutional activations for spatial saliency maps."),
             ("SHAP 0.45.0:", "Shapley Additive exPlanations (TreeExplainer) calculating exact feature attribution."),
             ("OpenCV 4.11.0:", "Image processing, bilinear resizing, and Grad-CAM colormap jet blending."),
             ("Albumentations 1.4.3:", "Fast agricultural data augmentation pipeline for training stability.")
         ]),
        ("Database & Persistence", "Data Storage & Relational Modeling",
         [
             ("SQLAlchemy 2.0.29:", "Declarative Object-Relational Mapping (ORM) and transaction management."),
             ("Flask-SQLAlchemy 3.1.1:", "Flask integration layer managing database session contexts."),
             ("SQLite 3 (Development):", "Embedded zero-configuration local database verified in instance/agritwin.db."),
             ("PostgreSQL 15 (Target):", "Configured via config.py (psycopg2-binary 2.9.9) for scalable production deployment.")
         ]),
        ("Development Tools & APIs", "Runtime & External Services",
         [
             ("OpenWeatherMap REST API:", "OneCall 3.0 API fetching 168-hour historical and forecasted weather telemetry."),
             ("VS Code & Jupyter:", "Integrated development environment and experimental notebook workflows."),
             ("Git & GitHub:", "Version control, feature branching, and codebase repository auditing."),
             ("Hardware Architecture:", "x86-64 server, 16GB RAM, NVIDIA CUDA 12.1 GPU acceleration supported.")
         ])
    ]

    top_w = 3.88
    top_h = 2.60
    start_x = 0.55
    gap_x = 0.29

    for idx in range(3):
        x = start_x + idx * (top_w + gap_x)
        cat_title, cat_sub, items = tech_stacks[idx]
        card = add_card(slide, x, 1.35, top_w, top_h, CARD_WHITE, BORDER_LIGHT)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.18)
        tf.margin_top = Inches(0.12)
        tf.margin_right = Inches(0.15)

        p0 = tf.paragraphs[0]
        p0.text = cat_title
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = DEEP_GREEN

        p_sub = tf.add_paragraph()
        p_sub.text = cat_sub
        p_sub.font.name = FONT_PRIMARY
        p_sub.font.size = Pt(8.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = ACCENT_GREEN
        p_sub.space_after = Pt(4)

        for b_pref, b_text in items:
            add_formatted_bullet(tf, b_pref, b_text, 8, 2.5)

    bot_w = 5.95
    bot_h = 2.55
    gap_bx = 0.33
    for idx in range(3, 5):
        x = start_x + (idx - 3) * (bot_w + gap_bx)
        cat_title, cat_sub, items = tech_stacks[idx]
        card = add_card(slide, x, 4.15, bot_w, bot_h, CARD_WHITE, BORDER_LIGHT)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.20)
        tf.margin_top = Inches(0.12)
        tf.margin_right = Inches(0.18)

        p0 = tf.paragraphs[0]
        p0.text = cat_title
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = DEEP_GREEN

        p_sub = tf.add_paragraph()
        p_sub.text = cat_sub
        p_sub.font.name = FONT_PRIMARY
        p_sub.font.size = Pt(8.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = ACCENT_GREEN
        p_sub.space_after = Pt(4)

        for b_pref, b_text in items:
            add_formatted_bullet(tf, b_pref, b_text, 8.5, 3)

# ------------------------------------------
# SLIDE 10: Results and Discussion
# ------------------------------------------
def build_slide_10(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "RESULTS AND DISCUSSION", "EMPIRICAL PERFORMANCE METRICS & MODEL EVALUATION")
    add_footer(slide, 10)

    # Top: Performance Metrics Table
    t_left = Inches(0.55)
    t_top = Inches(1.35)
    t_w = Inches(12.233)
    t_h = Inches(1.75)

    rows = 5
    cols = 5
    table_shape = slide.shapes.add_table(rows, cols, t_left, t_top, t_w, t_h)
    tbl = table_shape.table

    tbl.columns[0].width = Inches(2.9)
    tbl.columns[1].width = Inches(2.3)
    tbl.columns[2].width = Inches(2.4)
    tbl.columns[3].width = Inches(2.3)
    tbl.columns[4].width = Inches(2.333)

    table_data = [
        ["Predictive Module", "Algorithm / Model", "Primary Metric", "Secondary Metric", "Test Benchmark Status"],
        ["Paddy Disease Classification", "MultiModal EfficientNet-B3", "Accuracy: 96.73%", "Macro F1: 0.9676 | Loss: 0.112", "1,007 / 1,041 Correct (Test)"],
        ["Weather-Based Disease Risk", "Attention-based BiLSTM", "Accuracy: 95.26%", "Macro F1: 0.9520 | ROC-AUC: 0.9958", "14,440 Sequences Evaluated"],
        ["Seasonal Crop Yield Forecasting", "LightGBM Regressor", "R² Score: 0.5579", "MAE: 0.2581 t/ha | RMSE: 0.5516", "500 Boosting Rounds"],
        ["Soil Macronutrient & Irrigation", "XGBoost / Gradient Boosted", "NPK RMSE: 9.3013 kg/ha", "NPK MAE: 6.9568 | Irrig RMSE: 35.97", "Agronomic demand converged"]
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, cell_value in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = cell_value
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_PRIMARY
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT
            if r_idx == 0:
                p.font.size = Pt(9.5)
                p.font.bold = True
                p.font.color.rgb = CARD_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = DEEP_GREEN
            else:
                p.font.size = Pt(8.5)
                p.font.color.rgb = TEXT_DARK
                cell.fill.solid()
                cell.fill.fore_color.rgb = SAGE_BG if r_idx % 2 == 1 else CARD_WHITE
                if c_idx == 2 or c_idx == 3:
                    p.font.bold = True
                    p.font.color.rgb = FOREST_GREEN

    # Bottom Half: Embed Actual Real Project Plots with Aspect-Ratio-Preserving Fit
    plot_assets = [
        ("Plots/1/14_confusion_matrix.png", "10-Class Disease Confusion Matrix", 
         "Held-out test accuracy: 96.73% across 1,041 validation samples", 0.55, 3.25, 2.80, 3.50),
        ("Plots/1/gradcam_sample_1.png", "Grad-CAM Saliency Heatmap Comparison", 
         "Original Leaf  •  Activation Map  •  Saliency Overlay", 3.50, 3.25, 3.30, 3.50),
        ("Plots/4/actual_vs_predicted.png", "LightGBM Actual vs Predicted Yield", 
         "R² = 0.5579 | RMSE = 0.5516 t/ha | MAE = 0.2581 t/ha", 6.95, 3.25, 2.85, 3.50),
        ("Plots/4/shap_summary.png", "SHAP Feature Importance for Yield", 
         "Top drivers: Rainfall, Cultivated Area, Mean Temperature", 9.95, 3.25, 2.833, 3.50)
    ]

    for p_path, p_title, p_caption, px, py, pw, ph in plot_assets:
        # Container card
        p_card = add_card(slide, px, py, pw, ph, CARD_WHITE, BORDER_LIGHT)
        tf_pc = p_card.text_frame
        tf_pc.word_wrap = True
        tf_pc.margin_top = Inches(0.06)
        ppc0 = tf_pc.paragraphs[0]
        ppc0.alignment = PP_ALIGN.CENTER
        ppc0.text = p_title
        ppc0.font.name = FONT_HEADING
        ppc0.font.size = Pt(8.5)
        ppc0.font.bold = True
        ppc0.font.color.rgb = DEEP_GREEN

        # Embed Image centered with aspect ratio preserved
        # Image area is py + 0.30 to py + ph - 0.40 (height = ph - 0.70)
        img_box_y = py + 0.28
        img_box_h = ph - 0.65
        add_picture_fit(slide, p_path, px + 0.08, img_box_y, pw - 0.16, img_box_h)

        # Bottom Caption Box
        cap_box = slide.shapes.add_textbox(Inches(px + 0.05), Inches(py + ph - 0.34), Inches(pw - 0.10), Inches(0.30))
        tf_cap = cap_box.text_frame
        tf_cap.word_wrap = True
        tf_cap.margin_left = tf_cap.margin_top = tf_cap.margin_right = tf_cap.margin_bottom = 0
        p_cap = tf_cap.paragraphs[0]
        p_cap.alignment = PP_ALIGN.CENTER
        p_cap.text = p_caption
        p_cap.font.name = FONT_PRIMARY
        p_cap.font.size = Pt(7.5)
        p_cap.font.bold = True
        p_cap.font.color.rgb = ACCENT_GREEN

# ------------------------------------------
# SLIDE 11: Research Gap and Contribution
# ------------------------------------------
def build_slide_11(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "RESEARCH GAP AND CONTRIBUTION", "COMPARATIVE ANALYSIS: CURRENT LITERATURE VS. AGRITWINX")
    add_footer(slide, 11)

    left_card = add_card(slide, 0.55, 1.35, 5.95, 5.40, CARD_WHITE, ALERT_BORDER)
    tf_l = left_card.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.25)
    tf_l.margin_top = Inches(0.18)
    tf_l.margin_right = Inches(0.20)

    p0 = tf_l.paragraphs[0]
    p0.text = "Research Gap in Existing Literature"
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(13.5)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(185, 28, 28)
    p0.space_after = Pt(8)

    add_formatted_bullet(tf_l, "Isolated Single-Task Focus:", "Existing agricultural studies predominantly investigate individual prediction tasks in isolation (e.g. only vision disease diagnosis, or only yield regression). Smallholders are forced to navigate multiple fragmented tools.", 9.5, 6)
    add_formatted_bullet(tf_l, "Unimodal Pathology Blindness:", "Conventional CNNs evaluate leaf images without agronomic context, ignoring cultivar disease resistance and crop age, which leads to high false positive rates in field conditions.", 9.5, 6)
    add_formatted_bullet(tf_l, "The 'Black-Box' Adoption Barrier:", "Deep neural networks and ensemble regressors typically output raw probabilities without interpretability. Without spatial lesion localization or feature rankings, farmers and agronomists hesitate to act.", 9.5, 6)
    add_formatted_bullet(tf_l, "Prohibitive Hardware Demands:", "Published agricultural digital twins frequently presuppose expensive on-field IoT sensors, robotic drones, or automated irrigation actuators, rendering them unaffordable for typical smallholders.", 9.5, 6)

    right_card = add_card(slide, 6.83, 1.35, 5.95, 5.40, CARD_WHITE, BORDER_GREEN)
    tf_r = right_card.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = Inches(0.25)
    tf_r.margin_top = Inches(0.18)
    tf_r.margin_right = Inches(0.20)

    pr0 = tf_r.paragraphs[0]
    pr0.text = "AgriTwinX's Engineered Contributions"
    pr0.font.name = FONT_HEADING
    pr0.font.size = Pt(13.5)
    pr0.font.bold = True
    pr0.font.color.rgb = DEEP_GREEN
    pr0.space_after = Pt(8)

    add_formatted_bullet(tf_r, "Unified 4-Engine Decision Support:", "Integrates foliar disease classification, soil nutrient deficit estimation, irrigation water depth, seasonal yield forecasting, and weather risk into one cohesive web platform.", 9.5, 6)
    add_formatted_bullet(tf_r, "Multimodal Contextual Fusion:", "Fuses EfficientNet-B3 visual feature maps with categorical variety embeddings and standardized crop age, boosting disease classification accuracy to 96.73% on held-out test data.", 9.5, 6)
    add_formatted_bullet(tf_r, "Dual-Domain Verifiable Explainability:", "Couples Grad-CAM visual heatmaps (validating infected foliar regions) with TreeSHAP feature attributions (explaining soil deficit and yield drivers) to foster agronomic trust.", 9.5, 6)
    add_formatted_bullet(tf_r, "Accessible Software-Only Digital Twin:", "Delivers real-time agronomic intelligence as a pure software platform with regional soil fallbacks, operating seamlessly on standard web browsers with zero physical hardware dependency.", 9.5, 6)

# ------------------------------------------
# SLIDE 12: Conclusion and Future Scope
# ------------------------------------------
def build_slide_12(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "CONCLUSION AND FUTURE SCOPE", "PROJECT SUMMARY, LESSONS LEARNED & RESEARCH ROADMAP")
    add_footer(slide, 12)

    left_card = add_card(slide, 0.55, 1.35, 5.95, 5.40, CARD_WHITE, BORDER_GREEN)
    tf_l = left_card.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.25)
    tf_l.margin_top = Inches(0.18)
    tf_l.margin_right = Inches(0.20)

    p0 = tf_l.paragraphs[0]
    p0.text = "Project Conclusion"
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(13.5)
    p0.font.bold = True
    p0.font.color.rgb = DEEP_GREEN
    p0.space_after = Pt(8)

    add_formatted_bullet(tf_l, "Integrated Precision Decision Support:", "Successfully designed, developed, and evaluated AgriTwinX as an explainable, multi-model digital twin platform tailored for rice cultivation.", 9.5, 6)
    add_formatted_bullet(tf_l, "High Empirical Predictive Performance:", "Achieved 96.73% disease classification accuracy (MultiModal EfficientNet-B3), 95.26% 24-hr weather risk accuracy (BiLSTM), and 0.258 t/ha yield MAE (LightGBM).", 9.5, 6)
    add_formatted_bullet(tf_l, "Transparent & Explainable AI:", "Integrated Grad-CAM visual heatmaps and TreeSHAP attributions directly into farmer-facing advisory cards, removing the 'black-box' opacity barrier.", 9.5, 6)
    add_formatted_bullet(tf_l, "Validated Full-Stack Prototype:", "Demonstrated concurrent inference orchestrator (mean response time <3.5s) on a Flask microframework with secure user sessions and persistent SQLite/PostgreSQL audit logs.", 9.5, 6)

    right_card = add_card(slide, 6.83, 1.35, 5.95, 5.40, CARD_WHITE, BORDER_LIGHT)
    tf_r = right_card.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = Inches(0.25)
    tf_r.margin_top = Inches(0.18)
    tf_r.margin_right = Inches(0.20)

    pr0 = tf_r.paragraphs[0]
    pr0.text = "Future Scope & Research Roadmap"
    pr0.font.name = FONT_HEADING
    pr0.font.size = Pt(13.5)
    pr0.font.bold = True
    pr0.font.color.rgb = DEEP_GREEN
    pr0.space_after = Pt(8)

    add_formatted_bullet(tf_r, "Broader Field-Level Validation:", "Deploy platform in multi-season agronomic field trials across diverse agro-climatic zones in southern and eastern India to benchmark performance under real farm variations.", 9.5, 6)
    add_formatted_bullet(tf_r, "Integration of Multi-Crop Datasets:", "Generalize the multimodal architecture beyond paddy to include staple cash crops such as wheat, maize, sugarcane, and millets.", 9.5, 6)
    add_formatted_bullet(tf_r, "Hyper-Local Real-Time Weather:", "Incorporate on-ground automated weather stations and satellite Synthetic Aperture Radar (SAR) telemetry for hyper-local microclimate risk resolution.", 9.5, 6)
    add_formatted_bullet(tf_r, "Agronomic Expert Clinical Evaluation:", "Partner with state agricultural universities (e.g. TNAU, KAU) and Krishi Vigyan Kendras (KVKs) to conduct formal blind trials with certified agronomists.", 9.5, 6)
    add_formatted_bullet(tf_r, "Potential IoT Sensor Expansion:", "Explore optional low-cost edge IoT telemetry (soil moisture, leaf wetness) as a future phase enhancement—maintained strictly as future work rather than an existing requirement.", 9.5, 6)

# ------------------------------------------
# SLIDE 13: References
# ------------------------------------------
def build_slide_13(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "REFERENCES", "GENUINE PEER-REVIEWED ACADEMIC CITATIONS (IEEE FORMAT)")
    add_footer(slide, 13)

    references = [
        ("[1]", "M. Tan and Q. V. Le, \"EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,\" in Proc. 36th Int. Conf. Mach. Learn. (ICML), PMLR 97, 2019, pp. 6105–6114."),
        ("[2]", "J. Michael, \"Explainable Artificial Intelligence (XAI) in Precision Agriculture: Current Trends, Challenges, and Future Perspectives,\" Journal of Agricultural Informatics, vol. 17, no. 2, pp. 45–62, 2026."),
        ("[3]", "R. M. Abou Samra and R. R. Ali, \"Explainable artificial intelligence in smart agriculture: A comprehensive review of interpretable remote sensing for sustainable decision-making,\" AgriEngineering, vol. 8, no. 7, pp. 270–295, 2026. https://doi.org/10.3390/agriengineering8070270"),
        ("[4]", "M. K. Tiwari and H. Dev, \"An Explainable AI-Driven Hybrid Deep Learning Model Integrating Lightweight CNN And Neural Architecture Search Network For Precision Agriculture Applications,\" Int. J. Adv. Signal Image Sci., vol. 12, no. 3, pp. 1115–1129, 2026."),
        ("[5]", "S. Vijayan and C. L. Chowdhary, \"RiceMultiModalNet: a proof-of-concept biologically constrained multi-modal deep learning for rice disease detection integrating phenological stage and environmental risk,\" Scientific Reports, vol. 16, Art. no. 4512, 2026."),
        ("[6]", "J. Deepa, \"Multi-modal deep learning for paddy health assessment: fusing leaf imagery with tabular metadata using a factorized bilinear pooling approach,\" Scientific Reports, vol. 16, Art. no. 5821, 2026."),
        ("[7]", "D. D. Olatinwo, H. C. Myburgh, A. De Freitas, and A. Abu-Mahfouz, \"Explainable Data-Driven Approach for Smart Crop Yield Prediction in Sub-Saharan Africa: Performance and Interpretability Analysis,\" Agriculture, vol. 16, no. 8, Art. no. 826, 2026."),
        ("[8]", "R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and D. Batra, \"Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization,\" in Proc. IEEE Int. Conf. Comput. Vis. (ICCV), 2017, pp. 618–626.")
    ]

    col_w = 5.95
    start_x = 0.55
    gap_x = 0.33
    y_pos = 1.35
    ref_h = 1.15
    gap_y = 0.12

    for idx, (num, citation) in enumerate(references):
        c = idx // 4
        r = idx % 4
        x = start_x + c * (col_w + gap_x)
        y = y_pos + r * (ref_h + gap_y)

        card = add_card(slide, x, y, col_w, ref_h, CARD_WHITE, BORDER_LIGHT)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.18)
        tf.margin_top = Inches(0.10)
        tf.margin_right = Inches(0.15)

        p = tf.paragraphs[0]
        r_num = p.add_run()
        r_num.text = num + " "
        r_num.font.name = FONT_PRIMARY
        r_num.font.size = Pt(9.5)
        r_num.font.bold = True
        r_num.font.color.rgb = ACCENT_GREEN

        r_text = p.add_run()
        r_text.text = citation
        r_text.font.name = FONT_PRIMARY
        r_text.font.size = Pt(8.5)
        r_text.font.color.rgb = TEXT_DARK

    b_card = add_card(slide, 0.55, 6.35, 12.233, 0.45, SAGE_BG, BORDER_GREEN)
    tf_bc = b_card.text_frame
    tf_bc.word_wrap = True
    tf_bc.margin_top = Inches(0.06)
    p_bc = tf_bc.paragraphs[0]
    p_bc.alignment = PP_ALIGN.CENTER
    p_bc.text = "All listed references represent authentic, peer-reviewed literature published in established journals (IEEE, Springer Nature, MDPI, Elsevier) and cited directly in the project report."
    p_bc.font.name = FONT_PRIMARY
    p_bc.font.size = Pt(9)
    p_bc.font.bold = True
    p_bc.font.color.rgb = DEEP_GREEN

# ------------------------------------------
# SLIDE 14: Outcome-Specific Supporting Evidence
# ------------------------------------------
def build_slide_14(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "OUTCOME-SPECIFIC SUPPORTING EVIDENCE", "TARGET DELIVERABLE: SCHOLARLY JOURNAL PUBLICATION ROADMAP")
    add_footer(slide, 14)

    # Left Card: Publication Details & Submission Readiness
    left_card = add_card(slide, 0.55, 1.35, 6.20, 5.40, CARD_WHITE, BORDER_GREEN)
    tf_l = left_card.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.25)
    tf_l.margin_top = Inches(0.18)
    tf_l.margin_right = Inches(0.20)

    p0 = tf_l.paragraphs[0]
    p0.text = "Scholarly Journal Publication Plan"
    p0.font.name = FONT_HEADING
    p0.font.size = Pt(13.5)
    p0.font.bold = True
    p0.font.color.rgb = DEEP_GREEN
    p0.space_after = Pt(8)

    add_formatted_bullet(tf_l, "Intended Project Outcome:", "Peer-reviewed scientific journal publication documenting the AgriTwinX architecture, multimodal fusion, and empirical findings.", 9.5, 6)
    add_formatted_bullet(tf_l, "Manuscript Working Title:", "\"AgriTwinX: An Explainable Multi-Modal Cyber-Physical Decision-Support Framework for Precision Paddy Farming\"", 9.5, 6)
    add_formatted_bullet(tf_l, "Target Journal Scope (Q1/Q2 Indexed):", "• Computers and Electronics in Agriculture (Elsevier, IF: 7.7, Q1)\n• Smart Agricultural Technology (Elsevier, CiteScore: 8.9, Q1)\n• AgriEngineering (MDPI, ESCI/Scopus Indexed, Q2)", 9, 6)
    add_formatted_bullet(tf_l, "Authorship Affiliations:", "Aiswarya AV (Student Investigator, URK23CS5048) and Mr. K. Martin Victor (Supervisor & Corresponding Author), Division of AI & ML, Karunya Institute of Technology and Sciences.", 9, 6)
    add_formatted_bullet(tf_l, "Manuscript Readiness Status:", "• [x] Empirical Benchmarking: Completed (EfficientNet, XGBoost, LightGBM, BiLSTM)\n• [x] XAI Framework Verification: Completed (Grad-CAM & TreeSHAP)\n• [x] Full-Stack Software Prototype: Completed (Flask, Blueprints, DB)\n• [ ] Draft Submission to Target Journal: In Progress (Internal Review)", 9, 4)

    # Card 1: Manuscript Submission / Tracking ID Placeholder
    p_card1 = add_card(slide, 7.05, 1.35, 5.733, 2.58, ALERT_BG, ALERT_BORDER)
    tf_p1 = p_card1.text_frame
    tf_p1.word_wrap = True
    tf_p1.margin_left = Inches(0.20)
    tf_p1.margin_top = Inches(0.15)
    tf_p1.margin_right = Inches(0.20)

    pp1_0 = tf_p1.paragraphs[0]
    pp1_0.text = "[📷 MANUSCRIPT SUBMISSION TRACKING ID & RECEIPT PLACEHOLDER]"
    pp1_0.font.name = FONT_HEADING
    pp1_0.font.size = Pt(11)
    pp1_0.font.bold = True
    pp1_0.font.color.rgb = RGBColor(185, 28, 28)
    pp1_0.space_after = Pt(6)

    add_formatted_bullet(tf_p1, "Evidence Required:", "Upload official journal portal submission confirmation snapshot displaying:", 9, 4, False)
    add_formatted_bullet(tf_p1, "1. Target Journal Name:", "e.g. Computers and Electronics in Agriculture (Elsevier)", 8.5, 2, True)
    add_formatted_bullet(tf_p1, "2. Manuscript ID:", "<<Insert Manuscript Tracking ID, e.g. COMPAG-D-26-XXXXX>>", 8.5, 2, True)
    add_formatted_bullet(tf_p1, "3. Submission Date:", "ODD SEMESTER 2026-2027 Term", 8.5, 2, True)
    add_formatted_bullet(tf_p1, "4. Verification Link:", "<<Insert Editorial Manager / ScholarOne Submission URL>>", 8.5, 2, True)

    # Card 2: Viva Voce Demonstration & Audit Placeholder
    p_card2 = add_card(slide, 7.05, 4.15, 5.733, 2.60, SAGE_BG, BORDER_GREEN)
    tf_p2 = p_card2.text_frame
    tf_p2.word_wrap = True
    tf_p2.margin_left = Inches(0.20)
    tf_p2.margin_top = Inches(0.15)
    tf_p2.margin_right = Inches(0.20)

    pp2_0 = tf_p2.paragraphs[0]
    pp2_0.text = "[📷 VIVA VOCE LIVE DEMONSTRATION & REPOSITORY EVIDENCE]"
    pp2_0.font.name = FONT_HEADING
    pp2_0.font.size = Pt(11)
    pp2_0.font.bold = True
    pp2_0.font.color.rgb = DEEP_GREEN
    pp2_0.space_after = Pt(6)

    add_formatted_bullet(tf_p2, "Evidence Required:", "Insert live web application screenshot & code audit verification:", 9, 4, False)
    add_formatted_bullet(tf_p2, "1. Farmer Dashboard:", "Browser view of /farmer/dashboard showing diagnosis & recommendations", 8.5, 2, True)
    add_formatted_bullet(tf_p2, "2. Grad-CAM Visualization:", "Analytical card comparing raw uploaded leaf with generated heatmap", 8.5, 2, True)
    add_formatted_bullet(tf_p2, "3. Codebase Repository:", "Git commit log & audited ModelRegistry weights in /ai_weights", 8.5, 2, True)
    add_formatted_bullet(tf_p2, "4. Database Verification:", "Audited records in SQLite /instance/agritwin.db treatment_logs table", 8.5, 2, True)

# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    prs = create_presentation()
    print("Building Slide 1: Title Slide...")
    build_slide_1(prs)
    print("Building Slide 2: Agenda...")
    build_slide_2(prs)
    print("Building Slide 3: Abstract...")
    build_slide_3(prs)
    print("Building Slide 4: Problem Definition, Scope & Objectives...")
    build_slide_4(prs)
    print("Building Slide 5: Literature Survey...")
    build_slide_5(prs)
    print("Building Slide 6: Proposed System...")
    build_slide_6(prs)
    print("Building Slide 7: System Architecture...")
    build_slide_7(prs)
    print("Building Slide 8: Implementation...")
    build_slide_8(prs)
    print("Building Slide 9: Technologies Used...")
    build_slide_9(prs)
    print("Building Slide 10: Results and Discussion...")
    build_slide_10(prs)
    print("Building Slide 11: Research Gap and Contribution...")
    build_slide_11(prs)
    print("Building Slide 12: Conclusion and Future Scope...")
    build_slide_12(prs)
    print("Building Slide 13: References...")
    build_slide_13(prs)
    print("Building Slide 14: Outcome-Specific Supporting Evidence...")
    build_slide_14(prs)

    output_filename = "AgriTwinX_Final_Project_Review.pptx"
    prs.save(output_filename)
    print(f"SUCCESS: Presentation successfully created and saved as '{output_filename}' ({len(prs.slides)} slides)!")

if __name__ == "__main__":
    main()
