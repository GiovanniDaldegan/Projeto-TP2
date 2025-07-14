import { socketio, user } from "./index.js";

// Emissores de eventos ao servidor

function requestRegisterUser(accType, username, password) {
  socketio.emit("register-user", {"acc_type": accType, "username": username, "password": password });
}

function requestLogin(username, password) {
  socketio.emit("login", {"username": username, "password": password});
}


// TODO #13: tranquilo - puxar nome e senha inseridos e fazer requisição de cadastro
// (passar tipo de conta: "client")

// TODO #14: tranquilo - puxar nome e senha inseridos, fazer requisição de login e logar


// setup dos listeners de eventos SocketIO
export function accountSetupListeners() {
  socketio.on("logged", (acc) => {
    user["acc_type"] = acc["acc_type"];
    user["user_id"] = acc["user_id"];
    user["username"] = acc["username"];
  });
}


// setup dos eventos do HTML da tela
export function accountSetupHTML() {}
  