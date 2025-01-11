document.getElementById("queueForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const arrivalRate = document.getElementById("arrival_rate").value;
    const serviceRate = document.getElementById("service_rate").value;

    fetch("/calculate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ arrival_rate: arrivalRate, service_rate: serviceRate }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                // Fill output fields with results
                document.getElementById("utilization").value = data.utilization.toFixed(2);
                document.getElementById("avg_customers_system").value = data.avg_customers_system.toFixed(2);
                document.getElementById("avg_customers_queue").value = data.avg_customers_queue.toFixed(2);
                document.getElementById("avg_time_system").value = data.avg_time_system.toFixed(2);
                document.getElementById("avg_time_queue").value = data.avg_time_queue.toFixed(2);

                // Display calculation steps
                const stepsList = document.getElementById("stepsList");
                stepsList.innerHTML = ""; // Clear previous steps
                data.steps.forEach((step) => {
                    const li = document.createElement("li");
                    li.textContent = step;
                    stepsList.appendChild(li);
                });
            }
        })
        .catch((error) => {
            console.error("Error during fetch:", error);
            alert("Terjadi kesalahan. Silakan coba lagi.");
        });
});
