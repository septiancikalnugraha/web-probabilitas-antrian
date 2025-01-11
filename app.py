from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    arrival_rate = data.get("arrival_rate")  # λ: Rata-rata pelanggan datang
    service_rate = data.get("service_rate")  # μ: Rata-rata pelayanan

    if arrival_rate and service_rate:
        try:
            arrival_rate = float(arrival_rate)
            service_rate = float(service_rate)

            if service_rate <= arrival_rate:
                return jsonify({"error": "Service rate must be greater than arrival rate."})

            # Calculations
            rho = arrival_rate / service_rate
            l = rho / (1 - rho)  # Avg customers in system (L)
            lq = l - rho  # Avg customers in queue (Lq)
            w = l / arrival_rate  # Avg time in system (W)
            wq = w - (1 / service_rate)  # Avg time in queue (Wq)

            # Steps for explanation
            steps = [
                f"1. Tingkat Utilisasi (ρ): ρ = λ / μ = {arrival_rate:.2f} / {service_rate:.2f} = {rho:.2f}",
                f"2. Rata-rata Pelanggan di Sistem (L): L = ρ / (1 - ρ) = {rho:.2f} / (1 - {rho:.2f}) = {l:.2f}",
                f"3. Rata-rata Pelanggan dalam Antrian (Lq): Lq = L - ρ = {l:.2f} - {rho:.2f} = {lq:.2f}",
                f"4. Waktu Rata-rata Pelanggan di Sistem (W): W = L / λ = {l:.2f} / {arrival_rate:.2f} = {w:.2f}",
                f"5. Waktu Rata-rata Pelanggan dalam Antrian (Wq): Wq = W - (1 / μ) = {w:.2f} - (1 / {service_rate:.2f}) = {wq:.2f}"
            ]

            result = {
                "utilization": rho,
                "avg_customers_system": l,
                "avg_customers_queue": lq,
                "avg_time_system": w,
                "avg_time_queue": wq,
                "steps": steps
            }
            return jsonify(result)

        except ValueError:
            return jsonify({"error": "Invalid input. Please provide numeric values."})
    return jsonify({"error": "Missing arrival or service rate."})

if __name__ == "__main__":
    app.run(debug=True)
