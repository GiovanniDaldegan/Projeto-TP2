import { socketio } from "./index.js";

// Emissores de eventos ao servidor
function requestProductInfo(idProduct) {
  socketio.emit("get-product", idProduct);
}

function addReview(userId, idProduct) {
  socketio.emit("review-product", {"user_id": userId, "id_product": idProduct});
}


// setup dos listeners de eventos do servidor
export function productSetupListeners() {}

// setup dos eventos do HTML da tela
export function productSetupHTML() {}
