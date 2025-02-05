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
            if (data.success) {
                document.getElementById("id_organization-naming").value = data.name;
                document.getElementById("id_organization-kpp").value = data.kpp;
                document.getElementById("id_organization-ogrn").value = data.ogrn;
                document.getElementById("id_organization-address").value = data.address;
                document.getElementById("id_organization-position_at_work").value = data.position_at_work;
                document.getElementById("id_organization-supervisor").value = data.supervisor;

            } else {
                alert("Организация не найдена");
            }
        })
        .catch(error => console.error("Ошибка при запросе данных:", error));
});

document.getElementById("findByBIK").addEventListener("click", function() {
    let bikInput = document.getElementById("id_bank-bic");
    let bik = bikInput.value.trim();

    if (!bik) {
        alert("Введите БИК");
        return;
    }

    fetch(`/find-bank/?bik=${bik}`)
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

$(document).ready(function () {
    $("#id_organization-inn").on("input", function () {
        if (/[a-zA-Zа-яА-Я]/.test($(this).val())) {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });
});

$(document).ready(function () {
    $("#id_organization-kpp").on("input", function () {
        if (/[a-zA-Zа-яА-Я]/.test($(this).val())) {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });
});

$(document).ready(function () {
    $("#id_organization-ogrn").on("input", function () {
        if (/[a-zA-Zа-яА-Я]/.test($(this).val())) {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });
});

$(document).ready(function () {
    $("#id_organization-phone").on("input", function () {
        let phone = $(this).val();
        let phonePattern = /^\+7\s?\d{3}\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}$/;

        if (!phonePattern.test(phone)) {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });
});

$(document).ready(function () {
    $("#id_bank-bic").on("input", function () {
        if (/[a-zA-Zа-яА-Я]/.test($(this).val())) {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });
});

$(document).ready(function () {
    $("#id_bank-correspondent_account").on("input", function () {
        if (/[a-zA-Zа-яА-Я]/.test($(this).val())) {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });
});

$(document).ready(function () {
    $("#id_bank-current_account").on("input", function () {
        if (/[a-zA-Zа-яА-Я]/.test($(this).val())) {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });
});
