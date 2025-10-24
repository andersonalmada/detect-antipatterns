document.addEventListener("DOMContentLoaded", async () => {
  const sourceSelect = document.getElementById("source-select");
  const detectorSelect = document.getElementById("detector-select");
  const form = document.getElementById("run-form");
  const resultOutput = document.getElementById("result-output");

  // Função para listar fontes
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

  // Função para listar detectores
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

  // Carregar listas na inicialização
  await loadSources();
  await loadDetectors();

  // Submit do formulário
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData();
    const file = document.getElementById("file-input").files[0];
    const sourceName = sourceSelect.value;
    const detectorName = detectorSelect.value;

    if (file) {
      formData.append("file", file);
    }

    formData.append("detector", detectorName);
    formData.append("source", sourceName);

    const res = await fetch("/api/v1/runs/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source: sourceName, detector: detectorName })
    });

    const data = await res.json();
    resultOutput.textContent = JSON.stringify(data, null, 2);
  });
});
