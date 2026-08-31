from django.shortcuts import render

from .models import Certification, Project


def projects_list(request):
    """Full list of uploaded projects — linked from the nav 'Projects' tab."""
    projects = Project.objects.all()
    return render(request, 'portfolio/projects_list.html', {'projects': projects})


def certifications_list(request):
    """Full gallery of uploaded certificates — linked from the nav tab."""
    certifications = Certification.objects.all()
    return render(request, 'portfolio/certifications_list.html', {'certifications': certifications})
