from django.db import models


class SiteOwner(models.Model):
    """
    Singleton-style model holding the top-level identity/contact info used
    across the whole site ({{ site_owner.* }} in templates). Edited from the
    Django admin — there should only ever be one row.
    """
    name = models.CharField(max_length=150, default='Maryam Bukar')
    headline = models.CharField(
        max_length=200,
        default='Aspiring Data Scientist & Analyst / Software Developer',
        help_text="Short line under the name on the homepage hero.",
    )
    bio = models.TextField(
        blank=True,
        help_text="Short paragraph shown in the hero section.",
    )
    university = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=150, blank=True)

    # Only shown on the site once filled in (per the spec).
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Site owner profile'
        verbose_name_plural = 'Site owner profile'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Enforce a single row so {{ site_owner }} is always unambiguous.
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AcademicFact(models.Model):
    """Current (university-level) academic facts shown on the homepage."""
    owner = models.OneToOneField(SiteOwner, on_delete=models.CASCADE, related_name='academic_facts')
    degree_program = models.CharField(max_length=200, blank=True)
    class_standing = models.CharField(max_length=100, blank=True, help_text="e.g. 'University Student'")
    cgpa = models.CharField(max_length=20, blank=True, help_text="e.g. '3.52 / 4.00'")
    deans_list = models.BooleanField(default=False)
    deans_list_detail = models.CharField(
        max_length=200, blank=True,
        help_text="e.g. 'Consecutive semesters'",
    )

    class Meta:
        verbose_name = 'Academic facts'
        verbose_name_plural = 'Academic facts'

    def __str__(self):
        return f"Academic facts for {self.owner}"


class EducationEntry(models.Model):
    """
    One level of education (university, secondary school, ...). Ordered by
    `order` and driven entirely by the admin so the homepage 'next/back'
    slider on the Education section has real data to page through.
    """
    institution = models.CharField(max_length=200)
    location = models.CharField(max_length=150, blank=True)
    program = models.CharField(max_length=200, blank=True)
    period = models.CharField(max_length=100, blank=True, help_text="e.g. '2025 – Present'")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first (most recent first).")

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.institution


class AdminLoginAttempt(models.Model):
    """
    Audit log of every attempt to sign in through the secured admin gate —
    successful or not — so Maryam can see who tried, how many times, and
    when, straight from the Django admin.
    """
    username_tried = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)
    was_successful = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Admin login attempt'

    def __str__(self):
        status = 'SUCCESS' if self.was_successful else 'FAILED'
        return f"[{status}] {self.username_tried} @ {self.timestamp:%Y-%m-%d %H:%M}"
