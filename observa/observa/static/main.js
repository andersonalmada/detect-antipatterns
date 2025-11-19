document.addEventListener("DOMContentLoaded", () => {
  // ----------------------
  // LOGIN HANDLING
  // ----------------------
  const loginScreen = document.getElementById("login-screen");
  const appContent = document.getElementById("app-content");
  const loginBtn = document.getElementById("login-btn");
  const loginUser = document.getElementById("login-username");
  const loginPass = document.getElementById("login-password");

  function showApp() {
    loginScreen.style.display = "none";
    appContent.style.display = "block";
  }

  if (localStorage.getItem("auth_token")) {
    showApp();
  }

  loginBtn.addEventListener("click", async () => {
    const res = await fetch("/api/v1/admin/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: loginUser.value,
        password: loginPass.value
      })
    });

    const data = await res.json();

    if (data.success) {
      localStorage.setItem("auth_token", data.token);
      showApp();
    } else {
      alert("Invalid username or password.");
    }
  });

  const logoutBtn = document.getElementById("logout-btn");

  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("auth_token");
    appContent.style.display = "none";
    loginScreen.style.display = "flex"; // volta a tela
    loginUser.value = "";
    loginPass.value = "";
  });

  const sourceSelect = document.getElementById("source-select");
  const detectorSelect = document.getElementById("detector-select");
  const resultOutput = document.getElementById("result-output");
  const sourceHistorySelect = document.getElementById("history-filter-source");
  const detectorHistorySelect = document.getElementById("history-filter-detector");

  // Campos do form de adicionar Source
  const addSourceBtn = document.getElementById("add-source-btn");
  const newSourceName = document.getElementById("new-source-name");
  const newSourceFile = document.getElementById("new-source-file");
  const newSourceApi = document.getElementById("new-source-api");

  // Campos do form de adicionar Detector
  const addDetectorBtn = document.getElementById("add-detector-btn");
  const newDetectorName = document.getElementById("new-detector-name");
  const newDetectorApi = document.getElementById("new-detector-api");

  const startDateInput = document.getElementById("history-start-date");
  const endDateInput = document.getElementById("history-end-date");

  const d = new Date();
  d.setHours(d.getHours() - 3);
  iso = d.toISOString().slice(0, 16);

  startDateInput.value = iso;
  endDateInput.value = iso;

  // Botão de run
  const runBtn = document.getElementById("run-btn");

  // Botão de history
  const historyRefreshBtn = document.getElementById("history-refresh-btn");

  historyRefreshBtn.addEventListener("click", async () => {
    loadHistoryFromAPI();
  });

  const autoRunBtn = document.getElementById("auto-run-btn");
  const intervalInput = document.getElementById("interval-seconds");
  let autoRunInterval = null;

  autoRunBtn.addEventListener("click", async () => {
    if (autoRunInterval) {
      clearInterval(autoRunInterval);
      autoRunInterval = null;
      autoRunBtn.textContent = "⏱️ Start Auto Run";
      autoRunBtn.classList.remove("btn-danger");
      autoRunBtn.classList.add("btn-outline-primary");
      return;
    }

    const intervalSeconds = parseInt(intervalInput.value);
    if (isNaN(intervalSeconds) || intervalSeconds < 1) {
      alert("Please enter a valid interval (in seconds).");
      return;
    }

    async function runDetection() {
      const selectedSources = Array.from(sourceSelect.selectedOptions).map(opt => opt.value);
      const selectedDetectors = Array.from(detectorSelect.selectedOptions).map(opt => opt.value);

      const res = await fetch("/api/v1/runs/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sources: selectedSources, detectors: selectedDetectors })
      });

      const data = await res.json();
      resultOutput.textContent = JSON.stringify(data, null, 2);
    }

    // Executa imediatamente uma vez
    runDetection();

    // Inicia o intervalo
    autoRunInterval = setInterval(runDetection, intervalSeconds * 1000);
    autoRunBtn.textContent = "⏹️ Stop Auto Run";
    autoRunBtn.classList.remove("btn-outline-primary");
    autoRunBtn.classList.add("btn-danger");
  });

  // ---------------------------
  // Funções de load
  // ---------------------------
  async function loadSources() {
    const res = await fetch("/api/v1/sources/list");
    const data = await res.json();
    sourceSelect.innerHTML = "";
    sourceHistorySelect.innerHTML = "";
    data.sources.forEach(src => {
      const opt = document.createElement("option");
      opt.value = src;
      opt.textContent = src;
      sourceSelect.appendChild(opt);

      const opt2 = document.createElement("option");
      opt2.value = src;
      opt2.textContent = src;
      sourceHistorySelect.appendChild(opt2);
    });
  }

  async function loadDetectors() {
    const res = await fetch("/api/v1/detectors/list");
    const data = await res.json();
    detectorSelect.innerHTML = "";
    detectorHistorySelect.innerHTML = "";
    data.detectors.forEach(det => {
      const opt = document.createElement("option");
      opt.value = det;
      opt.textContent = det;
      detectorSelect.appendChild(opt);

      const opt2 = document.createElement("option");
      opt2.value = det;
      opt2.textContent = det;
      detectorHistorySelect.appendChild(opt2);
    });
  }

  // Carrega listas na inicialização
  loadSources();
  loadDetectors();

  // ---------------------------
  // Adicionar nova fonte
  // ---------------------------
  addSourceBtn.addEventListener("click", async () => {
    name = newSourceName.value
    api = newSourceApi.value
    file = newSourceFile.files[0]

    payload = {}

    if (!name) {
      alert("Please provide a source name.");
      return;
    }

    payload.name = name

    if (api) {
      payload.api_url = api;
      payload.json_data = null;
    } else if (file) {
      const text = await file.text();
      let parsed;
      try {
        parsed = JSON.parse(text);
      } catch (err) {
        alert("Invalid JSON file.");
        return;
      }
      payload.json_data = parsed;
      payload.api_url = null;
    } else {
      alert("Please provide either a JSON file or an API URL.");
      return;
    }

    const res = await fetch("/api/v1/sources/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      alert("Source added successfully!");
      newSourceName.value = "";
      newSourceFile.value = "";
      newSourceApi.value = "";
      loadSources();
    } else {
      alert("Error adding source.");
    }
  });

  // ---------------------------
  // Adicionar novo detector
  // ---------------------------
  addDetectorBtn.addEventListener("click", async () => {
    if (!newDetectorName.value || !newDetectorApi.value) {
      alert("Please provide both a detector name and an API URL.");
      return;
    }

    const payload = {
      name: newDetectorName.value,
      api_url: newDetectorApi.value
    };

    const res = await fetch("/api/v1/detectors/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      alert("Detector added successfully!");
      newDetectorName.value = "";
      newDetectorApi.value = "";
      loadDetectors();
    } else {
      alert("Error adding detector.");
    }
  });

  // ---------------------------
  // Run detector
  // ---------------------------
  runBtn.addEventListener("click", async () => {
    const selectedSources = Array.from(sourceSelect.selectedOptions).map(opt => opt.value);
    const selectedDetectors = Array.from(detectorSelect.selectedOptions).map(opt => opt.value);

    const res = await fetch("/api/v1/runs/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sources: selectedSources, detectors: selectedDetectors })
    });

    const data = await res.json();
    resultOutput.textContent = JSON.stringify(data, null, 2);
  });

  const clearDbBtn = document.getElementById("clear-db-btn");

  clearDbBtn.addEventListener("click", async () => {
    if (!confirm("⚠️ This will delete all sources and detectors. Continue?")) return;

    const res = await fetch("/api/v1/admin/clear", { method: "DELETE" });
    const data = await res.json();

    alert(data.message);
    await loadSources();
    await loadDetectors();
  });

  sourceSelect.addEventListener("keydown", async (e) => {
    if (e.key === "Delete") {
      const selected = Array.from(sourceSelect.selectedOptions).map(opt => opt.value);
      if (!selected.length) return;

      if (!confirm(`⚠️ Delete selected sources: ${selected.join(", ")}?`)) return;

      const res = await fetch("/api/v1/admin/sources", {
        method: "DELETE", // ou DELETE se preferir
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ names: selected })
      });

      const data = await res.json();
      alert(data.message);
      await loadSources();
    }
  });

  // Função para deletar detectores
  detectorSelect.addEventListener("keydown", async (e) => {
    if (e.key === "Delete") {
      const selected = Array.from(detectorSelect.selectedOptions).map(opt => opt.value);
      if (!selected.length) return;

      if (!confirm(`⚠️ Delete selected detectors: ${selected.join(", ")}?`)) return;

      const res = await fetch("/api/v1/admin/detectors", {
        method: "DELETE", // ou DELETE
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ names: selected })
      });

      const data = await res.json();
      alert(data.message);
      await loadDetectors();
    }
  });

  sourceSelect.addEventListener("dblclick", async () => {
    const selectedOptions = Array.from(sourceSelect.selectedOptions);
    if (selectedOptions.length !== 1) {
      alert("Please select a single source to see details.");
      return;
    }
    const name = selectedOptions[0].value;

    const res = await fetch(`/api/v1/sources/get?name=${encodeURIComponent(name)}`);
    if (!res.ok) {
      alert("Error fetching source details.");
      return;
    }
    const data = await res.json();
    alert("Source details:\n" + JSON.stringify(data, null, 2));
  });

  detectorSelect.addEventListener("dblclick", async () => {
    const selectedOptions = Array.from(detectorSelect.selectedOptions);
    if (selectedOptions.length !== 1) {
      alert("Please select a single detector to see details.");
      return;
    }
    const name = selectedOptions[0].value;

    const res = await fetch(`/api/v1/detectors/get?name=${encodeURIComponent(name)}`);
    if (!res.ok) {
      alert("Error fetching detector details.");
      return;
    }
    const data = await res.json();
    alert("Detector details:\n" + JSON.stringify(data, null, 2));
  });

  let stackedHistoryChart = null;

  function createOrUpdateHistoryChart(execs) {
    const labels = execs.map(e =>
      new Date(e.timestamp).toLocaleString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
      })
    );

    console.log(execs)

    const detectedData = execs.map(e => e.detected);
    const remainingData = execs.map(e => e.total - e.detected);

    if (!stackedHistoryChart) {
      stackedHistoryChart = new Chart(document.getElementById("stackedBarHistory"), {
        type: "bar",
        data: {
          labels,
          datasets: [
            {
              label: "Detected",
              data: detectedData,
              backgroundColor: "#F28B82",
              stack: "stack1"
            },
            {
              label: "Passed",
              data: remainingData,
              backgroundColor: "#A7E0A5",
              stack: "stack1"
            }
          ]
        },
        options: {
          responsive: true,
          plugins: { legend: { position: "top" } },
          scales: {
            x: { stacked: true },
            y: { stacked: true, beginAtZero: true }
          }
        }
      });
    } else {
      stackedHistoryChart.data.labels = labels;
      stackedHistoryChart.data.datasets[0].data = detectedData;
      stackedHistoryChart.data.datasets[1].data = remainingData;
      stackedHistoryChart.update();
    }
  }

  async function loadHistoryFromAPI() {
    const source = sourceHistorySelect.value;
    const detector = detectorHistorySelect.value;

    const start = startDateInput.value;
    const end = endDateInput.value;

    if (!source || !detector) return;

    let url = `/api/v1/runs/history?source=${encodeURIComponent(source)}&detector=${encodeURIComponent(detector)}`;
    if (start) url += `&start=${encodeURIComponent(start)}`;
    if (end) url += `&end=${encodeURIComponent(end)}`;

    const res = await fetch(url);
    const execs = await res.json();

    createOrUpdateHistoryChart(execs);
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && loginScreen.style.display !== "none") {
      loginBtn.click();
    }
  });
});

