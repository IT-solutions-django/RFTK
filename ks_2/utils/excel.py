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
    html_file = "ks_2/utils/updated_file.html"

    html_load_options = cells.HtmlLoadOptions()

    workbook = cells.Workbook(html_file, html_load_options)

    workbook.save("ks_2/utils/output.xlsx")


def change_html(count_rows):
    with open("ks_2/utils/Счет_на_оплату.html", "r",
              encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    element_to_remove = soup.find("div",
                                  string=lambda text: text and "Evaluation Only. Created with Aspose.Cells" in text)

    if element_to_remove:
        element_to_remove.decompose()

    target_row = soup.find("td", string=lambda
        text: text and "Bonolit" in text)

    if target_row:
        parent_row = target_row.find_parent("tr")

        if parent_row:
            num_rows_to_add = count_rows - 1

            if num_rows_to_add >= 1:
                for _ in range(num_rows_to_add):
                    new_row = BeautifulSoup(str(parent_row), "html.parser")

                    parent_row.insert_after(new_row)

            with open("ks_2/utils/updated_file.html",
                      "w",
                      encoding="utf-8") as file:
                file.write(str(soup))


def excel_to_html():
    file_path = "ks_2/utils/КС-2 №1 от 03.02.2025 г..xlsx"
    workbook = Workbook(file_path)

    save_options = HtmlSaveOptions()
    save_options.export_active_worksheet_only = True
    save_options.export_images_as_base64 = True

    html_file = "ks_2/utils/Счет_на_оплату.html"
    workbook.save(html_file, save_options)


def create_ks2_excel(data, formset_data):
    excel_to_html()
    change_html(len(formset_data))
    html_to_excel()

    file_path = 'ks_2/utils/output.xlsx'

    workbook = openpyxl.load_workbook(file_path)

    sheet = workbook["КС-2"]

    sheet['K5'] = f'{data["investor"].naming}, {data["investor"].address}'
    sheet['Y7'] = f'{data["counterparty"].naming}, {data["counterparty"].address}'
    sheet['Y9'] = f'{data["organization"].naming}, {data["organization"].address}'
    sheet['EW8'] = ''
    sheet['K11'] = f'{data["name_construction"]}, {data["address_construction"]}'
    sheet['K13'] = f'{data["name_object"]}'
    sheet['EW14'] = f'{data["view_okdp"]}'
    sheet['EW16'] = f'{data["number_agreement"]}'
    sheet['BJ20'] = f'{data["name"]}'
    sheet['CB20'] = f'{data["date"]}'
    sheet['DA20'] = f'{data["period_from"]}'
    sheet['DN20'] = f'{data["period_by"]}'
    sheet['BX24'] = f'{data["price_outlay"]}'

    start_table_row = 29
    total_sum = 0
    total_q = 0

    for idx, table_data in enumerate(formset_data, 1):
        total_sum += table_data['amount']
        total_q += table_data['quantity']

        sheet[f'A{start_table_row + idx}'] = f'{idx}'
        sheet[f'I{start_table_row + idx}'] = table_data['number_outlay']
        sheet[f'R{start_table_row + idx}'] = table_data['name']
        sheet[f'CP{start_table_row + idx}'] = table_data['number_unit']
        sheet[f'DB{start_table_row + idx}'] = table_data['unit_of_measurement']
        sheet[f'DN{start_table_row + idx}'] = f"{table_data['quantity']}"
        sheet[f'ED{start_table_row + idx}'] = table_data['price']
        sheet[f'ET{start_table_row + idx}'] = table_data['amount']

    sheet[f'DN{start_table_row + len(formset_data) + 1}'] = f'{total_q}'
    sheet[f'ET{start_table_row + len(formset_data) + 1}'] = f'{total_sum}'

    sheet[f'Q{start_table_row + len(formset_data) + 4}'] = f'{data["organization"].position_at_work}'
    sheet[f'CK{start_table_row + len(formset_data) + 4}'] = f'{data["organization"].supervisor}'

    sheet[f'CK{start_table_row + len(formset_data) + 8}'] = f'{data["counterparty"].naming}'

    if data['organization'].stamp:
        image_file = data['organization'].stamp
        img = Image(BytesIO(image_file.read()))

        img.width = 50
        img.height = 50

        sheet.add_image(img, f"U{start_table_row + len(formset_data) + 6}")

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename=invoice.xlsx"
    workbook.save(response)
    return response
