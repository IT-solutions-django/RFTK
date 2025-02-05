from django.contrib import admin
from .models import InvoiceDocument, InformationOrganization, BankDetailsOrganization, Buyer, BankDetailsBuyer, \
    InvoiceDocumentTable

admin.site.register(InvoiceDocument)

admin.site.register(InformationOrganization)
admin.site.register(BankDetailsOrganization)
admin.site.register(Buyer)
admin.site.register(BankDetailsBuyer)
admin.site.register(InvoiceDocumentTable)
