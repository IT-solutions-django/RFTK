from django.contrib import admin
from invoice.models import ReconciliationDocument, ReconciliationDocumentTable

admin.site.register(ReconciliationDocument)
admin.site.register(ReconciliationDocumentTable)
