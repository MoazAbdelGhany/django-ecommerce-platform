document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".add-to-cart-form").forEach(form => {
        form.addEventListener("submit", function (e) {
            e.preventDefault(); 

            const url = form.action;
            const formData = new FormData(form);

            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value
                }
            })
        });
    });

});