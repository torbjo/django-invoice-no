# TODO
# list all invoices on client?
# contact person. invoice.our_ref overrides invoice.client.contact

from django.contrib import admin
from django.conf.urls import patterns, url
from django.http import HttpResponse

from models import Account, Client, Invoice, InvoiceLine
from utils import render_pdf



## Client
class ClientAdmin (admin.ModelAdmin):
    ''' Payer '''
    list_display = '__unicode__', 'contact', 'phone', 'email'



## Invoice
class InvoiceInline (admin.TabularInline):
    model = InvoiceLine
    extra = 4

class InvoiceAdmin (admin.ModelAdmin):
    # @todo only for change, not add. override get_readonly_fields()
    #readonly_fields = 'date', 'due', 'client', 'text'
    #fields = 'date', 'due', 'client', 'text'
    date_hierarchy = 'date'
    actions_selection_counter = True
    # @todo text&comment => extra fieldset
    #list_filter
    #raw_id_fields = 'lines',

    inlines = [InvoiceInline]

    # Action: Download PDF
    actions = ('make_pdf',)
    def make_pdf (self, request, queryset):
        # q: can save queryset / invoice ids in session, then redirect to view?
        #assert(len(queryset)==1)
        if len(queryset) > 1:
            self.message_user (request, 'Sorry, no support for multi-page PDF (yet)!', 'ERROR')
            return
        if not queryset[0].account:
            self.message_user (request, 'ERROR: Invoice is missing account/payer! You can fix it.', 'ERROR')
            return
        response = HttpResponse (content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice-%d.pdf"' % queryset[0].pk
        render_pdf (queryset[0], response)
        return response
        #self.message_user (request, 'PDF ready for download')
    make_pdf.short_description = 'Create PDF of selected invoice(s)'



admin.site.register (Account)
admin.site.register (Client, ClientAdmin)
admin.site.register (Invoice, InvoiceAdmin)
