function sortButtonCilcked(event) {
    // 阻止默认行为
    event.preventDefault();

    // 通过 event.currentTarget 获得被点击的按钮对象
    const currentBtn = event.currentTarget;
    const currentKey = currentBtn.getAttribute("key");

    // 确定当前按钮的排序顺序，若为空则默认设置为 "asc"
    let currentOrder = currentBtn.getAttribute("order");
    let newOrder = "";
    if (!currentOrder) {
        newOrder = "desc";
    } else {
        newOrder = currentOrder === "asc" ? "desc" : "asc";
    }
    // 更新当前按钮内图标的显示情况
    renderSortBar(currentKey, newOrder);

    // 更新 URL 查询字符串中的排序参数，保留已有的其他参数
    const params = new URLSearchParams(window.location.search);
    params.set("page", 1);
    params.set("sort", currentKey);
    params.set("order", newOrder);
    history.replaceState(null, "", "?" + params.toString());

    // 调用数据更新函数，根据新的 URL 参数重新加载视频数据
    updateCurrentPage();
}

function renderSortBar(key, order) {
    document.querySelectorAll(".btn-sort img").forEach((img) => {
        if (img.parentElement.getAttribute("key") === key && img.getAttribute("order") === order) {
            img.parentElement.setAttribute("order", order);
            img.style.display = "block";
        } else {
            if (img.parentElement.getAttribute("key") !== key) {
                img.parentElement.setAttribute("order", "");
            }
            img.style.display = "none";
        }
    });
}
