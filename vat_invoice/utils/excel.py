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


def html_to_excel():
    html_file = "vat_invoice/utils/updated_file.html"

    html_load_options = cells.HtmlLoadOptions()

    workbook = cells.Workbook(html_file, html_load_options)

    workbook.save("vat_invoice/utils/output.xlsx")


def change_html(count_rows):
    with open("vat_invoice/utils/Счет_на_оплату.html", "r",
              encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    element_to_remove = soup.find("div",
                                  string=lambda text: text and "Evaluation Only. Created with Aspose.Cells" in text)

    if element_to_remove:
        element_to_remove.decompose()

    target_row = soup.find("td", string=lambda
        text: text and "Кола" in text)

    if target_row:
        parent_row = target_row.find_parent("tr")

        if parent_row:
            num_rows_to_add = count_rows - 1

            if num_rows_to_add >= 1:
                for _ in range(num_rows_to_add):
                    new_row = BeautifulSoup(str(parent_row), "html.parser")

                    parent_row.insert_after(new_row)

            with open("vat_invoice/utils/updated_file.html", "w",
                      encoding="utf-8") as file:
                file.write(str(soup))


def excel_to_html():
    file_path = "vat_invoice/utils/Счет-фактура №2 от 01.02.2025 г..xlsx"
    workbook = Workbook(file_path)

    save_options = HtmlSaveOptions()
    save_options.export_active_worksheet_only = True
    save_options.export_images_as_base64 = True

    html_file = "vat_invoice/utils/Счет_на_оплату.html"
    workbook.save(html_file, save_options)


def create_vat_invoice_excel(data, formset_data):
    excel_to_html()
    change_html(len(formset_data))
    html_to_excel()

    file_path = 'vat_invoice/utils/output.xlsx'

    workbook = openpyxl.load_workbook(file_path)

    sheet = workbook["Счет-фактура"]

    sheet['A2'] = 'Счет-фактура'
    sheet['AF2'] = data['name']
    sheet['BF2'] = data['date']
    sheet['AF6'] = data['organization'].naming
    sheet['AF7'] = data['organization'].address
    sheet['AF8'] = f"{data['organization'].inn} / {data['organization'].kpp}"
    sheet['AF9'] = f"{data['shipper'].naming}, {data['shipper'].address}"
    sheet['AF10'] = f"{data['consignee'].naming}, {data['consignee'].address}"
    sheet['AF11'] = data['payment_document']
    sheet['AJ12'] = data['shipping_document']

    sheet['DG6'] = f'{data["counterparty"].naming}'
    sheet['DG7'] = f'{data["counterparty"].address}'
    sheet['DG8'] = f"{data['counterparty'].inn} / {data['counterparty'].kpp}"
    sheet['DV10'] = data['state_ID_contract']

    start_table_row = 25
    total_sum = 0

    for idx, table_data in enumerate(formset_data, 1):
        total_sum += table_data["amount"]

        sheet[f'A{start_table_row + idx}'] = f'{idx}'
        sheet[f'E{start_table_row + idx}'] = f'{table_data["name"]}'
        sheet[f'AD{start_table_row + idx}'] = f'{table_data["product_type_code"]}'
        sheet[f'AK{start_table_row + idx}'] = f'{table_data["unit_of_measurement"]}'
        sheet[f'AP{start_table_row + idx}'] = f'{table_data["unit_of_measurement"]}'
        sheet[f'BD{start_table_row + idx}'] = f'{table_data["quantity"]}'
        sheet[f'BL{start_table_row + idx}'] = f'{table_data["price"]}'
        sheet[f'BW{start_table_row + idx}'] = f'{table_data["amount"]}'
        sheet[f'CL{start_table_row + idx}'] = f'{table_data["excise"]}'
        sheet[f'DN{start_table_row + idx}'] = f'{table_data["amount"]}'
        sheet[f'EC{start_table_row + idx}'] = f'{table_data["country"]}'
        sheet[f'EK{start_table_row + idx}'] = f'{table_data["country"]}'
        sheet[f'ES{start_table_row + idx}'] = f'{table_data["number_GTD"]}'

    sheet[f'BW{start_table_row + len(formset_data) + 1}'] = f'{total_sum}'
    sheet[f'DN{start_table_row + len(formset_data) + 1}'] = f'{total_sum}'

    sheet[f'AW{start_table_row + len(formset_data) + 3}'] = data['organization'].supervisor
    sheet[f'EB{start_table_row + len(formset_data) + 3}'] = data['organization'].accountant

    if data['organization'].stamp:
        image_file = data['organization'].stamp
        img = Image(BytesIO(image_file.read()))

        img.width = 50
        img.height = 50

        sheet.add_image(img, f"CY{start_table_row + len(formset_data) + 8}")

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename=invoice.xlsx"
    workbook.save(response)
    return response
