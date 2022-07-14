from django import template
from django.utils import timezone

from core.models import Card

register = template.Library()


@register.simple_tag(name='card_overdue')
def card_overdue():
    cards = Card.objects.all()
    for card in cards:
        if card.valid_date < timezone.now():
            card.status = 'overdue'
            card.save()
    return ''
