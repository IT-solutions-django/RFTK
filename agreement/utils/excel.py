import convertapi
import tempfile
from django.http import HttpResponse
import os
import base64


def create_agreement_excel(html, organization, is_stamp, download_pdf=False):
    # if organization and organization.stamp and is_stamp:
    #     stamp_data = organization.stamp.read()
    #     stamp_base64 = base64.b64encode(stamp_data).decode('utf-8')
    #     stamp_html = f'<img src="data:image/png;base64,{stamp_base64}" style="height:128px; width:128px; object-fit:contain">'
    #     html = html.replace('{print_stamp}', stamp_html)
    #
    #     sign_data = organization.signature.read()
    #     sign_base64 = base64.b64encode(sign_data).decode('utf-8')
    #     sign_html = f'<img src="data:image/png;base64,{sign_base64}" style="height:auto; width:80px; object-fit:contain">'
    #     html = html.replace('{print_sign_director}', sign_html)
    # else:
    #     html = html.replace('{print_stamp}', 'М.П.')
    #     html = html.replace('{print_sign_director}', '')

    convertapi.api_credentials = 'secret_K6wBgPb3icOrsjW5'

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as temp_html:
        temp_html.write(html)
        temp_html.flush()

        result = convertapi.convert('pdf', {'File': temp_html.name})
        result_pdf_file = result.save_files('output.pdf')[0]

        with open(result_pdf_file, "rb") as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type="application/pdf")
            if download_pdf:
                response["Content-Disposition"] = "attachment; filename=agreement.pdf"
            else:
                response["Content-Disposition"] = "inline; filename=agreement.pdf"

        os.remove(result_pdf_file)

        return response



