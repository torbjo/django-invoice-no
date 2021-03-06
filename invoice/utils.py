import os
from f60giro.invoice import render as render_invoice
from models import Invoice


# not in use. @todo move to f60giro
def make_pdf (invoice_id):
    '''Returns file-like object (StringIO) containing pdf data'''
    from cStringIO import StringIO
    fp = StringIO()
    size = fp.tell()
    fp.seek(0)
    return (size, fp)


# Converts data between Django model and what f60giro.invoice expects.
# Args: invoice_data, fileobj
def render_pdf (data, fp):
    '''Renders PDF of invoice into a file like object (fp) '''

    biller = data.account.__dict__
    logofile = os.path.join (os.getcwd(), '..', 'logo.png')
    if os.path.exists (logofile):
        biller['logo'] = logofile

    lines = []
    for l in data.invoiceline_set.all():
        lines.append ((l.text, l.quantity, l.amount))
    # @todo support passing invoice-lines as dict
    #invoice['lines'] = map (object.__dict__, data.invoiceline_set.all())

    invoice = data.__dict__
    invoice['invoice_no'] = data.invoice_no()
    invoice['payer'] = data.client.__dict__
    invoice['lines'] = lines
    invoice['giro'] = dict (
        account = data.account.account_no,
        add_static_background = True,
    )

    render_invoice (fp, biller, invoice)
