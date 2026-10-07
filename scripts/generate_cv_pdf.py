"""Genera una hoja de vida de una página, legible y compatible con ATS."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, ListFlowable, ListItem, Paragraph, SimpleDocTemplate


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = BASE_DIR / "assets" / "Juan-Sebastian-Rubiano-CV.pdf"

PORTFOLIO_URL = "https://zhulgon.github.io/"
LINKEDIN_URL = "https://www.linkedin.com/in/juansrubiano"
GITHUB_URL = "https://github.com/Zhulgon"
EMAIL = "jsebastian000124@gmail.com"

PALETTE = {
    "ink": colors.HexColor("#20231F"),
    "muted": colors.HexColor("#5E655D"),
    "line": colors.HexColor("#D8DCD5"),
    "accent": colors.HexColor("#35665D"),
}


def register_fonts():
    """Use embedded system fonts for reliable Spanish characters and clean rendering."""
    font_dir = Path("C:/Windows/Fonts")
    regular = font_dir / "calibri.ttf"
    bold = font_dir / "calibrib.ttf"

    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("CV-Regular", str(regular)))
        pdfmetrics.registerFont(TTFont("CV-Bold", str(bold)))
        return "CV-Regular", "CV-Bold"

    return "Helvetica", "Helvetica-Bold"


def build_styles():
    regular, bold = register_fonts()
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="Name",
            parent=styles["Heading1"],
            fontName=bold,
            fontSize=24.5,
            leading=26.5,
            textColor=PALETTE["ink"],
            spaceAfter=2.5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Role",
            parent=styles["Normal"],
            fontName=bold,
            fontSize=10.7,
            leading=13.6,
            textColor=PALETTE["accent"],
            spaceAfter=6.5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Contact",
            parent=styles["Normal"],
            fontName=regular,
            fontSize=8.65,
            leading=11.2,
            textColor=PALETTE["muted"],
            spaceAfter=9.5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            fontName=bold,
            fontSize=9.9,
            leading=12.1,
            textColor=PALETTE["accent"],
            spaceBefore=10,
            spaceAfter=4.2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["Normal"],
            fontName=regular,
            fontSize=9.2,
            leading=13.45,
            textColor=PALETTE["ink"],
            spaceAfter=4.3,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Project",
            parent=styles["Normal"],
            fontName=bold,
            fontSize=9.45,
            leading=11.9,
            textColor=PALETTE["ink"],
            spaceAfter=1.5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Meta",
            parent=styles["Normal"],
            fontName=bold,
            fontSize=7.85,
            leading=9.45,
            textColor=PALETTE["accent"],
            spaceAfter=1.05,
        )
    )

    return styles


def section(title, styles):
    return [
        Paragraph(title.upper(), styles["Section"]),
        HRFlowable(
            width="100%",
            thickness=0.45,
            color=PALETTE["line"],
            spaceBefore=0,
            spaceAfter=5.2,
        ),
    ]


def bullet_list(items, styles):
    return ListFlowable(
        [ListItem(Paragraph(item, styles["Body"]), leftIndent=8) for item in items],
        bulletType="bullet",
        leftIndent=10,
        bulletFontName="Helvetica",
        bulletFontSize=6.8,
        bulletColor=PALETTE["accent"],
        spaceBefore=0,
        spaceAfter=1.5,
    )


def contact_line(styles):
    text = (
        "Bucaramanga, Colombia | "
        f"<link href='mailto:{EMAIL}' color='{PALETTE['ink']}'>{EMAIL}</link> | "
        f"<link href='{LINKEDIN_URL}' color='{PALETTE['ink']}'>LinkedIn</link> | "
        f"<link href='{GITHUB_URL}' color='{PALETTE['ink']}'>GitHub</link> | "
        f"<link href='{PORTFOLIO_URL}' color='{PALETTE['ink']}'>Portafolio</link>"
    )
    return Paragraph(text, styles["Contact"])


def project_block(meta, title, description, styles):
    return [
        Paragraph(meta, styles["Meta"]),
        Paragraph(title, styles["Project"]),
        Paragraph(description, styles["Body"]),
    ]


def build_story():
    styles = build_styles()
    story = [
        Paragraph("Juan Sebastián Rubiano", styles["Name"]),
        Paragraph(
            "Tecnólogo en Desarrollo de Sistemas Informáticos | Proyecto de grado en curso",
            styles["Role"],
        ),
        contact_line(styles),
    ]

    story.extend(section("Perfil", styles))
    story.append(
        Paragraph(
            "Tecnólogo en Desarrollo de Sistemas Informáticos con materias de Ingeniería de Sistemas finalizadas "
            "y proyecto de grado en curso. Tengo experiencia en la operación y atención al cliente de una óptica, "
            "donde identifiqué necesidades de información y diseñé soluciones digitales. Busco un rol de entrada "
            "en implementación, análisis de datos o software, aportando criterio operativo, comunicación y aprendizaje rápido.",
            styles["Body"],
        )
    )

    story.extend(section("Competencias", styles))
    story.append(
        Paragraph(
            "<b>Datos y analítica:</b> Python, SQL, Excel, Tableau, Power BI, estadística descriptiva, dashboards, "
            "limpieza y análisis exploratorio de datos.<br/>"
            "<b>Software:</b> TypeScript, React, Node.js, NestJS, PostgreSQL, APIs REST, Git/GitHub y Docker.",
            styles["Body"],
        )
    )

    story.extend(section("Experiencia aplicada", styles))
    story.append(Paragraph("Operación y atención al cliente - Óptica - 2 años", styles["Project"]))
    story.append(
        bullet_list(
            [
                "Participé en la gestión comercial y atención al cliente, con seguimiento de inventario, ventas, agenda e indicadores.",
                "Identifiqué información dispersa entre Excel, Word, PDF y notas, y diseñé Óptica Suite para centralizar procesos y facilitar su consulta.",
                "Analicé ventas e indicadores para entender necesidades operativas y apoyar decisiones del negocio.",
            ],
            styles,
        )
    )

    story.extend(section("Proyectos seleccionados", styles))
    story.extend(
        project_block(
            "SOFTWARE Y PROCESOS OPERATIVOS",
            "Óptica Suite",
            "Proyecto de software para organizar inventario, ventas, agenda y reportes de una óptica. Utiliza PostgreSQL y APIs para estructurar información de la operación.",
            styles,
        )
    )
    story.extend(
        project_block(
            "ANALÍTICA Y VISUALIZACIÓN",
            "Dashboard de recursos humanos en Tableau",
            "Dashboard que presenta datos de empleados en indicadores de plantilla, rotación, contrataciones y distribución por áreas.",
            styles,
        )
    )

    story.append(
        Paragraph(
            "<b>Otros proyectos:</b> estadística aplicada a cojinetes, aplicación de finanzas y hábitos, "
            "ejercicios de machine learning y catálogo de monturas con realidad aumentada.",
            styles["Body"],
        )
    )

    story.extend(section("Formación y certificaciones", styles))
    story.append(
        Paragraph(
            "<b>Universitaria Tecnológica de Santander (UTS):</b> Tecnólogo en Desarrollo de Sistemas Informáticos. "
            "Ingeniería de Sistemas: materias finalizadas; proyecto de grado en curso.<br/>"
            "<b>Certificaciones destacadas:</b> Google Data Analytics, Google Advanced Data Analytics, PCAP Python, "
            "EF SET English Certificate C1 e IBM en IA, ciberseguridad y tecnologías emergentes.",
            styles["Body"],
        )
    )

    story.extend(section("Interés profesional", styles))
    story.append(
        Paragraph(
            "Roles junior o trainee en implementación de soluciones, análisis de datos y desarrollo de software. "
            "Experiencia en atención al cliente, identificación de necesidades y comunicación con usuarios.",
            styles["Body"],
        )
    )

    return story


def draw_page(canvas, doc):
    canvas.saveState()
    width, height = A4

    canvas.setFillColor(PALETTE["accent"])
    canvas.rect(doc.leftMargin, height - 0.72 * cm, doc.width, 0.06 * cm, stroke=0, fill=1)

    canvas.setStrokeColor(PALETTE["line"])
    canvas.setLineWidth(0.4)
    canvas.line(doc.leftMargin, 0.95 * cm, width - doc.rightMargin, 0.95 * cm)

    canvas.setFillColor(PALETTE["muted"])
    canvas.setFont("Helvetica", 7.2)
    canvas.drawString(doc.leftMargin, 0.62 * cm, "Juan Sebastián Rubiano | Hoja de vida")
    canvas.drawRightString(width - doc.rightMargin, 0.62 * cm, "Página 1")
    canvas.restoreState()


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        leftMargin=1.55 * cm,
        rightMargin=1.55 * cm,
        topMargin=1.15 * cm,
        bottomMargin=1.2 * cm,
        title="Juan Sebastián Rubiano - Hoja de vida",
        author="Juan Sebastián Rubiano",
        subject="Hoja de vida para roles de entrada en implementación, datos y software",
    )
    doc.build(build_story(), onFirstPage=draw_page, onLaterPages=draw_page)
    print(f"PDF generado en: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
