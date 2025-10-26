document.addEventListener("DOMContentLoaded", () => {
  const sourceSelect = document.getElementById("source-select");
  const detectorSelect = document.getElementById("detector-select");
  const resultOutput = document.getElementById("result-output");

  // Campos do form de adicionar Source
  const addSourceBtn = document.getElementById("add-source-btn");
  const newSourceName = document.getElementById("new-source-name");
  const newSourceFile = document.getElementById("new-source-file");

  // Campos do form de adicionar Detector
  const addDetectorBtn = document.getElementById("add-detector-btn");
  const newDetectorName = document.getElementById("new-detector-name");
  const newDetectorApi = document.getElementById("new-detector-api");

  // Botão de run
  const runBtn = document.getElementById("run-btn");

  // ---------------------------
  // Funções de load
  // ---------------------------
  async function loadSources() {
    const res = await fetch("/api/v1/sources/list");
    const data = await res.json();
    sourceSelect.innerHTML = "";
    data.sources.forEach(src => {
      const opt = document.createElement("option");
      opt.value = src;
      opt.textContent = src;
      sourceSelect.appendChild(opt);
    });
  }

  async function loadDetectors() {
    const res = await fetch("/api/v1/detectors/list");
    const data = await res.json();
    detectorSelect.innerHTML = "";
    data.detectors.forEach(det => {
      const opt = document.createElement("option");
      opt.value = det;
      opt.textContent = det;
      detectorSelect.appendChild(opt);
    });
  }

  // Carrega listas na inicialização
  loadSources();
  loadDetectors();

  // ---------------------------
  // Adicionar nova fonte
  // ---------------------------
  addSourceBtn.addEventListener("click", async () => {
    if (!newSourceName.value || !newSourceFile.files[0]) {
      alert("Please provide both a source name and a JSON file.");
      return;
    }

    const file = newSourceFile.files[0];
    const text = await file.text();

    let parsed = JSON.parse(text);
    if (Array.isArray(parsed)) {
      parsed = { data: parsed }; // embrulha num objeto
    }

    const payload = {
      name: newSourceName.value,
      json_data: parsed
    };

    const res = await fetch("/api/v1/sources/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      alert("Source added successfully!");
      newSourceName.value = "";
      newSourceFile.value = "";
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
    const sourceName = sourceSelect.value;
    const detectorName = detectorSelect.value;

    const res = await fetch("/api/v1/runs/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source: sourceName, detector: detectorName })
    });

    const data = await res.json();
    resultOutput.textContent = JSON.stringify(data, null, 2);
  });
});
