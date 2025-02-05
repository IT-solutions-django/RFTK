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
            if (data.success) {
                document.getElementById("id_counterparty-naming").value = data.name;
                document.getElementById("id_counterparty-kpp").value = data.kpp;
                document.getElementById("id_counterparty-ogrn").value = data.ogrn;
                document.getElementById("id_counterparty-ogrn").value = data.address;

            } else {
                alert("Организация не найдена");
            }
        })
        .catch(error => console.error("Ошибка при запросе данных:", error));
});

document.getElementById("findByBIKCounterparty").addEventListener("click", function() {
    let bikInput = document.getElementById("id_counterparty_bank-bic");
    let bik = bikInput.value.trim();

    if (!bik) {
        alert("Введите БИК");
        return;
    }

    fetch(`/find-bank/?bik=${bik}`)
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

$(document).ready(function () {
    $("#id_counterparty-inn").on("input", function () {
        if (/[a-zA-Zа-яА-Я]/.test($(this).val())) {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });
});

$(document).ready(function () {
    $("#id_counterparty-kpp").on("input", function () {
        if (/[a-zA-Zа-яА-Я]/.test($(this).val())) {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });
});

$(document).ready(function () {
    $("#id_counterparty-ogrn").on("input", function () {
        if (/[a-zA-Zа-яА-Я]/.test($(this).val())) {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });
});

$(document).ready(function () {
    $("#id_counterparty_bank-bic").on("input", function () {
        if (/[a-zA-Zа-яА-Я]/.test($(this).val())) {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });
});

$(document).ready(function () {
    $("#id_counterparty_bank-correspondent_account").on("input", function () {
        if (/[a-zA-Zа-яА-Я]/.test($(this).val())) {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });
});

$(document).ready(function () {
    $("#id_counterparty_bank-current_account").on("input", function () {
        if (/[a-zA-Zа-яА-Я]/.test($(this).val())) {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });
});