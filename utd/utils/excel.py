import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from openpyxl.worksheet.table import Table, TableStyleInfo
from aspose.cells import Workbook, HtmlSaveOptions
from bs4 import BeautifulSoup
import aspose.cells as cells
from datetime import datetime
from openpyxl.drawing.image import Image
from io import BytesIO


def html_to_excel():
    html_file = "utd/utils/updated_file.html"

    html_load_options = cells.HtmlLoadOptions()

    workbook = cells.Workbook(html_file, html_load_options)

    workbook.save("utd/utils/output.xlsx")


def change_html(count_rows):
    with open("utd/utils/Счет_на_оплату.html", "r",
              encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    element_to_remove = soup.find("div",
                                  string=lambda text: text and "Evaluation Only. Created with Aspose.Cells" in text)

    if element_to_remove:
        element_to_remove.decompose()

    target_row = soup.find("td", string=lambda
        text: text and "MacBook Air" in text)

    if target_row:
        parent_row = target_row.find_parent("tr")

        if parent_row:
            num_rows_to_add = count_rows - 1

            if num_rows_to_add >= 1:
                for _ in range(num_rows_to_add):
                    new_row = BeautifulSoup(str(parent_row), "html.parser")

                    parent_row.insert_after(new_row)

            with open("utd/utils/updated_file.html", "w",
                      encoding="utf-8") as file:
                file.write(str(soup))


def excel_to_html():
    file_path = "utd/utils/Универсальный передаточный документ №3 от 31.01.2025 г..xlsx"
    workbook = Workbook(file_path)

    save_options = HtmlSaveOptions()
    save_options.export_active_worksheet_only = True
    save_options.export_images_as_base64 = True

    html_file = "utd/utils/Счет_на_оплату.html"
    workbook.save(html_file, save_options)


def create_utd_excel(data, formset_data):
    excel_to_html()
    change_html(len(formset_data))
    html_to_excel()

    file_path = 'utd/utils/output.xlsx'

    workbook = openpyxl.load_workbook(file_path)

    sheet = workbook["УПД"]

    sheet['O2'] = 'УПД'
    sheet['AP2'] = data['name']
    sheet['BK2'] = data['date']
    sheet['AP6'] = data['organization'].naming
    sheet['AP7'] = data['organization'].address
    sheet['AP8'] = f"{data['organization'].inn} / {data['organization'].kpp}"
    sheet['AP9'] = f"{data['shipper'].naming}, {data['shipper'].address}"
    sheet['AP10'] = f"{data['consignee'].naming}, {data['consignee'].address}"
    sheet['AT11'] = data['payment_document']
    sheet['AX12'] = data['shipping_document']

    sheet['DL6'] = f'{data["counterparty"].naming}'
    sheet['DL7'] = f'{data["counterparty"].address}'
    sheet['DL8'] = f"{data['counterparty'].inn} / {data['counterparty'].kpp}"
    sheet['EE10'] = data['state_ID_contract']

    start_table_row = 21
    total_sum = 0

    for idx, table_data in enumerate(formset_data, 1):
        total_sum += table_data["amount"]

        sheet[f'A{start_table_row + idx}'] = f'{table_data["product_code"]}'
        sheet[f'N{start_table_row + idx}'] = f'{idx}'
        sheet[f'R{start_table_row + idx}'] = f'{table_data["name"]}'
        sheet[f'AQ{start_table_row + idx}'] = f'{table_data["product_type_code"]}'
        sheet[f'AW{start_table_row + idx}'] = f'{table_data["unit_of_measurement"]}'
        sheet[f'BA{start_table_row + idx}'] = f'{table_data["unit_of_measurement"]}'
        sheet[f'BN{start_table_row + idx}'] = f'{table_data["quantity"]}'
        sheet[f'BU{start_table_row + idx}'] = f'{table_data["price"]}'
        sheet[f'CE{start_table_row + idx}'] = f'{table_data["amount"]}'
        sheet[f'CR{start_table_row + idx}'] = f'{table_data["excise"]}'
        sheet[f'DQ{start_table_row + idx}'] = f'{table_data["amount"]}'
        sheet[f'ED{start_table_row + idx}'] = f'{table_data["country"]}'
        sheet[f'EJ{start_table_row + idx}'] = f'{table_data["country"]}'
        sheet[f'ET{start_table_row + idx}'] = f'{table_data["number_GTD"]}'

    sheet[f'CE{start_table_row + len(formset_data) + 1}'] = f'{total_sum}'
    sheet[f'DQ{start_table_row + len(formset_data) + 1}'] = f'{total_sum}'

    sheet[f'BS{start_table_row + len(formset_data) + 3}'] = data['organization'].supervisor
    sheet[f'EL{start_table_row + len(formset_data) + 3}'] = data['organization'].accountant

    sheet[f'AW{start_table_row + len(formset_data) + 9}'] = data['basis_for_transfer']
    sheet[f'AJ{start_table_row + len(formset_data) + 11}'] = data['data_transportation']

    sheet[f'A{start_table_row + len(formset_data) + 14}'] = data['organization'].position_at_work
    sheet[f'AZ{start_table_row + len(formset_data) + 14}'] = data['organization'].supervisor

    date_str = str(data['shipment_date'])
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d %B %Y").split(' ')
    sheet[f'AL{start_table_row + len(formset_data) + 16}'] = formatted_date[0]
    sheet[f'AR{start_table_row + len(formset_data) + 16}'] = formatted_date[1]
    sheet[f'BP{start_table_row + len(formset_data) + 16}'] = formatted_date[2]

    sheet[f'A{start_table_row + len(formset_data) + 21}'] = data['organization'].position_at_work
    sheet[f'AZ{start_table_row + len(formset_data) + 21}'] = data['organization'].supervisor

    sheet[
        f'A{start_table_row + len(formset_data) + 24}'] = f"{data['organization'].naming} ИНН/КПП {data['organization'].inn} / {data['organization'].kpp}"

    sheet[f'EE{start_table_row + len(formset_data) + 14}'] = data["counterparty"].naming

    date_str = str(data['date_of_receipt'])
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d %B %Y").split(' ')
    sheet[f'DP{start_table_row + len(formset_data) + 16}'] = formatted_date[0]
    sheet[f'DV{start_table_row + len(formset_data) + 16}'] = formatted_date[1]
    sheet[f'ET{start_table_row + len(formset_data) + 16}'] = formatted_date[2]

    sheet[f'EE{start_table_row + len(formset_data) + 21}'] = data["counterparty"].naming

    sheet[
        f'CF{start_table_row + len(formset_data) + 24}'] = f"{data['counterparty'].naming} ИНН/КПП {data['counterparty'].inn} / {data['counterparty'].kpp}"

    if data['organization'].stamp:
        image_file = data['organization'].stamp

        image_data = image_file.read()

        img_stream1 = BytesIO(image_data)
        img1 = Image(img_stream1)
        img1.width = 50
        img1.height = 50

        sheet.add_image(img1, f"E{start_table_row + len(formset_data) + 26}")

        img_stream2 = BytesIO(image_data)
        img2 = Image(img_stream2)
        img2.width = 50
        img2.height = 50

        sheet.add_image(img2, f"CI{start_table_row + len(formset_data) + 26}")

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename=invoice.xlsx"
    workbook.save(response)
    return response
