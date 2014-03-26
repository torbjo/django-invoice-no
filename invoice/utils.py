from f60giro.invoice import render as render_invoice
from models import Invoice


# not in use
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

    # @todo fix nuking of \r on the django model
    biller = data.account.__dict__
    biller['address'] = biller['address'].replace('\r', '')
    import os
    logofile = os.path.join (os.getcwd(), '..', 'logo.png')
    if os.path.exists (logofile):
        biller['logo'] = logofile

    payer = data.client.__dict__
    payer['address'] = payer['address'].replace('\r', '')

    # Note amount is Decimal while quantity is float. So have type
    # missmatch. Workaround is to cast to float.
    # Correct way: Fraction(o.amount) * Fraction(o.quantity)
    # or change o.quantity to Decimal datatype in Django
    lines = []
    for l in data.invoiceline_set.all():
        lines.append ((l.text, l.quantity, float(l.amount)))

    invoice = data.__dict__
    invoice['invoice_no'] = data.invoice_no()
    invoice['payer'] = payer
    invoice['lines'] = lines
    invoice['giro'] = dict (
        account = data.account.account_no,
        add_static_background = True,
    )

    render_invoice (fp, biller, invoice)
