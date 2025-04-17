document.addEventListener("DOMContentLoaded", function () {
    // 点赞按钮功能
    const likeButton = document.getElementById("like-button");
    if (likeButton) {
        likeButton.addEventListener("click", function (event) {
            event.preventDefault();
            const uuid = likeButton.getAttribute("data-uuid");
            fetch(`/play/${uuid}/like`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: JSON.stringify({}),
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`Server error: ${response.status}`);
                    }
                    return response.json();
                })
                .then((data) => {
                    document.getElementById("like-count").textContent = data.like_count;
                    if (data.action === "liked") {
                        likeButton.classList.add("liked");
                    } else {
                        likeButton.classList.remove("liked");
                    }
                })
                .catch((error) => console.error("Error:", error));
        });
    }

    // Tag 输入框：按 Enter 触发添加标签
    const tagInput = document.getElementById("tag-input");
    if (tagInput) {
        tagInput.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                document.getElementById("add-tag-button").click();
            }
        });
    }

    // 添加标签功能
    const addTagButton = document.getElementById("add-tag-button");
    if (addTagButton) {
        addTagButton.addEventListener("click", function (event) {
            event.preventDefault();
            const tagName = tagInput.value.trim();
            if (!tagName) return;
            const uuid = addTagButton.getAttribute("data-video-uuid");
            fetch(`/play/${uuid}/add_tag`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: JSON.stringify({ tag_name: tagName }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.status === "ok") {
                        const tagsContainer = document.querySelector(".tags-container");
                        if (tagsContainer.textContent.trim() === "暂无标签") {
                            tagsContainer.textContent = "";
                        }
                        // 新增跳转项（统一结构）
                        const jumpItem = document.createElement("div");
                        jumpItem.classList.add("jump-item");

                        const jumpButton = document.createElement("button");
                        jumpButton.type = "button";
                        jumpButton.classList.add("jump-button");
                        jumpButton.onclick = () => {
                            window.location.href = `/?search=${encodeURIComponent(data.tag.name)}&page=1`;
                        };
                        const spanText = document.createElement("span");
                        spanText.classList.add("span-text");
                        spanText.setAttribute("keyword", "tag");
                        spanText.setAttribute("data-id", data.tag.id);
                        spanText.textContent = data.tag.name;

                        jumpButton.appendChild(spanText);
                        jumpItem.appendChild(jumpButton);

                        // 添加删除按钮
                        const deleteButton = document.createElement("button");
                        deleteButton.type = "button";
                        deleteButton.classList.add("tag-delete-button");
                        deleteButton.setAttribute("data-tag-id", data.tag.id);
                        deleteButton.setAttribute("data-video-uuid", data.video.uuid);

                        jumpItem.appendChild(deleteButton);
                        tagsContainer.appendChild(jumpItem);

                        tagInput.value = "";
                    } else if (data.status === "appended") {
                        tagInput.value = "";
                    } else {
                        alert(data.message || "添加标签失败");
                    }
                })
                .catch((error) => console.error("Error:", error));
        });
    }

    // 删除标签事件
    const tagsContainer = document.querySelector(".tags-container");
    if (tagsContainer) {
        tagsContainer.addEventListener("click", function (event) {
            if (event.target && event.target.classList.contains("tag-delete-button")) {
                event.preventDefault();
                const tagId = event.target.getAttribute("data-tag-id");
                const uuid = event.target.getAttribute("data-video-uuid");
                fetch(`/play/${uuid}/remove_tag/${tagId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-Requested-With": "XMLHttpRequest",
                    },
                    body: JSON.stringify({}),
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.status === "ok") {
                            event.target.parentNode.remove();
                            if (tagsContainer.children.length === 0) {
                                const span = document.createElement("span");
                                span.textContent = "暂无标签";
                                tagsContainer.appendChild(span);
                            }
                        } else {
                            alert(data.message || "删除标签失败");
                        }
                    })
                    .catch((error) => console.error("Error:", error));
            }
        });
    }
});
