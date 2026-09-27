document.addEventListener("DOMContentLoaded", () => {

    document
        .querySelectorAll("form[data-validate]")
        .forEach((form) => {

            if (!form.action.includes("/recommendations/")) {
                return;
            }

            form.addEventListener("submit", async (event) => {

                event.preventDefault();

                if (!form.checkValidity()) {
                    form.reportValidity();
                    return;
                }

                const button = form.querySelector(
                    "button[type='submit']"
                );

                if (button) {
                    button.disabled = true;
                    button.textContent = "Generating...";
                }

                const formData = new FormData(form);
                const data = {};

                formData.forEach((value, key) => {
                    data[key] = value;
                });

                if (data.total_budget !== undefined) {
                    data.total_budget = Number(data.total_budget);
                }

                if (data.number_of_items !== undefined) {
                    data.number_of_items =
                        Number(data.number_of_items);
                }

                if (data.guests !== undefined) {
                    data.guests = Number(data.guests);
                }

                if (data.budget !== undefined) {
                    data.budget = Number(data.budget);
                }

                try {

                    const response = await fetch(
                        form.action,
                        {
                            method: "POST",
                            credentials: "include",
                            headers: {
                                "Content-Type":
                                    "application/json"
                            },
                            body: JSON.stringify(data)
                        }
                    );

                    const result = await response.json();

                    if (!response.ok) {
                        throw new Error(
                            JSON.stringify(result.detail)
                        );
                    }

                    sessionStorage.setItem(
                        "recommendationResult",
                        JSON.stringify(result)
                    );

                    window.location.href =
                        "/recommendations";

                } catch (error) {

                    alert(
                        "Recommendation failed: " +
                        error.message
                    );

                    if (button) {
                        button.disabled = false;
                        button.textContent =
                            "Generate Recommendation";
                    }
                }

            });

        });

});