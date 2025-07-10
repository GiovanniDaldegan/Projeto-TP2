import { socketio } from "./index.js";

// Funções emissoras de requisição
function createList(listName) {
  socketio.emit("create-shopping-list", listName);
}

function getLists() {
  socketio.emit("get-shopping-lists")
}

// Funções próprias do módulo
function feedShoppingLists(shoppingLists) {
  const listContainer = document.getElementById("list-content");

  shoppingLists.forEach(list => {
    const listItem = document.createElement("article");
    listItem.classList.add("shopping-list");

    listItem.innerHTML = `
      <h3 class="list-name">${list["name"]}</h3>
      <span class="list-size">${list["size"]}</span>
    `;

    listContainer.appendChild(listItem)
    console.log(listItem.innerHTML);
  });
}


// setup dos listeners de eventos da tela
export function shoppingListSetupListeners() {}


// setup dos eventos do HTML da tela
export function shoppingListSetupHTML() {}

export function setupListPanel() {
  const btnMinhasListas = document.getElementById("btn-minhas-listas");
  const listPanel = document.getElementById("list-panel");
  const closeListPanelBtn = document.getElementById("close-list-panel");
  const filterToggle = document.getElementById("filter-toggle");

  const ulLista = document.getElementById("shopping-list-items");
  const criarListaBtn = document.getElementById("btn-create-list"); 
  const modalNewList = document.getElementById("modal-new-list");
  const btnCancelModal = document.getElementById("btn-cancel");

  const newListForm = document.getElementById("form-new-list");
  const listName = document.getElementById("input-list-name");

  
  // Exibe o painel de listas
  btnMinhasListas.addEventListener("click", () => {
    listPanel.classList.add("active");  
    document.body.classList.add("list-open");
    filterToggle.style.display = "none";
  });

  // Fecha o painel de listas
  closeListPanelBtn.addEventListener("click", () => {
    listPanel.classList.remove("active");
    document.body.classList.remove("list-open");
    filterToggle.style.display = "block";
  });

  // Exibe o modal para criação de nova lista
  criarListaBtn.addEventListener("click", () => {
    modalNewList.style.display = "flex";
  });

  // Fecha o modal 
  btnCancelModal.addEventListener("click", () => {
    modalNewList.style.display = "none";
  });

  // Confirma a criação de lista
  newListForm.addEventListener("submit", (e) => {
    e.preventDefault();
    modalNewList.style.display = "none";
    createList(listName.value);
  });

  // mock up
  feedShoppingLists([{"name" : "FODA", 'size' : 123}, {"name" : "FODA2", 'size' : 321}])
}
