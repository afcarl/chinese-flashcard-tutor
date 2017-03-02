from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
import csv
import hashlib

from chinese_tutor.models import FlashCard
from chinese_tutor.models import UserAttempt


def export(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="flash_cards.csv"'

    writer = csv.writer(response)
    writer.writerow(['ip_address', 'user_hash', 'stimulus', 'true_response',
                     'user_response'])

    pred = UserAttempt.objects.order_by('time')
    for p in pred:
        writer.writerow([p.user, hashlib.md5(p.user.encode()).hexdigest()[0:6],
                         p.flash_card.stimulus, p.flash_card.response,
                         p.user_response])
    return response


def index(request):
    user = request.META.get('REMOTE_ADDR')
    if not user:
        user = "Unknown"

    user_attempts = UserAttempt.objects.filter(user=user).count()
    object_count = 80

    if object_count - user_attempts <= 0:
        template = loader.get_template('chinese_tutor/done.html')
        context = RequestContext(request, {'code':
                                           hashlib.md5(user.encode()).hexdigest()[0:6]})
        return HttpResponse(template.render(context))

    if len(UserAttempt.objects.filter(user=user)) > 0:
        last_cards = [a.flash_card.id for a in
                      UserAttempt.objects.filter(user=user).order_by('-time')[:2]]
        card = FlashCard.objects.exclude(id__in=last_cards).order_by('?')[0]
    else:
        card = FlashCard.objects.order_by('?')[0]

    template = loader.get_template('chinese_tutor/index.html')
    context = RequestContext(request, {
        'flash_card': card,
        'remaining': object_count - user_attempts,
    })
    return HttpResponse(template.render(context))


def attempt(request, flash_card_id, value):
    user = request.META.get('REMOTE_ADDR')
    if not user:
        user = "Unknown"

    flash_card = FlashCard.objects.get(id__exact=flash_card_id)
    attempt = UserAttempt(user=user, flash_card=flash_card,
                          user_response=value)
    attempt.save()

    return HttpResponseRedirect(reverse('index'))
