from django.contrib import admin
from .models import Client, Invoice, InvoiceLine
#from .forms import InvoiceInlineForm


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

    # @todo text&comment => extra fieldset
    #readonly_fields = 'date',
    #list_filter
    #actions
    #raw_id_fields = 'lines',


class ClientAdmin (admin.ModelAdmin):
    list_display = 'name', 'contact', 'email'
#    fields = ('name', 'address', ('contact', 'email'), 'comment')


admin.site.register (Client, ClientAdmin)
admin.site.register (Invoice, InvoiceAdmin)
#admin.site.register (InvoiceLine)
