import logging
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

# Настройка логирования для вывода ошибок в консоль
logging.basicConfig(level=logging.DEBUG)

def html_to_excel():
    try:
        html_file = "invoice/utils/updated_file.html"
        html_load_options = cells.HtmlLoadOptions()
        workbook = cells.Workbook(html_file, html_load_options)
        workbook.save("invoice/utils/output.xlsx")
    except Exception as e:
        logging.error(f"Ошибка в html_to_excel: {e}")
        raise

def change_html(count_rows):
    try:
        with open("invoice/utils/Счет_на_оплату.html", "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        element_to_remove = soup.find("div", string=lambda text: text and "Evaluation Only. Created with Aspose.Cells" in text)

        if element_to_remove:
            element_to_remove.decompose()

        target_row = soup.find("td", string=lambda text: text and "Лента-герметик самоклеящаяся Технониколь Никобенд, красная, 15х1000 см" in text)

        if target_row:
            parent_row = target_row.find_parent("tr")

            if parent_row:
                num_rows_to_add = count_rows - 1
                if num_rows_to_add >= 1:
                    for _ in range(num_rows_to_add):
                        new_row = BeautifulSoup(str(parent_row), "html.parser")
                        parent_row.insert_after(new_row)

            with open("invoice/utils/updated_file.html", "w", encoding="utf-8") as file:
                file.write(str(soup))
    except Exception as e:
        logging.error(f"Ошибка в change_html: {e}")
        raise

def excel_to_html():
    try:
        file_path = "invoice/utils/Счет на оплату №3 от 31.01.2025 г..xlsx"
        workbook = Workbook(file_path)
        save_options = HtmlSaveOptions()
        save_options.export_active_worksheet_only = True
        save_options.export_images_as_base64 = True
        html_file = "invoice/utils/Счет_на_оплату.html"
        workbook.save(html_file, save_options)
    except Exception as e:
        logging.error(f"Ошибка в excel_to_html: {e}")
        raise

def create_invoice_excel(data, organization_data, formset_data):
    try:
        excel_to_html()
        change_html(len(formset_data))
        html_to_excel()

        file_path = 'invoice/utils/output.xlsx'
        workbook = openpyxl.load_workbook(file_path)

        sheet = workbook["Счет на оплату"]

        sheet['A1'] = organization_data['name']
        sheet['A2'] = organization_data['address']
        sheet['A3'] = f"ИНН/КПП {organization_data['inn']} / {organization_data['kpp']}"
        sheet['A4'] = f"ОГРН {organization_data['ogrn']}"

        sheet['A8'] = organization_data['name']

        sheet['A10'] = organization_data['name']
        sheet[
            'A11'] = f"{organization_data['address']}\nИНН/КПП {organization_data['kpp']}/{organization_data['kpp']}\nОГРН {organization_data['ogrn']}\n{data['bank_organization'].naming}, {data['bank_organization'].location}\nКор. счет {data['bank_organization'].correspondent_account}\nБИК {data['bank_organization'].bic}"

        sheet['AY10'] = f"{data['counterparty'].naming}"
        sheet[
            'AY11'] = f"{data['counterparty'].address}\nИНН {data['counterparty'].inn}\nОГРН {data['counterparty'].ogrn}\n{data['bank_counterparty'].naming}, {data['bank_counterparty'].location}\nКор. счет {data['bank_counterparty'].correspondent_account}\nБИК {data['bank_counterparty'].bic}"

        sheet['A13'] = f"{data['name']} от {data['date']}"

        sheet['A15'] = f"за {data['payment_for']}"

        start_table_row = 17

        sheet[f'CG{start_table_row}'] = 'Скидка'

        total_sum = 0

        for idx, table_data in enumerate(formset_data, 1):
            total_sum += table_data["amount"]

            sheet[f'A{start_table_row + idx}'] = f'{idx}'
            sheet[f'E{start_table_row + idx}'] = f'{table_data["name"]}'
            sheet[f'BB{start_table_row + idx}'] = f'{table_data["price"]}'
            sheet[f'BP{start_table_row + idx}'] = f'{table_data["quantity"]}'
            sheet[f'BY{start_table_row + idx}'] = f'{table_data["unit_of_measurement"]}'
            sheet[f'CG{start_table_row + idx}'] = f'{table_data["discount"]}'
            sheet[f'CN{start_table_row + idx}'] = f'{table_data["amount"]}'

        sheet[f'A{start_table_row + len(formset_data) + 1}'] = 'Итого'
        sheet[f'CN{start_table_row + len(formset_data) + 1}'] = f'{total_sum}'
        sheet[f'A{start_table_row + len(formset_data) + 2}'] = f'{data["agreement"]}'

        sheet[f'A{start_table_row + len(formset_data) + 7}'] = organization_data['position_at_work']
        sheet[f'AI{start_table_row + len(formset_data) + 7}'] = organization_data['supervisor']
        sheet[f'AI{start_table_row + len(formset_data) + 9}'] = organization_data['accountant']

        if data['organization'].stamp:
            image_file = data['organization'].stamp
            img = Image(BytesIO(image_file.read()))

            img.width = 50
            img.height = 50

            sheet.add_image(img, f"CU{start_table_row + len(formset_data) + 8}")

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f"attachment; filename=invoice.xlsx"
        workbook.save(response)
        return response

    except Exception as e:
        logging.error(f"Ошибка в create_invoice_excel: {e}")
        raise
