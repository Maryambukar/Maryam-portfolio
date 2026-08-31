# Maryam Bukar — Django Portfolio

A from-scratch Django rebuild matching the brown/cream reference design: fixed
dark-brown sidebar navigation, large scrolling sections, no placeholder image
area, a manual (non-AI) portfolio chatbot, an auto-updating PDF CV, and a
security-hardened admin-only login.

## 1. Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# then edit .env with real values (SECRET_KEY, SITE_ADMIN_USERNAME, email creds)

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # username MUST match SITE_ADMIN_USERNAME in .env
python manage.py seed_portfolio    # loads the real, confirmed content (bio, CGPA, education, etc.)
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

## 2. Admin access

The public site has **no visible "user login."** The only way into the
Django admin / dashboard is:

```
http://127.0.0.1:8000/control/login/
```

This form only ever accepts the single username set in `SITE_ADMIN_USERNAME`
(.env). Every attempt — successful or not — is logged in
`Admin login attempts` inside the Django admin (IP, browser, timestamp).
After 3 failed attempts, `django-axes` locks that username/IP out for an
hour (`AXES_FAILURE_LIMIT` / `AXES_COOLOFF_TIME` in `config/settings.py`).

## 3. Editing content

Everything shown on the front end (bio, CGPA, education entries,
certifications + certificate images, skills, projects, experience,
achievements, LinkedIn/GitHub links) is edited from `/control/` after
logging in — it links straight into the relevant Django admin section.
LinkedIn/GitHub buttons only render once those URL fields are filled in.

## 4. CV download

`/download-cv/` builds a PDF on the fly (via `reportlab`) straight from
current database content — nothing is cached, so it's always current, and
empty sections are simply omitted (never printed as "COMING SOON").

## 5. Chatbot

`chatbot/intents.py` is a plain keyword-matching rule engine — there is no
external API call of any kind. It answers from the same database models the
site itself uses, and returns a fixed "I don't have that information..."
line for anything it can't answer. No `ANTHROPIC_API_KEY` or Anthropic
package is used anywhere in this project.

## 6. Contact form

Submitting the contact form sends an email directly to
`CONTACT_RECEIVING_EMAIL` (.env) via SMTP, and keeps a backup copy in the
database (`Contact messages` in the admin) in case the email ever fails to
send. For Gmail, use an **App Password**, not your normal password.

## 7. Notes

- This project was generated in a sandboxed environment without internet
  access, so Django itself could not be installed to run
  `python manage.py check` / `runserver` here. Please run those two
  commands yourself right after `migrate` to confirm a clean bill of
  health before deploying.
- Pinned dependency versions in `requirements.txt` match what was specified
  (Django 5.1.4-compatible stack). Double-check versions still resolve
  together in your environment before deploying.


