from django.db.models import Q
from django.views.generic import ListView, FormView, DetailView

from core.forms import FilterForm
from core.models import Card, Transaction


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

