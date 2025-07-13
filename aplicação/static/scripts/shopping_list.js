import { socketio, user } from "./index.js";

// Emissores de eventos ao servidor

function getAllLists(userId) {
  socketio.emit("get-all-shopping-lists", userId)
}

function createList(userId, listName) {
  socketio.emit("create-shopping-list", {
    "id_user": userId,
    "name": listName
  });
}

function deleteList(userId, listId) {
  socketio.emit("delete-list", {
    "id_user": userId,
    "id_list": listId
  });
}

function getList(listId) {
  socketio.emit("get-shopping-list", listId);
}

function addToList(listId, productId, quantity) {
  socketio.emit("add-to-list", {
      "id_list": listId,
      "id_product": productId,
      "quantity": quantity
  });
}

function removeFromList(listId, productId) {
  socketio.emit("remove-from-list", {
      "id_list": listId,
      "id_product": productId
  });
}

function setProductTaken(listId, productId, taken) {
  socketio.emit("set-product-taken", {
      "id_list": listId,
      "id_product": productId,
      "taken": taken
  })
}


// TODO #15: médio - adicionar as listas fornecidas ao painel de listas de compras
// (melhorar e estilizar o html de listItem)
function renderAllShoppingLists(shoppingLists) {
  const panelTitle = document.getElementById("list-panel-title");
  const listPanelFooter = document.getElementById("list-footer");

  const listContainer = document.getElementById("shopping-list-items");
  const existingListsContainer = document.getElementById("existing-lists");

  panelTitle.innerHTML = "Listas de Compras";
  listPanelFooter.innerHTML = `<button id="btn-create-list" class="btn-create-list">+ Nova Lista</button>`;

  if (!shoppingLists) {
    listContainer.innerHTML = "Você não possui listas.";
    existingListsContainer.innerHTML = "Você não possui listas."
  }
  else {
    listContainer.innerHTML = "";

    shoppingLists.forEach(list => {
      // Atualiza listas do painel de listas de compras
      const listItem = document.createElement("article");
      listItem.classList.add("item-shopping-list");

      const listBtn = document.createElement("button");
      listBtn.classList.add("open-list");
      listBtn.id = list["id"]; 
      listBtn.textContent = list["name"];

      listBtn.addEventListener("click", () => {
        getList(list["id"]);
        renderShoppingListName(list["name"]);
      });

      const deleteBtn = document.createElement("button");
      deleteBtn.classList.add("delete-list");
      deleteBtn.id = list["id"];
      deleteBtn.textContent = "X";

      deleteBtn.addEventListener("click", () => {
        deleteList(user["userId"], list["id"]);
      });
  
      listItem.appendChild(listBtn);
      listItem.appendChild(deleteBtn);
      listContainer.appendChild(listItem);


      // Atualiza botões de adicionar a lista
      existingListsContainer.innerHTML = "";

      shoppingLists.forEach((list) => {
        const btn = document.createElement("button");
        btn.textContent = list["name"];
        btn.name = list["name"];

        btn.addEventListener("click", () => {
          alert(`Produto adicionado à lista."${list["name"]}"`);
          closeAddToListModal();
        });
        existingListsContainer.appendChild(btn);
      });
    });
  }
}

// Apresenta o nome da lista no título do painel de listas
function renderShoppingListName(listName) {

}

// Apresenta os preços total e do carrinho (itens pegos)
function renderShoppingListPrices(totalPrice, cartPrice) {
  const listPanelFooter = document.getElementById("list-footer");

  listPanelFooter.innerHTML = `
    Preço total: <span>R$ ${totalPrice.toFixed(2).replace('.', ',')}</span> <br>
    Preço do carrinho: <span>R$ ${cartPrice.toFixed(2).replace('.', ',')}</span>
  `;
}

// Apresenta os itens da lista de compras (salvando id e nome do produto nos objs)
function renderShoppingListItems(listItems) {
  const listContainer = document.getElementById("shopping-list-items");
  listContainer.innerHTML = "";

  renderShoppingListPrices(1.2, 141411.233);
  
  // preenche a lista com os produtos
  listItems.forEach((product) => {
    const itemProduct = document.createElement("button");
    itemProduct.classList.add("product-item");
    itemProduct.id = product["product_id"];
    itemProduct.name = product["product_name"];

    itemProduct.addEventListener("click", () => {
      // ir p página de produto (import)
    });

    itemProduct.innerHTML = `
      <p>${product["product_name"]}</p>
      <span id="price-${product["product_id"]}">R$ preço</span>
      <span id="quant-${product["quantity"]}">${product["quantity"]}</span>
      <input type="checkbox" value="false"></input>
    `;

    listContainer.appendChild(itemProduct);
  });
}

// Abre o modal "Adicionar à Lista"
export function openAddToListModal(shoppingLists) {
  const modal = document.getElementById("modal-add-to-list");

  modal.classList.remove("hidden");
  document.body.classList.add("list-open"); // ativa o overlay + bloqueia scroll
}

// Função para fechar o modal de criação de lista
function closeAddToListModal() {
  const modal = document.getElementById("modal-add-to-list");
  modal.classList.add("hidden");
  document.body.classList.remove("list-open");
}

// Setup do Modal 
function setupAddToListModal() {
  const modalAdd = document.getElementById("modal-add-to-list");
  const modalNew = document.getElementById("modal-new-list");

  const btnCloseAdd = document.getElementById("close-add-to-list");
  const btnCancelAdd = document.getElementById("btn-cancel-add-to-list");
  const btnCreateNew = document.getElementById("btn-create-new-list");

  const btnCancelNew = document.getElementById("btn-cancel");
  const formNewList = document.getElementById("form-new-list");

  if (!modalAdd || !modalNew) return;

  // Fecha o modal
  btnCloseAdd.addEventListener("click", () => {
    closeAddToListModal();
  });

  // Cancela a Ação
  btnCancelAdd.addEventListener("click", () => {
    closeAddToListModal();
  });

  // Cria uma nova lista de compras
  btnCreateNew.addEventListener("click", () => {
    closeAddToListModal();
    modalNew.style.display = "flex";
    document.body.classList.add("list-open"); 
  });

  // Cancela a criação da lista
  btnCancelNew.addEventListener("click", () => {
    modalNew.style.display = "none";
    document.body.classList.remove("list-open");
  });

  formNewList.addEventListener("submit", (e) => {
    e.preventDefault();
    modalNew.style.display = "none";
    document.body.classList.remove("list-open");
  });
}

// Setup do Painel de Listas
function setupListPanel() {
  const btnMinhasListas = document.getElementById("btn-minhas-listas");
  const listPanel = document.getElementById("list-panel");
  const closeListPanelBtn = document.getElementById("close-list-panel");
  const filterToggle = document.getElementById("filter-toggle");

  const criarListaBtn = document.getElementById("btn-create-list"); 
  const modalNewList = document.getElementById("modal-new-list");
  const btnCancelModal = document.getElementById("btn-cancel");

  const newListForm = document.getElementById("form-new-list");
  const listName = document.getElementById("input-list-name");

  // Abre o painel
  btnMinhasListas.addEventListener("click", () => {
    listPanel.classList.add("active");
    document.body.classList.add("list-open");
    filterToggle.style.display = "none";
  });

  // Fecha o painel
  closeListPanelBtn.addEventListener("click", () => {
    listPanel.classList.remove("active");
    document.body.classList.remove("list-open");
    filterToggle.style.display = "block";

    getAllLists(user["userId"]);
  });

  // Cria uma nova lista
  criarListaBtn.addEventListener("click", () => {
    modalNewList.style.display = "flex";
    document.body.classList.add("list-open");
  });

  // Cancela a criação da lista
  btnCancelModal.addEventListener("click", () => {
    modalNewList.style.display = "none";
    document.body.classList.remove("list-open");
  });

  newListForm.addEventListener("submit", (e) => {
    e.preventDefault();
    modalNewList.style.display = "none";
    document.body.classList.remove("list-open");

    createList(user["userId"], listName.value);
  });
}

// setup dos listeners de eventos da tela
export function shoppingListSetupListeners() {
  socketio.on("all-shopping-lists", (lists) => {
    renderAllShoppingLists(lists);
  });

  socketio.on("shopping-list", (listItems) => {
    renderShoppingListItems(listItems)
  });
}

// setup dos eventos do HTML da tela
export function shoppingListSetupHTML() {
  // requisição inicial
  getAllLists(user["userId"]);

  setupListPanel();
  setupAddToListModal();
}
