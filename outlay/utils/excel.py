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
    html_file = "outlay/utils/updated_file.html"

    html_load_options = cells.HtmlLoadOptions()

    workbook = cells.Workbook(html_file, html_load_options)

    workbook.save("outlay/utils/output.xlsx")


def change_html(count_rows):
    with open("outlay/utils/Счет_на_оплату.html", "r",
              encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    element_to_remove = soup.find("div",
                                  string=lambda text: text and "Evaluation Only. Created with Aspose.Cells" in text)

    if element_to_remove:
        element_to_remove.decompose()

    target_row = soup.find("td", string=lambda
        text: text and "Блок газобетонный" in text)

    if target_row:
        parent_row = target_row.find_parent("tr")

        if parent_row:
            num_rows_to_add = count_rows - 1

            if num_rows_to_add >= 1:
                for _ in range(num_rows_to_add):
                    new_row = BeautifulSoup(str(parent_row), "html.parser")

                    parent_row.insert_after(new_row)

            with open("outlay/utils/updated_file.html",
                      "w",
                      encoding="utf-8") as file:
                file.write(str(soup))


def excel_to_html():
    file_path = "outlay/utils/Сметная стоимость №1 от 03.02.2025.xlsx"
    workbook = Workbook(file_path)

    save_options = HtmlSaveOptions()
    save_options.export_active_worksheet_only = True
    save_options.export_images_as_base64 = True

    html_file = "outlay/utils/Счет_на_оплату.html"
    workbook.save(html_file, save_options)


def create_outlay_excel(data, formset_data):
    excel_to_html()
    change_html(len(formset_data))
    html_to_excel()

    file_path = 'outlay/utils/output.xlsx'

    workbook = openpyxl.load_workbook(file_path)

    sheet = workbook["Смета"]

    sheet['BT1'] = f'Приложение № {data["number_outlay"]}'
    sheet['BT2'] = f'от {data["date"]}'
    sheet['BT3'] = data['base']
    sheet['A5'] = data['name']
    sheet['A7'] = data['name_construction']
    sheet['A8'] = f'по адресу {data["address"]}'
    sheet['A10'] = f'Срок выполнения работ: {data["work_time"]}'

    start_table_row = 12
    total_sum = 0

    for idx, table_data in enumerate(formset_data, 1):
        total_sum += table_data['amount']

        sheet[f'A{start_table_row + idx}'] = f'{idx}'
        sheet[f'E{start_table_row + idx}'] = table_data['name']
        sheet[f'BL{start_table_row + idx}'] = table_data['unit_of_measurement']
        sheet[f'BS{start_table_row + idx}'] = table_data['quantity']
        sheet[f'CB{start_table_row + idx}'] = table_data['price']
        sheet[f'CQ{start_table_row + idx}'] = table_data['amount']

    sheet[f'CQ{start_table_row + len(formset_data) + 1}'] = f'{total_sum}'
    sheet[f'CQ{start_table_row + len(formset_data) + 3}'] = f'{total_sum}'
    sheet[f'A{start_table_row + len(formset_data) + 5}'] = f'Итого: {total_sum}'

    sheet[
        f'BE{start_table_row + len(formset_data) + 9}'] = f'{data["organization"].naming}, ИНН/КПП {data["organization"].inn}/{data["organization"].kpp}'
    sheet[f'BE{start_table_row + len(formset_data) + 10}'] = f'{data["organization"].position_at_work}'
    sheet[f'BS{start_table_row + len(formset_data) + 11}'] = f'{data["organization"].supervisor}'

    sheet[
        f'B{start_table_row + len(formset_data) + 9}'] = f'{data["counterparty"].naming}, ИНН/КПП {data["counterparty"].inn}/{data["counterparty"].kpp}'
    sheet[f'Q{start_table_row + len(formset_data) + 11}'] = f'{data["counterparty"].naming}'

    if data['organization'].stamp:
        image_file = data['organization'].stamp
        img = Image(BytesIO(image_file.read()))

        img.width = 50
        img.height = 50

        sheet.add_image(img, f"CH{start_table_row + len(formset_data) + 13}")

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename=invoice.xlsx"
    workbook.save(response)
    return response
