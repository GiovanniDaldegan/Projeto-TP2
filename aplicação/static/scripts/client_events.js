export function request_product_list(socketio, searchTerm, filters) {
    socketio.emit("get-product-list", {
        "search_term"   : searchTerm,
        "filters"       : filters
    });
}

export function request_categories(socketio) {
    socketio.emit("get-categories");
}
