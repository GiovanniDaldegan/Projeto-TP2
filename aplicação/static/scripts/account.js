var socketio = io();

document.addEventListener("DOMContentLoaded", () => {
  accountSetupListeners();
  accountSetupHTML();
});



// Emissores de eventos ao servidor

function requestRegisterUser(accType, username, password) {
  socketio.emit("register-user", {"acc_type": accType, "username": username, "password": password });
}

function requestLogin(username, password) {
  socketio.emit("login-user", {"username": username, "password": password});
}


// TODO #13: tranquilo - puxar nome e senha inseridos e fazer requisição de cadastro
// (passar tipo de conta: "client")



// setup dos listeners de eventos SocketIO
export function accountSetupListeners() {
  socketio.on("logged", (acc) => {
    sessionStorage.setItem("acc_type", acc["acc_type"]);
    sessionStorage.setItem("user_id", acc["user_id"]);
    sessionStorage.setItem("username", acc["username"]);

    location.href = "/";
  });
}


// setup dos eventos do HTML da tela
export function accountSetupHTML() {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  
  if (loginForm){
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");

    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      requestLogin(usernameInput.value, passwordInput.value);
    })
  }

  if (registerForm) {
    const createAccBtn = document.getElementById("btn-create-account")
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");

    createAccBtn.addEventListener("click", (e) => {
      e.preventDefault();
      requestRegisterUser("client", usernameInput.value, passwordInput.value);
    });
  }
}
