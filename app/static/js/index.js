document.addEventListener("DOMContentLoaded", function () {
    // 获取 URL 参数
    const params = new URLSearchParams(window.location.search);
    // 重新渲染页面
    for (const key of params.keys()) {
        if (key === "search") {
            renderSearchBar(params.get(key, ""));
        } else if (key === "sort" || key === "order") {
            renderSortBar(params.get("sort"), params.get("order"));
        } else {
            renderFilterBar(key, params.get(key));
        }
    }
    updateCurrentPage();
});

// 更新当前页面
function updateCurrentPage() {
    queryVideos();
}

// 更新视频列表的通用函数
function queryVideos() {
    const params = new URLSearchParams(window.location.search);
    fetch("/api/videos?" + params.toString())
        .then((response) => response.json())
        .then((data) => {
            const showcase = document.querySelector(".showcase");
            if (data.total > 0) {
                showcase.style["display"] = "grid";
                showcase.innerHTML = data.videos.join("");
            } else {
                showcase.style["display"] = "flex";
                showcase.innerHTML = "<img src='/static/img/empty.svg' id='there-is-empty'>";
            }
            const pagination = document.querySelector(".pagination");
            pagination.innerHTML = data.pages;
        })
        .catch((err) => console.error("Error:search failed.", err));
}
