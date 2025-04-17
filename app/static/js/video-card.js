function videoCardClicked(event) {
    event.preventDefault();
    const path = window.location.pathname;
    const video = event.target.closest(".video-card");
    if (!video) return;
    if (path === "/") {
        window.open(`/play/${video.getAttribute("value")}`);
    } else {
    }
}
