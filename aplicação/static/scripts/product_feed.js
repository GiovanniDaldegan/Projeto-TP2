import { request_product_list } from "./client_events.js";

var socketio = io();

document.addEventListener("DOMContentLoaded", () => {

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
