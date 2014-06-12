"""
Very simple invoicing/billing system.
"""

from django.db import models
from datetime import date, timedelta


class Account (models.Model):
    '''Biller'''
    name = models.CharField (max_length=100)
    address = models.TextField()
    org_no = models.CharField (max_length=32, blank=True)
    account_no = models.CharField (max_length=32)
    phone = models.CharField (max_length=32, blank=True)
    email = models.EmailField (blank=True)
    comment = models.TextField (blank=True)

    class Meta:
        ordering = 'name',

    def __unicode__ (self):
        return self.name

    def clean (self):
        self.address = self.address.replace ('\r', '')



class Client (models.Model):
    ''' Payer '''
    display_name = models.CharField (max_length=32, blank=True, help_text='Our name')
    name = models.CharField (max_length=100, help_text='Company name')
    address = models.TextField()
    org_no = models.CharField (max_length=32, blank=True)
    phone = models.CharField (max_length=32, blank=True)
    email = models.EmailField (blank=True)
    contact = models.CharField ('contact person', max_length=64, blank=True)
    comment = models.TextField (blank=True)
    # @todo owner?

    class Meta:
        ordering = 'name',

    def __unicode__ (self):
        return self.display_name or self.name

    def clean (self):
        self.address = self.address.replace ('\r', '')



class Invoice (models.Model):
    date = models.DateField (auto_now_add=True)
    due = models.DateField (default=lambda: date.today()+timedelta(days=20))
    client = models.ForeignKey (Client)
    account = models.ForeignKey (Account, default=1)
    contact = models.CharField (max_length=64, blank=True, help_text='Uses the contact stored on the client if not given')
    #contact = models.CharField (max_length=64, blank=True, help_text='Default is to use client contact')
    #user = models.CharField (max_length=64, blank=True, verbose_name='Your ref.')
    text = models.TextField ('invoice text', blank=True)
    comment = models.TextField (blank=True, help_text='internal comments')

    def __unicode__ (self):
        return unicode(self.client) + ': ' + self.date.isoformat()
#               ' : ' + self.invoiceline_set.first().text    # slow

    def invoice_no (self):
        return str(self.date).replace('-','') + str(self.pk)
    # @todo property. use decorator instead?
#    def _invoice_no (self):
#        return str(self.date).replace('-','') + str(self.pk)
#    invoice_no = property (_invoice_no)



class InvoiceLine (models.Model):
    invoice = models.ForeignKey (Invoice)
    text = models.CharField (max_length=100)
    quantity = models.PositiveIntegerField (default=1)
    amount = models.IntegerField()
    #unit = models.CharField (max_length=16)
    # @todo amount -> unit_price?
    def __unicode__ (self): return self.text
