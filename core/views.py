from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, FormView, DetailView
import random
from core.forms import *
from core.models import *


class CardList(ListView, FormView):
    model = Card
    form_class = FilterForm
    template_name = 'card_list.html'

    def get_queryset(self):
        blank = False
        for obj in self.request.GET.values():
            print(obj)
            if obj is None or obj == '':
                pass
            else:
                blank = True

        series = self.request.GET.get('series')
        number = self.request.GET.get('number')
        cardholder_name = self.request.GET.get('cardholder_name')
        status = self.request.GET.get('status')

        if blank is False:
            object_list = Card.objects.all()
        else:
            object_list = Card.objects.filter(Q(series=series)
                                              | Q(number=number)
                                              | Q(cardholder_name=cardholder_name)
                                              | Q(status=status)
                                              )

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

    def sum_num(number):
        return number // 10 + number % 10

    def luna(card_number):
        evenNumbers = card_number[::2]
        oddNumbers = list(card_number[1::2])
        sumOddNumbers = 0
        for i in oddNumbers:
            sumOddNumbers += int(i)

        summ = 0
        for i in evenNumbers:
            k = int(i) * 2
            summ += sum_num(k)
        return (summ + sumOddNumbers) % 10

    def generate_card_number():
        result = '4'
        for i in range(2, 16):
            random.seed()
            result += str(random.randint(1, 9))
            if i % 4 == 0:
                result += ' '

        for i in range(0, 9):
            if luna((result + str(i)).replace(" ", '')) == 0:
                result += str(i)
                return result

    if request.method == 'POST':
        print(request.POST)
        amount = int(request.POST.get('amount'))
        series = request.POST.get('series')
        cardholder_name = request.POST.get('cardholder_name')
        date = request.POST.get('date')

        def generate_cvv():
            return str(random.randrange(100, 999))

        def get_cvv():
            cvv = '000'
            while cvv[0] != cvv[1] != cvv[2]:
                cvv = generate_cvv()
            return cvv

        if date == '1 year':
            delta_days = 365
        elif date == '6 month':
            delta_days = 182
        elif date == '1 month':
            delta_days = 30
        else:
            raise ValidationError

        if amount > 0:
            for i in range(amount):
                if series == 'visa':
                    image = ImageFile(open('core/staticfiles/img/visa_default.png', 'rb'))
                elif series == 'mastercard':
                    image = ImageFile(open('core/staticfiles/img/mastercard_default.png', 'rb'))
                else:
                    raise ValidationError

                Card.objects.create(image=image,
                                    series=series,
                                    number=generate_card_number(),
                                    cardholder_name=cardholder_name,
                                    release_date=timezone.now(),
                                    valid_date=timezone.now() + timedelta(days=delta_days),
                                    cvv_code=get_cvv(),
                                    status='active',
                                    balance=0)
        else:
            raise ValidationError

    context['form'] = form
    context['create'] = True
    return render(request, 'card_create.html', context)
