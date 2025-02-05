document.getElementById('organizationForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);

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
            const select = document.getElementById('id_organization');
            const option = new Option(data.name, data.id, true, true);
            select.add(option);

            const select_bank = document.getElementById('id_bank_organization');
            const option_bank = new Option(data.bank_name, data.bank_id, true, true);
            select_bank.add(option_bank);

        }
    })
    .catch(error => console.error('Ошибка:', error));
});


document.getElementById('counterpartyForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);

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
            const select = document.getElementById('id_counterparty');
            const option = new Option(data.name, data.id, true, true);
            select.add(option);

            const select_bank = document.getElementById('id_bank_counterparty');
            const option_bank = new Option(data.bank_name, data.bank_id, true, true);
            select_bank.add(option_bank);

        }
    })
    .catch(error => console.error('Ошибка:', error));
});


document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('.add-row').addEventListener('click', function () {
        var formsetBody = document.getElementById('formset-body');
        var firstRow = formsetBody.querySelector('tr');
        var newRow = firstRow.cloneNode(true);

        var inputs = newRow.querySelectorAll('input');
        inputs.forEach(function (input) {
            input.value = '';
        });

        formsetBody.appendChild(newRow);
        updateManagementForm();
    });

    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-row')) {
            var rowCount = document.querySelectorAll('#formset-body tr').length;
            if (rowCount > 1) {
                var row = event.target.closest('tr');
                row.remove();
                updateManagementForm();
            }
        }
    });

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
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const formsetBody = document.getElementById("formset-body");

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

    updateRowNumbers();
});


$(document).ready(function() {
    $('#id_organization').on('change.select2', function() {
        let organizationId = $(this).val();
        let $bankSelect = $('#id_bank_organization');

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

    function calculateRowSum(row) {
        const quantity = parseFloat(row.querySelector(".quantity input").value) || 0;
        const price = parseFloat(row.querySelector(".price input").value) || 0;
        const discountInput = row.querySelector(".discount input");
        const discount = discountInput ? parseFloat(discountInput.value) || 0 : 0; // Проверяем, есть ли поле

        const amount = quantity * price - discount;
        row.querySelector(".amount input").value = amount.toFixed(2);
    }

    formsetBody.addEventListener("input", function (event) {
        const input = event.target;
        const row = input.closest(".form-row");

        if (row && (input.matches(".quantity input") || input.matches(".price input") || input.matches(".discount input"))) {
            calculateRowSum(row);
        }
    });
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
