document.querySelectorAll("[data-file-input]").forEach((input) => {
  input.addEventListener("change", () => {
    const output = input.parentElement.querySelector("[data-file-name]");
    output.textContent = input.files[0]?.name || "No file selected";
  });
});

document.querySelectorAll("[data-table-controls]").forEach((controls) => {
  const table = document.getElementById(controls.dataset.tableControls);
  const search = controls.querySelector("[data-table-search]");
  const status = controls.querySelector("[data-table-status]");
  const section = controls.closest(".data-section");
  const counter = section?.querySelector("[data-visible-count]");
  const rows = Array.from(table.tBodies[0].rows);
  const storageKey = `reconcileflow-table-filter:${window.location.pathname}:${table.id}`;
  let savedFilter = {};
  try { savedFilter = JSON.parse(sessionStorage.getItem(storageKey) || "{}"); } catch (_error) { savedFilter = {}; }
  if (savedFilter.search !== undefined) search.value = savedFilter.search;
  if (savedFilter.status !== undefined) status.value = savedFilter.status;

  const applyFilters = () => {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    rows.forEach((row) => {
      const matchesText = !query || row.textContent.toLocaleLowerCase().includes(query);
      const matchesStatus = !status.value || row.dataset.status === status.value;
      row.hidden = !(matchesText && matchesStatus);
      if (!row.hidden) visible += 1;
    });
    if (counter) counter.textContent = visible;
    const totalCell = table.querySelector("[data-filter-total]");
    const totalOutput = document.querySelector(`[data-table-total="${table.id}"]`);
    if (table.dataset.sumColumn !== undefined && (totalCell || totalOutput)) {
      const column = Number(table.dataset.sumColumn);
      const total = rows.reduce((sum, row) => {
        if (row.hidden) return sum;
        return sum + Number(row.cells[column]?.dataset.value || 0);
      }, 0);
      const formatted = total.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      if (totalCell) totalCell.textContent = formatted;
      if (totalOutput) totalOutput.textContent = formatted;
    }
    sessionStorage.setItem(storageKey, JSON.stringify({ search: search.value, status: status.value }));
  };

  search.addEventListener("input", applyFilters);
  status.addEventListener("change", applyFilters);
  applyFilters();
});

const reportPreview = document.querySelector("[data-report-preview]");
if (reportPreview) {
  const storageKey = "reconcileflow-report-workshop-v1";
  let initializing = true;
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(storageKey) || "{}"); } catch (_error) { saved = {}; }

  const persist = () => {
    if (initializing) return;
    const state = {};
    document.querySelectorAll("[data-report-input]").forEach((input) => { state[`input:${input.dataset.reportInput}`] = input.value; });
    document.querySelectorAll("[data-report-toggle], [data-logo-toggle], [data-column-toggle]").forEach((input) => {
      const key = input.dataset.reportToggle || input.dataset.logoToggle || input.dataset.columnToggle;
      const group = input.dataset.reportToggle ? "field" : input.dataset.logoToggle ? "logo" : "column";
      state[`${group}:${key}`] = input.checked;
    });
    localStorage.setItem(storageKey, JSON.stringify(state));
  };

  document.querySelectorAll("[data-report-input]").forEach((input) => {
    const key = input.dataset.reportInput;
    if (saved[`input:${key}`] !== undefined) input.value = saved[`input:${key}`];
    const render = () => {
      document.querySelectorAll(`[data-report-output="${key}"]`).forEach((node) => { node.textContent = input.value; });
      persist();
    };
    input.addEventListener("input", render);
    render();
  });

  document.querySelectorAll("[data-report-toggle]").forEach((input) => {
    const key = input.dataset.reportToggle;
    if (saved[`field:${key}`] !== undefined) input.checked = saved[`field:${key}`];
    const render = () => {
      document.querySelectorAll(`[data-report-field="${key}"]`).forEach((node) => { node.hidden = !input.checked; });
      persist();
    };
    input.addEventListener("change", render);
    render();
  });

  document.querySelectorAll("[data-logo-toggle]").forEach((input) => {
    const key = input.dataset.logoToggle;
    if (saved[`logo:${key}`] !== undefined) input.checked = saved[`logo:${key}`];
    const render = () => {
      document.querySelectorAll(`[data-report-logo="${key}"]`).forEach((node) => { node.hidden = !input.checked; });
      persist();
    };
    input.addEventListener("change", render);
    render();
  });

  document.querySelectorAll("[data-column-toggle]").forEach((input) => {
    const key = input.dataset.columnToggle;
    if (saved[`column:${key}`] !== undefined) input.checked = saved[`column:${key}`];
    const render = () => {
      document.querySelectorAll(`[data-report-column="${key}"]`).forEach((node) => { node.hidden = !input.checked; });
      persist();
    };
    input.addEventListener("change", render);
    render();
  });

  initializing = false;
  persist();
  document.querySelector("[data-print-report]")?.addEventListener("click", () => window.print());
}
