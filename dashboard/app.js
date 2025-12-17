const API = "http://localhost:8000";

async function updateDashboard() {
  try {
    // ---- TELEMETRY ----
    const telemetryRes = await fetch(`${API}/telemetry?limit=10`);
    const telemetry = await telemetryRes.json();

    if (telemetry.length > 0) {
      const latest = telemetry[0];

      document.getElementById("vib-val").innerText =
        latest.vibration_level.toFixed(3);

      document.getElementById("temp-val").innerText =
        latest.temperature.toFixed(1);
    }

    // ---- TABLE ----
    const tbody = document.getElementById("telemetry-body");
    tbody.innerHTML = "";

    telemetry.forEach(row => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="p-3">${row.timestamp.split("T")[1].split(".")[0]}</td>
        <td class="p-3">${row.device_id}</td>
        <td class="p-3">${row.vibration_level.toFixed(3)}</td>
        <td class="p-3 ${row.anomaly ? "text-red-400" : "text-green-400"}">
          ${row.anomaly ? "ALERT" : "OK"}
        </td>
      `;
      tbody.appendChild(tr);
    });

    // ---- ALERTS ----
    const alertsRes = await fetch(`${API}/alerts?limit=5`);
    const alerts = await alertsRes.json();

    document.getElementById("anomaly-count").innerText = alerts.length;

    const alertsBox = document.getElementById("alerts-container");
    if (alerts.length === 0) {
      alertsBox.innerHTML =
        `<p class="text-gray-500 italic text-sm">No alerts</p>`;
    } else {
      alertsBox.innerHTML = alerts.map(a => `
        <div class="mb-2 p-3 bg-red-900/30 border border-red-500/50 rounded">
          <b>⚠ Anomaly</b><br/>
          Device: ${a.device_id}<br/>
          Vib: ${a.vibration_level.toFixed(2)}
        </div>
      `).join("");
    }

  } catch (err) {
    console.error("Dashboard error:", err);
  }
}

setInterval(updateDashboard, 2000);
updateDashboard();
