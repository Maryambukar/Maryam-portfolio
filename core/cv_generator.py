"""
Builds a professional CV PDF straight from the current database content.
Sections with no real data are simply omitted — we never print
"COMING SOON" into the actual document.
"""
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (HRFlowable, ListFlowable, ListItem, Paragraph,
                                 SimpleDocTemplate, Spacer)

from portfolio.models import Certification, Experience, Project, SkillCategory

from .models import AcademicFact, EducationEntry, SiteOwner

ESPRESSO = colors.HexColor('#3B2A20')
CARAMEL = colors.HexColor('#A9673B')
INK = colors.HexColor('#2B2118')


def _styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle('CVName', parent=ss['Title'], textColor=ESPRESSO, fontSize=24, spaceAfter=2))
    ss.add(ParagraphStyle('CVHeadline', parent=ss['Normal'], textColor=CARAMEL, fontSize=12, spaceAfter=10))
    ss.add(ParagraphStyle('CVSection', parent=ss['Heading2'], textColor=ESPRESSO, spaceBefore=14, spaceAfter=4))
    ss.add(ParagraphStyle('CVBody', parent=ss['Normal'], textColor=INK, fontSize=10, leading=14))
    ss.add(ParagraphStyle('CVMeta', parent=ss['Normal'], textColor=colors.HexColor('#6B5A4C'), fontSize=9))
    return ss


def generate_cv_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
    )
    ss = _styles()
    story = []

    owner = SiteOwner.load()
    facts = AcademicFact.objects.filter(owner=owner).first()

    story.append(Paragraph(owner.name or 'Portfolio Owner', ss['CVName']))
    if owner.headline:
        story.append(Paragraph(owner.headline, ss['CVHeadline']))

    contact_bits = [b for b in [owner.email, owner.phone, owner.location] if b]
    if contact_bits:
        story.append(Paragraph(' &nbsp;|&nbsp; '.join(contact_bits), ss['CVMeta']))
    links = [u for u in [owner.linkedin_url, owner.github_url] if u]
    if links:
        story.append(Paragraph(' &nbsp;|&nbsp; '.join(links), ss['CVMeta']))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width='100%', color=CARAMEL, thickness=1))

    if owner.bio:
        story.append(Paragraph('Profile', ss['CVSection']))
        story.append(Paragraph(owner.bio, ss['CVBody']))

    # --- Education ---
    education_entries = list(EducationEntry.objects.all())
    has_university_facts = facts and any([
        owner.university, facts.degree_program, facts.class_standing, facts.cgpa, facts.deans_list
    ])
    if education_entries or has_university_facts:
        story.append(Paragraph('Education', ss['CVSection']))
        if has_university_facts:
            line1 = owner.university or ''
            line2_bits = [b for b in [facts.degree_program, facts.class_standing] if b]
            story.append(Paragraph(f"<b>{line1}</b>", ss['CVBody']))
            if line2_bits:
                story.append(Paragraph(' — '.join(line2_bits), ss['CVBody']))
            extra_bits = []
            if facts.cgpa:
                extra_bits.append(f"CGPA: {facts.cgpa}")
            if facts.deans_list:
                extra_bits.append(f"Dean's List{': ' + facts.deans_list_detail if facts.deans_list_detail else ''}")
            if extra_bits:
                story.append(Paragraph(' | '.join(extra_bits), ss['CVMeta']))
            story.append(Spacer(1, 4))
        for edu in education_entries:
            heading = edu.institution
            if edu.period:
                heading += f"  ({edu.period})"
            story.append(Paragraph(f"<b>{heading}</b>", ss['CVBody']))
            sub_bits = [b for b in [edu.program, edu.location] if b]
            if sub_bits:
                story.append(Paragraph(' — '.join(sub_bits), ss['CVMeta']))
            if edu.description:
                story.append(Paragraph(edu.description, ss['CVBody']))
            story.append(Spacer(1, 4))

    # --- Certifications ---
    certifications = Certification.objects.all()
    if certifications:
        story.append(Paragraph('Certifications', ss['CVSection']))
        items = []
        for c in certifications:
            label = c.title
            if c.issuer:
                label += f" — {c.issuer}"
            if c.date_earned:
                label += f" ({c.date_earned:%Y})"
            items.append(ListItem(Paragraph(label, ss['CVBody'])))
        story.append(ListFlowable(items, bulletType='bullet'))

    # --- Skills ---
    skill_categories = SkillCategory.objects.prefetch_related('skills')
    if any(cat.skills.exists() for cat in skill_categories):
        story.append(Paragraph('Skills', ss['CVSection']))
        for cat in skill_categories:
            names = [s.name for s in cat.skills.all()]
            if names:
                story.append(Paragraph(f"<b>{cat.name}:</b> {', '.join(names)}", ss['CVBody']))

    # --- Projects ---
    projects = Project.objects.all()
    if projects:
        story.append(Paragraph('Projects', ss['CVSection']))
        for p in projects:
            story.append(Paragraph(f"<b>{p.title}</b>", ss['CVBody']))
            if p.description:
                story.append(Paragraph(p.description, ss['CVBody']))
            if p.tech_stack:
                story.append(Paragraph(p.tech_stack, ss['CVMeta']))
            story.append(Spacer(1, 4))

    # --- Experience ---
    experiences = Experience.objects.all()
    if experiences:
        story.append(Paragraph('Experience', ss['CVSection']))
        for e in experiences:
            heading = e.role_title
            if e.organization:
                heading += f" — {e.organization}"
            if e.period:
                heading += f" ({e.period})"
            story.append(Paragraph(f"<b>{heading}</b>", ss['CVBody']))
            if e.description:
                story.append(Paragraph(e.description, ss['CVBody']))
            story.append(Spacer(1, 4))

    if contact_bits:
        story.append(Paragraph('Contact', ss['CVSection']))
        story.append(Paragraph(' &nbsp;|&nbsp; '.join(contact_bits + links), ss['CVBody']))

    doc.build(story)
    buffer.seek(0)
    return buffer
