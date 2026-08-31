"""
Manual, rule-based portfolio assistant.

No external AI model is called here — every answer is either a fixed
string or pulled straight from the database. Matching is done with simple
keyword sets so rephrased questions still land on the right intent,
without ever fabricating information that isn't in the database.
"""
import re

from core.models import AcademicFact, SiteOwner
from portfolio.models import Certification, Experience, Project, SkillCategory

FALLBACK = "I don't have that information in Maryam's portfolio yet."

GREETING_WORDS = {
    'hi', 'hello', 'hey', 'yo', 'sup', 'howdy',
    'goodmorning', 'goodafternoon', 'goodevening', 'goodnight',
}


def _normalize(text):
    text = text.lower().strip()
    # collapse "good morning" -> "goodmorning" so greeting matching is simple
    text = re.sub(r'[^a-z\s]', '', text)
    return text


def _tokens(text):
    return set(_normalize(text).split())


def _is_greeting(tokens, raw_normalized):
    joined = raw_normalized.replace(' ', '')
    if any(word in joined for word in GREETING_WORDS):
        return True
    return bool(tokens & GREETING_WORDS)


# Each entry: (set of trigger keywords, handler function)
def _about(tokens):
    owner = SiteOwner.load()
    if owner.bio:
        return owner.bio
    return "Maryam is a university student studying Data Science & Analytics, also building her software development skills."


def _university(tokens):
    owner = SiteOwner.load()
    if owner.university:
        return f"Maryam studies at {owner.university}."
    return FALLBACK


def _degree(tokens):
    facts = AcademicFact.objects.first()
    if facts and facts.degree_program:
        return f"Maryam is pursuing {facts.degree_program}."
    return FALLBACK


def _cgpa(tokens):
    facts = AcademicFact.objects.first()
    if facts and facts.cgpa:
        return f"Maryam's current CGPA is {facts.cgpa}."
    return FALLBACK


def _academic_standing(tokens):
    facts = AcademicFact.objects.first()
    if facts and (facts.class_standing or facts.deans_list):
        bits = []
        if facts.class_standing:
            bits.append(facts.class_standing)
        if facts.deans_list:
            bits.append(f"on the Dean's List{': ' + facts.deans_list_detail if facts.deans_list_detail else ''}")
        return "Maryam is " + " and ".join(bits) + "."
    return FALLBACK


def _certifications(tokens):
    certs = list(Certification.objects.all())
    if not certs:
        return "There are currently no certifications listed on Maryam's portfolio yet."
    names = ', '.join(c.title for c in certs)
    return f"Maryam's certifications include: {names}."


def _skills(tokens):
    categories = SkillCategory.objects.prefetch_related('skills')
    lines = []
    for cat in categories:
        names = [s.name for s in cat.skills.all()]
        if names:
            lines.append(f"{cat.name}: {', '.join(names)}")
    if not lines:
        return "There are currently no technical skills listed on Maryam's portfolio yet."
    return "Here's a summary of Maryam's skills — " + "; ".join(lines) + "."


def _projects(tokens):
    projects = list(Project.objects.all())
    if not projects:
        return "There are currently no featured projects available."
    titles = ', '.join(p.title for p in projects)
    return f"Maryam has worked on: {titles}. You can see full details on the Projects page."


def _experience(tokens):
    experiences = list(Experience.objects.all())
    if not experiences:
        return "There is currently no professional experience listed on Maryam's portfolio yet."
    bits = [f"{e.role_title} at {e.organization}" if e.organization else e.role_title for e in experiences]
    return "Maryam's experience includes: " + '; '.join(bits) + "."


def _achievements(tokens):
    from portfolio.models import Achievement
    achievements = list(Achievement.objects.all())
    if not achievements:
        return "There are currently no achievements listed on Maryam's portfolio yet."
    return "Achievements: " + '; '.join(a.title for a in achievements) + "."


def _contact(tokens):
    owner = SiteOwner.load()
    bits = [b for b in [owner.email, owner.phone] if b]
    if bits:
        return "You can reach Maryam at " + ' or '.join(bits) + ", or through the Contact page."
    return "You can reach Maryam through the Contact page."


def _cv(tokens):
    return "You can download Maryam's up-to-date CV using the 'Download CV' button in the sidebar."


def _education(tokens):
    owner = SiteOwner.load()
    facts = AcademicFact.objects.first()
    if owner.university or (facts and facts.degree_program):
        bits = [b for b in [owner.university, facts.degree_program if facts else None] if b]
        return "Maryam is studying " + ' — '.join(bits) + "."
    return FALLBACK


# keyword_set -> handler, checked in order (more specific intents first)
INTENTS = [
    ({'cgpa', 'gpa'}, _cgpa),
    ({'dean', 'deans', 'standing', 'academic'}, _academic_standing),
    ({'university', 'school', 'college', 'aun'}, _university),
    ({'degree', 'program', 'major', 'course'}, _degree),
    ({'education', 'study', 'studies', 'studying', 'studied'}, _education),
    ({'certification', 'certifications', 'certificate', 'certificates'}, _certifications),
    ({'skill', 'skills', 'technology', 'technologies', 'tools', 'languages'}, _skills),
    ({'project', 'projects', 'built', 'build', 'portfolio'}, _projects),
    ({'experience', 'internship', 'work', 'job'}, _experience),
    ({'achievement', 'achievements', 'award', 'awards', 'leadership'}, _achievements),
    ({'contact', 'email', 'phone', 'reach'}, _contact),
    ({'cv', 'resume', 'resmue', 'download'}, _cv),
    ({'about', 'who', 'bio'}, _about),
]


def get_response(user_message):
    if not user_message or not user_message.strip():
        return FALLBACK

    normalized = _normalize(user_message)
    tokens = _tokens(user_message)

    if _is_greeting(tokens, normalized):
        return "Hello! I'm Maryam's portfolio assistant. Ask me about her education, skills, projects, experience or how to get in touch."

    for keywords, handler in INTENTS:
        if tokens & keywords:
            return handler(tokens)

    return FALLBACK
