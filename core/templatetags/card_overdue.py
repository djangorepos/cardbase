from django import template
from django.utils import timezone
from core.models import Card

register = template.Library()


@register.simple_tag(name='card_overdue')
def card_overdue():
    # Retrieve only the overdue and active cards
    overdue_cards = Card.objects.filter(valid_date__lt=timezone.now(), status='active')
    for card in overdue_cards:
        print(f"Card ID: {card.id}, Valid Date: {card.valid_date}, Status: {card.status}")
        card.status = 'overdue'
        card.save()

    # Alternatively, you can use bulk update for better performance
    # overdue_cards.update(status='overdue')

    return ''
