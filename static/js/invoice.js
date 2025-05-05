document.addEventListener('DOMContentLoaded', function() {

    new Sortable(document.getElementById('formset-body'), {
        handle: '.drag-handle',
        animation: 150,
        ghostClass: 'bg-light',
        onEnd: function() {
            updateRowNumbers();
        }
    });

    function updateRowNumbers() {
        document.querySelectorAll("#formset-body .row-number").forEach((cell, index) => {
            cell.textContent = index + 1;
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const codeToUnitMap = {
    // Штучные единицы
    '796': 'шт',    // Штука
    '839': 'пар',   // Пара (2 шт)
    '778': 'упак',  // Упаковка

    // Весовые единицы
    '166': 'кг',    // Килограмм
    '168': 'т',     // Тонна
    '163': 'г',     // Грамм

    // Объемные единицы
    '112': 'л',     // Литр
    '137': 'м3',    // Кубический метр

    // Длина
    '006': 'м',     // Метр
    '039': 'км',    // Километр
    '041': 'мм',    // Миллиметр

    // Технические единицы
    '055': 'м2',    // Квадратный метр
    '111': 'см3',   // Кубический сантиметр

    // Тара
    '114': 'бут',   // Бутылка
    '116': 'банк',  // Банка
    '131': 'фл',    // Флакон

    // Для жидкостей
    '122': 'бал',   // Баллон
    '132': 'туб',   // Тюбик

    // Популярные в торговле
    '250': 'рул',   // Рулон
    '356': 'час',   // Час
    '366': 'сут',   // Сутки
    '536': 'компл', // Комплект
    '831': 'лист',  // Лист
    };

    document.querySelectorAll('.code_unit input').forEach(input => {
        const datalist = document.createElement('datalist');
        datalist.id = `datalist-${Math.random().toString(36).substr(2, 9)}`;

        Object.entries(codeToUnitMap).forEach(([code, unit]) => {
            const option = document.createElement('option');
            option.value = code;
            option.textContent = `${code} - ${unit}`;
            datalist.appendChild(option);
        });

        document.body.appendChild(datalist);
        input.setAttribute('list', datalist.id);

        input.addEventListener('change', function() {
            const code = this.value;
            const unit = codeToUnitMap[code];

            if (unit) {
                const row = this.closest('tr');
                const unitInput = row.querySelector('.unit_of_measurement input');
                if (unitInput) {
                    unitInput.value = unit;
                }
            }
        });
    });
});

$(document).ready(function () {
    $("#id_organization-inn").on("input", function () {
        let query = $(this).val();
        if (query.length < 3) {
            $("#innSuggestions").empty().hide();
            return;
        }

        $.ajax({
            url: "/inn_autocomplete",
            data: { query: query },
            dataType: "json",
            success: function (data) {
                let suggestions = data.suggestions;
                let dropdown = $("#innSuggestions");
                dropdown.empty();

                if (suggestions.length) {
                    suggestions.forEach(function (item) {
                        dropdown.append(
                            `<div class="dropdown-item dropdown-item-inn" data-inn="${item.inn}">${item.value}</div>`
                        );
                    });

                    dropdown.show();
                } else {
                    dropdown.hide();
                }
            },
        });
    });

    $(document).on("click", ".dropdown-item-inn", function () {
        let inn = $(this).data("inn");
        $("#id_organization-inn").val(inn);
        $("#innSuggestions").hide();

        fetch(`/find-company/?inn=${inn}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("id_organization-naming").value = "";
            document.getElementById("id_organization-kpp").value = "";
            document.getElementById("id_organization-ogrn").value = "";
            document.getElementById("id_organization-address").value = "";
            document.getElementById("id_organization-position_at_work").value = "";
            document.getElementById("id_organization-supervisor").value = "";
            if (data.success) {
                if (data.type == 'Юридическое лицо') {
                    document.getElementById("id_organization-naming").value = data.name;
                    document.getElementById("id_organization-kpp").value = data.kpp;
                    document.getElementById("id_organization-ogrn").value = data.ogrn;
                    document.getElementById("id_organization-address").value = data.address;
                    document.getElementById("id_organization-position_at_work").value = data.position_at_work;
                    document.getElementById("id_organization-supervisor").value = data.supervisor;
                    const type_selection = document.getElementById("type_selection");
                    if (type_selection) {
                        document.getElementById("type_selection").value = "ogrn";
                    }
                }
                else {
                    document.getElementById("id_organization-naming").value = data.name;
                    document.getElementById("id_organization-ogrn").value = data.ogrn;
                    document.getElementById("id_organization-address").value = data.address;
                    const type_selection = document.getElementById("type_selection");
                    if (type_selection) {
                        document.getElementById("type_selection").value = "ogrnip";
                    }
                }

            } else {
                alert("Организация не найдена");
            }
        })
        .catch(error => console.error("Ошибка при запросе данных:", error));
    });

    $(document).click(function (e) {
        if (!$(e.target).closest("#innSuggestions, #id_organization-inn").length) {
            $("#innSuggestions").hide();
        }
    });
});

$(document).ready(function () {
    $("#id_counterparty-inn").on("input", function () {
        let query = $(this).val();
        if (query.length < 3) {
            $("#innSuggestionsCounterparty").empty().hide();
            return;
        }

        $.ajax({
            url: "/inn_autocomplete",
            data: { query: query },
            dataType: "json",
            success: function (data) {
                let suggestions = data.suggestions;
                let dropdown = $("#innSuggestionsCounterparty");
                dropdown.empty();

                if (suggestions.length) {
                    suggestions.forEach(function (item) {
                        dropdown.append(
                            `<div class="dropdown-item dropdown-item-inn-counterparty" data-inn="${item.inn}">${item.value}</div>`
                        );
                    });

                    dropdown.show();
                } else {
                    dropdown.hide();
                }
            },
        });
    });

    $(document).on("click", ".dropdown-item-inn-counterparty", function () {
        let inn = $(this).data("inn");
        $("#id_counterparty-inn").val(inn);
        $("#innSuggestionsCounterparty").hide();

        fetch(`/find-company/?inn=${inn}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("id_counterparty-naming").value = "";
            document.getElementById("id_counterparty-kpp").value = "";
            document.getElementById("id_counterparty-ogrn").value = "";
            document.getElementById("id_counterparty-address").value = "";
            if (data.success) {
                if (data.type == 'Юридическое лицо') {
                    document.getElementById("id_counterparty-naming").value = data.name;
                    document.getElementById("id_counterparty-kpp").value = data.kpp;
                    document.getElementById("id_counterparty-ogrn").value = data.ogrn;
                    document.getElementById("id_counterparty-address").value = data.address;
                    const type_selection = document.getElementById("type_selection");
                    if (type_selection) {
                        document.getElementById("type_selection").value = "ogrn";
                    }
                }
                else {
                    document.getElementById("id_counterparty-naming").value = data.name;
                    document.getElementById("id_counterparty-ogrn").value = data.ogrn;
                    document.getElementById("id_counterparty-address").value = data.address;
                    const type_selection = document.getElementById("type_selection");
                    if (type_selection) {
                        document.getElementById("type_selection").value = "ogrnip";
                    }
                }


            } else {
                alert("Организация не найдена");
            }
        })
        .catch(error => console.error("Ошибка при запросе данных:", error));
    });

    $(document).click(function (e) {
        if (!$(e.target).closest("#innSuggestionsCounterparty, #id_counterparty-inn").length) {
            $("#innSuggestionsCounterparty").hide();
        }
    });
});

$(document).ready(function () {
    $('#addOrganizationModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var modalType = button.data('modal-type');

        var form = $(this).find('form');
        form.find('#modal_type').val(modalType);
    });
});

document.getElementById('organizationForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const modalType = document.getElementById('modal_type').value;

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.errors) {
            alert('Ошибка: ' + JSON.stringify(data.errors));
        } else {
            document.querySelector('#addOrganizationModal .btn-close').click();

            if (modalType === 'organization') {
                const select = document.getElementById('id_organization');
                const option = new Option(data.name, data.id, true, true);
                select.add(option);

                const select_bank = document.getElementById('id_bank_organization');
                if (select_bank) {
                    const option_bank = new Option(data.bank_name, data.bank_id, true, true);
                    select_bank.add(option_bank);
                }
            }
            else {const select = document.getElementById('id_shipper');
                const option = new Option(data.name, data.id, true, true);
                select.add(option);
                }

            this.reset();

        }
    })
    .catch(error => console.error('Ошибка:', error));
});


$(document).ready(function () {
    $('#addCounterpartyModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var modalType = button.data('modal-type');

        var form = $(this).find('form');
        form.find('#modal_type_consignee').val(modalType);
    });
});


document.getElementById('counterpartyForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const modalType = document.getElementById('modal_type_consignee').value;

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.errors) {
            alert('Ошибка: ' + JSON.stringify(data.errors));
        } else {
            document.querySelector('#addCounterpartyModal .btn-close').click();

            if (modalType === 'counterparty') {
                const select = document.getElementById('id_counterparty');
                const option = new Option(data.name, data.id, true, true);
                select.add(option);

                const select_bank = document.getElementById('id_bank_counterparty');
                if (select_bank) {
                    const option_bank = new Option(data.bank_name, data.bank_id, true, true);
                    select_bank.add(option_bank);
                }

                const select_consignee = document.getElementById('id_consignee');
                if (select_consignee) {
                    const option_consignee = new Option(data.name, data.id, true, true);
                    select_consignee.add(option_consignee);
                };

                const select_investor = document.getElementById('id_investor');
                if (select_investor) {
                    const option_investor = new Option(data.name, data.id, true, true);
                    select_investor.add(option_investor);
                };
            }
            else {
                const select = document.getElementById('id_consignee');
                if (select) {
                    const option = new Option(data.name, data.id, true, true);
                    select.add(option);
                };

                const select_investor = document.getElementById('id_investor');
                if (select_investor) {
                    const option_investor = new Option(data.name, data.id, true, true);
                    select_investor.add(option_investor);
                };

            }

            this.reset();
        }
    })
    .catch(error => console.error('Ошибка:', error));
});


document.addEventListener('DOMContentLoaded', function () {
    ndsInput = document.getElementById("id_nds");

    calculateTotalSum();

    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-row')) {
            var rowCount = document.querySelectorAll('#formset-body tr').length;
            if (rowCount > 1) {
                var row = event.target.closest('tr');
                row.remove();
                updateManagementForm();
            }
        }

        if (event.target.classList.contains('add-new-last-row')) {
            const lastRow = document.querySelector('#formset-body tr:last-child');
            const lastAddButton = lastRow.querySelector('.add-row');
            lastAddButton.click();
        }

        if (event.target.classList.contains('add-row')) {
            addNewRow(event.target);
        }
    });

    function calculateTotalSum() {
        let ndsRate = 0;

        if (ndsInput) {
            ndsRate = parseFloat(ndsInput.value) || 0;
        }

        let total = 0;
        let totalNds = 0;

        const amountInputs = document.querySelectorAll('.amount input');


        amountInputs.forEach(input => {
            if (input.value) {
                total += parseFloat(input.value) || 0;

                if (ndsRate > 0) {
                const nds = input.value * ndsRate / (100 + ndsRate);
                totalNds += nds;
            }
            }
        });

        if (document.getElementById('total-sum')) {
            document.getElementById('total-sum').textContent = total.toFixed(2);
        }
        if (document.getElementById('total-nds')) {
            document.getElementById('total-nds').textContent = totalNds.toFixed(2);
        }

    }

    function addNewRow(button) {
        var formsetBody = document.getElementById('formset-body');
        var firstRow = formsetBody.querySelector('tr');
        var newRow = firstRow.cloneNode(true);

        var currentRow = button.closest('tr');

        var inputs = newRow.querySelectorAll('input');
        inputs.forEach(function (input) {
            input.value = '';
        });

        var textareas = newRow.querySelectorAll('textarea');
        textareas.forEach(function (textarea) {
            textarea.value = '';
        });

        currentRow.insertAdjacentElement('afterend', newRow);
        updateManagementForm();
    }

    function updateManagementForm() {
        var totalForms = document.getElementById('id_form-TOTAL_FORMS');
        var formCount = document.querySelectorAll('#formset-body tr').length;
        totalForms.value = formCount;

        var rows = document.querySelectorAll('#formset-body tr');
        rows.forEach(function (row, index) {
            var inputs = row.querySelectorAll('input');
            inputs.forEach(function (input) {
                var name = input.name;
                if (name) {
                    var updatedName = name.replace(/-\d+-/, '-' + index + '-');
                    input.name = updatedName;
                }
            });

            var textareas = row.querySelectorAll('textarea');
            textareas.forEach(function (textarea) {
                var name = textarea.name;
                if (name) {
                    var updatedName = name.replace(/-\d+-/, '-' + index + '-');
                    textarea.name = updatedName;
                }
            });

            // Убедимся, что у каждой строки есть кнопка "Добавить строку"
            var addButton = row.querySelector('.add-row');
            if (!addButton) {
                var newAddButton = document.createElement('button');
                newAddButton.textContent = 'Добавить строку';
                newAddButton.classList.add('add-row');
                row.appendChild(newAddButton);
            }
        });

        const codeToUnitMap = {
    // Штучные единицы
    '796': 'шт',    // Штука
    '839': 'пар',   // Пара (2 шт)
    '778': 'упак',  // Упаковка

    // Весовые единицы
    '166': 'кг',    // Килограмм
    '168': 'т',     // Тонна
    '163': 'г',     // Грамм

    // Объемные единицы
    '112': 'л',     // Литр
    '137': 'м3',    // Кубический метр

    // Длина
    '006': 'м',     // Метр
    '039': 'км',    // Километр
    '041': 'мм',    // Миллиметр

    // Технические единицы
    '055': 'м2',    // Квадратный метр
    '111': 'см3',   // Кубический сантиметр

    // Тара
    '114': 'бут',   // Бутылка
    '116': 'банк',  // Банка
    '131': 'фл',    // Флакон

    // Для жидкостей
    '122': 'бал',   // Баллон
    '132': 'туб',   // Тюбик

    // Популярные в торговле
    '250': 'рул',   // Рулон
    '356': 'час',   // Час
    '366': 'сут',   // Сутки
    '536': 'компл', // Комплект
    '831': 'лист',  // Лист
    };

    document.querySelectorAll('.code_unit input').forEach(input => {
        const datalist = document.createElement('datalist');
        datalist.id = `datalist-${Math.random().toString(36).substr(2, 9)}`;

        Object.entries(codeToUnitMap).forEach(([code, unit]) => {
            const option = document.createElement('option');
            option.value = code;
            option.textContent = `${code} - ${unit}`;
            datalist.appendChild(option);
        });

        document.body.appendChild(datalist);
        input.setAttribute('list', datalist.id);

        input.addEventListener('change', function() {
            const code = this.value;
            const unit = codeToUnitMap[code];

            if (unit) {
                const row = this.closest('tr');
                const unitInput = row.querySelector('.unit_of_measurement input');
                if (unitInput) {
                    unitInput.value = unit;
                }
            }
        });
    });

        setTimeout(calculateTotalSum, 100);
    }

    if (ndsInput) {
        $(ndsInput).on('change', function() {
           setTimeout(calculateTotalSum, 100);
        });
    }

    document.getElementById('duplicate-last-row')?.addEventListener('click', function() {
        duplicateLastRow();
    });

    function duplicateLastRow() {
        var formsetBody = document.getElementById('formset-body');
        var rows = formsetBody.querySelectorAll('tr');
        if (rows.length === 0) return;

        var lastRow = rows[rows.length - 1];
        var newRow = lastRow.cloneNode(true);

        var idInput = newRow.querySelector('input[name$="-id"]');
        if (idInput) idInput.value = '';

        var inputs = lastRow.querySelectorAll('input:not([name$="-id"])');
        var newInputs = newRow.querySelectorAll('input:not([name$="-id"])');

        inputs.forEach(function(input, index) {
            if (input.type !== 'button' && input.type !== 'submit' && !input.classList.contains('add-row') && !input.classList.contains('remove-row')) {
                newInputs[index].value = input.value;
            }
        });

        formsetBody.appendChild(newRow);

        updateManagementForm();
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const formsetBody = document.getElementById("formset-body");
    const duplicateLastRow = document.getElementById('duplicate-last-row');

    function updateRowNumbers() {
        document.querySelectorAll("#formset-body .row-number").forEach((cell, index) => {
            cell.textContent = index + 1;
        });
    }

    formsetBody.addEventListener("click", function (event) {
        if (event.target.closest(".add-row") || event.target.closest(".remove-row")) {
            setTimeout(updateRowNumbers, 100);
        }
    });

    duplicateLastRow.addEventListener("click", function (event) {
       setTimeout(updateRowNumbers, 100);
    });

    updateRowNumbers();
});


$(document).ready(function() {
    $('#id_organization').on('change.select2', function() {
        let organizationId = $(this).val();
        let $bankSelect = $('#id_bank_organization');
        let $consigneeSelect = $('#id_shipper');
        if ($consigneeSelect.length > 0) {
            $consigneeSelect.val(organizationId).trigger('change.select2');
        }

        if ($bankSelect.length === 0) {
            return;
        }

        $.ajax({
            url: '/get_banks',
            data: { organization_id: organizationId },
            success: function(response) {
                $bankSelect.empty();

                $.each(response.banks, function(index, bank) {
                    $bankSelect.append($('<option>', {
                        value: bank.id,
                        text: bank.naming
                    }));
                });

                $bankSelect.trigger('change.select2');
            }
        });
    });
});

$(document).ready(function() {
    $('#id_counterparty').on('change.select2', function() {
        let organizationId = $(this).val();
        let $bankSelect = $('#id_bank_counterparty');
        let $consigneeSelect = $('#id_consignee');
        if ($consigneeSelect.length > 0) {
            $consigneeSelect.val(organizationId).trigger('change.select2');
        }

        if ($bankSelect.length === 0) {
            return;
        }

        $.ajax({
            url: '/get_banks_counterparty',
            data: { organization_id: organizationId },
            success: function(response) {
                $bankSelect.empty();

                $.each(response.banks, function(index, bank) {
                    $bankSelect.append($('<option>', {
                        value: bank.id,
                        text: bank.naming
                    }));
                });

                $bankSelect.trigger('change.select2');
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const formsetBody = document.getElementById("formset-body");
    const ndsInput = document.getElementById("id_nds");

    function calculateTotalSum() {
        let ndsRate = 0;
        if (ndsInput) {
            ndsRate = parseFloat(ndsInput.value) || 0;
        }

        let total = 0;
        let totalNds = 0;

        const amountInputs = document.querySelectorAll('.amount input');


        amountInputs.forEach(input => {
            if (input.value) {
                total += parseFloat(input.value) || 0;

                if (ndsRate > 0) {
                const nds = input.value * ndsRate / (100 + ndsRate);
                totalNds += nds;
            }
            }
        });


        if (document.getElementById('total-sum')) {
            document.getElementById('total-sum').textContent = total.toFixed(2);
        }
        if (document.getElementById('total-nds')) {
            document.getElementById('total-nds').textContent = totalNds.toFixed(2);
        }
    }

    function calculateRowSum(row) {
        const quantity = parseFloat(row.querySelector(".quantity input").value) || 0;
        const price = parseFloat(row.querySelector(".price input").value) || 0;
        const discountInput = row.querySelector(".discount input");
        const discount = discountInput ? parseFloat(discountInput.value) || 0 : 0;

        let ndsValue = 0;
        if (ndsInput) {
            ndsValue = parseFloat(ndsInput.value) || 0;
        }

        const amount = quantity * price - discount;
        let nds;
        if (ndsValue == -1) {
            nds = 0;
        }
        else {
            nds = amount * ndsValue * 0.01;
        }

        const amountInput = row.querySelector(".amount input");
        if (amountInput) {
            amountInput.value = (amount + nds).toFixed(2);
        }
    }

    function recalculateAllRows() {
        document.querySelectorAll(".form-row").forEach(row => calculateRowSum(row));
    }

    formsetBody.addEventListener("input", function (event) {
        const input = event.target;
        const row = input.closest(".form-row");

        if (row && (input.matches(".quantity input") || input.matches(".price input") || input.matches(".discount input"))) {
            calculateRowSum(row);
            calculateTotalSum();
        }
    });

    if (ndsInput) {
        $(ndsInput).on('change', function() {
            recalculateAllRows();
        });
    }

});


document.addEventListener("DOMContentLoaded", function () {
    $('.select2').select2({
        width: '100%',
        placeholder: "Выберите значение",
        allowClear: true
    });
});

$(document).ready(function () {
    $("#id_address").on("input", function () {
        let query = $(this).val();
        if (query.length > 2) {
            $.ajax({
                url: "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address",
                method: "POST",
                contentType: "application/json",
                headers: {
                    "Authorization": "Token bb47885575aa2239d036af551ba88f3da668d266"
                },
                data: JSON.stringify({ query: query }),
                success: function (data) {
                    let suggestions = data.suggestions.map(item => item.value);
                    $("#address_list").empty();
                    suggestions.forEach(addr => {
                        $("#address_list").append(`<option value="${addr}">`);
                    });
                }
            });
        }
    });
});

document.getElementById("findByINN").addEventListener("click", function() {
    let innInput = document.getElementById("id_organization-inn");
    let inn = innInput.value.trim();

    if (!inn) {
        alert("Введите ИНН");
        return;
    }

    fetch(`/find-company/?inn=${inn}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("id_organization-naming").value = "";
            document.getElementById("id_organization-kpp").value = "";
            document.getElementById("id_organization-ogrn").value = "";
            document.getElementById("id_organization-address").value = "";
            document.getElementById("id_organization-position_at_work").value = "";
            document.getElementById("id_organization-supervisor").value = "";
            if (data.success) {
                if (data.type == 'Юридическое лицо') {
                    document.getElementById("id_organization-naming").value = data.name;
                    document.getElementById("id_organization-kpp").value = data.kpp;
                    document.getElementById("id_organization-ogrn").value = data.ogrn;
                    document.getElementById("id_organization-address").value = data.address;
                    document.getElementById("id_organization-position_at_work").value = data.position_at_work;
                    document.getElementById("id_organization-supervisor").value = data.supervisor;
                    const type_selection = document.getElementById("type_selection");
                    if (type_selection) {
                        document.getElementById("type_selection").value = "ogrn";
                    }
                }
                else {
                    document.getElementById("id_organization-naming").value = data.name;
                    document.getElementById("id_organization-ogrn").value = data.ogrn;
                    document.getElementById("id_organization-address").value = data.address;
                    const type_selection = document.getElementById("type_selection");
                    if (type_selection) {
                        document.getElementById("type_selection").value = "ogrnip";
                    }
                }

            } else {
                alert("Организация не найдена");
            }
        })
        .catch(error => console.error("Ошибка при запросе данных:", error));
});

document.addEventListener("DOMContentLoaded", function () {
    let findByBIKButton = document.getElementById("findByBIK");

    if (findByBIKButton) {
        findByBIKButton.addEventListener("click", function () {
            let bikInput = document.getElementById("id_bank-bic");
            if (!bikInput) return;

            let bik = bikInput.value.trim();
            if (!bik) {
                alert("Введите БИК");
                return;
            }

            fetch(`/find-bank/?bik=${bik}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        let bankName = document.getElementById("id_bank-naming");
                        let bankLocation = document.getElementById("id_bank-location");
                        let correspondentAccount = document.getElementById("id_bank-correspondent_account");

                        if (bankName) bankName.value = data.bank_name;
                        if (bankLocation) bankLocation.value = data.address;
                        if (correspondentAccount) correspondentAccount.value = data.correspondent_account;
                    } else {
                        alert("Банк не найден");
                    }
                })
                .catch(error => console.error("Ошибка при запросе данных:", error));
        });
    }
});

document.getElementById("findByINNCounterparty").addEventListener("click", function() {
    let innInput = document.getElementById("id_counterparty-inn");
    let inn = innInput.value.trim();

    if (!inn) {
        alert("Введите ИНН");
        return;
    }

    fetch(`/find-company/?inn=${inn}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("id_counterparty-naming").value = "";
            document.getElementById("id_counterparty-kpp").value = "";
            document.getElementById("id_counterparty-ogrn").value = "";
            document.getElementById("id_counterparty-address").value = "";
            if (data.success) {
                if (data.type == 'Юридическое лицо') {
                    document.getElementById("id_counterparty-naming").value = data.name;
                    document.getElementById("id_counterparty-kpp").value = data.kpp;
                    document.getElementById("id_counterparty-ogrn").value = data.ogrn;
                    document.getElementById("id_counterparty-address").value = data.address;
                    const type_selection = document.getElementById("type_selection");
                    if (type_selection) {
                        document.getElementById("type_selection").value = "ogrn";
                    }
                }
                else {
                    document.getElementById("id_counterparty-naming").value = data.name;
                    document.getElementById("id_counterparty-ogrn").value = data.ogrn;
                    document.getElementById("id_counterparty-address").value = data.address;
                    const type_selection = document.getElementById("type_selection");
                    if (type_selection) {
                        document.getElementById("type_selection").value = "ogrnip";
                    }
                }


            } else {
                alert("Организация не найдена");
            }
        })
        .catch(error => console.error("Ошибка при запросе данных:", error));
});

document.addEventListener("DOMContentLoaded", function () {
    let findByBIKButton = document.getElementById("findByBIKCounterparty");

    if (findByBIKButton) {
        findByBIKButton.addEventListener("click", function () {
            let bikInput = document.getElementById("id_counterparty_bank-bic");
            if (!bikInput) return;

            let bik = bikInput.value.trim();
            if (!bik) {
                alert("Введите БИК");
                return;
            }

            fetch(`/find-bank/?bik=${bik}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        let bankName = document.getElementById("id_counterparty_bank-naming");
                        let bankLocation = document.getElementById("id_counterparty_bank-location");
                        let correspondentAccount = document.getElementById("id_counterparty_bank-correspondent_account");

                        if (bankName) bankName.value = data.bank_name;
                        if (bankLocation) bankLocation.value = data.address;
                        if (correspondentAccount) correspondentAccount.value = data.correspondent_account;
                    } else {
                        alert("Банк не найден");
                    }
                })
                .catch(error => console.error("Ошибка при запросе данных:", error));
        });
    }
});

$(document).ready(function () {
    $("#id_bank-bic").on("input", function () {
        let query = $(this).val();
        if (query.length < 3) {
            $("#bicSuggestions").empty().hide();
            return;
        }

        $.ajax({
            url: "/bank_autocomplete",
            data: { query: query },
            dataType: "json",
            success: function (data) {
                let suggestions = data.suggestions;
                let dropdown = $("#bicSuggestions");
                dropdown.empty();

                if (suggestions.length) {
                    suggestions.forEach(function (item) {
                        dropdown.append(
                            `<div class="dropdown-item dropdown-item-bic" data-inn="${item.inn}">${item.value}</div>`
                        );
                    });

                    dropdown.show();
                } else {
                    dropdown.hide();
                }
            },
        });
    });

    $(document).on("click", ".dropdown-item-bic", function () {
        let inn = $(this).data("inn");
        $("#id_bank-bic").val(inn);
        $("#bicSuggestions").hide();

        fetch(`/find-bank/?bik=${inn}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("id_bank-naming").value = data.bank_name;
                document.getElementById("id_bank-location").value = data.address;
                document.getElementById("id_bank-correspondent_account").value = data.correspondent_account;
            } else {
                alert("Банк не найден");
            }
        })
        .catch(error => console.error("Ошибка при запросе данных:", error));
    });

    $(document).click(function (e) {
        if (!$(e.target).closest("#bicSuggestions, #id_bank-bic").length) {
            $("#bicSuggestions").hide();
        }
    });
});


$(document).ready(function () {
    $("#id_counterparty_bank-bic").on("input", function () {
        let query = $(this).val();
        if (query.length < 3) {
            $("#bicSuggestionsCounterparty").empty().hide();
            return;
        }

        $.ajax({
            url: "/bank_autocomplete",
            data: { query: query },
            dataType: "json",
            success: function (data) {
                let suggestions = data.suggestions;
                let dropdown = $("#bicSuggestionsCounterparty");
                dropdown.empty();



                if (suggestions.length) {
                    suggestions.forEach(function (item) {
                        dropdown.append(
                            `<div class="dropdown-item dropdown-item-bic-counterparty" data-inn="${item.inn}">${item.value}</div>`
                        );
                    });

                    dropdown.show();
                } else {
                    dropdown.hide();
                }
            },
        });
    });

    $(document).on("click", ".dropdown-item-bic-counterparty", function () {
        let inn = $(this).data("inn");
        $("#id_counterparty_bank-bic").val(inn);
        $("#bicSuggestionsCounterparty").hide();

        fetch(`/find-bank/?bik=${inn}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("id_counterparty_bank-naming").value = data.bank_name;
                document.getElementById("id_counterparty_bank-location").value = data.address;
                document.getElementById("id_counterparty_bank-correspondent_account").value = data.correspondent_account;
            } else {
                alert("Банк не найден");
            }
        })
        .catch(error => console.error("Ошибка при запросе данных:", error));
    });

    $(document).click(function (e) {
        if (!$(e.target).closest("#bicSuggestionsCounterparty, #id_counterparty_bank-bic").length) {
            $("#bicSuggestionsCounterparty").hide();
        }
    });
});

$(document).ready(function() {
    $('#id_sample').on('change.select2', function() {
        var sampleId = $(this).val();

        if (!sampleId) return;

        $.ajax({
            url: '/get_labels/',
            data: { sample_id: sampleId },
            success: function(response) {
                updateFields(response.labels);
            },
            error: function(xhr, status, error) {
                console.error('Ошибка запроса:', error);
            }
        });
    });

    var initialSampleId = $('#id_sample').val();
    if (initialSampleId) {
        $('#id_sample').trigger('change.select2');
        const nameDocument = document.getElementById("id_name");
        fetchSavedValues(nameDocument.value);
    }
});

function updateFields(labels) {
    $('#new_fields_container').empty();

    labels.forEach(function(label) {
        var fieldHtml = `
            <div class="form-group">
                <label for="dop_id_${label.id}">${label.name}</label>
                <input type="text" name="${label.code}" id="dop_id_${label.id}" class="form-control w-md-50">
            </div>
        `;
        $('#new_fields_container').append(fieldHtml);
    });
}

function fetchSavedValues(sampleId) {
    $.ajax({
        url: '/get_saved_values/',
        data: { sample_id: sampleId },
        success: function(response) {
            Object.entries(response.values).forEach(([fieldCode, value]) => {
                $(`input[name="${fieldCode}"]`).val(value);
            });
        },
        error: function(xhr, status, error) {
            console.error('Ошибка при загрузке сохранённых данных:', error);
        }
    });
}

$(document).ready(function () {
    $("#id_bank_org-bic").on("input", function () {
        let query = $(this).val();
        if (query.length < 3) {
            $("#bicSuggestionsBank").empty().hide();
            return;
        }

        $.ajax({
            url: "/bank_autocomplete",
            data: { query: query },
            dataType: "json",
            success: function (data) {
                let suggestions = data.suggestions;
                let dropdown = $("#bicSuggestionsBank");
                dropdown.empty();

                if (suggestions.length) {
                    suggestions.forEach(function (item) {
                        dropdown.append(
                            `<div class="dropdown-item dropdown-item-bic-bank" data-inn="${item.inn}">${item.value}</div>`
                        );
                    });

                    dropdown.show();
                } else {
                    dropdown.hide();
                }
            },
        });
    });

    $(document).on("click", ".dropdown-item-bic-bank", function () {
        let inn = $(this).data("inn");
        $("#id_bank_org-bic").val(inn);
        $("#bicSuggestionsBank").hide();

        fetch(`/find-bank/?bik=${inn}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("id_bank_org-naming").value = data.bank_name;
                document.getElementById("id_bank_org-location").value = data.address;
                document.getElementById("id_bank_org-correspondent_account").value = data.correspondent_account;
            } else {
                alert("Банк не найден");
            }
        })
        .catch(error => console.error("Ошибка при запросе данных:", error));
    });

    $(document).click(function (e) {
        if (!$(e.target).closest("#bicSuggestionsBank, #id_bank_org-bic").length) {
            $("#bicSuggestionsBank").hide();
        }
    });
});


document.getElementById('bankForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);

    const organizationSelect = document.getElementById('id_organization');
    const selectedOrganization = organizationSelect.value;

    if (!selectedOrganization) {
        alert('Пожалуйста, выберите организацию из списка');
        return;
    }

    formData.append('org', selectedOrganization);

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.errors) {
            alert('Ошибка: ' + JSON.stringify(data.errors));
        } else {
            let $bankSelect = $('#id_bank_organization');
            $bankSelect.empty();

            $.each(data.banks, function(index, bank) {
                $bankSelect.append($('<option>', {
                    value: bank.id,
                    text: bank.naming
                }));
            });

            $bankSelect.trigger('change.select2');


            const modal = bootstrap.Modal.getInstance(document.getElementById('addBankModal'));
            modal.hide();
            this.reset();
        }
    })
    .catch(error => console.error('Ошибка:', error));
});


$(document).ready(function () {
    $("#id_bank_coun-bic").on("input", function () {
        let query = $(this).val();
        if (query.length < 3) {
            $("#bicSuggestionsBankCoun").empty().hide();
            return;
        }

        $.ajax({
            url: "/bank_autocomplete",
            data: { query: query },
            dataType: "json",
            success: function (data) {
                let suggestions = data.suggestions;
                let dropdown = $("#bicSuggestionsBankCoun");
                dropdown.empty();

                if (suggestions.length) {
                    suggestions.forEach(function (item) {
                        dropdown.append(
                            `<div class="dropdown-item dropdown-item-bic-bank-coun" data-inn="${item.inn}">${item.value}</div>`
                        );
                    });

                    dropdown.show();
                } else {
                    dropdown.hide();
                }
            },
        });
    });

    $(document).on("click", ".dropdown-item-bic-bank-coun", function () {
        let inn = $(this).data("inn");
        $("#id_bank_coun-bic").val(inn);
        $("#bicSuggestionsBankCoun").hide();

        fetch(`/find-bank/?bik=${inn}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("id_bank_coun-naming").value = data.bank_name;
                document.getElementById("id_bank_coun-location").value = data.address;
                document.getElementById("id_bank_coun-correspondent_account").value = data.correspondent_account;
            } else {
                alert("Банк не найден");
            }
        })
        .catch(error => console.error("Ошибка при запросе данных:", error));
    });

    $(document).click(function (e) {
        if (!$(e.target).closest("#bicSuggestionsBankCoun, #id_bank_coun-bic").length) {
            $("#bicSuggestionsBankCoun").hide();
        }
    });
});


document.getElementById('bankCounForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);

    const organizationSelect = document.getElementById('id_counterparty');
    const selectedOrganization = organizationSelect.value;

    if (!selectedOrganization) {
        alert('Пожалуйста, выберите организацию из списка');
        return;
    }

    formData.append('org', selectedOrganization);

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.errors) {
            alert('Ошибка: ' + JSON.stringify(data.errors));
        } else {
            let $bankSelect = $('#id_bank_counterparty');
            $bankSelect.empty();

            $.each(data.banks, function(index, bank) {
                $bankSelect.append($('<option>', {
                    value: bank.id,
                    text: bank.naming
                }));
            });

            $bankSelect.trigger('change.select2');


            const modal = bootstrap.Modal.getInstance(document.getElementById('addBankCounModal'));
            modal.hide();
            this.reset();
        }
    })
    .catch(error => console.error('Ошибка:', error));
});
