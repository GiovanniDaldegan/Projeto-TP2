const productFeedContainer = document.getElementById("product-feed");
const filterToggleBtn = document.getElementById("filter-toggle");
const filterPanel = document.getElementById("filter-panel");
const closeFilterBtn = document.getElementById("close-filter");

// Função para criar os cards dos produtos
function createProductCard(product) {
  const card = document.createElement("article");
  card.classList.add("card-produto");

  card.innerHTML = `
    <img class="produto-img" src="${product.image}" alt="${product.name}">
    <div class="produto-info">
      <span class="supermercado">${product.store}</span>
      <h3 class="nome-produto">${product.name}</h3>
      <span class="preco">R$ ${product.price.toFixed(2).replace('.', ',')}</span>
      <div class="btn-produto">
        <button class="btn-adicionar-lista" type="button">+ Lista</button>
        <button class="btn-adicionar-carrinho" type="button">+ Carrinho</button>
      </div>
    </div>
  `;

  return card;
}

// Renderização do Feed
function renderFeed(products, showFilterBtn = false) {
  productFeedContainer.innerHTML = "";

  if (products.length === 0) {
    filterToggleBtn.style.display = "none";
    filterPanel.classList.remove("active");

    const noResults = document.createElement("p");
    noResults.classList.add("no-results");
    noResults.textContent = "Nenhum produto encontrado.";
    productFeedContainer.appendChild(noResults);
    return;
  }

  filterToggleBtn.style.display = showFilterBtn ? "block" : "none";

  products.forEach(product => {
    const card = createProductCard(product);
    productFeedContainer.appendChild(card);
  });
}

// Simulação de produtos
const baseProduct = {
  id: 1,
  name: "Amaciante Ypê",
  price: 15.99,
  store: "Big Box",
  image: "/static/img/amaciante.png"
};

const mockProducts = Array.from({ length: 30 }, (_, i) => ({
  ...baseProduct,
  id: i + 1,
  name: `${baseProduct.name} #${i + 1}`
}));


function simulateSearch(query) {
  if (query.trim().toLowerCase() === "nada") return [];
  return mockProducts.filter(p => p.name.toLowerCase().includes(query.toLowerCase()));
}

document.addEventListener("DOMContentLoaded", () => {
  const searchForm = document.getElementById("search-form");
  const searchInput = document.getElementById("product-name");


  filterToggleBtn.style.display = "none";

  // Renderiza feed inicial com produtos
  renderFeed(mockProducts, false);

  // Simulação de busca
  searchForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const query = searchInput.value;
    const results = simulateSearch(query);
    renderFeed(results, true);
  });

  // Exibe o painel de filtro
  filterToggleBtn.addEventListener("click", () => {
    filterPanel.classList.add("active");
    filterToggleBtn.style.display = "none";
  });

  // Fecha o painel de filtro
  closeFilterBtn.addEventListener("click", () => {
    filterPanel.classList.remove("active");
    filterToggleBtn.style.display = "block";
  });
});
