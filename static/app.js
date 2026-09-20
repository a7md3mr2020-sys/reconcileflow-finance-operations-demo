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
  let rows = Array.from(table.tBodies[0].rows);
  const storageKey = `reconcileflow-table-filter:${window.location.pathname}:${table.id}`;
  let savedFilter = {};
  try { savedFilter = JSON.parse(sessionStorage.getItem(storageKey) || "{}"); } catch (_error) { savedFilter = {}; }
  if (savedFilter.search !== undefined) search.value = savedFilter.search;
  if (savedFilter.status !== undefined) status.value = savedFilter.status;

  const applyFilters = () => {
    rows = Array.from(table.tBodies[0].rows);
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    rows.forEach((row) => {
      const matchesText = !query || (row.dataset.searchText || row.textContent).toLocaleLowerCase().includes(query);
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
    if (table.hasAttribute("data-invoice-totals")) {
      ["invoice", "collected", "balance"].forEach((field) => {
        const output = table.querySelector(`[data-invoice-total="${field}"]`);
        const total = rows.reduce((sum, row) => sum + (row.hidden ? 0 : Number(row.dataset[field] || 0)), 0);
        if (output) output.textContent = total.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      });
    }
    sessionStorage.setItem(storageKey, JSON.stringify({ search: search.value, status: status.value }));
  };

  search.addEventListener("input", applyFilters);
  status.addEventListener("change", applyFilters);
  table.addEventListener("reconcileflow:table-changed", applyFilters);
  applyFilters();
});

document.querySelectorAll(".project-picker").forEach((picker) => {
  const checkboxes = Array.from(picker.querySelectorAll('input[name="project"]'));
  const output = picker.querySelector("[data-project-selection]");
  const button = picker.querySelector("[data-open-projects]");
  const update = () => {
    const selected = checkboxes.filter((checkbox) => checkbox.checked).length;
    const label = `${selected} projects selected`;
    output.textContent = window.reconcileflowTranslateText?.(label) || label;
    button.disabled = selected < 2;
  };
  checkboxes.forEach((checkbox) => checkbox.addEventListener("change", update));
  update();
});

const formatAmount = (value) => Number(value).toLocaleString("en-US", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
});

document.querySelectorAll("[data-amount-form]").forEach((form) => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const input = form.querySelector('input[name="amount"]');
    const button = form.querySelector("button");
    const row = form.closest("tr");
    const previousStatus = row.dataset.status;
    button.disabled = true;
    form.classList.remove("is-error", "is-saved");
    input.setCustomValidity("");
    try {
      const response = await fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } });
      const data = await response.json();
      if (!response.ok || !data.ok) throw new Error(data.error || "The adjustment could not be saved.");

      input.value = Number(data.movement.after).toFixed(2);
      const variance = row.querySelector("[data-row-variance]");
      variance.dataset.value = data.row.amount_variance;
      variance.textContent = formatAmount(data.row.amount_variance);
      variance.classList.toggle("positive", data.row.amount_variance > 0);
      variance.classList.toggle("negative", data.row.amount_variance < 0);
      row.dataset.status = data.row.status;
      const status = row.querySelector("[data-row-status]");
      status.className = `status status-${data.row.status}`;
      status.textContent = data.row.status_label;
      row.querySelector("[data-row-differences]").textContent = data.row.differences.join(", ") || "None";
      window.reconcileflowTranslateElement?.(row);

      const bookingTable = row.closest("table");
      const allBookingRows = Array.from(bookingTable.tBodies[0].rows);
      const combinedVariance = allBookingRows.reduce((sum, item) => sum + Number(item.querySelector("[data-row-variance]")?.dataset.value || 0), 0);
      document.querySelector("[data-combined-variance]").textContent = formatAmount(combinedVariance);
      if (previousStatus !== data.row.status) {
        document.querySelector("[data-combined-matched]").textContent = allBookingRows.filter((item) => item.dataset.status === "matched").length;
      }

      const dailyBody = document.querySelector("[data-daily-matching-body]");
      if (dailyBody && data.daily_html !== undefined) {
        dailyBody.innerHTML = data.daily_html;
        window.reconcileflowTranslateElement?.(dailyBody);
        dailyBody.closest("table").dispatchEvent(new CustomEvent("reconcileflow:table-changed"));
      }

      const movementBody = document.querySelector("[data-movement-body]");
      const movementRow = document.createElement("tr");
      movementRow.dataset.status = data.movement.side;
      movementRow.innerHTML = `<td>${data.movement.occurred_at.slice(0, 16).replace("T", " ")}</td><td></td><td class="reference"></td><td></td><td class="number">${formatAmount(data.movement.before)}</td><td class="number">${formatAmount(data.movement.after)}</td><td class="number variance ${data.movement.movement > 0 ? "positive" : data.movement.movement < 0 ? "negative" : ""}" data-value="${data.movement.movement}">${formatAmount(data.movement.movement)}</td><td></td>`;
      movementRow.cells[1].textContent = data.movement.project;
      movementRow.cells[2].textContent = data.movement.reference;
      movementRow.cells[3].textContent = data.movement.side === "system_a" ? "System A" : "System B";
      movementRow.cells[7].textContent = data.movement.action;
      movementBody.prepend(movementRow);
      window.reconcileflowTranslateElement?.(movementRow);
      movementBody.closest("table").dispatchEvent(new CustomEvent("reconcileflow:table-changed"));
      const combinedMovement = Array.from(movementBody.rows).reduce((sum, item) => sum + Number(item.cells[6]?.dataset.value || 0), 0);
      document.querySelector("[data-combined-movement]").textContent = formatAmount(combinedMovement);
      bookingTable.dispatchEvent(new CustomEvent("reconcileflow:table-changed"));
      form.classList.add("is-saved");
      window.setTimeout(() => form.classList.remove("is-saved"), 1400);
    } catch (error) {
      form.classList.add("is-error");
      input.setCustomValidity(error.message);
      input.reportValidity();
      input.addEventListener("input", () => input.setCustomValidity(""), { once: true });
    } finally {
      button.disabled = false;
    }
  });
});

document.addEventListener("submit", async (event) => {
  const form = event.target.closest("[data-invoice-form]");
  if (!form) return;
  event.preventDefault();
  const button = form.querySelector('button[type="submit"]');
  const row = form.closest("tr");
  const originalLabel = button.textContent;
  let message = form.querySelector("[data-save-message]");
  if (!message) {
    message = document.createElement("span");
    message.dataset.saveMessage = "";
    message.setAttribute("role", "status");
    form.append(message);
  }
  button.disabled = true;
  message.textContent = "";
  try {
    const response = await fetch(form.action, {
      method: "POST", body: new FormData(form), headers: { "Accept": "application/json" }
    });
    const data = await response.json();
    if (!response.ok || !data.ok) throw new Error(data.error || "Could not save this change.");
    const company = data.company;
    if (form.hasAttribute("data-invoice-add")) {
      const container = document.createElement("tbody");
      container.innerHTML = data.row_html;
      const newRow = container.querySelector("tr");
      document.querySelector("[data-invoice-names-body]").append(newRow);
      form.reset();
      window.reconcileflowTranslateElement?.(newRow);
      row?.closest("table")?.dispatchEvent(new CustomEvent("reconcileflow:table-changed"));
      document.getElementById("invoice-names-table")?.dispatchEvent(new CustomEvent("reconcileflow:table-changed"));
    } else if (row) {
      row.dataset.status = company.direction;
      if (row.closest("#invoice-table")) {
        row.dataset.searchText = `${company.name} ${company.code} ${company.notes}`;
        row.dataset.invoice = company.invoice;
        row.dataset.collected = company.paid + company.payment;
        row.dataset.balance = company.balance;
        row.cells[1].querySelector("strong").textContent = company.name;
        const stage = row.querySelector('select[name="stage"]');
        stage.value = company.stage;
        stage.className = `stage-select stage-${company.stage}`;
        row.querySelector("[data-invoice-value]").textContent = formatAmount(company.invoice);
        row.querySelector("[data-paid-value]").textContent = formatAmount(company.paid);
        row.querySelector('input[name="payment"]').value = Number(company.payment).toFixed(2);
        const balance = row.querySelector("[data-balance-value]");
        balance.textContent = formatAmount(company.balance);
        balance.classList.toggle("positive", company.balance > 0);
        balance.classList.toggle("negative", company.balance < 0);
        const directionLabel = company.direction[0].toUpperCase() + company.direction.slice(1);
        row.querySelector("[data-direction]").textContent = window.reconcileflowTranslateText?.(directionLabel) || directionLabel;
        row.querySelector("[data-progress]").textContent = `${company.progress}%`;
        row.cells[9].textContent = company.notes;
      } else {
        row.dataset.searchText = `${company.name} ${company.code} ${company.notes}`;
        row.querySelector('input[name="name"]').value = company.name;
        row.querySelector('input[name="invoice"]').value = Number(company.invoice).toFixed(2);
        row.querySelector('input[name="paid"]').value = Number(company.paid).toFixed(2);
      }
      row.closest("table").dispatchEvent(new CustomEvent("reconcileflow:table-changed"));
    }
    button.textContent = window.reconcileflowTranslateText?.("Saved") || "Saved";
    window.setTimeout(() => { button.textContent = originalLabel; }, 1500);
  } catch (error) {
    message.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});

document.querySelectorAll("[data-invoice-output-link]").forEach((link) => {
  link.addEventListener("click", () => {
    const controls = document.querySelector('[data-table-controls="invoice-table"], [data-table-controls="invoice-names-table"]');
    const url = new URL(link.href);
    const query = controls?.querySelector("[data-table-search]")?.value.trim() || "";
    const direction = controls?.querySelector("[data-table-status]")?.value || "";
    if (query) url.searchParams.set("q", query);
    else url.searchParams.delete("q");
    if (direction) url.searchParams.set("direction", direction);
    else url.searchParams.delete("direction");
    link.href = url.toString();
  });
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
