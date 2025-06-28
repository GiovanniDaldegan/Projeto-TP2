export function request_product_list(socketio, filters) {
    socketio.emit("get-product-list", filters);
}

export function request_categories(socketio) {
    socketio.emit("get-categories");
}
