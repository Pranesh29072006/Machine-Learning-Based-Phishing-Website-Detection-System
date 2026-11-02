"""
Script to generate a comprehensive, publication-ready academic project report
in Word (.docx) format for:
'Machine Learning Based Phishing Website Detection System'
with embedded IoT Threat Alert Subsystem Block Diagram.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Phishing_Website_Detection_System_Report.docx")

# Define Color Palette
COLOR_PRIMARY_NAVY = RGBColor(15, 23, 42)       # #0F172A
COLOR_SECONDARY_BLUE = RGBColor(37, 99, 235)    # #2563EB
COLOR_CYAN = RGBColor(14, 165, 233)             # #0EA5E9
COLOR_DARK_TEXT = RGBColor(51, 65, 85)          # #334155
COLOR_MUTED = RGBColor(100, 116, 139)           # #64748B
COLOR_RED = RGBColor(220, 38, 38)               # #DC2626
COLOR_GREEN = RGBColor(22, 163, 74)             # #16A34A

HEX_NAVY = "0F172A"
HEX_LIGHT_BG = "F8FAFC"
HEX_BORDER = "CBD5E1"
HEX_ROW_ALT = "F1F5F9"
HEX_DANGER_BG = "FEF2F2"
HEX_SAFE_BG = "F0FDF4"
HEX_CYAN_BG = "F0F9FF"


def set_cell_background(cell, hex_color):
    """Set background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner margins (padding) for a table cell in dxa (1/20 pt)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)


def create_callout_box(doc, text, title="NOTE:", hex_bg=HEX_LIGHT_BG, hex_border="2563EB"):
    """Create a styled callout quote box with colored left border."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, hex_bg)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="36" w:space="0" w:color="{hex_border}"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tc_pr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    r_title = p.add_run(f"{title} ")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = COLOR_PRIMARY_NAVY
    
    r_text = p.add_run(text)
    r_text.font.name = "Arial"
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = COLOR_DARK_TEXT
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


def add_custom_heading(doc, text, level=1):
    """Add styled headings with consistent hierarchy and spacing."""
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Arial"
    
    if level == 1:
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        run.font.size = Pt(16)
        run.font.color.rgb = COLOR_PRIMARY_NAVY
        # Add subtle bottom line to Heading 1
        pBdr = parse_xml(
            f'<w:pBdr {nsdecls("w")}>'
            f'<w:bottom w:val="single" w:sz="12" w:space="4" w:color="{HEX_BORDER}"/>'
            f'</w:pBdr>'
        )
        p._p.get_or_add_pPr().append(pBdr)
    elif level == 2:
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        run.font.size = Pt(13)
        run.font.color.rgb = COLOR_SECONDARY_BLUE
    elif level == 3:
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run.font.size = Pt(11)
        run.font.color.rgb = COLOR_DARK_TEXT
    return p


def add_styled_paragraph(doc, text, space_after=6, italic=False, bold=False):
    """Add standardized body text."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(10)
    run.font.color.rgb = COLOR_DARK_TEXT
    run.italic = italic
    run.bold = bold
    return p


def build_document():
    doc = Document()
    
    # Configure Standard Page Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Machine Learning Based Phishing Website Detection System")
        hrun.font.name = "Arial"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = COLOR_MUTED
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Department of Computer Science & Engineering | Academic Project Report")
        frun.font.name = "Arial"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = COLOR_MUTED

    # -------------------------------------------------------------------------
    # COVER / TITLE PAGE
    # -------------------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(40)
    title_p.paragraph_format.space_after = Pt(10)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    t_run = title_p.add_run("MACHINE LEARNING BASED PHISHING WEBSITE DETECTION SYSTEM")
    t_run.bold = True
    t_run.font.name = "Arial"
    t_run.font.size = Pt(22)
    t_run.font.color.rgb = COLOR_PRIMARY_NAVY
    
    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(30)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    s_run = sub_p.add_run("With Embedded IoT Multi-Factor Alert & Threat Verification Subsystem")
    s_run.font.name = "Arial"
    s_run.font.size = Pt(13)
    s_run.font.color.rgb = COLOR_SECONDARY_BLUE
    s_run.bold = True
    
    desc_p = doc.add_paragraph()
    desc_p.paragraph_format.space_before = Pt(20)
    desc_p.paragraph_format.space_after = Pt(40)
    desc_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    d_run = desc_p.add_run(
        "A Comprehensive Project Report Submitted in Partial Fulfillment of the Requirements\n"
        "for the Award of the Degree of\n"
        "BACHELOR OF TECHNOLOGY / BACHELOR OF ENGINEERING\n"
        "IN\n"
        "COMPUTER SCIENCE AND ENGINEERING"
    )
    d_run.font.name = "Arial"
    d_run.font.size = Pt(11)
    d_run.font.color.rgb = COLOR_DARK_TEXT
    d_run.italic = True
    
    # Metadata Block
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    
    cell_00 = meta_table.cell(0, 0)
    cell_00.width = Inches(3.2)
    p00 = cell_00.paragraphs[0]
    p00.add_run("SUBMITTED BY:\n").bold = True
    p00.add_run("Student Candidate\nDepartment of CSE\nAcademic Year 2026")
    
    cell_01 = meta_table.cell(0, 1)
    cell_01.width = Inches(3.2)
    p01 = cell_01.paragraphs[0]
    p01.add_run("UNDER THE GUIDANCE OF:\n").bold = True
    p01.add_run("Project Supervisor / Guide\nDepartment of Computer Science & Engineering\nFaculty of Engineering")
    
    for row in meta_table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.15
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = COLOR_DARK_TEXT

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CERTIFICATE & ABSTRACT
    # -------------------------------------------------------------------------
    add_custom_heading(doc, "CERTIFICATE OF AUTHENTICITY", level=1)
    add_styled_paragraph(
        doc,
        "This is to certify that the project entitled 'Machine Learning Based Phishing Website Detection System "
        "with Embedded IoT Alert Subsystem' is a bona fide record of work carried out under our supervision and guidance "
        "in partial fulfillment of the requirements for the award of the Degree of Bachelor of Technology in "
        "Computer Science and Engineering. The results embodied in this report have been verified through empirical "
        "machine learning evaluation, isolated database testing, and automated unit testing suites."
    )
    
    sig_p = doc.add_paragraph()
    sig_p.paragraph_format.space_before = Pt(40)
    sig_p.paragraph_format.space_after = Pt(20)
    sig_run = sig_p.add_run(
        "________________________                     ________________________\n"
        "    Project Guide                               Head of Department\n"
        "Department of CSE                               Department of CSE"
    )
    sig_run.font.name = "Arial"
    sig_run.font.size = Pt(10)
    sig_run.font.color.rgb = COLOR_DARK_TEXT

    add_custom_heading(doc, "ABSTRACT", level=1)
    add_styled_paragraph(
        doc,
        "Phishing attacks remain one of the most critical and pervasive threat vectors in modern cyberspace, "
        "accounting for over 80% of reported security incidents that lead to credential theft, session hijacking, "
        "and unauthorized network intrusion. Traditional defense mechanisms rely predominantly on static blacklists "
        "and centralized Domain Name System (DNS) reputation databases. However, these traditional measures fail to "
        "counter zero-hour phishing attacks, fast-flux domains, and dynamically generated fraudulent Uniform Resource "
        "Locators (URLs) which often exist for mere hours before being retired."
    )
    add_styled_paragraph(
        doc,
        "This project presents an end-to-end, zero-trust cybersecurity solution titled 'Machine Learning Based Phishing "
        "Website Detection System'. The system operates by converting raw URL strings into a standardized 17-dimensional "
        "lexical and structural feature vector. Crucially, the solution executes non-destructive inspection—evaluating URLs "
        "offline without establishing live TCP connections or executing untrusted target scripts, completely eliminating "
        "browser drive-by exploitation risks."
    )
    add_styled_paragraph(
        doc,
        "The machine learning pipeline evaluates multiple supervised classifiers—including Random Forest, Gradient Boosting, "
        "Decision Trees, and Logistic Regression—on an authentic, balanced dataset of 7,000 real-world URLs sourced from "
        "Cisco OpenDNS, the University of New Brunswick (UNB) CIC benign repository, PhishTank, and OpenPhish. The champion "
        "Random Forest model achieves an exceptional Accuracy of 95.93%, Precision of 97.49%, and an F1-Score of 95.86% on "
        "held-out unseen test samples. To address the phenomenon of domain-level data leakage, a rigorous domain-disjoint "
        "evaluation (GroupShuffleSplit with 0 domain overlap) was executed, verifying a 97.21% accuracy on completely novel domains."
    )
    add_styled_paragraph(
        doc,
        "Furthermore, this report documents the hardware integration subsystem featuring an ESP32 microcontroller, RFID reader, "
        "audio buzzer, LCD display, camera module, and regulated power supply operating via bidirectional UART serial communication. "
        "This hardware extension enables two-factor physical access authorization and real-time audio-visual threat notification, "
        "creating a unified digital-physical defense framework."
    )

    create_callout_box(
        doc,
        "Keywords: Cybersecurity, Phishing Detection, Machine Learning, Random Forest, Lexical Analysis, "
        "Domain-Disjoint Evaluation, Flask, SQLite, ESP32, IoT Security, Zero-Trust Non-Destructive Inspection.",
        title="INDEX TERMS:",
        hex_bg=HEX_CYAN_BG,
        hex_border="0EA5E9"
    )

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # -------------------------------------------------------------------------
    add_custom_heading(doc, "CHAPTER 1: INTRODUCTION", level=1)
    
    add_custom_heading(doc, "1.1 Background & Motivation", level=2)
    add_styled_paragraph(
        doc,
        "The exponential expansion of global digital services, internet banking, e-commerce platforms, and cloud infrastructure "
        "has transformed Uniform Resource Locators (URLs) into the primary gateway for web interactions. Unfortunately, "
        "this reliance has made the URL the primary target of cyber deception. Phishing involves the psychological manipulation "
        "and technical counterfeiting of legitimate online entities to deceive users into disclosing sensitive personal identifiers, "
        "passwords, credit card numbers, or cryptographic keys."
    )
    add_styled_paragraph(
        doc,
        "According to the Anti-Phishing Working Group (APWG) and cybersecurity telemetry from CISA, modern threat actors deploy "
        "millions of unique phishing landing pages annually. Rather than hacking through hardened server perimeters, adversaries "
        "exploit the human element using deceptive URL structural manipulations, such as subdomain cloaking, Unicode typosquatting, "
        "open redirection, and embedded IP host addresses."
    )

    add_custom_heading(doc, "1.2 Problem Statement", level=2)
    add_styled_paragraph(
        doc,
        "Conventional browser protection modules depend extensively on community-curated blacklists (e.g., Google Safe Browsing, "
        "PhishTank feeds). While blacklists exhibit low false-positive rates, they suffer from fundamental architectural latency: "
        "a phishing website must first be detected, reported, human-verified, and propagated to end-user clients. Empirical studies "
        "indicate that over 65% of phishing campaigns conclude within four hours of launching—long before blacklist entries propagate. "
        "Consequently, there is an urgent necessity for a client-side, zero-day predictive machine learning system capable of classifying "
        "a URL based solely on its intrinsic lexical and syntactic characteristics before navigation occurs."
    )

    add_custom_heading(doc, "1.3 Project Objectives", level=2)
    add_styled_paragraph(doc, "The primary objectives of this project are:")
    
    objectives = [
        ("Lexical Feature Extraction: ", "Design and implement a robust 17-dimensional URL feature extraction engine capable of analyzing length, domain depth, character distribution, IPv4/IPv6 presence, protocol encryption, and credential harvesting keywords."),
        ("Empirical ML Training & Validation: ", "Train and benchmark multiple supervised classifiers on a balanced 7,000-URL benchmark, ensuring zero data leakage and authentic domain-disjoint evaluation."),
        ("Zero-Trust Non-Destructive Architecture: ", "Guarantee that URL analysis executes purely offline without connecting to the destination, preventing drive-by malware infections."),
        ("Web Application Deployment: ", "Develop a modern, dark-themed Cybersecurity Operations Center (SOC) web dashboard using Python Flask, SQLite, Bootstrap 5, and Chart.js."),
        ("Embedded IoT Subsystem Integration: ", "Design a complementary physical security architecture integrating an ESP32 microcontroller, RFID reader, buzzer, LCD, and camera over UART to provide physical multi-factor authentication and alert signaling."),
        ("Rigorous Verification: ", "Implement a complete automated test suite verifying all features, boundary inputs, security controls, and database isolation.")
    ]
    for prefix, body in objectives:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r_pre = p.add_run(prefix)
        r_pre.bold = True
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(10)
        r_pre.font.color.rgb = COLOR_SECONDARY_BLUE
        r_body = p.add_run(body)
        r_body.font.name = "Arial"
        r_body.font.size = Pt(10)
        r_body.font.color.rgb = COLOR_DARK_TEXT

    # -------------------------------------------------------------------------
    # CHAPTER 2: SYSTEM ARCHITECTURE & BLOCK DIAGRAM
    # -------------------------------------------------------------------------
    add_custom_heading(doc, "CHAPTER 2: SYSTEM ARCHITECTURE & BLOCK DIAGRAM", level=1)
    
    add_custom_heading(doc, "2.1 Unified Digital-Physical Security Architecture", level=2)
    add_styled_paragraph(
        doc,
        "The overall system combines a high-performance software machine learning application running on a host workstation (Laptop) "
        "with an embedded hardware microcontroller unit (ESP32) that handles physical security verification, audio-visual feedback, "
        "and hardware-level alerting. Figure 2.1 illustrates the hardware block diagram and serial communication topology."
    )

    add_custom_heading(doc, "2.2 Hardware Subsystem Block Diagram Breakdown", level=2)
    add_styled_paragraph(
        doc,
        "The embedded block diagram submitted for this project consists of seven interconnected hardware modules communicating "
        "with the central processing laptop over universal asynchronous receiver-transmitter (UART) serial lines:"
    )

    # Hardware Block Diagram ASCII / Box Representation
    diag_box = doc.add_table(rows=1, cols=1)
    diag_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_d = diag_box.cell(0, 0)
    cell_d.width = Inches(6.5)
    set_cell_background(cell_d, "0B132B")
    set_cell_margins(cell_d, top=160, bottom=160, left=180, right=180)
    
    dp = cell_d.paragraphs[0]
    dp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    d_run = dp.add_run(
        "+---------------------------------------------------------------------------+\n"
        "|                    HARDWARE SUBSYSTEM BLOCK DIAGRAM                       |\n"
        "+---------------------------------------------------------------------------+\n"
        "|                                                                           |\n"
        "|   +-------------------+                     +-------------------------+   |\n"
        "|   |    RFID Reader    | ---> [SPI / I2C] -> |                         |   |\n"
        "|   | (Token / Badge)   |                     |                         |   |\n"
        "|   +-------------------+                     |                         |   |\n"
        "|                                             |                         |   |\n"
        "|   +-------------------+                     |                         |   |\n"
        "|   |   Camera Module   | ---> [DVP / USB] -> |          ESP32          |   |\n"
        "|   | (Visual Evidence) |                     |     Microcontroller     |   |\n"
        "|   +-------------------+                     |                         |   |\n"
        "|                                             |                         |   |\n"
        "|   +-------------------+                     |                         |   |\n"
        "|   | Power Supply Unit | ---> [5V / 3.3V] -> |                         |   |\n"
        "|   |  (Regulated PSU)  |                     |                         |   |\n"
        "|   +-------------------+                     +------------+------------+   |\n"
        "|                                                          |                |\n"
        "|                                                [UART Tx] | ^ [UART Rx]    |\n"
        "|                                                          v |              |\n"
        "|   +-------------------+                     +------------+------------+   |\n"
        "|   |   Buzzer Alarm    | <-- [GPIO PWM] <--- |                         |   |\n"
        "|   |  (Audio Warning)  |                     |                         |   |\n"
        "|   +-------------------+                     |      Laptop / Host      |   |\n"
        "|                                             |  (Flask ML & Database)  |   |\n"
        "|   +-------------------+                     |                         |   |\n"
        "|   |    LCD Display    | <-- [I2C 0x27] <--- |                         |   |\n"
        "|   |  (Status / Verdict|                     +-------------------------+   |\n"
        "|   +-------------------+                                                   |\n"
        "+---------------------------------------------------------------------------+\n"
    )
    d_run.font.name = "Courier New"
    d_run.font.size = Pt(8.5)
    d_run.font.color.rgb = RGBColor(0, 242, 254)

    cap_p = doc.add_paragraph()
    cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap_p.paragraph_format.space_before = Pt(4)
    cap_p.paragraph_format.space_after = Pt(12)
    c_run = cap_p.add_run("Figure 2.1: Integrated Hardware Block Diagram & Bidirectional Serial Communication Topology")
    c_run.font.name = "Arial"
    c_run.font.size = Pt(9)
    c_run.font.color.rgb = COLOR_MUTED
    c_run.italic = True

    # Hardware Components Detailed Table
    hw_table = doc.add_table(rows=8, cols=3)
    hw_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hw_table.autofit = False
    
    headers = ["Hardware Component", "Interface / Pinout", "Functional Role in Cybersecurity Architecture"]
    for i, h in enumerate(headers):
        c = hw_table.cell(0, i)
        set_cell_background(c, HEX_NAVY)
        set_cell_margins(c, top=80, bottom=80, left=120, right=120)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    col_widths = [Inches(1.8), Inches(1.6), Inches(3.1)]
    hw_data = [
        ("ESP32 Microcontroller", "Tensilica Dual-Core 240MHz, 36 GPIOs", "Coordinates edge sensor acquisition, drives display, generates PWM siren pulses, and exchanges serial frames with host."),
        ("RFID Reader (RC522 / EM-18)", "SPI (MISO, MOSI, SCK, CS) / UART", "Provides physical dual-factor authorization (2FA). Users must badge in before web analysis console unlocks."),
        ("Audio Buzzer", "GPIO Active High / PWM", "Sounds an aggressive 85dB pulsating audible alarm when high-risk phishing websites are flagged."),
        ("Liquid Crystal Display (LCD)", "I2C 16x2 / 20x4 (SDA/SCL)", "Displays real-time classification verdicts: 'SAFE [98.5%]' or 'DANGER: PHISH [99.2%]' directly at the physical console."),
        ("Camera Module (ESP32-CAM / USB)", "DVP Parallel / USB 2.0 Host", "Captures an automated snapshot when unauthorized access or a phishing payload is triggered, storing visual audit logs."),
        ("UART Serial Bus (Tx / Rx)", "GPIO 1 (TX0) & GPIO 3 (RX0) @ 115200 bps", "Facilitates full-duplex communication: sends RFID badge IDs to laptop and receives ML threat predictions from Flask backend."),
        ("Power Supply Unit (PSU)", "Regulated 5V DC (2.0A) / 3.3V LDO", "Powers the ESP32 chip, LCD backlighting, camera sensor, and active buzzer without drawing excessive current from laptop USB ports.")
    ]

    for row_idx, row_data in enumerate(hw_data, start=1):
        hex_bg = HEX_ROW_ALT if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(row_data):
            c = hw_table.cell(row_idx, col_idx)
            c.width = col_widths[col_idx]
            set_cell_background(c, hex_bg)
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(9)
            r.font.color.rgb = COLOR_DARK_TEXT
            if col_idx == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------------------
    # CHAPTER 3: THE 17 HEURISTIC URL FEATURE VECTORS
    # -------------------------------------------------------------------------
    add_custom_heading(doc, "CHAPTER 3: THE 17 HEURISTIC URL FEATURE VECTORS", level=1)
    add_styled_paragraph(
        doc,
        "A cornerstone of this project is the mathematical extraction of seventeen lexical and syntactic features "
        "from submitted URL strings. Crucially, the training pipeline (train_model.py) and the live Flask inference engine "
        "(app.py) utilize the exact same feature extraction module (feature_extraction.py), strictly maintaining the "
        "ordered feature vector:"
    )

    feat_table = doc.add_table(rows=18, cols=4)
    feat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    feat_table.autofit = False

    f_headers = ["#", "Feature Identifier", "Data Type", "Threat Significance & Adversarial Vector"]
    f_widths = [Inches(0.4), Inches(2.0), Inches(1.0), Inches(3.1)]

    for i, h in enumerate(f_headers):
        c = feat_table.cell(0, i)
        c.width = f_widths[i]
        set_cell_background(c, HEX_NAVY)
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    features_info = [
        ("1", "url_length", "Float", "Extremely long URLs (>75 chars) frequently hide malicious redirection tokens or deep nested directory paths."),
        ("2", "domain_length", "Float", "Long hostnames (>30 chars) often pad legitimate brand names with deceptive descriptive suffixes to mislead users."),
        ("3", "num_dots", "Float", "Three or more dots in a URL usually indicate multi-level subdomains or disguised hosts."),
        ("4", "num_hyphens", "Float", "Hyphens in hostnames (e.g., paypal-security-update.com) are a classic trademark spoofing indicator."),
        ("5", "num_digits", "Float", "High digit counts represent autogenerated hashes, session IDs, or dynamic malware paths."),
        ("6", "has_ip_address", "Binary (0/1)", "Direct IPv4/IPv6 hosts (e.g., http://192.168.1.1/login) bypass domain registration WHOIS tracking."),
        ("7", "is_https", "Binary (0/1)", "Checks protocol encryption. Note: modern phishing pages may also use free TLS certificates."),
        ("8", "has_at_symbol", "Binary (0/1)", "RFC standards interpret text before '@' as credentials, routing browsers to the host after the symbol."),
        ("9", "num_suspicious_symbols", "Float", "Abundance of query delimiters (?, =, &, %, ~, +, $) used in token and state transmission."),
        ("10", "num_subdomains", "Float", "Multiple subdomains (e.g., login.secure.bank.attacker.com) conceal the true root domain."),
        ("11", "is_shortened", "Binary (0/1)", "Shortening services (bit.ly, tinyurl, t.co) conceal destination domains from human inspection."),
        ("12", "path_length", "Float", "Deep directory paths indicate embedded credential harvesting landing pages."),
        ("13", "num_query_params", "Float", "Frequency of query parameters carrying session state or target identification hashes."),
        ("14", "has_sensitive_keywords", "Float", "Detects high-risk phishing keywords (login, verify, account, banking, secure, update, signin)."),
        ("15", "has_double_slash_redirect", "Binary (0/1)", "Double slashes (//) within the URL path component can trigger open-redirect browser behaviors."),
        ("16", "prefix_suffix_hyphen", "Binary (0/1)", "Presence of hyphens within the domain portion specifically to mimic legitimate brand names."),
        ("17", "has_tld_in_subdomain", "Binary (0/1)", "Deceptive placement of .com or .org inside subdomains (e.g., google.com.malicious.net).")
    ]

    for row_idx, f_row in enumerate(features_info, start=1):
        hex_bg = HEX_ROW_ALT if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(f_row):
            c = feat_table.cell(row_idx, col_idx)
            c.width = f_widths[col_idx]
            set_cell_background(c, hex_bg)
            set_cell_margins(c, top=50, bottom=50, left=80, right=80)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(8.5)
            r.font.color.rgb = COLOR_DARK_TEXT
            if col_idx in (0, 1):
                r.bold = True
                if col_idx == 1:
                    r.font.name = "Courier New"

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------------------
    # CHAPTER 4: MACHINE LEARNING EVALUATION & GENERALIZATION
    # -------------------------------------------------------------------------
    add_custom_heading(doc, "CHAPTER 4: MACHINE LEARNING EVALUATION & GENERALIZATION", level=1)
    
    add_custom_heading(doc, "4.1 Benchmark Dataset Provenance", level=2)
    add_styled_paragraph(
        doc,
        "The models were trained and tested on a curated dataset comprising 7,000 URLs: 3,500 legitimate URLs and 3,500 confirmed "
        "phishing URLs. Legitimate samples were extracted from Cisco OpenDNS top-10,000 domains (covering root landing pages, "
        "documentation, blogs, and query parameters) combined with the University of New Brunswick (UNB) CIC benign dataset. "
        "Phishing samples were compiled from PhishTank verified active archives and the OpenPhish community live feed."
    )

    add_custom_heading(doc, "4.2 Multi-Algorithm Performance Benchmark", level=2)
    add_styled_paragraph(
        doc,
        "Four candidate machine learning algorithms were trained and evaluated on 1,400 held-out test samples (20% stratified test split). "
        "The empirical findings are summarized in Table 4.1."
    )

    # ML Benchmark Table
    ml_table = doc.add_table(rows=5, cols=6)
    ml_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    ml_table.autofit = False

    ml_headers = ["Model Architecture", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    ml_widths = [Inches(2.0), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9)]

    for i, h in enumerate(ml_headers):
        c = ml_table.cell(0, i)
        c.width = ml_widths[i]
        set_cell_background(c, HEX_NAVY)
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    ml_data = [
        ("Random Forest (Champion)", "95.93%", "97.49%", "94.29%", "95.86%", "0.9934"),
        ("Gradient Boosting", "95.79%", "97.48%", "94.00%", "95.71%", "0.9932"),
        ("Decision Tree Classifier", "94.71%", "97.57%", "91.71%", "94.55%", "0.9471"),
        ("Logistic Regression", "83.71%", "84.91%", "82.00%", "83.43%", "0.9168")
    ]

    for row_idx, row in enumerate(ml_data, start=1):
        hex_bg = HEX_ROW_ALT if row_idx % 2 == 1 else "FFFFFF"
        if row_idx == 1:
            hex_bg = HEX_SAFE_BG
        for col_idx, text in enumerate(row):
            c = ml_table.cell(row_idx, col_idx)
            c.width = ml_widths[col_idx]
            set_cell_background(c, hex_bg)
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(9)
            r.font.color.rgb = COLOR_DARK_TEXT
            if col_idx == 0:
                r.bold = True

    add_styled_paragraph(
        doc,
        "Table 4.1: Empirical Comparative Performance of Machine Learning Classifiers on Held-Out Test Data (N = 1,400)",
        italic=True,
        space_after=8
    )

    add_custom_heading(doc, "4.3 Confusion Matrix Analysis", level=2)
    add_styled_paragraph(
        doc,
        "The champion Random Forest classifier achieved the following distribution across the 1,400 test samples:"
    )

    # Confusion Matrix Table
    cm_table = doc.add_table(rows=3, cols=3)
    cm_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cm_table.autofit = False
    
    cm_widths = [Inches(2.1), Inches(2.2), Inches(2.2)]
    
    # Headers
    cm_table.cell(0, 0).text = "Actual \\ Predicted"
    cm_table.cell(0, 1).text = "Predicted Legitimate (0)"
    cm_table.cell(0, 2).text = "Predicted Phishing (1)"
    
    # Row 1
    cm_table.cell(1, 0).text = "Actual Legitimate (0)"
    cm_table.cell(1, 1).text = "True Negatives (TN): 683\n(Correctly Passed - 97.6%)"
    cm_table.cell(1, 2).text = "False Positives (FP): 17\n(False Alarms - 2.4%)"
    
    # Row 2
    cm_table.cell(2, 0).text = "Actual Phishing (1)"
    cm_table.cell(2, 1).text = "False Negatives (FN): 40\n(Missed Threats - 5.7%)"
    cm_table.cell(2, 2).text = "True Positives (TP): 660\n(Threats Intercepted - 94.3%)"

    for r_idx, row in enumerate(cm_table.rows):
        for c_idx, c in enumerate(row.cells):
            c.width = cm_widths[c_idx]
            if r_idx == 0 or c_idx == 0:
                set_cell_background(c, HEX_NAVY)
                p = c.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
            elif (r_idx == 1 and c_idx == 1) or (r_idx == 2 and c_idx == 2):
                set_cell_background(c, HEX_SAFE_BG)
                p = c.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.color.rgb = COLOR_GREEN
                    run.bold = True
            else:
                set_cell_background(c, HEX_DANGER_BG)
                p = c.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.color.rgb = COLOR_RED
                    run.bold = True
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_custom_heading(doc, "4.4 Academic Generalization: Domain-Disjoint Evaluation", level=2)
    add_styled_paragraph(
        doc,
        "A critical vulnerability in numerous published academic phishing detection systems is Domain-Level Data Leakage: "
        "when multiple URLs from the same domain (e.g. distractify.com or docs.google.com) reside in both the training set and "
        "the test set, the classifier can achieve artificially elevated accuracy simply by memorizing domain characteristics rather "
        "than learning generalizable lexical principles."
    )
    add_styled_paragraph(
        doc,
        "To rigorously eliminate this bias, we implemented a GroupShuffleSplit clustered on registered domain names. This partitioned "
        "the dataset such that 100% of domains in the test set were completely absent from the training set. Even under this strict "
        "zero-leakage constraint, the Random Forest model achieved:"
    )

    create_callout_box(
        doc,
        "Domain-Disjoint Test Samples: 1,360 URLs\n"
        "Domain Overlap between Train & Test: EXACTLY ZERO (0)\n"
        "Disjoint Test Accuracy: 97.21%\n"
        "Disjoint Test Precision: 98.18%\n"
        "Disjoint Test Recall: 96.92%\n"
        "Disjoint Test F1-Score: 97.55%\n"
        "Confusion Matrix: True Negatives = 567, False Positives = 14, False Negatives = 24, True Positives = 755.",
        title="EMPIRICAL GENERALIZATION VERIFICATION:",
        hex_bg=HEX_SAFE_BG,
        hex_border="16A34A"
    )

    # -------------------------------------------------------------------------
    # CHAPTER 5: SOFTWARE IMPLEMENTATION & TESTING
    # -------------------------------------------------------------------------
    add_custom_heading(doc, "CHAPTER 5: SOFTWARE IMPLEMENTATION & VERIFICATION", level=1)
    
    add_custom_heading(doc, "5.1 Flask Backend & Security Controls", level=2)
    add_styled_paragraph(
        doc,
        "The software architecture is engineered using Python Flask with production-grade cybersecurity safeguards:\n"
        "1. Input Sanitation: Strips carriage returns, newlines, and null bytes; enforces length limits (<2048 chars).\n"
        "2. Protocol Whitelisting: Accepts only http:// and https://; explicitly rejects file:, data:, javascript:, and ftp:.\n"
        "3. Database Parameterization: Employs SQLite with parameterized '?' placeholders, guaranteeing protection against SQL Injection.\n"
        "4. Non-Destructive Offline Inference: The server never issues outbound HTTP GET/POST requests to analyzed targets, preventing drive-by exploits.\n"
        "5. Test Database Isolation: Unit test runs automatically redirect database operations to a temporary database, preventing the loss of user history."
    )

    add_custom_heading(doc, "5.2 Automated Testing Results", level=2)
    add_styled_paragraph(
        doc,
        "The system incorporates an automated regression suite in test_system.py covering 43 distinct unit and integration test cases. "
        "Table 5.1 details the test execution breakdown."
    )

    test_table = doc.add_table(rows=7, cols=4)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_table.autofit = False

    t_headers = ["Test Category", "Target Under Test", "Cases Executed", "Outcome"]
    t_widths = [Inches(1.8), Inches(2.7), Inches(1.0), Inches(1.0)]

    for i, h in enumerate(t_headers):
        c = test_table.cell(0, i)
        c.width = t_widths[i]
        set_cell_background(c, HEX_NAVY)
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    test_data = [
        ("Feature Extraction", "Individual verification of all 17 feature extractors (IPv4, IPv6, symbols, subdomains)", "18", "18/18 PASS"),
        ("Input Validation", "Disallowed schemes (javascript, file, ftp), empty, malformed hosts ('...'), length limit", "6", "6/6 PASS"),
        ("Model Inference", "Legitimate URL prediction, Phishing prediction, Mock model compute failure recovery", "4", "4/4 PASS"),
        ("Database Security", "Isolated DB insert, retrieve, search query filtering, and history clearing", "1", "1/1 PASS"),
        ("HTTP Web Routes", "GET /, /history, /model-performance, /about, /result, and custom 404 handler", "8", "8/8 PASS"),
        ("REST API & Method Safety", "POST /api/analyze, invalid payload handling, disallowed GET on POST-only endpoints", "6", "6/6 PASS")
    ]

    for row_idx, row in enumerate(test_data, start=1):
        hex_bg = HEX_ROW_ALT if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(row):
            c = test_table.cell(row_idx, col_idx)
            c.width = t_widths[col_idx]
            set_cell_background(c, hex_bg)
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(9)
            r.font.color.rgb = COLOR_DARK_TEXT
            if col_idx == 3:
                r.bold = True
                r.font.color.rgb = COLOR_GREEN

    add_styled_paragraph(
        doc,
        "Table 5.1: Summary of Automated Unit & Integration Testing Suite (Ran 43 tests in 1.28s - 100% Passing)",
        italic=True,
        space_after=8
    )

    # -------------------------------------------------------------------------
    # CHAPTER 6: CONCLUSION & DEMONSTRATION GUIDE
    # -------------------------------------------------------------------------
    add_custom_heading(doc, "CHAPTER 6: CONCLUSION & ACADEMIC DEMONSTRATION", level=1)
    add_styled_paragraph(
        doc,
        "The 'Machine Learning Based Phishing Website Detection System' successfully addresses the challenges of detecting zero-hour "
        "fraudulent URLs without requiring dangerous live HTTP requests or relying on stale static blacklists. By integrating a 17-dimensional "
        "feature extractor, an empirically validated Random Forest classifier (95.93% accuracy, 97.21% domain-disjoint generalization), "
        "an offline SQLite scan history database, and an embedded IoT hardware alert subsystem (ESP32, RFID, LCD, Buzzer, Camera over UART), "
        "the project delivers an exemplary final-year academic contribution."
    )

    add_custom_heading(doc, "6.1 Step-by-Step Demonstration Sequence", level=2)
    steps = [
        ("Step 1: Start Application: ", "In PowerShell, execute 'python app.py' to launch the web dashboard at http://127.0.0.1:5000."),
        ("Step 2: Safe Domain Inspection: ", "Click the 'Google (Safe)' or 'Wikipedia (Safe)' sample pill and select 'Analyze Website'. Demonstrate the emerald green 'CLASSIFIED LEGITIMATE' badge, confidence score, and feature diagnostic breakdown."),
        ("Step 3: Phishing Threat Detection: ", "Enter 'http://192.168.1.1/paypal-login/verification.php?cmd=_login_submit'. Show the crimson 'SUSPECTED PHISHING THREAT' verdict, threat confidence (>99%), and highlight how the presence of an IP host and sensitive keywords triggered the model."),
        ("Step 4: Scan History Inspection: ", "Navigate to 'Scan History' to show persistent SQLite logging. Demonstrate real-time search filtering (e.g. searching 'paypal' or 'google')."),
        ("Step 5: Model Performance Review: ", "Open 'Model Performance' to present the live confusion matrix, multi-algorithm comparison chart, feature importance weights, and the Academic Generalization card."),
        ("Step 6: Automated Test Verification: ", "In the terminal, execute 'python test_system.py' to prove that all 43 tests pass cleanly in under 2 seconds without erasing user scan history.")
    ]
    for s_title, s_body in steps:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        r1 = p.add_run(s_title)
        r1.bold = True
        r1.font.name = "Arial"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_SECONDARY_BLUE
        r2 = p.add_run(s_body)
        r2.font.name = "Arial"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_DARK_TEXT

    # References
    add_custom_heading(doc, "REFERENCES", level=1)
    refs = [
        "1. Anti-Phishing Working Group (APWG). (2025). 'Phishing Activity Trends Report, 4th Quarter 2024.' APWG Technical Committee.",
        "2. University of New Brunswick (UNB) Canadian Institute for Cybersecurity (CIC). (2016). 'URL-2016 Dataset: Benign, Spam, Phishing, and Malware URLs.'",
        "3. PhishTank Developer Archive. (2024). 'Verified Online Valid Phishing URL Repository.' OpenDNS / Cisco Systems.",
        "4. OpenPhish. (2026). 'Active Global Phishing Threat Intelligence Community Feed.' https://openphish.com",
        "5. Breiman, L. (2001). 'Random Forests.' Machine Learning, 45(1), 5-32.",
        "6. Pedregosa, F., et al. (2011). 'Scikit-learn: Machine Learning in Python.' Journal of Machine Learning Research, 12, 2825-2830.",
        "7. NIST Special Publication 800-63B. (2023). 'Digital Identity Guidelines: Authentication and Lifecycle Management.'",
        "8. Espressif Systems. (2024). 'ESP32 Technical Reference Manual: Dual Core Tensilica LX6 Microcontroller & UART Subsystems.'"
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(ref)
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_DARK_TEXT

    # Save to disk
    doc.save(OUTPUT_PATH)
    print(f"[SUCCESS] Word report successfully created at: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    build_document()
