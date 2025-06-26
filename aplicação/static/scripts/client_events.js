export function request_product_list(socketio, product_name, filters) {
    socketio.emit("get-product-list", {
        product_name : product_name,
        filters      : filters
    });
}

export function request_filters(socketio) {
    socketio.emit("get-filters");
}
