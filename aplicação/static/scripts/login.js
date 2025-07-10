import { socketio } from "./index.js";

// Funções emissoras de requisição
function register() {

  const user = {
    "type"     : "sei la",
    "username" : document.getElementById("name-input").value,
    "password" : document.getElementById("pass-input").value
  }

  socketio.emit("register", user)
}


// Funções próprias do módulo


// setup dos listeners de eventos da tela
export function loginSetupListeners() {
  // const registerBttn = document.getElementById("register-bttn", () => {});
}


// setup dos eventos do HTML da tela
export function loginSetupHTML() {}
