import { socketio } from "./index.js";

// setup dos listeners de eventos da tela
export function shoppingListSetupListeners() {}

function getLists() {
  socketio.emit("get-shopping-lists")
}

// setup dos eventos do HTML da tela
export function shoppingListSetupHTML() {
  setupListPanel();
  setupAddToListModal();
}

// Listas de Teste
const listasExistentes = [
  "Lista do Mercado",
  "Lista de Produtos de Limpeza",
  "Lista de Compras Rápidas"
];


// Abre o modal "Adicionar à Lista"
export function openAddToListModal() {
  const modal = document.getElementById("modal-add-to-list");
  const existingListsContainer = document.getElementById("existing-lists");

  existingListsContainer.innerHTML = "";

  listasExistentes.forEach((nomeLista) => {
    const btn = document.createElement("button");
    btn.textContent = nomeLista;
    btn.addEventListener("click", () => {
      alert(`Produto adicionado à lista "${nomeLista}"`);
      closeAddToListModal();
    });
    existingListsContainer.appendChild(btn);
  });

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
export function setupAddToListModal() {
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
export function setupListPanel() {
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
    createList(listName.value);
  });
}
