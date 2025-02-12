import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from openpyxl.worksheet.table import Table, TableStyleInfo
from aspose.cells import Workbook, HtmlSaveOptions, SaveFormat
from bs4 import BeautifulSoup
import aspose.cells as cells
from datetime import datetime
from openpyxl.drawing.image import Image
from io import BytesIO
import locale
from PyPDF2 import PdfReader, PdfWriter
import os


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


def create_utd_excel(data, formset_data, pdf=False):
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

    date_str = str(data['date'])
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d-%m-%Y")
    sheet['BK2'] = formatted_date

    sheet['AP6'] = data['organization'].naming
    sheet['AP7'] = data['organization'].address
    sheet['AP8'] = f'{data["organization"].inn} / {data["organization"].kpp}'
    sheet['AP9'] = f'{data["shipper"].naming}, {data["shipper"].address}'
    sheet['AP10'] = f'{data["consignee"].naming}, {data["consignee"].address}'
    sheet['AT11'] = data['payment_document']
    sheet['AX12'] = data['shipping_document']

    sheet['DL6'] = f'{data["counterparty"].naming}'
    sheet['DL7'] = f'{data["counterparty"].address}'
    sheet['DL8'] = f'{data["counterparty"].inn} / {data["counterparty"].kpp}'
    sheet['EE10'] = data['state_ID_contract']

    start_table_row = 21
    total_sum = 0
    total_sum_nds = 0

    if data['nds'] > 0:
        nds = int(data['nds'])
    else:
        nds = 0

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
        sheet[f'CX{start_table_row + idx}'] = f'{data["nds"]}%'
        if nds > 0:
            sheet[f'DD{start_table_row + idx}'] = f'{float(table_data["amount"]) * nds * 0.01}'
            total_sum_nds += float(table_data["amount"]) * nds * 0.01
        else:
            sheet[f'DD{start_table_row + idx}'] = f'{0}'
        sheet[
            f'DQ{start_table_row + idx}'] = f'{float(table_data["amount"]) + float(table_data["amount"]) * nds * 0.01}'
        sheet[f'ED{start_table_row + idx}'] = f'{table_data["country"]}'
        sheet[f'EJ{start_table_row + idx}'] = f'{table_data["country"]}'
        sheet[f'ET{start_table_row + idx}'] = f'{table_data["number_GTD"]}'

    sheet[f'DD{start_table_row + len(formset_data) + 1}'] = f'{round(total_sum_nds, 2)}'
    sheet[f'CE{start_table_row + len(formset_data) + 1}'] = f'{total_sum}'
    sheet[f'DQ{start_table_row + len(formset_data) + 1}'] = f'{float(total_sum) + float(total_sum_nds)}'

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
        f'A{start_table_row + len(formset_data) + 24}'] = f'{data["organization"].naming} ИНН/КПП {data["organization"].inn} / {data["organization"].kpp}'

    sheet[f'CF{start_table_row + len(formset_data) + 14}'] = ''
    sheet[f'EE{start_table_row + len(formset_data) + 14}'] = data["counterparty"].naming

    if data['date_of_receipt']:
        date_str = str(data['date_of_receipt'])
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d %B %Y").split(' ')
        sheet[f'DP{start_table_row + len(formset_data) + 16}'] = formatted_date[0]
        sheet[f'DV{start_table_row + len(formset_data) + 16}'] = formatted_date[1]
        sheet[f'ET{start_table_row + len(formset_data) + 16}'] = formatted_date[2]
    else:
        sheet[f'DP{start_table_row + len(formset_data) + 16}'] = ''
        sheet[f'DV{start_table_row + len(formset_data) + 16}'] = ''
        sheet[f'ET{start_table_row + len(formset_data) + 16}'] = ''

    sheet[f'CF{start_table_row + len(formset_data) + 21}'] = ''
    sheet[f'EE{start_table_row + len(formset_data) + 21}'] = data["counterparty"].naming

    sheet[
        f'CF{start_table_row + len(formset_data) + 24}'] = f'{data["counterparty"].naming} ИНН/КПП {data["counterparty"].inn} / {data["counterparty"].kpp}'

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
        if row[0].row in [start_table_row + len(formset_data) + 3, start_table_row + len(formset_data) + 14]:
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
