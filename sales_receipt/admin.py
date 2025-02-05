from django.contrib import admin
from invoice.models import SalesReceiptDocument, SalesReceiptDocumentTable

admin.site.register(SalesReceiptDocument)
admin.site.register(SalesReceiptDocumentTable)
