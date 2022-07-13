from django.db.models import Q
from django.views.generic import ListView, FormView

from core.forms import FilterForm
from core.models import Card


class CardList(ListView, FormView):
    model = Card
    form_class = FilterForm
    template_name = 'card_list.html'
    paginate_by = 10

    def get_queryset(self):
        print(self.request.GET)
        blank = False
        for obj in self.request.GET.values():
            print(obj)
            if obj is None or obj == '':
                pass
            else:
                blank = True
        print(blank)
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


def card_detail(request, pk):
    pass
