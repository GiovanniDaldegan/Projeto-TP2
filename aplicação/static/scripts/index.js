import { productSearchSetupHTML, productSearchSetupListeners} from "./product_search.js";
import { shoppingListSetupHTML, shoppingListSetupListeners, setupListPanel } from "./shopping_list.js";
import { registerSetupHTML, registerSetupListeners } from "./register.js";
import { loginSetupHTML, loginSetupListeners} from "./login.js";

export var socketio = io();

export var user = {user_id : null, username : null};

function setupProductSearch() {
  productSearchSetupListeners();
  productSearchSetupHTML();
}

function setupShoppingList() {
  shoppingListSetupHTML();
  shoppingListSetupListeners();
}

function setupRegister() {
  registerSetupHTML();
  registerSetupListeners();
}

function setupLogin() {
  loginSetupHTML();
  loginSetupListeners();
}

document.addEventListener("DOMContentLoaded", () => {

  // TODO: eventos de ativação chamam as funções de inicialização de outras telas
  setupProductSearch();
  setupShoppingList();
});


