from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your message', 'class': 'form-control', 'rows': 6}),
        }

    def clean_subject(self):
        subject = self.cleaned_data['subject'].strip()
        if not subject:
            raise forms.ValidationError('Please add a subject for your message.')
        return subject
