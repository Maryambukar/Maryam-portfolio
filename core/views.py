from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django_ratelimit.decorators import ratelimit

from portfolio.models import Achievement, Certification, Experience, Project, SkillCategory

from .cv_generator import generate_cv_pdf
from .forms import SecureAdminLoginForm
from .models import AdminLoginAttempt, EducationEntry, SiteOwner


def _get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def home(request):
    context = {
        'education_entries': EducationEntry.objects.all(),
        'certifications': Certification.objects.all(),
        'skill_categories': SkillCategory.objects.prefetch_related('skills').all(),
        'projects': Project.objects.filter(is_featured=True),
        'experiences': Experience.objects.all(),
        'achievements': Achievement.objects.all(),
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


@ratelimit(key='ip', rate='10/m', block=True)
def download_cv(request):
    """
    Real Django file response — assembles a PDF straight from current
    database content every time it's requested, so it's never stale.
    """
    pdf_buffer = generate_cv_pdf()
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    site_owner = SiteOwner.load()
    filename = f"{site_owner.name.replace(' ', '_')}_CV.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@ratelimit(key='ip', rate='10/m', block=True)
def secure_admin_login(request):
    """
    The ONLY entry point into the dashboard/Django admin. Restricted to the
    single username configured as SITE_ADMIN_USERNAME. Every attempt —
    successful or not — is logged with IP, user agent and timestamp.
    django-axes (see settings.AXES_*) enforces the actual 3-attempt lockout
    on top of this.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard:home')

    form = SecureAdminLoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        username_tried = request.POST.get('username', '')
        ip = _get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:300]
        allowed_username = settings.SITE_ADMIN_USERNAME

        if allowed_username and username_tried != allowed_username:
            AdminLoginAttempt.objects.create(
                username_tried=username_tried, ip_address=ip,
                user_agent=user_agent, was_successful=False,
            )
            messages.error(
                request,
                "This login is reserved for the site administrator only. "
                "If you are a visitor looking for the portfolio, please use "
                "the navigation menu. Unauthorized attempts are logged and "
                "repeated attempts will be blocked.",
            )
        elif form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                AdminLoginAttempt.objects.create(
                    username_tried=username_tried, ip_address=ip,
                    user_agent=user_agent, was_successful=True,
                )
                login(request, user)
                return redirect('dashboard:home')
            AdminLoginAttempt.objects.create(
                username_tried=username_tried, ip_address=ip,
                user_agent=user_agent, was_successful=False,
            )
            messages.error(request, "This account is not authorized for admin access.")
        else:
            AdminLoginAttempt.objects.create(
                username_tried=username_tried, ip_address=ip,
                user_agent=user_agent, was_successful=False,
            )
            messages.error(
                request,
                "Incorrect credentials. This page is for site administration "
                "only — attempts are logged, and repeated failures will "
                "lock you out.",
            )

    return render(request, 'core/admin_login.html', {'form': form})
