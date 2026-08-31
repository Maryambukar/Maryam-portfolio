import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from .intents import get_response


@require_POST
@csrf_protect
@ratelimit(key='ip', rate='30/m', block=True)
def chatbot_reply(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        data = {}

    user_message = (data.get('message') or '').strip()[:500]
    reply = get_response(user_message)
    return JsonResponse({'reply': reply})
