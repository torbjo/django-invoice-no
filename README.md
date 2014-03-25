Django Invoice Norwegian
========================

Django app to manage invoices and create standard Norwegian F60 giro.

It depends on http://github.com/torbjo/f60-giro.git to do the actual
PDF rendering (using ReportLabs). Do this to install it:

    $ cd invoice
    $ git clone github.com:torbjo/f60-giro.git f60-giro.git
    $ ln -s f60-giro.git/f60 f60giro


This is work in progress, but usable ...
