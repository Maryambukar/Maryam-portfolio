from .models import AcademicFact, SiteOwner


def site_owner_context(request):
    """
    Makes {{ site_owner }} and {{ academic_facts }} available in every
    template without every view having to fetch them manually.
    """
    site_owner = SiteOwner.load()
    academic_facts = AcademicFact.objects.filter(owner=site_owner).first()
    return {
        'site_owner': site_owner,
        'academic_facts': academic_facts,
    }
