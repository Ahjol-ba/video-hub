const searchEnter = document.getElementById("enter-search");
const searchInput = document.getElementById("input-search");
const searchCLear = document.getElementById("clear-search");

function searchInputListener(event) {
    event.preventDefault();
    searchCLear.style.display = searchInput.value.length > 0 ? "block" : "none";
    searchInput.addEventListener("keydown", function (newEven) {
        if (newEven.key == "Enter") searchEnterListener(newEven);
    });
}

function searchEnterListener(event) {
    event.preventDefault();
    const params = new URLSearchParams(window.location.search);
    params.set("search", searchInput.value);
    history.replaceState(null, "", "?" + params.toString());
    updateCurrentPage();
}

function searchClearListener(event) {
    event.preventDefault();
    searchInput.value = "";
    searchEnterListener(event);
    searchInput.focus();
}

function renderSearchBar(value) {
    searchInput.value = value;
    searchCLear.style.display = searchInput.value.length > 0 ? "block" : "none";
}
