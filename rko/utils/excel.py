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


def create_rko_excel(data, formset_data):
    file_path = 'rko/utils/Расходный кассовый ордер №1 от 06.02.2025 г..xlsx'

    workbook = openpyxl.load_workbook(file_path)

    sheet = workbook["Расходный кассовый ордер"]

    for col in sheet.columns:
        try:
            sheet.column_dimensions[col[0].column_letter].width = 1.3
        except:
            continue

    for row in sheet.iter_rows():
        if row[0].row == 2:
            sheet.row_dimensions[row[0].row].height = 29
        else:
            sheet.row_dimensions[row[0].row].height = 16

    sheet['A4'] = f'{data["organization"].naming}'
    sheet['BX10'] = f'{data["name"]}'
    sheet['CO10'] = f'{data["date"]}'
    sheet['W15'] = f'{data["account_debit"]}'
    sheet['BK15'] = f'{data["account_loan"]}'
    sheet['BX15'] = f'{data["summa"]}'
    sheet['I17'] = f'{data["payer"]}'
    sheet['L19'] = f'{data["base"]}'
    sheet['H21'] = f'{data["summa"]} рублей'
    sheet['M23'] = f'{data["annex"]}'
    sheet['T25'] = f'{data["organization"].position_at_work}'
    sheet['BZ25'] = f'{data["organization"].supervisor}'
    sheet['AW28'] = f'{data["organization"].accountant}'
    sheet['E37'] = f'{data["passport"]}'
    sheet['AO42'] = f'{data["organization"].supervisor}'

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename=invoice.xlsx"
    workbook.save(response)
    return response
