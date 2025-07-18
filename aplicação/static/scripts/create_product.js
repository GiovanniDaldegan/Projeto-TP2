var socketio = io();

function requestCreateProduct(name, price=null) {
  socketio.emit("register-product", {
    "name" : 'churrasco'
  })
}

document.addEventListener("DOMContentLoaded", () => {
  const createProductBtn = document.getElementById("btn-create-product")
  
  const productName = document.getElementById("product_name").value;
  const productCat = document.getElementById("category").value;
  const productMarket = document.getElementById("supermarket").value;
  const productPrice = document.getElementById("price").value;

  createProductBtn.addEventListener("click", () => {
    console.log(productName)
    requestCreateProduct(productName);
  });
});