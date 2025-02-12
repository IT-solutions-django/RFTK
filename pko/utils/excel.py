import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from openpyxl.worksheet.table import Table, TableStyleInfo
from aspose.cells import Workbook, HtmlSaveOptions, SaveFormat
from bs4 import BeautifulSoup
import aspose.cells as cells
from openpyxl.drawing.image import Image
from io import BytesIO
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
import os


def create_pko_excel(data, formset_data, pdf=False):
    file_path = 'pko/utils/Приходный кассовый ордер №1 от 06.02.2025 г..xlsx'

    workbook = openpyxl.load_workbook(file_path)

    sheet = workbook["Приходный кассовый ордер"]

    for row in sheet.iter_rows():
        if row[0].row == 2:
            sheet.row_dimensions[row[0].row].height = 25

    sheet['A4'] = f'{data["organization"].naming}'
    sheet['AN9'] = f'{data["name"]}'

    date_str = str(data['date'])
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d-%m-%Y")
    sheet['BA9'] = f'{formatted_date}'

    sheet['A15'] = f'{data["account_debit"]}'
    sheet['V15'] = f'{data["account_loan"]}'
    sheet['AP15'] = f'{data["summa"]}'
    sheet['L17'] = f'{data["payer"]}'
    sheet['L19'] = f'{data["base"]}'
    sheet['I23'] = f'{data["summa"]} рублей'
    sheet['M27'] = f'{data["annex"]}'
    sheet['AK32'] = f'{data["organization"].accountant}'
    sheet['AK35'] = f'{data["organization"].supervisor}'
    sheet['BR2'] = f'{data["organization"].naming}'

    date_str = str(data['date'])
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d-%m-%Y")
    sheet['BR6'] = f'к приходному кассовому ордеру № {data["name"]} от {formatted_date}'

    sheet['CC8'] = f'{data["payer"]}'
    sheet['CC11'] = f'{data["base"]}'
    sheet['CC13'] = f'{data["summa"]} рублей'
    sheet['BR14'] = ''
    sheet['BR29'] = f'{data["organization"].accountant}'
    sheet['BR35'] = f'{data["organization"].supervisor}'

    if data['organization'].stamp and data['is_stamp']:
        image_file = data['organization'].stamp
        img = Image(BytesIO(image_file.read()))

        img.width = 45 * 2.83
        img.height = 45 * 2.83

        sheet.add_image(img, "BR17")

    if data['organization'].signature and data['is_stamp']:
        image_file = data['organization'].signature

        image_data = image_file.read()

        img_stream = BytesIO(image_data)

        img1 = Image(img_stream)
        img1.width = 70
        img1.height = 25
        sheet.add_image(img1, "T35")

        img_stream_2 = BytesIO(image_data)

        img2 = Image(img_stream_2)
        img2.width = 70
        img2.height = 25
        sheet.add_image(img2, "BR33")

    if pdf:
        temp_excel_path = "pko/utils/invoice.xlsx"
        temp_pdf_path = "pko/utils/invoice.pdf"
        temp_modified_pdf_path = "pko/utils/invoice_modified.pdf"

        workbook.save(temp_excel_path)

        workbook_aspose = Workbook(temp_excel_path)
        workbook_aspose.save(temp_pdf_path, SaveFormat.PDF)

        reader = PdfReader(temp_pdf_path)
        writer = PdfWriter()

        pages_to_remove = [i for i in range(1, 55)]

        for i in range(len(reader.pages)):
            if i not in pages_to_remove:
                writer.add_page(reader.pages[i])

        with open(temp_modified_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)

        with open(temp_modified_pdf_path, "rb") as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type="application/pdf")
            response["Content-Disposition"] = "attachment; filename=invoice.pdf"

        os.remove(temp_excel_path)
        os.remove(temp_pdf_path)
        os.remove(temp_modified_pdf_path)

        return response

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename=invoice.xlsx"
    workbook.save(response)
    return response
