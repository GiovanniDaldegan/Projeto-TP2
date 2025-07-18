import { productSearchSetupHTML, productSearchSetupListeners} from "./product_search.js";
import { shoppingListSetupHTML, shoppingListSetupListeners } from "./shopping_list.js";

export var socketio = io();

export var user = {userId : 1, username : "Jorge da Capadócia"};

function setupProductSearch() {
  productSearchSetupListeners();
  productSearchSetupHTML();
}

function setupShoppingList() {
  shoppingListSetupHTML();
  shoppingListSetupListeners();
}

document.addEventListener("DOMContentLoaded", () => {
  setupProductSearch();
  setupShoppingList();
  console.log(sessionStorage.getItem("username"));
});


