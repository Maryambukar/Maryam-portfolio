from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render


def _is_the_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required(login_url='core:admin_login')
@user_passes_test(_is_the_admin, login_url='core:admin_login')
def dashboard_home(request):
    """
    Landing page after a successful secured login. Links out to the real
    editing surfaces (Django admin sections) for every content type on the
    site, so Maryam can add/edit/delete everything that appears on the
    front end from one place.
    """
    sections = [
        {'label': 'Site profile & academic facts', 'url': '/django-admin/core/siteowner/1/change/'},
        {'label': 'Education entries', 'url': '/django-admin/core/educationentry/'},
        {'label': 'Certifications', 'url': '/django-admin/portfolio/certification/'},
        {'label': 'Skill categories & skills', 'url': '/django-admin/portfolio/skillcategory/'},
        {'label': 'Projects', 'url': '/django-admin/portfolio/project/'},
        {'label': 'Experience', 'url': '/django-admin/portfolio/experience/'},
        {'label': 'Achievements', 'url': '/django-admin/portfolio/achievement/'},
        {'label': 'Contact messages received', 'url': '/django-admin/contact/contactmessage/'},
        {'label': 'Admin login attempts (security log)', 'url': '/django-admin/core/adminloginattempt/'},
    ]
    return render(request, 'dashboard/home.html', {'sections': sections})
