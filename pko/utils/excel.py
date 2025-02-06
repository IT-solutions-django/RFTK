import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from openpyxl.worksheet.table import Table, TableStyleInfo
from aspose.cells import Workbook, HtmlSaveOptions
from bs4 import BeautifulSoup
import aspose.cells as cells
from openpyxl.drawing.image import Image
from io import BytesIO


def create_pko_excel(data, formset_data):
    file_path = 'pko/utils/Приходный кассовый ордер №1 от 06.02.2025 г..xlsx'

    workbook = openpyxl.load_workbook(file_path)

    sheet = workbook["Приходный кассовый ордер"]

    sheet['A4'] = f'{data["organization"].naming}'
    sheet['AN9'] = f'{data["name"]}'
    sheet['BA9'] = f'{data["date"]}'
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
    sheet['BR6'] = f'к приходному кассовому ордеру № {data["name"]} от {data["date"]}'
    sheet['CC8'] = f'{data["payer"]}'
    sheet['CC11'] = f'{data["base"]}'
    sheet['CC13'] = f'{data["summa"]}'
    sheet['BR14'] = ''
    sheet['BR29'] = f'{data["organization"].accountant}'
    sheet['BR35'] = f'{data["organization"].supervisor}'

    if data['organization'].stamp:
        image_file = data['organization'].stamp
        img = Image(BytesIO(image_file.read()))

        img.width = 50
        img.height = 50

        sheet.add_image(img, "BR23")

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename=invoice.xlsx"
    workbook.save(response)
    return response
