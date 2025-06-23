var socketio = io();

// ! EXEMPLO !
// listener para o evento "get-product-list", cliente recebe o objeto transmitido e armazena em product_list
socketio.on("get-product-list", (product_list) => {
    console.log(product_list["product0"]);
    
    location.replace("https://www.pudim.com.br");
});
