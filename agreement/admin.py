from django.contrib import admin
from invoice.models import AgreementDocument, TemplateDocument, LabelTemplateDocument, ValueLabel

admin.site.register(AgreementDocument)
admin.site.register(TemplateDocument)
admin.site.register(LabelTemplateDocument)
admin.site.register(ValueLabel)
