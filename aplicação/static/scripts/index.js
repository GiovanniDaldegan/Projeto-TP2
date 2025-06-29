import { searchSetupHTML, searchListenersSocketio} from "./product_search.js";

export var socketio = io();


function setupProductSearch() {
  searchListenersSocketio(socketio);
  searchSetupHTML(socketio);
}

document.addEventListener("DOMContentLoaded", () => {

  // TODO: eventos de ativação chamam as funções de inicialização de outras telas
  setupProductSearch();
});
