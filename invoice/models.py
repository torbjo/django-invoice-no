""" Register invoices and render to PDF.

"""

from django.db import models
import datetime


class Client (models.Model):
    name = models.CharField (max_length=100)
    address = models.TextField()
    contact = models.CharField (max_length=64, blank=True, verbose_name='Contact person')
    email = models.EmailField (blank=True)
    # Q: email to client or to contact person
    # a: checkbox to select?
    comment = models.TextField (blank=True)

    class Meta:
        ordering = 'name',

    def __unicode__ (self):
        return self.name


class Invoice (models.Model):
    date = models.DateField (auto_now=True)
    client = models.ForeignKey (Client)
    # changed to ForeignKey on InvoiceLine instead
    #lines = models.ManyToManyField ('InvoiceLine')
    text = models.TextField (blank=True, help_text='Extra text to put on the invoice')
    comment = models.TextField (blank=True, help_text='Internal comments')
    #invoice_no = models.IntegerField()
    # due_date / betalingsfrist / betingelser (14 dager)
    #due_date = models.DateField(default=datetime.date.today() + datetime.timedelta(days=14))

    def __unicode__ (self):
        return self.client.name + ' : ' + self.date.isoformat()


class InvoiceLine (models.Model):
    invoice = models.ForeignKey (Invoice)
    text = models.CharField (max_length=100)
    quantity = models.FloatField (default=1)  # @todo DecimalField or RationalField
    amount = models.DecimalField (max_digits=12, decimal_places=2)
    def __unicode__ (self):
        return self.text
