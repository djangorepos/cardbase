from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView, FormView, DetailView
import random
from core.forms import *
from core.models import *


def sum_num(number):
    """Sum digits of a number, used for Luhn algorithm."""
    return number // 10 + number % 10


def lunh(number):
    """Check validity using the Luhn algorithm."""
    even_numbers = number[::2]
    odd_numbers = list(number[1::2])
    sum_odd_numbers = sum(int(i) for i in odd_numbers)

    summ = 0
    for j in even_numbers:
        k = int(j) * 2
        summ += sum_num(k)

    return (summ + sum_odd_numbers) % 10


def generate_card_number(card_type):
    """Generate a valid card number using the Luhn algorithm."""
    while True:
        result = '4' if card_type == "visa" else "5"  # Starting with 4 for Visa cards. Adjust for others if needed.

        for k in range(2, 16):
            result += str(random.randint(1, 9))  # Add random digits for the card number

        # Try adding the last digit (check Luhn)
        for l in range(0, 10):
            number = result + str(l)
            if lunh(number) == 0:
                return number  # Return a valid card number once it's found


def generate_cvv():
    cvv = '000'
    while cvv[0] == cvv[1] or cvv[1] == cvv[2] or cvv[2] == cvv[0]:
        cvv = str(random.randrange(100, 999))
    return cvv

class CardList(ListView, FormView):
    model = Card
    form_class = FilterForm
    template_name = 'card_list.html'

    def get_queryset(self):
        blank = 0
        for obj in self.request.GET.values():
            print(obj)
            if obj is None or obj == '':
                blank += 1

        series = self.request.GET.get('series')
        number = self.request.GET.get('number')
        cardholder_name = self.request.GET.get('cardholder_name')
        status = self.request.GET.get('status')
        print(blank)

        if blank == 4:
            object_list = Card.objects.all()
        else:
            object_list = Card.objects.all()
            if series and series != '':
                object_list = object_list.filter(series=series)
            if number and number != '':
                object_list = object_list.filter(number=number)
            if cardholder_name and cardholder_name != '':
                object_list = object_list.filter(cardholder_name=cardholder_name)
            if status and status != '':
                object_list = object_list.filter(status=status)

        return object_list.order_by('release_date')


class CardDetail(DetailView):
    model = Card
    template_name = 'card_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['transactions'] = Transaction.objects.filter(card=self.object)
        return self.render_to_response(context)


def card_create(request):
    context = {}
    form = CreateForm

    if request.method == 'POST':
        print(request.POST)
        amount = int(request.POST.get('amount'))
        series = request.POST.get('series')
        cardholder_name = request.POST.get('cardholder_name')
        date = request.POST.get('date')

        if date == '3 years':
            delta_years = 3
        elif date == '5 years':
            delta_years = 5
        elif date == '10 years':
            delta_years = 10
        else:
            raise ValidationError("Could not generate a valid card number.")

        release_date = timezone.now()
        valid_date = timezone.now() + relativedelta(years=delta_years)

        if amount > 0:
            for a in range(amount):
                card_number = generate_card_number(series)
                card_cvv = generate_cvv()

                if not card_number:
                    raise ValidationError("Invalid card number generated.")

                if not card_cvv:
                    raise ValidationError("Invalid card verification value.")

                # Ensure that card number is assigned correctly
                print("Generated card:", card_number, card_cvv)

                Card.objects.create(image=None,
                                    series=series,
                                    number=card_number,
                                    cardholder_name=cardholder_name,
                                    release_date=release_date,
                                    valid_date=valid_date,
                                    cvv_code=card_cvv,
                                    status='active',
                                    balance=0)
        else:
            raise ValidationError

    context['form'] = form
    context['create'] = True
    return render(request, 'card_create.html', context)


def card_activate(request, pk):
    card = Card.objects.get(id=pk)
    card.status = 'active'
    card.save()
    return redirect('card_list')


def card_deactivate(request, pk):
    card = Card.objects.get(id=pk)
    card.status = 'not_active'
    card.save()
    return redirect('card_list')


def card_delete(request, pk):
    Card.objects.get(id=pk).delete()
    return redirect('card_list')
