from django.contrib import admin
from .models import Account, Client, Invoice, InvoiceLine
#from .forms import InvoiceInlineForm

from django.conf.urls import patterns, url
from django.http import HttpResponse



# TODO
# list all invoices on client?


class InvoiceInline (admin.TabularInline):
    model = InvoiceLine
    extra = 4
#    model = Invoice.lines.through
#    form = InvoiceInlineForm


class InvoiceAdmin (admin.ModelAdmin):
    date_hierarchy = 'date'
    actions_selection_counter = True

    inlines = [InvoiceInline]
#    exclude = 'lines',
    #list_display = 'client__display_name', # not possible?

    def get_urls (self):
        return patterns ('',
            (r'^pdf_view/(?P<invoice_id>\d+)/$', self.admin_site.admin_view (self.pdf_view)),
        ) + super (InvoiceAdmin, self).get_urls()

    # custom views
    def pdf_view (self, request, invoice_id):
        print request.path
        return HttpResponse ('Fuck you!')

    # custom actions
    actions = ('make_pdf',)
    def make_pdf (self, request, queryset):
        print queryset
        self.message_user (request, 'PDF ready for download')
    make_pdf.short_description = 'Create PDF of selected invoice(s)'

    # @todo text&comment => extra fieldset
    #readonly_fields = 'date',
    #list_filter
    #actions
    #raw_id_fields = 'lines',



class ClientAdmin (admin.ModelAdmin):
    ''' Payer '''
    list_display = '__unicode__', 'contact', 'phone', 'email'
    #list_display = 'name', 'contact', 'phone', 'email'
    #fields = ('name', 'address', ('contact', 'email'), 'comment')

#    URLS = patterns ('',
#        (r'^my_view1/$', self.admin_site.admin_view (self.my_view1)),
#        (r'^my_view2/$', self.admin_site.admin_view (self.my_view2, cacheable=True)),
#    )

    # not in use
    def get_urls (self):
        return patterns ('',
            # @todo view that takes id to row?
            #(r'^my_view/$', self.my_view),
            (r'^my_view/$', self.admin_site.admin_view (self.my_view)),
            #(r'^my_view/$', self.admin_site.admin_view (self.my_view, cacheable=True)),
        ) + super (ClientAdmin, self).get_urls()

    # @todo howto use admin templates?
    def my_view (self, request):
        print request.path
        return HttpResponse ('Fuck you!')



admin.site.register (Account)
admin.site.register (Client, ClientAdmin)
admin.site.register (Invoice, InvoiceAdmin)



'''
@todo move to __init__.py
#from django.contrib.admin.sites import AdminSite
#class MyAdminSite (AdminSite):
class MyAdminSite (admin.sites.AdminSite):
    'Add some own views/urls to the default admin site'

#    def get_urls (self):
#        return patterns ('',
#            (r'^my_admin_view/$', self.my_view),
#        ) + super (MyAdminSite, self).get_urls()

    def my_view (self, *args):
        print args

admin.site = MyAdminSite()
'''
