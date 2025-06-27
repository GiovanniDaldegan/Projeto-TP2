import { request_product_list, request_categories } from "./client_events.js";

var socketio = io();

// inserção dos filtros fornecidos pelo servidor no select de filtros de pesquisa
socketio.on("categories", (categories) => {
    const categorySelect = document.getElementById("category-filters");
    var categoriesHTML = "";

    categories.forEach(element => {
        categoriesHTML += `<option value="${element}">${element}</option>\n`
    });

    categorySelect.innerHTML = categoriesHTML;
});

document.addEventListener("DOMContentLoaded", () => {

    request_categories(socketio);
    
    /*
    document.getElementById("search-screen-button").addEventListener("click", () => {
        request_categories(socketio);

        // mostrar tela de pesquisa e lista de produtos
    });
    */

    document.getElementById("search-form").addEventListener("submit", (e) => {
        e.preventDefault();

        const categoryFilters = document.getElementById("category-filters").options;

        var activeFilters = {
            "product_name"    : document.getElementById("product-name").value,
            "price_range"     : [
                document.getElementById("min-price").value,
                document.getElementById("max-price").value
            ],
            "min_rating"      : document.getElementById("min-rating").value,
            "categories"      : []
        }

        for (var i = 0; i < categoryFilters.length; i++) {
            if (categoryFilters[i].selected)
                activeFilters["categories"].push(categoryFilters[i].value);
        }

        console.log(activeFilters);

        request_product_list(socketio, activeFilters);
    });
});
