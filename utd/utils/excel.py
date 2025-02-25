import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from openpyxl.worksheet.table import Table, TableStyleInfo
from aspose.cells import Workbook, HtmlSaveOptions, SaveFormat, License
from bs4 import BeautifulSoup
import aspose.cells as cells
from datetime import datetime
from openpyxl.drawing.image import Image
from io import BytesIO
import locale
from PyPDF2 import PdfReader, PdfWriter
import os

# license_as = License()
# license_as.set_license("lic/Aspose.TotalforPythonvia.NET.lic")

months_russian = [
    'Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
    'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'
]


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


def create_utd_excel(data, formset_data, pdf=False, watch_document=False):
    excel_to_html()
    change_html(len(formset_data))
    html_to_excel()

    file_path = 'utd/utils/output.xlsx'

    workbook = openpyxl.load_workbook(file_path)
    workbook.remove(workbook["Evaluation Warning"])

    sheet = workbook["УПД"]

    for row in sheet.iter_rows():
        if row[0].row in [7, 9, 10, 11, 12]:
            sheet.row_dimensions[row[0].row].height = 22

    sheet['O2'] = 'УПД'
    sheet['AP2'] = data['name']

    if data['type_document'] == 'Счет-фактура и передаточный документ(акт)':
        sheet['H7'] = '1'
    else:
        sheet['H7'] = '2'

    date_str = str(data['date'])
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d %B %Y").split(' ')

    month = date_obj.month
    month_russian = months_russian[month - 1]

    sheet['BK2'] = f'{formatted_date[0]} {month_russian} {formatted_date[2]}'

    sheet['AP6'] = data['organization'].naming
    sheet['AP7'] = data['organization'].address
    sheet['AP8'] = f'{data["organization"].inn} / {data["organization"].kpp}'
    if data["shipper"]:
        sheet['AP9'] = f'{data["shipper"].naming}, {data["shipper"].address}'
    else:
        sheet['AP9'] = ''
    if data["consignee"]:
        sheet['AP10'] = f'{data["consignee"].naming}, {data["consignee"].address}'
    else:
        sheet['AP10'] = ''
    sheet['AT11'] = data['payment_document']
    sheet['AX12'] = data['shipping_document']

    if data["counterparty"]:
        sheet['DL6'] = f'{data["counterparty"].naming}'
        sheet['DL7'] = f'{data["counterparty"].address}'
        sheet['DL8'] = f'{data["counterparty"].inn} / {data["counterparty"].kpp}'
    else:
        sheet['DL6'] = ''
        sheet['DL7'] = ''
        sheet['DL8'] = ''
    sheet['EE10'] = data['state_ID_contract']

    start_table_row = 21
    total_sum = 0
    total_sum_nds = 0
    total_sum_with_nds = 0

    if int(data['nds']) > 0:
        nds = int(data['nds'])
    else:
        nds = 0

    for idx, table_data in enumerate(formset_data, 1):
        sheet.row_dimensions[start_table_row + idx].height = 22

        total_sum += table_data["amount"]

        if table_data["product_code"]:
            sheet[f'A{start_table_row + idx}'] = f'{table_data["product_code"]}'
        else:
            sheet[f'A{start_table_row + idx}'] = ''
        sheet[f'N{start_table_row + idx}'] = f'{idx}'
        sheet[f'R{start_table_row + idx}'] = f'{table_data["name"]}'

        if table_data["product_type_code"]:
            sheet[f'AQ{start_table_row + idx}'] = f'{table_data["product_type_code"]}'
        else:
            sheet[f'AQ{start_table_row + idx}'] = ''

        sheet[f'AW{start_table_row + idx}'] = ''
        sheet[f'BA{start_table_row + idx}'] = f'{table_data["unit_of_measurement"]}'
        sheet[f'BN{start_table_row + idx}'] = f'{table_data["quantity"]}'
        sheet[f'BU{start_table_row + idx}'] = f'{table_data["price"]}'
        sheet[f'CE{start_table_row + idx}'] = f'{round(float(table_data["quantity"]) * float(table_data["price"]), 2)}'
        total_sum_with_nds += float(table_data["quantity"]) * float(table_data["price"])

        if table_data["excise"]:
            sheet[f'CR{start_table_row + idx}'] = f'{table_data["excise"]}'
        else:
            sheet[f'CR{start_table_row + idx}'] = 'Без акциза'
        if data["nds"] == '-1':
            sheet[f'CX{start_table_row + idx}'] = 'Без НДС'
        else:
            sheet[f'CX{start_table_row + idx}'] = f'{data["nds"]}%'
        if nds > 0:
            sheet[f'DD{start_table_row + idx}'] = f'{round(float(table_data["quantity"]) * float(table_data["price"]) * nds * 0.01, 2)}'
            total_sum_nds += float(table_data["quantity"]) * float(table_data["price"]) * nds * 0.01
        else:
            sheet[f'DD{start_table_row + idx}'] = f'{0}'
        sheet[
            f'DQ{start_table_row + idx}'] = f'{table_data["amount"]}'

        if table_data["country"]:
            sheet[f'ED{start_table_row + idx}'] = ''
            sheet[f'EJ{start_table_row + idx}'] = f'{table_data["country"]}'
        else:
            sheet[f'ED{start_table_row + idx}'] = ''
            sheet[f'EJ{start_table_row + idx}'] = ''

        if table_data["number_GTD"]:
            sheet[f'ET{start_table_row + idx}'] = f'{table_data["number_GTD"]}'
        else:
            sheet[f'ET{start_table_row + idx}'] = ''

    sheet[f'DD{start_table_row + len(formset_data) + 1}'] = f'{round(total_sum_nds, 2)}'
    sheet[f'CE{start_table_row + len(formset_data) + 1}'] = f'{round(total_sum_with_nds, 2)}'
    sheet[f'DQ{start_table_row + len(formset_data) + 1}'] = f'{float(total_sum)}'

    if data['organization']:
        sheet[f'BS{start_table_row + len(formset_data) + 3}'] = data['organization'].supervisor
        sheet[f'EL{start_table_row + len(formset_data) + 3}'] = data['organization'].accountant
    else:
        sheet[f'BS{start_table_row + len(formset_data) + 3}'] = ''
        sheet[f'EL{start_table_row + len(formset_data) + 3}'] = ''

    sheet[f'AW{start_table_row + len(formset_data) + 9}'] = data['basis_for_transfer']
    sheet[f'AJ{start_table_row + len(formset_data) + 11}'] = data['data_transportation']

    if data['organization']:
        sheet[f'A{start_table_row + len(formset_data) + 14}'] = data['organization'].position_at_work
        sheet[f'AZ{start_table_row + len(formset_data) + 14}'] = data['organization'].supervisor
    else:
        sheet[f'A{start_table_row + len(formset_data) + 14}'] = ''
        sheet[f'AZ{start_table_row + len(formset_data) + 14}'] = ''

    if data['shipment_date']:
        date_str = str(data['shipment_date'])
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d %B %Y").split(' ')

        month = date_obj.month
        month_russian = months_russian[month - 1]

        sheet[f'AL{start_table_row + len(formset_data) + 16}'] = formatted_date[0]
        sheet[f'AR{start_table_row + len(formset_data) + 16}'] = month_russian
        sheet[f'BP{start_table_row + len(formset_data) + 16}'] = formatted_date[2]
    else:
        sheet[f'AL{start_table_row + len(formset_data) + 16}'] = ''
        sheet[f'AR{start_table_row + len(formset_data) + 16}'] = ''
        sheet[f'BP{start_table_row + len(formset_data) + 16}'] = ''

    sheet[f'A{start_table_row + len(formset_data) + 21}'] = data['organization'].position_at_work
    sheet[f'AZ{start_table_row + len(formset_data) + 21}'] = data['organization'].supervisor

    sheet[
        f'A{start_table_row + len(formset_data) + 24}'] = ''

    sheet[f'CF{start_table_row + len(formset_data) + 14}'] = ''
    sheet[f'EE{start_table_row + len(formset_data) + 14}'] = ''

    if data['date_of_receipt']:
        date_str = str(data['date_of_receipt'])
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d %B %Y").split(' ')

        month = date_obj.month
        month_russian = months_russian[month - 1]

        sheet[f'DP{start_table_row + len(formset_data) + 16}'] = formatted_date[0]
        sheet[f'DV{start_table_row + len(formset_data) + 16}'] = month_russian
        sheet[f'ET{start_table_row + len(formset_data) + 16}'] = formatted_date[2]
    else:
        sheet[f'DP{start_table_row + len(formset_data) + 16}'] = ''
        sheet[f'DV{start_table_row + len(formset_data) + 16}'] = ''
        sheet[f'ET{start_table_row + len(formset_data) + 16}'] = ''

    sheet[f'CF{start_table_row + len(formset_data) + 21}'] = ''
    sheet[f'EE{start_table_row + len(formset_data) + 21}'] = ''

    sheet[
        f'CF{start_table_row + len(formset_data) + 24}'] = ''

    if data['organization'].stamp and data['is_stamp']:
        image_file = data['organization'].stamp

        image_data = image_file.read()

        img_stream1 = BytesIO(image_data)
        img1 = Image(img_stream1)
        img1.width = 45 * 2.83
        img1.height = 45 * 2.83

        sheet.add_image(img1, f"E{start_table_row + len(formset_data) + 24}")

    if data['organization'].signature and data['is_stamp']:
        image_file = data['organization'].signature

        image_data = image_file.read()

        img_stream = BytesIO(image_data)

        img1 = Image(img_stream)
        img1.width = 70
        img1.height = 30
        sheet.add_image(img1, f"AD{start_table_row + len(formset_data) + 14}")

        img_stream2 = BytesIO(image_data)
        img2 = Image(img_stream2)
        img2.width = 70
        img2.height = 30
        sheet.add_image(img2, f"AD{start_table_row + len(formset_data) + 21}")

        img_stream3 = BytesIO(image_data)
        img3 = Image(img_stream3)
        img3.width = 70
        img3.height = 30
        sheet.add_image(img3, f"AZ{start_table_row + len(formset_data) + 3}")

    for row in sheet.iter_rows():
        if row[0].row in [start_table_row + len(formset_data) + 3, start_table_row + len(formset_data) + 14,
                          start_table_row + len(formset_data) + 19, start_table_row + len(formset_data) + 21]:
            sheet.row_dimensions[row[0].row].height = 22

    if pdf:
        temp_excel_path = "utd/utils/invoice.xlsx"
        temp_pdf_path = "utd/utils/invoice.pdf"
        temp_modified_pdf_path = "utd/utils/invoice_modified.pdf"

        workbook.save(temp_excel_path)

        workbook_aspose = Workbook(temp_excel_path)
        workbook_aspose.save(temp_pdf_path, SaveFormat.PDF)

        reader = PdfReader(temp_pdf_path)
        writer = PdfWriter()

        pages_to_remove = [i for i in range(2, 80)]

        for i in range(len(reader.pages)):
            if i not in pages_to_remove:
                writer.add_page(reader.pages[i])

        with open(temp_modified_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)

        with open(temp_modified_pdf_path, "rb") as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type="application/pdf")
            if watch_document:
                response["Content-Disposition"] = "inline; filename=invoice.pdf"
            else:
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
