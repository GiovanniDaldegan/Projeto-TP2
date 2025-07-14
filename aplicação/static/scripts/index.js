import { productSearchSetupHTML, productSearchSetupListeners} from "./product_search.js";
import { shoppingListSetupHTML, shoppingListSetupListeners } from "./shopping_list.js";
import { accountSetupHTML, accountSetupListeners } from "./account.js";

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

function setupAccount() {
  accountSetupHTML();
  accountSetupListeners();
}

document.addEventListener("DOMContentLoaded", () => {
  setupProductSearch();
  setupShoppingList();
  //setupAccount();
});


