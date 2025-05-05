import convertapi
import tempfile
from django.http import HttpResponse
import os
import base64


def create_pko_registry_pdf(html, download_pdf=False):

    convertapi.api_credentials = 'secret_BJVUgKzV7vvvWN1m'

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as temp_html:
        temp_html.write(html)
        temp_html.flush()

        result = convertapi.convert('pdf', {'File': temp_html.name})
        result_pdf_file = result.save_files('output.pdf')[0]

        with open(result_pdf_file, "rb") as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type="application/pdf")
            if download_pdf:
                response["Content-Disposition"] = "attachment; filename=pko_registry.pdf"
            else:
                response["Content-Disposition"] = "inline; filename=pko_registry.pdf"

        os.remove(result_pdf_file)

        return response



