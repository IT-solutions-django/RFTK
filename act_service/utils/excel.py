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
    html_file = "act_service/utils/updated_file.html"

    html_load_options = cells.HtmlLoadOptions()

    workbook = cells.Workbook(html_file, html_load_options)

    workbook.save("act_service/utils/output.xlsx")


def change_html(count_rows):
    with open("act_service/utils/Счет_на_оплату.html", "r",
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

            with open("act_service/utils/updated_file.html",
                      "w",
                      encoding="utf-8") as file:
                file.write(str(soup))


def excel_to_html():
    file_path = "act_service/utils/Акт оказания услуг №1 от 05.02.2025 г..xlsx"
    workbook = Workbook(file_path)

    save_options = HtmlSaveOptions()
    save_options.export_active_worksheet_only = True
    save_options.export_images_as_base64 = True

    html_file = "act_service/utils/Счет_на_оплату.html"
    workbook.save(html_file, save_options)


def create_act_service_excel(data, formset_data):
    try:
        excel_to_html()
        change_html(len(formset_data))
        html_to_excel()

        file_path = 'act_service/utils/output.xlsx'

        workbook = openpyxl.load_workbook(file_path)

        sheet = workbook["Акт оказания услуг"]

        sheet['A2'] = f'Акт № {data["name"]} от {data["date"]}'
        sheet['A4'] = f'выполненных работ / оказанных услуг по договору {data["agreement"]}'
        sheet['A5'] = f'за {data["payment_for"]}'
        sheet[
            'Q7'] = f'{data["organization"].naming}, ИНН {data["organization"].inn}, КПП {data["organization"].kpp}, {data["organization"].address}'
        sheet[
            'Q9'] = f'{data["counterparty"].naming}, ИНН {data["counterparty"].inn}, КПП {data["counterparty"].kpp}, {data["counterparty"].address}'

        start_table_row = 11
        total_sum = 0

        for idx, table_data in enumerate(formset_data, 1):
            total_sum += table_data['amount']

            sheet[f'A{start_table_row + idx}'] = f'{idx}'
            sheet[f'E{start_table_row + idx}'] = table_data['name']
            sheet[f'BB{start_table_row + idx}'] = table_data['quantity']
            sheet[f'BM{start_table_row + idx}'] = table_data['unit_of_measurement']
            sheet[f'BW{start_table_row + idx}'] = f"{table_data['price']}"
            sheet[f'CN{start_table_row + idx}'] = table_data['amount']

        sheet[f'CN{start_table_row + len(formset_data) + 1}'] = f'{total_sum}'

        sheet[
            f'A{start_table_row + len(formset_data) + 4}'] = f'Всего оказано услуг {len(formset_data)} на сумму {total_sum} руб.'
        sheet[
            f'A{start_table_row + len(formset_data) + 6}'] = ''

        sheet[f'A{start_table_row + len(formset_data) + 11}'] = f'{data["organization"].position_at_work}'
        sheet[f'Q{start_table_row + len(formset_data) + 14}'] = f'{data["organization"].supervisor}'

        sheet[f'BT{start_table_row + len(formset_data) + 14}'] = f'{data["counterparty"].naming}'

        if data['organization'].stamp:
            image_file = data['organization'].stamp
            img = Image(BytesIO(image_file.read()))

            img.width = 50
            img.height = 50

            sheet.add_image(img, f"R{start_table_row + len(formset_data) + 17}")

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f"attachment; filename=invoice.xlsx"
        workbook.save(response)
        return response
    except Exception as e:
        print(e)
