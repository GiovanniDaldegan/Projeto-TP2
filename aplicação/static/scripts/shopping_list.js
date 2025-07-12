import { socketio, user } from "./index.js";

// Emissores de eventos ao servidor

function getAllLists() {
  socketio.emit("get-all-shopping-lists")
}

function createList(listName, userId) {
  socketio.emit("create-shopping-list", {"user_id": userId, "list_name": listName});
}

function deleteList(listId) {
  socketio.emti("delete-list", listId);
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
// (melhorar o html de listItem)
function feedShoppingLists(shoppingLists) {
  const listContainer = document.getElementById("shopping-list-items");
  const existingListsContainer = document.getElementById("existing-lists");

  if (shoppingLists.length == 0) {
    listContainer.innerHTML = "Você não possui listas.";
    existingListsContainer.innerHTML = "Você não possui listas."
  }
  else {
    listContainer.innerHTML = "";

    shoppingLists.forEach(list => {
      // Atualiza listas do painel de listas de compras
      const listItem = document.createElement("article");
      listItem.classList.add("item-shopping-list");
  
      listItem.innerHTML = `
        <h3 class="list-name">${list["name"]}</h3>
        <span class="list-size">${list["size"]} itens</span>
      `;
  
      console.log(listItem);
      listContainer.appendChild(listItem);

      // Atualiza botões de adicionar a lista
      existingListsContainer.innerHTML = "";

      shoppingLists.forEach((lista) => {
        const btn = document.createElement("button");
        btn.textContent = lista["name"];
        btn.addEventListener("click", () => {
          alert(`Produto adicionado à lista "${lista["name"]}"`);
          closeAddToListModal();
        });
        existingListsContainer.appendChild(btn);
      });
    });
  }
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
    createList(user["user_id"], listName.value);
  });
}

// setup dos listeners de eventos da tela
export function shoppingListSetupListeners() {
  socketio.on("all-shopping-lists", (lists) => {
    feedShoppingLists(lists);
  });
}

// setup dos eventos do HTML da tela
export function shoppingListSetupHTML() {
  // requisição inicial
  getAllLists();

  setupListPanel();
  setupAddToListModal();
}
