from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import redirect, render
from django_ratelimit.decorators import ratelimit

from .forms import ContactForm


@ratelimit(key='ip', rate='5/m', block=True)
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)

            email_body = (
                f"New message from the portfolio contact form.\n\n"
                f"From: {contact_message.name} <{contact_message.email}>\n"
                f"Subject: {contact_message.subject}\n\n"
                f"{contact_message.message}"
            )
            try:
                email = EmailMessage(
                    subject=f"Portfolio contact: {contact_message.subject}",
                    body=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_RECEIVING_EMAIL],
                    reply_to=[contact_message.email],
                )
                email.send(fail_silently=False)
                contact_message.email_sent = True
                messages.success(request, "Thanks — your message has been sent. I'll get back to you soon.")
            except BadHeaderError:
                messages.error(request, "Invalid header found. Please try again.")
            except Exception:
                messages.warning(
                    request,
                    "Your message was saved, but there was a problem emailing it directly. "
                    "It will still be reviewed.",
                )
            contact_message.save()
            return redirect('contact:contact')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})
