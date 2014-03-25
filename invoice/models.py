# encoding: utf8
"""
Register invoices and render to PDF.

TODO:
* AddressField, PhoneField?
* get_absolute_url() - Any object that has a URL that uniquely identifies it should define this method.
* unique on org_no
* webpage for client (1:n?)
* list of contact persons

"""

from django.db import models
import datetime

#from django.core.exceptions import ValidationError
#raise ValidationError('Lack of empaty')


class Account (models.Model):
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

    '''
    def save (self, *args, **kwargs):
        #print dir(self)
        self.address = self.address.replace ('\r', '')
        super (Account,self).save (*args, **kwargs)
    '''


class Client (models.Model):
    display_name = models.CharField (max_length=32, blank=True, help_text='Our name')
    name = models.CharField (max_length=100, help_text='Company name')
    # @todo howto display help text after (not bellow) field? css?
    #display_name = models.CharField (max_length=32, blank=True, help_text='Our name')
    #name = models.CharField (max_length=100, help_text='Company name')
    address = models.TextField()
    org_no = models.CharField (max_length=32, blank=True)
    phone = models.CharField (max_length=32, blank=True)
    email = models.EmailField (blank=True)
    #contact = models.CharField (max_length=64, blank=True, verbose_name='Contact person')
    # @todo owner?
    contact = models.CharField ('contact person', max_length=64, blank=True)
    comment = models.TextField (blank=True)

    class Meta:
        ordering = 'name',

    def __unicode__ (self):
        return self.display_name or self.name



class Invoice (models.Model):
    date = models.DateField (auto_now=True)
    due = models.DateField (default=datetime.date.today() + datetime.timedelta(days=20))
    # @todo default must be callable!
    client = models.ForeignKey (Client)
    #account = models.ForeignKey (Account)
    account = models.ForeignKey (Account, null=True)   # tmp tmp
    contact = models.CharField ('contact person', max_length=64, blank=True)
    #contact = models.CharField (max_length=64, blank=True, verbose_name='Deres ref.:')
    #our_contact = models.CharField (max_length=64, blank=True, verbose_name='Vår ref.:')
    text = models.TextField (blank=True, help_text='Extra text to put on the invoice')
    comment = models.TextField (blank=True, help_text='Internal comments')
    #invoice_no = models.IntegerField() # @todo auto-sequence
    # @todo auto-generate invoice_no. no db field.

    def __unicode__ (self):
        return self.date.isoformat() + ': ' + unicode(self.client) + \
               ' : ' + self.invoiceline_set.first().text    # slow
        #return self.client.name + ' : ' + self.date.isoformat()

    def invoice_no (self):
        return '1234'

#    def _get_full_name (self):
#        "Returns the persons full name"
#        return '%s %s' % (self.first_name, self.last_name)
#    full_name = property (_get_full_name)



class InvoiceLine (models.Model):
    invoice = models.ForeignKey (Invoice)
    text = models.CharField (max_length=100)
    #quantity = models.TextField (max_length=32)
    quantity = models.FloatField (default=1)  # @todo DecimalField or RationalField
    #unit = models.CharField (max_length=16)
    amount = models.DecimalField (max_digits=12, decimal_places=2)
    # @todo amount -> unit_price?
    def __unicode__ (self):
        return self.text
