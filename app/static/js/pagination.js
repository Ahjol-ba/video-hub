function jumpPage(event) {
    event.preventDefault();
    const btn = event.target;
    const currntPage = btn.getAttribute("page");
    const params = new URLSearchParams(window.location.search);
    params.set("page", currntPage);
    window.location.href = "?" + params.toString();
}
