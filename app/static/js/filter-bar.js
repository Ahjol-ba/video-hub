function filterBtnCilcked(event) {
    event.preventDefault();

    // 通过 event.currentTarget 获得被点击的按钮对象
    const btn = event.currentTarget;
    const currentKey = btn.getAttribute("key");
    const currentIdx = btn.getAttribute("idx");

    // 获取当前URL中的参数
    const params = new URLSearchParams(window.location.search);
    // 设置参数
    params.set("page", 1);
    params.set(currentKey, currentIdx);
    //  更新当前页URL
    history.replaceState(null, "", "?" + params.toString());
    // 渲染动画
    renderFilterBar(currentKey, currentIdx);
    // 查询视频
    updateCurrentPage();
}

function renderFilterBar(key, index) {
    document.querySelectorAll(`.btn-filter[key="${key}"]`).forEach((btn) => {
        const btnKey = btn.getAttribute("key");
        const btnIndex = btn.getAttribute("idx");
        btn.classList.remove("selected");
        if (key === btnKey && index === btnIndex) {
            btn.classList.add("selected");
        }
    });
}
