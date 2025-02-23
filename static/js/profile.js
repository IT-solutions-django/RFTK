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
                    document.getElementById("type_selection").value = "ogrn";
                }
                else {
                    document.getElementById("id_organization-naming").value = data.name;
                    document.getElementById("id_organization-ogrn").value = data.ogrn;
                    document.getElementById("id_organization-address").value = data.address;
                    document.getElementById("type_selection").value = "ogrnip";
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
                    document.getElementById("type_selection").value = "ogrn";
                }
                else {
                    document.getElementById("id_organization-naming").value = data.name;
                    document.getElementById("id_organization-ogrn").value = data.ogrn;
                    document.getElementById("id_organization-address").value = data.address;
                    document.getElementById("type_selection").value = "ogrnip";
                }

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

$(document).ready(function () {
    $("#id_organization-address").on("input", function () {
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

$(document).ready(function () {
    $("#id_bank-location").on("input", function () {
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
                    $("#address_list_bank").empty();
                    suggestions.forEach(addr => {
                        $("#address_list_bank").append(`<option value="${addr}">`);
                    });
                }
            });
        }
    });
});
