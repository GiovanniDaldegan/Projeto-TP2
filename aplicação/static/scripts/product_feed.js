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

socketio.on("get-product-list", (productList) => {
    console.log(productList);
});


document.addEventListener("DOMContentLoaded", () => {

    // TODO: mover para o evento que ativa a tela de pesquisa
    request_categories(socketio);
    
    /*
    document.getElementById("search-screen-button").addEventListener("click", () => {
        request_categories(socketio);

        // mostrar tela de pesquisa e lista de produtos
    });
    */

    document.getElementById("search-form").addEventListener("submit", (e) => {
        e.preventDefault();

        const searchTerm = document.getElementById("product-name").value;
        const categoryFilters = document.getElementById("category-filters").options;

        var activeFilters = {
            "min_price"     : document.getElementById("min-price").value,
            "max_price"     : document.getElementById("max-price").value,
            "rating"        : document.getElementById("min-rating").value,
            "categories"    : [],
            "sort"          : ""
        }

        for (var i = 0; i < categoryFilters.length; i++) {
            if (categoryFilters[i].selected)
                activeFilters["categories"].push(categoryFilters[i].value);
        }

        console.log(activeFilters);

        request_product_list(socketio, searchTerm, activeFilters);
    });
});
