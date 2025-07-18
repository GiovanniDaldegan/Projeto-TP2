import { socketio } from "./index.js";
import { openAddToListModal} from "./shopping_list.js";

// Emissores de eventos ao servidor

function requestProductList(params) {
  socketio.emit("get-product-list", params);
}

function requestCategories() {
    socketio.emit("get-categories");
}


// Função para criar os cards dos produtos
function createProductCard(product) {
  const card = document.createElement("article");
  card.classList.add("card-produto");

  if (!product.price_range[0]) {
    var price = "0,00";
  }
  else {
    var price = product.price_range[0].toFixed(2).replace('.', ',');
  }

  card.dataset.id = product.id; 
  card.dataset.name = product.name;
  card.dataset.supermarket = product.market;
  card.dataset.price = price;
  card.dataset.imageUrl = `static/img/products/${product.name}.png`;

  card.innerHTML = `
    <img class="produto-img" src="static/img/products/${product["name"]}.png" alt="${product["name"]}">
    <div class="produto-info">
      <span class="supermercado">${product["market"]}</span>
      <h3 class="nome-produto">${product["name"]}</h3>
      <span class="preco">R$ ${price}</span>
      <div class="btn-produto">
        <button class="btn-adicionar-lista" type="button">+ Lista</button>
      </div>
    </div>
  `;

    const btnAdd = card.querySelector(".btn-adicionar-lista");
    btnAdd.addEventListener("click", () => {
      openAddToListModal(product.id);
    });
  
    return card;
}

// Renderização do Feed
function renderFeed(products) {
  if (!products) return;

  const productFeedContainer = document.getElementById("product-feed");
  //const filterToggleBtn = document.getElementById("filter-toggle");
  const filterPanel = document.getElementById("filter-panel");

  productFeedContainer.innerHTML = "";

  if (products.length === 0) {
    //filterToggleBtn.style.display = "none";
    //filterPanel.classList.remove("active");

    const noResults = document.createElement("p");
    noResults.classList.add("no-results");
    noResults.textContent = "Nenhum produto encontrado.";
    productFeedContainer.appendChild(noResults);
    return;
  }

  //filterToggleBtn.style.display = showFilterBtn ? "block" : "none";

  products.forEach(product => {
    const card = createProductCard(product);
    productFeedContainer.appendChild(card);
  });
}

// Coleta de parâmetros de pesquisa
function getSearchParams() {
  const categorySelect = document.getElementById("category-filters");
  const minPrice = document.getElementById("min-price").value;
  const maxPrice = document.getElementById("max-price").value;
  const searchTerm = document.getElementById("search-term").value;
  
  const category = categorySelect.options[categorySelect.selectedIndex].value;
  
  var params = {
    "search_term" : searchTerm,
    "filters" : {}
  }

  
  if (category != "todos") params["filters"]["category"] = category;

  // registra a faixa de preço
  if (sessionStorage.getItem("price-filters") === "true") {
    if (minPrice > 0)
      params["filters"]["min_price"] = parseInt(minPrice);
    if (maxPrice > 0)
      params["filters"]["max_price"] = parseInt(maxPrice);
  }

  return params;
}


// Inicialização de listeners de eventos de reposta do servidor
export function productSearchSetupListeners() {
  requestCategories();

  // Faz requisição inicial da lista de produtos
  requestProductList(getSearchParams());

  // inserção de categorias no select de categoria
  socketio.on("categories", (categories) => {
    const categorySelect = document.getElementById("category-filters");
    var categoriesHTML = "<option value=\"todos\" selected>Todos</option>";

    categories.forEach(element => {
      categoriesHTML += `<option value="${element}">${element}</option>\n`
    });

    categorySelect.innerHTML = categoriesHTML;
  });

  socketio.on("product-list", (productList) => {
    renderFeed(productList);
  });
}

// Inicialização do HTML
export function productSearchSetupHTML() {
  sessionStorage.setItem("price-filters", "false");

  const filterToggleBtn = document.getElementById("filter-toggle");
  const filterPanel = document.getElementById("filter-panel");
  const closeFilterBtn = document.getElementById("close-filter");
  const applyPriceFiltersBtn = document.getElementById("apply-price-filters");

  const searchForm = document.getElementById("search-form");


  filterToggleBtn.style.display = "block";
  
  // Exibe o painel de filtro
  filterToggleBtn.addEventListener("click", () => {
    filterPanel.classList.add("active");
    filterToggleBtn.style.display = "none";
    document.body.classList.add("list-open");
  });

  // Fecha o painel de filtro
  closeFilterBtn.addEventListener("click", () => {
    filterPanel.classList.remove("active");
    filterToggleBtn.style.display = "block";
    document.body.classList.remove("list-open");
  });
  
  // Aplica filtros
  applyPriceFiltersBtn.addEventListener("click", () => {
    sessionStorage.setItem("price-filters", "true");
    requestProductList(getSearchParams());
  });


  // Pesquisa de produtos
  searchForm.addEventListener("submit", (e) => {
    e.preventDefault();
    requestProductList(getSearchParams());
  });
}
