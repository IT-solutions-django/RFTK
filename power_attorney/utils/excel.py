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
    html_file = "power_attorney/utils/updated_file.html"

    html_load_options = cells.HtmlLoadOptions()

    workbook = cells.Workbook(html_file, html_load_options)

    workbook.save("power_attorney/utils/output.xlsx")


def change_html(count_rows):
    with open("power_attorney/utils/Счет_на_оплату.html", "r",
              encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    element_to_remove = soup.find("div",
                                  string=lambda text: text and "Evaluation Only. Created with Aspose.Cells" in text)

    if element_to_remove:
        element_to_remove.decompose()

    target_row = soup.find("td", string=lambda
        text: text and "Beton" in text)

    if target_row:
        parent_row = target_row.find_parent("tr")

        if parent_row:
            num_rows_to_add = count_rows - 1

            if num_rows_to_add >= 1:
                for _ in range(num_rows_to_add):
                    new_row = BeautifulSoup(str(parent_row), "html.parser")

                    parent_row.insert_after(new_row)

            with open("power_attorney/utils/updated_file.html",
                      "w",
                      encoding="utf-8") as file:
                file.write(str(soup))


def excel_to_html():
    file_path = "power_attorney/utils/Доверенность №1 от 05.02.2025 г..xlsx"
    workbook = Workbook(file_path)

    save_options = HtmlSaveOptions()
    save_options.export_active_worksheet_only = True
    save_options.export_images_as_base64 = True

    html_file = "power_attorney/utils/Счет_на_оплату.html"
    workbook.save(html_file, save_options)


def create_power_attorney_excel(data, formset_data):
    excel_to_html()
    change_html(len(formset_data))
    html_to_excel()

    file_path = 'power_attorney/utils/output.xlsx'

    workbook = openpyxl.load_workbook(file_path)

    sheet = workbook["Доверенность"]

    for col in sheet.columns:
        try:
            sheet.column_dimensions[col[0].column_letter].width = 1
        except:
            continue

    sheet['A3'] = f'{data["name"]}'
    sheet['O3'] = f'{data["date"]}'
    sheet['Z3'] = f'{data["validity_period"]}'
    sheet['AK3'] = f'{data["person_power"]}'
    sheet['A5'] = f'{data["to_receive_from"]}'
    sheet['AS5'] = f'{data["according_document"]}'

    sheet[
        'M15'] = f'{data["organization"].naming}, ИНН {data["organization"].inn} КПП {data["organization"].kpp}, {data["organization"].address}'
    sheet['A17'] = f'Доверенность № {data["name"]}'
    sheet[
        'A23'] = f'{data["organization"].naming}, ИНН {data["organization"].inn} КПП {data["organization"].kpp}, {data["organization"].address}'
    sheet[
        'A26'] = f'{data["organization"].naming}, ИНН {data["organization"].inn} КПП {data["organization"].kpp}, {data["organization"].address}'

    sheet[
        'A29'] = f'Счет № {data["bank_organization"].current_account} в {data["bank_organization"].naming}, {data["bank_organization"].location}, БИК {data["bank_organization"].bic}, корр.сч. {data["bank_organization"].correspondent_account}'

    sheet['A31'] = f'Доверенность выдана: {data["person_power"]}'
    sheet['A33'] = f'Паспорт: {data["passport_series"]} {data["passport_number"]}'
    sheet['A35'] = f'Кем выдан: {data["issued_by"]}'
    sheet['A37'] = f'Дата выдачи: {data["date_issue"]}'
    sheet['A39'] = f'На получение от {data["to_receive_from"]}'
    sheet['A41'] = f'материальных ценностей по {data["according_document"]}'

    start_table_row = 45

    for idx, table_data in enumerate(formset_data, 1):
        sheet[f'A{start_table_row + idx}'] = f'{idx}'
        sheet[f'E{start_table_row + idx}'] = table_data['name']
        sheet[f'CG{start_table_row + idx}'] = table_data['unit_of_measurement']
        sheet[f'CN{start_table_row + idx}'] = f"{table_data['quantity']}"

    sheet[f'BA{start_table_row + len(formset_data) + 5}'] = f'{data["organization"].supervisor}'

    sheet[f'BA{start_table_row + len(formset_data) + 9}'] = f'{data["organization"].accountant}'

    if data['organization'].stamp:
        image_file = data['organization'].stamp
        img = Image(BytesIO(image_file.read()))

        img.width = 50
        img.height = 50

        sheet.add_image(img, f"T{start_table_row + len(formset_data) + 7}")

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f"attachment; filename=invoice.xlsx"
    workbook.save(response)
    return response
