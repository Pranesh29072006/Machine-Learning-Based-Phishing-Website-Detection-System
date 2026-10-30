"""
Script to generate:
1. High-resolution professional Block Diagram image (PNG, 300 DPI) using matplotlib.
2. Complete, publication-quality Microsoft Word (.docx) document detailing the entire
   ESP32 Embedded System Architecture, Block Diagram, Interfacing Pinout, Operational Flow,
   and Electrical Specifications.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIAGRAM_IMG_PATH = os.path.join(BASE_DIR, "esp32_system_block_diagram.png")
DOCX_OUTPUT_PATH = os.path.join(BASE_DIR, "ESP32_Project_Block_Diagram_Specification.docx")


# ==============================================================================
# PART 1: GENERATE HIGH-RESOLUTION SYSTEM BLOCK DIAGRAM IMAGE
# ==============================================================================
def generate_block_diagram_image():
    print("[1/2] Generating high-resolution block diagram image...")
    fig, ax = plt.subplots(figsize=(15, 10.5), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')

    # Color definitions
    c_psu_bg = '#FEF3C7'
    c_psu_border = '#D97706'
    c_psu_text = '#92400E'

    c_input_bg = '#EFF6FF'
    c_input_border = '#3B82F6'
    c_input_card = '#DBEAFE'
    c_input_text = '#1E3A8A'

    c_mcu_bg = '#0F172A'
    c_mcu_border = '#38BDF8'
    c_mcu_card = '#1E293B'
    c_mcu_text = '#F8FAFC'

    c_output_bg = '#F0FDF4'
    c_output_border = '#22C55E'
    c_output_card = '#DCFCE7'
    c_output_text = '#14532D'

    c_host_bg = '#FAF5FF'
    c_host_border = '#A855F7'
    c_host_card = '#F3E8FF'
    c_host_text = '#581C87'

    # Title Banner
    ax.text(8.0, 10.5, "SYSTEM BLOCK DIAGRAM: ESP32 EMBEDDED SMART ACCESS SYSTEM",
            ha='center', va='center', fontsize=16, fontweight='bold', color='#0F172A')
    ax.text(8.0, 10.15, "RFID Authentication | Camera Capture | ESP32 Core | LCD Display | Buzzer | UART Serial | Host Laptop",
            ha='center', va='center', fontsize=10.5, fontstyle='italic', color='#475569')

    # -------------------------------------------------------------
    # 1. POWER SUPPLY UNIT (TOP)
    # -------------------------------------------------------------
    psu_box = patches.FancyBboxPatch((2.2, 8.8), 11.6, 1.0,
                                     boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor=c_psu_bg, edgecolor=c_psu_border, linewidth=2.0)
    ax.add_patch(psu_box)
    ax.text(8.0, 9.4, "POWER SUPPLY UNIT (PSU)", ha='center', va='center',
            fontsize=12, fontweight='bold', color=c_psu_text)
    ax.text(8.0, 9.05, "Regulated 5V DC / 3.3V DC (2.0A Low-Ripple Power Rail + Common GND)",
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#78350F')

    # -------------------------------------------------------------
    # 2. INPUT SUBSYSTEM (LEFT)
    # -------------------------------------------------------------
    in_sub_box = patches.FancyBboxPatch((0.6, 3.8), 3.8, 4.6,
                                       boxstyle="round,pad=0.1,rounding_size=0.2",
                                       facecolor=c_input_bg, edgecolor=c_input_border, linewidth=1.8, linestyle='--')
    ax.add_patch(in_sub_box)
    ax.text(2.5, 8.1, "INPUT SUBSYSTEM", ha='center', va='center',
            fontsize=11, fontweight='bold', color=c_input_text)

    # RFID Card
    rfid_box = patches.FancyBboxPatch((0.85, 6.1), 3.3, 1.6,
                                     boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor=c_input_card, edgecolor='#2563EB', linewidth=1.8)
    ax.add_patch(rfid_box)
    ax.text(2.5, 7.2, "RFID READER", ha='center', va='center', fontsize=11, fontweight='bold', color='#1E40AF')
    ax.text(2.5, 6.85, "(RC522 / EM-18 Module)", ha='center', va='center', fontsize=9, color='#1E3A8A')
    ax.text(2.5, 6.45, "13.56 MHz / 125 kHz\nSPI / UART Interface\nContactless Card Sensing",
            ha='center', va='center', fontsize=8, color='#334155', multialignment='center')

    # Camera Module
    cam_box = patches.FancyBboxPatch((0.85, 4.1), 3.3, 1.6,
                                    boxstyle="round,pad=0.1,rounding_size=0.15",
                                    facecolor=c_input_card, edgecolor='#2563EB', linewidth=1.8)
    ax.add_patch(cam_box)
    ax.text(2.5, 5.2, "CAMERA MODULE", ha='center', va='center', fontsize=11, fontweight='bold', color='#1E40AF')
    ax.text(2.5, 4.85, "(OV2640 / ESP32-CAM)", ha='center', va='center', fontsize=9, color='#1E3A8A')
    ax.text(2.5, 4.45, "2-Megapixel UXGA CMOS\nHigh-Speed DVP / SCCB Bus\nInstant Portrait Capture",
            ha='center', va='center', fontsize=8, color='#334155', multialignment='center')

    # -------------------------------------------------------------
    # 3. CENTRAL PROCESSING UNIT: ESP32 (CENTER)
    # -------------------------------------------------------------
    mcu_sub_box = patches.FancyBboxPatch((5.1, 3.6), 5.8, 4.9,
                                        boxstyle="round,pad=0.1,rounding_size=0.25",
                                        facecolor=c_mcu_bg, edgecolor=c_mcu_border, linewidth=2.5)
    ax.add_patch(mcu_sub_box)
    ax.text(8.0, 8.15, "MAIN PROCESSING CONTROLLER", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#38BDF8')
    ax.text(8.0, 7.75, "ESP32 MICROCONTROLLER", ha='center', va='center',
            fontsize=14, fontweight='heavy', color='#FFFFFF')

    # Core specs inner panels
    core_p1 = patches.FancyBboxPatch((5.4, 6.4), 5.2, 1.0,
                                     boxstyle="round,pad=0.08,rounding_size=0.1",
                                     facecolor=c_mcu_card, edgecolor='#475569', linewidth=1.2)
    ax.add_patch(core_p1)
    ax.text(8.0, 7.0, "Dual-Core Xtensa 32-bit LX6 @ 240 MHz", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='#93C5FD')
    ax.text(8.0, 6.65, "520 KB SRAM | 4MB Flash | FreeRTOS Kernel", ha='center', va='center',
            fontsize=8.5, color='#CBD5E1')

    core_p2 = patches.FancyBboxPatch((5.4, 5.15), 5.2, 1.0,
                                     boxstyle="round,pad=0.08,rounding_size=0.1",
                                     facecolor=c_mcu_card, edgecolor='#475569', linewidth=1.2)
    ax.add_patch(core_p2)
    ax.text(8.0, 5.75, "Hardware Peripheral Interfaces", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='#38BDF8')
    ax.text(8.0, 5.4, "SPI (RFID) | I2C (LCD) | GPIO Matrix (Buzzer)\nDual Hardware UART (Serial Communication)",
            ha='center', va='center', fontsize=8.2, color='#CBD5E1', multialignment='center')

    core_p3 = patches.FancyBboxPatch((5.4, 3.9), 5.2, 1.0,
                                     boxstyle="round,pad=0.08,rounding_size=0.1",
                                     facecolor=c_mcu_card, edgecolor='#475569', linewidth=1.2)
    ax.add_patch(core_p3)
    ax.text(8.0, 4.5, "Integrated Wireless Engines", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='#A7F3D0')
    ax.text(8.0, 4.15, "802.11 b/g/n Wi-Fi & Bluetooth v4.2 BR/EDR / BLE", ha='center', va='center',
            fontsize=8.5, color='#CBD5E1')

    # -------------------------------------------------------------
    # 4. OUTPUT SUBSYSTEM (RIGHT)
    # -------------------------------------------------------------
    out_sub_box = patches.FancyBboxPatch((11.6, 3.8), 3.8, 4.6,
                                        boxstyle="round,pad=0.1,rounding_size=0.2",
                                        facecolor=c_output_bg, edgecolor=c_output_border, linewidth=1.8, linestyle='--')
    ax.add_patch(out_sub_box)
    ax.text(13.5, 8.1, "OUTPUT SUBSYSTEM", ha='center', va='center',
            fontsize=11, fontweight='bold', color=c_output_text)

    # LCD Display
    lcd_box = patches.FancyBboxPatch((11.85, 6.1), 3.3, 1.6,
                                    boxstyle="round,pad=0.1,rounding_size=0.15",
                                    facecolor=c_output_card, edgecolor='#16A34A', linewidth=1.8)
    ax.add_patch(lcd_box)
    ax.text(13.5, 7.2, "LCD DISPLAY", ha='center', va='center', fontsize=11, fontweight='bold', color='#166534')
    ax.text(13.5, 6.85, "(16x2 / 20x4 I2C LCD)", ha='center', va='center', fontsize=9, color='#14532D')
    ax.text(13.5, 6.45, "PCF8574 I2C Adapter\nAddress: 0x27 / 0x3F\nReal-Time Status & Prompts",
            ha='center', va='center', fontsize=8, color='#334155', multialignment='center')

    # Buzzer
    buzz_box = patches.FancyBboxPatch((11.85, 4.1), 3.3, 1.6,
                                     boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=1.8)
    ax.add_patch(buzz_box)
    ax.text(13.5, 5.2, "BUZZER UNIT", ha='center', va='center', fontsize=11, fontweight='bold', color='#991B1B')
    ax.text(13.5, 4.85, "(Active Piezo Sounder)", ha='center', va='center', fontsize=9, color='#7F1D1D')
    ax.text(13.5, 4.45, "5V Transistor Driver (2N2222)\nSingle Beep: Access Granted\nContinuous Alarm: Access Denied",
            ha='center', va='center', fontsize=8, color='#334155', multialignment='center')

    # -------------------------------------------------------------
    # 5. HOST / SUPERVISORY SYSTEM: LAPTOP (BOTTOM)
    # -------------------------------------------------------------
    host_box = patches.FancyBboxPatch((4.2, 0.4), 7.6, 2.2,
                                     boxstyle="round,pad=0.1,rounding_size=0.2",
                                     facecolor=c_host_bg, edgecolor=c_host_border, linewidth=2.2)
    ax.add_patch(host_box)
    ax.text(8.0, 2.25, "HOST SUPERVISORY SYSTEM: LAPTOP / PC", ha='center', va='center',
            fontsize=12, fontweight='bold', color=c_host_text)

    host_inner = patches.FancyBboxPatch((4.5, 0.65), 7.0, 1.35,
                                        boxstyle="round,pad=0.08,rounding_size=0.12",
                                        facecolor=c_host_card, edgecolor='#C084FC', linewidth=1.2)
    ax.add_patch(host_inner)
    ax.text(8.0, 1.65, "Host Processing Application (Python / OpenCV)", ha='center', va='center',
            fontsize=10, fontweight='bold', color='#581C87')
    ax.text(8.0, 1.3, "• Face Recognition & Biometric Matching  • SQLite Attendance & Security DB",
            ha='center', va='center', fontsize=8.5, color='#4C1D95')
    ax.text(8.0, 0.95, "• Real-Time Monitoring GUI Dashboard  • Cloud / Web Synchronization",
            ha='center', va='center', fontsize=8.5, color='#4C1D95')

    # -------------------------------------------------------------
    # POWER SUPPLY ARROWS (DOTTED ORANGE)
    # -------------------------------------------------------------
    # Down to ESP32
    ax.annotate("", xy=(8.0, 8.5), xytext=(8.0, 8.8),
                arrowprops=dict(arrowstyle="-|>", color='#D97706', lw=2.2, linestyle=':'))
    ax.text(8.25, 8.65, "5V / 3.3V", fontsize=8, fontweight='bold', color='#B45309')

    # To RFID
    ax.annotate("", xy=(2.5, 7.7), xytext=(3.5, 8.8),
                arrowprops=dict(arrowstyle="-|>", color='#D97706', lw=2.0, linestyle=':'))
    ax.text(2.6, 8.25, "3.3V DC", fontsize=7.5, fontweight='bold', color='#B45309')

    # To Camera
    ax.annotate("", xy=(1.0, 5.7), xytext=(2.3, 8.8),
                arrowprops=dict(arrowstyle="-|>", color='#D97706', lw=1.8, linestyle=':'))
    ax.text(1.2, 7.0, "3.3V DC", fontsize=7.5, fontweight='bold', color='#B45309')

    # To LCD
    ax.annotate("", xy=(13.5, 7.7), xytext=(12.5, 8.8),
                arrowprops=dict(arrowstyle="-|>", color='#D97706', lw=2.0, linestyle=':'))
    ax.text(12.7, 8.25, "5V DC", fontsize=7.5, fontweight='bold', color='#B45309')

    # To Buzzer
    ax.annotate("", xy=(15.0, 5.7), xytext=(13.7, 8.8),
                arrowprops=dict(arrowstyle="-|>", color='#D97706', lw=1.8, linestyle=':'))
    ax.text(14.2, 7.0, "5V DC", fontsize=7.5, fontweight='bold', color='#B45309')

    # -------------------------------------------------------------
    # DATA INTERCONNECT ARROWS
    # -------------------------------------------------------------
    # 1. RFID -> ESP32
    ax.annotate("", xy=(5.1, 6.9), xytext=(4.15, 6.9),
                arrowprops=dict(arrowstyle="->", color='#2563EB', lw=2.5))
    ax.text(4.62, 7.2, "Card UID\n(SPI / UART)", ha='center', va='center',
            fontsize=8, fontweight='bold', color='#1D4ED8')

    # 2. Camera -> ESP32
    ax.annotate("", xy=(5.1, 4.9), xytext=(4.15, 4.9),
                arrowprops=dict(arrowstyle="->", color='#2563EB', lw=2.5))
    ax.text(4.62, 5.2, "Image Frame\n(DVP / SCCB)", ha='center', va='center',
            fontsize=8, fontweight='bold', color='#1D4ED8')

    # 3. ESP32 -> LCD
    ax.annotate("", xy=(11.85, 6.9), xytext=(10.9, 6.9),
                arrowprops=dict(arrowstyle="->", color='#16A34A', lw=2.5))
    ax.text(11.37, 7.2, "Status Data\n(I2C: SDA/SCL)", ha='center', va='center',
            fontsize=8, fontweight='bold', color='#15803D')

    # 4. ESP32 -> Buzzer
    ax.annotate("", xy=(11.85, 4.9), xytext=(10.9, 4.9),
                arrowprops=dict(arrowstyle="->", color='#DC2626', lw=2.5))
    ax.text(11.37, 5.2, "Alert Trigger\n(GPIO Output)", ha='center', va='center',
            fontsize=8, fontweight='bold', color='#B91C1C')

    # 5. BIDIRECTIONAL UART BETWEEN ESP32 AND LAPTOP
    # ESP32 TX -> Laptop RX (Left Line)
    ax.annotate("", xy=(6.8, 2.6), xytext=(6.8, 3.6),
                arrowprops=dict(arrowstyle="->", color='#7C3AED', lw=3.0))
    ax.text(6.1, 3.1, "UART Tx (ESP32)\n---> UART Rx (Laptop)\n[Card UID / Trigger]",
            ha='center', va='center', fontsize=8, fontweight='bold', color='#6D28D9')

    # Laptop TX -> ESP32 RX (Right Line)
    ax.annotate("", xy=(9.2, 3.6), xytext=(9.2, 2.6),
                arrowprops=dict(arrowstyle="->", color='#9333EA', lw=3.0))
    ax.text(9.9, 3.1, "UART Tx (Laptop)\n---> UART Rx (ESP32)\n[Auth Status / Grant]",
            ha='center', va='center', fontsize=8, fontweight='bold', color='#7E22CE')

    # Legend at very bottom
    legend_text = (
        "Legend:  [Blue] Input Signals   |   [Green/Red] Output Control Signals   |   "
        "[Purple] Bidirectional UART Serial Bus   |   [Amber Dotted] Regulated DC Power Rails"
    )
    ax.text(8.0, 0.15, legend_text, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='#334155')

    plt.tight_layout()
    plt.savefig(DIAGRAM_IMG_PATH, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"[OK] Diagram successfully saved to: {DIAGRAM_IMG_PATH}")


# ==============================================================================
# PART 2: GENERATE MICROSOFT WORD (.DOCX) DOCUMENT
# ==============================================================================
def set_cell_background(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
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

def create_callout_box(doc, text, title="NOTE:", hex_bg="F8FAFC", hex_border="2563EB"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, hex_bg)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="36" w:space="0" w:color="{hex_border}"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    cell._tc.get_or_add_tcPr().append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    r_title = p.add_run(f"{title} ")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    
    r_text = p.add_run(text)
    r_text.font.name = "Arial"
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = RGBColor(51, 65, 85)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_custom_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Arial"
    
    if level == 1:
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(15, 23, 42)
        pBdr = parse_xml(
            f'<w:pBdr {nsdecls("w")}>'
            f'<w:bottom w:val="single" w:sz="12" w:space="4" w:color="CBD5E1"/>'
            f'</w:pBdr>'
        )
        p._p.get_or_add_pPr().append(pBdr)
    elif level == 2:
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        run.font.size = Pt(12.5)
        run.font.color.rgb = RGBColor(37, 99, 235)
    elif level == 3:
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_styled_paragraph(doc, text, space_after=6, italic=False, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(51, 65, 85)
    run.italic = italic
    run.bold = bold
    return p

def add_bullet_point(doc, lead_in, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    
    r_lead = p.add_run(lead_in + ": ")
    r_lead.bold = True
    r_lead.font.name = "Arial"
    r_lead.font.size = Pt(10)
    r_lead.font.color.rgb = RGBColor(15, 23, 42)
    
    r_text = p.add_run(text)
    r_text.font.name = "Arial"
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = RGBColor(51, 65, 85)
    return p


def generate_word_document():
    print("[2/2] Generating comprehensive Word (.docx) document...")
    doc = Document()
    
    # Page Setup (Standard Letter, 0.75-inch margins)
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # -------------------------------------------------------------
    # DOCUMENT HEADER / BANNER TABLE
    # -------------------------------------------------------------
    header_tbl = doc.add_table(rows=1, cols=1)
    header_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_tbl.autofit = False
    
    h_cell = header_tbl.cell(0, 0)
    h_cell.width = Inches(7.0)
    set_cell_background(h_cell, "0F172A")
    set_cell_margins(h_cell, top=200, bottom=200, left=240, right=240)
    
    hp = h_cell.paragraphs[0]
    hp.paragraph_format.space_before = Pt(4)
    hp.paragraph_format.space_after = Pt(2)
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hrun1 = hp.add_run("SYSTEM HARDWARE SPECIFICATION & BLOCK DIAGRAM\n")
    hrun1.bold = True
    hrun1.font.name = "Arial"
    hrun1.font.size = Pt(16)
    hrun1.font.color.rgb = RGBColor(255, 255, 255)
    
    hrun2 = hp.add_run("ESP32-Based Smart Multi-Sensor Access Control & Surveillance Terminal\n")
    hrun2.font.name = "Arial"
    hrun2.font.size = Pt(11)
    hrun2.font.color.rgb = RGBColor(56, 189, 248)
    
    hrun3 = hp.add_run("Subsystems: ESP32 MCU | RFID Reader | Camera | LCD | Buzzer | UART Serial | Laptop Host | PSU")
    hrun3.font.name = "Arial"
    hrun3.font.size = Pt(9)
    hrun3.italic = True
    hrun3.font.color.rgb = RGBColor(203, 213, 225)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Metadata Strip
    meta_p = doc.add_paragraph()
    meta_p.paragraph_format.space_after = Pt(12)
    meta_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    mr1 = meta_p.add_run("Document Version: 1.0  |  Status: Engineering Verified  |  Target MCU: ESP32 Tensilica Xtensa")
    mr1.font.name = "Arial"
    mr1.font.size = Pt(8.5)
    mr1.font.color.rgb = RGBColor(100, 116, 139)

    # -------------------------------------------------------------
    # SECTION 1: EXECUTIVE OVERVIEW
    # -------------------------------------------------------------
    add_custom_heading(doc, "1. Executive Overview & System Architecture", level=1)
    
    add_styled_paragraph(
        doc,
        "This engineering report outlines the complete hardware architecture and system block diagram for an "
        "advanced multi-sensor authentication and surveillance terminal powered by the ESP32 microcontroller. "
        "The system fuses contactless Radio Frequency Identification (RFID) card scanning with optical camera capture "
        "to establish a dual-factor biometric access verification platform. Real-time visual feedback is rendered on "
        "an alphanumeric LCD display, acoustic signaling is driven via an active buzzer, and full-duplex UART serial "
        "telemetry connects the edge node directly to a supervisory Host Laptop workstation for database logging and "
        "facial recognition processing."
    )

    create_callout_box(
        doc,
        "All hardware modules interface seamlessly through synchronized peripheral buses (SPI, I2C, UART, and GPIO). "
        "A centralized Power Supply Unit (PSU) distributes regulated 5V and 3.3V DC rails with a common ground reference "
        "to eliminate ground loops and guarantee transient stability during RF and camera operations.",
        title="CORE ARCHITECTURE PRINCIPLE:",
        hex_bg="F0F9FF",
        hex_border="0EA5E9"
    )

    # -------------------------------------------------------------
    # SECTION 2: SYSTEM BLOCK DIAGRAM (HIGH-RES IMAGE)
    # -------------------------------------------------------------
    add_custom_heading(doc, "2. High-Resolution System Block Diagram", level=1)
    
    add_styled_paragraph(
        doc,
        "Figure 1 provides the complete schematic block diagram of the system. The central ESP32 Microcontroller "
        "coordinates input ingestion from the RFID Reader and Camera Module, drives the Output Section (LCD & Buzzer), "
        "receives steady DC power from the Power Supply Unit, and exchanges bidirectional serial frames with the Host Laptop."
    )

    # Embed Image
    if os.path.exists(DIAGRAM_IMG_PATH):
        img_p = doc.add_paragraph()
        img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_p.paragraph_format.space_before = Pt(8)
        img_p.paragraph_format.space_after = Pt(4)
        run_img = img_p.add_run()
        run_img.add_picture(DIAGRAM_IMG_PATH, width=Inches(6.8))

        # Caption
        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_p.paragraph_format.space_after = Pt(14)
        r_cap = cap_p.add_run("Figure 1: Full System Block Diagram of the ESP32-Based Multi-Sensor Access Node.")
        r_cap.font.name = "Arial"
        r_cap.font.size = Pt(9)
        r_cap.bold = True
        r_cap.font.color.rgb = RGBColor(100, 116, 139)
    else:
        add_styled_paragraph(doc, "[Warning: Diagram image could not be loaded]", italic=True)

    # -------------------------------------------------------------
    # SECTION 3: SUBSYSTEM FUNCTIONAL SPECIFICATIONS
    # -------------------------------------------------------------
    add_custom_heading(doc, "3. Subsystem Functional Breakdown", level=1)

    # 3.1 Controller
    add_custom_heading(doc, "3.1 Central Controller: ESP32 Microcontroller", level=2)
    add_styled_paragraph(
        doc,
        "The ESP32 SoC serves as the master intelligence of the node. Key specifications and duties include:"
    )
    add_bullet_point(doc, "Compute Engine", "Xtensa Dual-Core 32-bit LX6 microprocessor operating at up to 240 MHz (delivering up to 600 DMIPS).")
    add_bullet_point(doc, "Memory Subsystem", "520 KB internal SRAM, 448 KB ROM, and an external 4MB SPI Flash memory partition for firmware and buffer storage.")
    add_bullet_point(doc, "Peripheral Multiplexing", "Dedicated hardware controllers for SPI (RFID interface), I2C (LCD interface), dual UART ports, and general-purpose I/O matrix.")
    add_bullet_point(doc, "Dual-Core Task Separation", "Core 0 is dedicated to high-speed UART serial buffering and camera DMA transfers, while Core 1 executes FreeRTOS tasks for RFID polling, LCD refreshes, and buzzer sequencing.")

    # 3.2 Input Subsystem
    add_custom_heading(doc, "3.2 Input Subsystem: RFID Reader & Camera Module", level=2)
    add_styled_paragraph(
        doc,
        "The input stage is responsible for capturing physical authentication tokens and visual evidence from visitors:"
    )
    add_bullet_point(
        doc,
        "RFID Reader (MFRC522 / EM-18)",
        "Interrogates passive RFID transponders/smart cards. Operating at 13.56 MHz (ISO 14443A) via SPI bus (or 125 kHz via UART), "
        "it reads unique 4-byte or 7-byte Card UIDs instantaneously upon card proximity (within 3 - 5 cm)."
    )
    add_bullet_point(
        doc,
        "Camera Module (OmniVision OV2640 / ESP32-CAM)",
        "A 2.0-megapixel CMOS sensor connected via an 8-bit parallel Digital Video Port (DVP) and I2C-compatible SCCB control bus. "
        "Upon an RFID interrupt, the camera immediately exposes and captures an image frame (JPEG format, 640x480 VGA or 800x600 SVGA) "
        "for security auditing."
    )

    # 3.3 Output Subsystem
    add_custom_heading(doc, "3.3 Output Subsystem: LCD Display & Buzzer", level=2)
    add_styled_paragraph(
        doc,
        "The output stage communicates real-time machine state and verification feedback to the end user:"
    )
    add_bullet_point(
        doc,
        "LCD Display (16x2 / 20x4 Alphanumeric with PCF8574 I2C Adapter)",
        "Displays 2 lines of 16 characters with LED backlighting. Utilizes an I2C backpack (PCF8574 IO expander at default address 0x27 or 0x3F), "
        "reducing micro-controller pin requirements to just 2 lines (SDA and SCL) while displaying dynamic prompts such as 'Scan ID Card', "
        "'Access Granted: Welcome', or 'Unauthorized Access'."
    )
    add_bullet_point(
        doc,
        "Active Piezo Buzzer",
        "Driven from an ESP32 GPIO pin through a 2N2222 NPN switching transistor with a flyback protection diode. "
        "Provides unambiguous acoustic cues: a single short chirp (100 ms) indicates card read success, a double tone indicates host verification, "
        "and a pulsating continuous alarm (3 seconds) alerts security to unauthorized attempts."
    )

    # 3.4 Host Laptop Workstation
    add_custom_heading(doc, "3.4 Host Supervisory Station: Laptop / PC via UART", level=2)
    add_styled_paragraph(
        doc,
        "The laptop operates as the central management workstation and high-performance biometric compute engine. "
        "It interfaces with the ESP32 via a bidirectional hardware UART link (typically bridged over USB using an on-board "
        "CP2102 or CH340 serial-to-USB converter IC) configured at a baud rate of 115,200 bps (8-N-1)."
    )
    add_bullet_point(
        doc,
        "ESP32 UART TX -> Laptop UART RX",
        "Transmits scanned RFID Card UID strings, status heartbeats, and captured image payloads from edge to host."
    )
    add_bullet_point(
        doc,
        "Laptop UART TX -> ESP32 UART RX",
        "Returns server-side database validation outcomes, authorized personnel names, door lock trigger codes, and supervisory commands back to the ESP32."
    )
    add_bullet_point(
        doc,
        "Host Software Stack",
        "Python runtime utilizing PySerial for hardware stream handling, OpenCV for automated facial feature matching against registered "
        "cardholder portraits, SQLite/MySQL for persistent audit logging, and a Tkinter/Web GUI for administrative oversight."
    )

    # 3.5 Power Supply Unit
    add_custom_heading(doc, "3.5 Power Supply Unit (PSU) & Power Distribution", level=2)
    add_styled_paragraph(
        doc,
        "Stable electrical power is essential to avoid brownouts during Wi-Fi transmission bursts and camera image sensor reads. "
        "The Power Supply Unit features an AC-to-DC switch-mode power converter (SMPS) delivering a regulated 5V DC at 2.0A minimum. "
        "High-current 5V rails feed the ESP32 VIN pin, LCD backlight, and Buzzer driver, while a low-dropout linear regulator (AMS1117-3.3) "
        "supplies clean 3.3V DC to the sensitive RFID radio receiver and CMOS camera core. All components share a common zero-volt ground (GND) plane."
    )

    # -------------------------------------------------------------
    # SECTION 4: PINOUT & INTERFACING TABLE
    # -------------------------------------------------------------
    add_custom_heading(doc, "4. Hardware Interfacing & Pin Mapping Matrix", level=1)
    
    add_styled_paragraph(
        doc,
        "Table 1 details the exact hardware interconnectivity, communication protocols, physical GPIO assignments on the ESP32, "
        "and operating logic voltages for all components in the block diagram."
    )

    # Table Generation
    table_data = [
        ("Subsystem Block", "Component Name", "Bus / Protocol", "ESP32 Pin Connection", "Voltage", "Functional Description"),
        ("Controller", "ESP32 MCU", "Internal Core", "VCC, GND, EN, Boot", "5V / 3.3V", "Master processing and peripheral coordination"),
        ("Input", "RFID Reader (RC522)", "SPI Bus (MOSI)", "GPIO 23", "3.3V", "Master-Out-Slave-In data line"),
        ("Input", "RFID Reader (RC522)", "SPI Bus (MISO)", "GPIO 19", "3.3V", "Master-In-Slave-Out card UID stream"),
        ("Input", "RFID Reader (RC522)", "SPI Bus (SCK)", "GPIO 18", "3.3V", "SPI Synchronous Serial Clock"),
        ("Input", "RFID Reader (RC522)", "SPI Bus (SDA / CS)", "GPIO 5", "3.3V", "Chip Select / Slave Enable line"),
        ("Input", "RFID Reader (RC522)", "Hardware Reset", "GPIO 22", "3.3V", "Module hardware power-on reset line"),
        ("Input", "Camera (OV2640)", "DVP 8-bit Parallel", "GPIO 35, 34, 39, 36, etc.", "3.3V", "High-speed DMA pixel stream from sensor"),
        ("Input", "Camera (OV2640)", "SCCB (I2C-compatible)", "GPIO 26 (SDA), GPIO 27 (SCL)", "3.3V", "Camera sensor register configuration"),
        ("Output", "LCD 16x2 Display", "I2C Bus (SDA)", "GPIO 21 (Data)", "5V / 3.3V", "PCF8574 I2C Serial Data line"),
        ("Output", "LCD 16x2 Display", "I2C Bus (SCL)", "GPIO 22 (Clock)", "5V / 3.3V", "PCF8574 I2C Serial Clock line"),
        ("Output", "Active Buzzer", "Digital Output (GPIO)", "GPIO 4 (via NPN 2N2222)", "5V", "Acoustic beep / alarm activation signal"),
        ("Host Link", "UART Serial (TX)", "Asynchronous Serial", "GPIO 1 (ESP32 U0TXD)", "3.3V / USB", "ESP32 transmits card UID to Laptop RX"),
        ("Host Link", "UART Serial (RX)", "Asynchronous Serial", "GPIO 3 (ESP32 U0RXD)", "3.3V / USB", "ESP32 receives verification from Laptop TX"),
        ("Power", "Power Supply Unit", "DC Power Bus", "VIN, 3V3, GND", "5V / 3.3V", "Regulated 2A power rail with common ground reference")
    ]

    pin_tbl = doc.add_table(rows=len(table_data), cols=6)
    pin_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    pin_tbl.autofit = False

    col_widths = [Inches(1.0), Inches(1.3), Inches(1.1), Inches(1.2), Inches(0.7), Inches(1.7)]

    for row_idx, row in enumerate(pin_tbl.rows):
        is_header = (row_idx == 0)
        # Prevent row split across pages
        tr_pr = row._tr.get_or_add_trPr()
        tr_pr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        for col_idx, cell in enumerate(row.cells):
            cell.width = col_widths[col_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05
            
            val = table_data[row_idx][col_idx]
            
            if is_header:
                set_cell_background(cell, "0F172A")
                run = p.add_run(val)
                run.bold = True
                run.font.name = "Arial"
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                bg = "F1F5F9" if (row_idx % 2 == 1) else "FFFFFF"
                set_cell_background(cell, bg)
                run = p.add_run(val)
                run.font.name = "Arial"
                run.font.size = Pt(8.0)
                run.font.color.rgb = RGBColor(51, 65, 85)
                if col_idx in [0, 3]:
                    run.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------
    # SECTION 5: STEP-BY-STEP OPERATIONAL DATA FLOW
    # -------------------------------------------------------------
    add_custom_heading(doc, "5. System Operational & Signal Flow Sequence", level=1)
    
    add_styled_paragraph(
        doc,
        "The interaction among the hardware blocks follows a strictly coordinated, deterministic state machine:"
    )

    steps = [
        ("Step 1: Power-On Initialization", "The Power Supply Unit stabilizes at 5V and 3.3V. The ESP32 boots FreeRTOS, configures the SPI bus for RC522, initializes the I2C bus for the LCD, establishes 115,200 baud UART connection to the laptop, and puts the camera in low-power standby. The LCD displays 'SYSTEM READY / SCAN CARD'."),
        ("Step 2: RFID Proximity Detection", "When an authorized card or fob enters the 13.56 MHz RF field of the RFID reader, an antenna resonance shift is detected. The reader extracts the factory-programmed 32-bit/56-bit UID and asserts an interrupt to the ESP32 over SPI. The ESP32 triggers a brief 50ms confirmation chirp on the buzzer."),
        ("Step 3: Camera Trigger & Frame Capture", "Concurrently with RFID acquisition, the ESP32 wakes the OV2640 camera sensor over the SCCB bus. An exposure command is issued and a single compressed JPEG frame is clocked into the ESP32's DMA buffer within 120 milliseconds."),
        ("Step 4: UART Serial Transmission (ESP32 TX -> Laptop RX)", "The ESP32 constructs a structured binary/ASCII packet: [HEADER | CARD_UID | TIMESTAMP | CHECKSUM]. It transmits the payload through UART0 TX (Pin 1) directly to the Laptop's USB-UART bridge at 115,200 baud."),
        ("Step 5: Host Biometric & Database Verification", "The Laptop receives the packet on UART RX. A background Python daemon extracts the UID, queries the central SQLite/MySQL database for user credentials, and if registered, compares the captured camera portrait against stored facial embeddings using OpenCV and facial landmark matching."),
        ("Step 6: Command Transmission (Laptop TX -> ESP32 RX)", "The Laptop computes the authorization result: 'ACCESS_GRANTED [User Name]' or 'ACCESS_DENIED [Reason Code]'. It sends the formatted response string through UART TX into the ESP32's UART RX (Pin 3)."),
        ("Step 7: Local Actuation & Visual Feedback", "Upon receiving the verification packet, the ESP32 parses the payload: If Granted, the LCD prints 'WELCOME [NAME]' and the buzzer emits a pleasant double-beep; If Denied, the LCD flashes 'ACCESS DENIED' and the buzzer sounds a rapid 3-second security alarm tone.")
    ]

    for lead, desc in steps:
        add_bullet_point(doc, lead, desc)

    # -------------------------------------------------------------
    # SECTION 6: POWER BUDGET & ELECTRICAL SPECIFICATIONS
    # -------------------------------------------------------------
    add_custom_heading(doc, "6. Power Budget & Electrical Analysis", level=1)

    add_styled_paragraph(
        doc,
        "A rigorous power budget is required to size the Power Supply Unit appropriately. Table 2 provides the nominal "
        "and peak current consumption of each block in the circuit."
    )

    pwr_data = [
        ("Hardware Block", "Operating Voltage", "Quiescent / Idle Current", "Peak / Active Current", "Power Consumption (Peak)"),
        ("ESP32 SoC (Dual Core)", "3.3V DC (Internal LDO)", "40 mA", "240 mA (Wi-Fi/Radio Burst)", "792 mW"),
        ("RFID Reader (RC522)", "3.3V DC", "13 mA", "26 mA (Active RF Transmit)", "85.8 mW"),
        ("Camera Module (OV2640)", "3.3V DC", "15 mA (Standby)", "140 mA (Active Capture/DMA)", "462 mW"),
        ("LCD Display (16x2 + I2C)", "5.0V DC", "4 mA (Backlight Off)", "25 mA (Backlight On)", "125 mW"),
        ("Active Buzzer Unit", "5.0V DC", "0 mA", "35 mA (Sounding)", "175 mW"),
        ("Total Node Demand", "5.0V DC Input", "~72 mA (Idle)", "~466 mA (Peak In-Rush)", "~1,639.8 mW (~1.64 W)")
    ]

    pwr_tbl = doc.add_table(rows=len(pwr_data), cols=5)
    pwr_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    pwr_tbl.autofit = False
    pwr_col_widths = [Inches(1.8), Inches(1.1), Inches(1.4), Inches(1.4), Inches(1.3)]

    for row_idx, row in enumerate(pwr_tbl.rows):
        is_header = (row_idx == 0)
        is_total = (row_idx == len(pwr_data) - 1)
        
        tr_pr = row._tr.get_or_add_trPr()
        tr_pr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        for col_idx, cell in enumerate(row.cells):
            cell.width = pwr_col_widths[col_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            val = pwr_data[row_idx][col_idx]
            
            if is_header:
                set_cell_background(cell, "0F172A")
                run = p.add_run(val)
                run.bold = True
                run.font.name = "Arial"
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
            elif is_total:
                set_cell_background(cell, "FEF3C7")
                run = p.add_run(val)
                run.bold = True
                run.font.name = "Arial"
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(146, 64, 14)
            else:
                bg = "F8FAFC" if (row_idx % 2 == 1) else "FFFFFF"
                set_cell_background(cell, bg)
                run = p.add_run(val)
                run.font.name = "Arial"
                run.font.size = Pt(8.0)
                run.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    create_callout_box(
        doc,
        "Because simultaneous activation of the Camera, ESP32 processing core, and RF field can cause inductive voltage dips, "
        "the Power Supply Unit must be rated for at least 5V / 2.0A (10W capability). A bulk electrolytic decoupling capacitor "
        "(100uF, 16V) alongside a 0.1uF ceramic decoupling capacitor must be placed directly across the ESP32 5V and GND rail.",
        title="HARDWARE STABILITY RECOMMENDATION:",
        hex_bg="FEF2F2",
        hex_border="DC2626"
    )

    # -------------------------------------------------------------
    # SECTION 7: SUMMARY & CONCLUSION
    # -------------------------------------------------------------
    add_custom_heading(doc, "7. Summary & Project Deliverables", level=1)
    
    add_styled_paragraph(
        doc,
        "This document completely defines the structural, electrical, and data communication interfaces of the ESP32-based "
        "hardware project. With dedicated inputs (RFID & Camera), clear outputs (LCD & Buzzer), high-throughput UART serial "
        "telemetry with the Host Laptop, and an isolated Power Supply Unit, the system forms a robust, production-ready "
        "edge IoT security platform suitable for modern access control, attendance management, and smart premises monitoring."
    )

    # Footer note
    doc.add_paragraph().paragraph_format.space_after = Pt(16)
    foot_p = doc.add_paragraph()
    foot_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = foot_p.add_run("--- End of Hardware Block Diagram & Engineering Specification ---")
    fr.font.name = "Arial"
    fr.font.size = Pt(8.5)
    fr.font.color.rgb = RGBColor(148, 163, 184)
    fr.italic = True

    # Save
    doc.save(DOCX_OUTPUT_PATH)
    print(f"[OK] Word document successfully generated at: {DOCX_OUTPUT_PATH}")


if __name__ == "__main__":
    generate_block_diagram_image()
    generate_word_document()

