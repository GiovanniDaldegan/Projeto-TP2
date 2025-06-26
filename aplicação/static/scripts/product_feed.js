import { request_product_list, request_filters } from "./client_events.js";

var socketio = io();

// inserção dos filtros fornecidos pelo servidor no select de filtros de pesquisa
socketio.on("filters", (filters) => {
    const searchSelect = document.getElementById("search-filters")
    var filtersHTML = "";

    filters.forEach(element => {
        filtersHTML += `<option value="${element}">${element}</option>\n`
    });
    console.log(filtersHTML);

    searchSelect.innerHTML = filtersHTML;
});

document.addEventListener("DOMContentLoaded", () => {
    request_filters(socketio);


    document.getElementById("search-form").addEventListener("submit", (e) => {
        e.preventDefault();

        const productName = document.getElementById("product-name").value;
        const filterOptions = document.getElementById("search-filters").options;

        var activeFilters = []

        for (var i = 0; i < filterOptions.length; i++) {
            if (filterOptions[i].selected)
                activeFilters.push(filterOptions[i].value);
        }

        request_product_list(socketio, productName, activeFilters);
    });
});
