from django.db import models


class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200, blank=True)
    date_earned = models.DateField(null=True, blank=True)
    certificate_image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-date_earned']

    def __str__(self):
        return self.title


class SkillCategory(models.Model):
    """e.g. 'Programming Languages', 'Databases & Tools', 'Other Skills'."""
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Skill categories'

    def __str__(self):
        return self.name


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tech_stack = models.CharField(max_length=300, blank=True, help_text="Comma-separated, e.g. 'Django, Python, Bootstrap'")
    project_url = models.URLField(blank=True, help_text="Live demo or repo link, if any.")
    thumbnail = models.ImageField(upload_to='projects/', blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]


class Experience(models.Model):
    role_title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True)
    period = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f"{self.role_title} — {self.organization}"


class Achievement(models.Model):
    title = models.CharField(max_length=200)
    detail = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title
