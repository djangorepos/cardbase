from django.forms import ModelForm

from core.models import Card


class FilterForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['series'].required = False
        self.fields['number'].required = False
        self.fields['cardholder_name'].required = False
        self.fields['status'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Card
        fields = ['series', 'number', 'cardholder_name', 'status']
