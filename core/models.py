from django.db import models


class Card(models.Model):
    SERIES = [('visa', 'visa'),
              ('mastercard', 'mastercard')]
    STATUS = [('active', 'active'),
              ('not_active', 'not_active'),
              ('overdue', 'overdue')]
    image = models.ImageField(blank=True, null=True)
    series = models.CharField(max_length=10, choices=SERIES)
    number = models.CharField(max_length=20, unique=True)
    cardholder_name = models.CharField(max_length=128)
    release_date = models.DateTimeField()
    valid_date = models.DateTimeField()
    cvv_code = models.CharField(max_length=3)
    status = models.CharField(max_length=128, choices=STATUS)
    balance = models.FloatField()

    def __str__(self):
        return self.number

    @property
    def image_url(self):
        # Provide the URL for predefined images based on series
        if self.image:
            return self.image.url
        elif self.series == 'visa':
            return '/media/core/staticfiles/img/visa_default.png'
        elif self.series == 'mastercard':
            return '/media/core/staticfiles/img/mastercard_default.png'

    class Meta:
        ordering = ['release_date']


class Transaction(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    date = models.DateTimeField()
    price = models.FloatField()

    def __str__(self):
        return self.card.number

    class Meta:
        ordering = ['date']
