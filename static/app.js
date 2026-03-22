
function qs(a) {
    return document.querySelector(a);
}

/**
 * Handle on load/init js
 */
window.onload = () => {
    const modal = new bootstrap.Modal('#loadingModal', {
        keyboard: false
    })

    qs("#uploadFileInput").onchange = async e => {
        var file = e.target.files[0];
        qs("#fileNameLabel").textContent = file.name;
        console.log(file.name);

        const formData = new FormData();
        formData.append('file', file);

        modal.show()
        const returned = await fetch("/upload", {
            method: "POST",
            body: formData,
        });

        if (returned.redirected) {
            window.location.href = returned.url;
        }

        const response = await returned.json();
        const status = returned.status;
    };
    if (qs("#hash").textContent) {
        qs("#convertFileBtn").addEventListener("click", async () => {
            modal.show();
            const returned = await fetch("/convert/" + qs("#hash").textContent, {
                method: "GET",
            });

            if (returned.redirected) {
                window.location.href = returned.url;
            }
        });
    }
    qs("#uploadFileBtn").addEventListener("click", () => {
        qs("#uploadFileInput").click();
    });
};

function getHash() {
    return qs("#hash").textContent;
}
