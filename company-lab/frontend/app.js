const apiStatus = document.getElementById("api-status");
const lastRefresh = document.getElementById("last-refresh");
const refreshAllButton = document.getElementById("refresh-all");

const employeesCount = document.getElementById("employees-count");
const openTicketsCount = document.getElementById("open-tickets-count");
const criticalTicketsCount = document.getElementById("critical-tickets-count");
const assetsCount = document.getElementById("assets-count");
const serversOnlineCount = document.getElementById("servers-online-count");
const servicesCount = document.getElementById("services-count");
const openChangesCount = document.getElementById("open-changes-count");

const servicesTable = document.getElementById("services-table");
const ticketsTable = document.getElementById("tickets-table");
const assetsTable = document.getElementById("assets-table");
const serversTable = document.getElementById("servers-table");
const changesTable = document.getElementById("changes-table");
const auditTable = document.getElementById("audit-table");

const ticketForm = document.getElementById("ticket-form");
const changeForm = document.getElementById("change-form");

function escapeHtml(value) {
  if (value === null || value === undefined) return "";
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function shortTime(value) {
  if (!value) return "--";
  try {
    return new Date(value).toLocaleString();
  } catch {
    return value;
  }
}

function badge(value) {
  const safe = escapeHtml(value || "unknown");
  const cls = safe.replaceAll(" ", "_");
  return `<span class="badge badge-${cls}">${safe}</span>`;
}

async function apiGet(path) {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`${path} returned HTTP ${response.status}`);
  }
  return response.json();
}

async function apiSend(path, method, body) {
  const response = await fetch(path, {
    method,
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`${method} ${path} failed: ${response.status} ${text}`);
  }

  return response.json();
}

function setApiStatus(ok, message) {
  apiStatus.textContent = message;
  apiStatus.classList.remove("pill-ok", "pill-warn", "pill-bad");
  apiStatus.classList.add(ok ? "pill-ok" : "pill-bad");
}

function renderError(table, cols, error) {
  table.innerHTML = `
    <tr>
      <td colspan="${cols}" class="error-text">${escapeHtml(error.message)}</td>
    </tr>
  `;
}

async function loadSummary() {
  const summary = await apiGet("/api/summary");

  employeesCount.textContent = summary.employees;
  openTicketsCount.textContent = summary.open_tickets;
  criticalTicketsCount.textContent = summary.critical_tickets;
  assetsCount.textContent = summary.assets;
  serversOnlineCount.textContent = `${summary.online_servers}/${summary.servers}`;
  servicesCount.textContent = summary.services;
  openChangesCount.textContent = summary.open_changes;
}

async function loadServices() {
  try {
    const services = await apiGet("/api/services");

    servicesTable.innerHTML = services.map(service => `
      <tr>
        <td><strong>${escapeHtml(service.name)}</strong></td>
        <td>${escapeHtml(service.host)}</td>
        <td>${escapeHtml(service.port)}</td>
        <td>${badge(service.status)}</td>
        <td>${escapeHtml(service.description)}</td>
        <td>${shortTime(service.last_check)}</td>
      </tr>
    `).join("");
  } catch (error) {
    renderError(servicesTable, 6, error);
  }
}

async function loadTickets() {
  try {
    const tickets = await apiGet("/api/tickets");

    ticketsTable.innerHTML = tickets.map(ticket => `
      <tr>
        <td>${ticket.id}</td>
        <td>
          <strong>${escapeHtml(ticket.title)}</strong>
          ${ticket.description ? `<br><small>${escapeHtml(ticket.description)}</small>` : ""}
        </td>
        <td>${badge(ticket.status)}</td>
        <td>${badge(ticket.priority)}</td>
        <td>${escapeHtml(ticket.assigned_to || "--")}</td>
        <td>${shortTime(ticket.updated_at || ticket.created_at)}</td>
        <td>
          <div class="actions">
            <button class="small" onclick="updateTicketStatus(${ticket.id}, 'open')">Open</button>
            <button class="small" onclick="updateTicketStatus(${ticket.id}, 'in_progress')">Progress</button>
            <button class="small" onclick="updateTicketStatus(${ticket.id}, 'waiting')">Waiting</button>
            <button class="small" onclick="updateTicketStatus(${ticket.id}, 'resolved')">Resolved</button>
            <button class="small" onclick="updateTicketStatus(${ticket.id}, 'closed')">Closed</button>
          </div>
        </td>
      </tr>
    `).join("");
  } catch (error) {
    renderError(ticketsTable, 7, error);
  }
}

async function loadAssets() {
  try {
    const assets = await apiGet("/api/assets");

    assetsTable.innerHTML = assets.map(asset => `
      <tr>
        <td>${escapeHtml(asset.asset_type)}</td>
        <td><strong>${escapeHtml(asset.name)}</strong></td>
        <td>${escapeHtml(asset.owner || "--")}</td>
        <td>${badge(asset.status)}</td>
      </tr>
    `).join("");
  } catch (error) {
    renderError(assetsTable, 4, error);
  }
}

async function loadServers() {
  try {
    const servers = await apiGet("/api/servers");

    serversTable.innerHTML = servers.map(server => `
      <tr>
        <td><strong>${escapeHtml(server.hostname)}</strong></td>
        <td><code>${escapeHtml(server.ip_address)}</code></td>
        <td>${escapeHtml(server.role)}</td>
        <td>${escapeHtml(server.os)}</td>
        <td>${badge(server.status)}</td>
      </tr>
    `).join("");
  } catch (error) {
    renderError(serversTable, 5, error);
  }
}

async function loadChanges() {
  try {
    const changes = await apiGet("/api/changes");

    changesTable.innerHTML = changes.map(change => `
      <tr>
        <td>${change.id}</td>
        <td>
          <strong>${escapeHtml(change.title)}</strong>
          ${change.description ? `<br><small>${escapeHtml(change.description)}</small>` : ""}
        </td>
        <td>${escapeHtml(change.service || "--")}</td>
        <td>${badge(change.risk)}</td>
        <td>${badge(change.status)}</td>
        <td>${shortTime(change.created_at)}</td>
      </tr>
    `).join("");
  } catch (error) {
    renderError(changesTable, 6, error);
  }
}

async function loadAudit() {
  try {
    const audit = await apiGet("/api/audit");

    auditTable.innerHTML = audit.map(item => `
      <tr>
        <td>${item.id}</td>
        <td>${shortTime(item.created_at)}</td>
        <td>${badge(item.event_type)}</td>
        <td>${escapeHtml(item.entity_type || "--")}${item.entity_id ? ` #${item.entity_id}` : ""}</td>
        <td>${escapeHtml(item.message)}</td>
      </tr>
    `).join("");
  } catch (error) {
    renderError(auditTable, 5, error);
  }
}

async function refreshAll() {
  refreshAllButton.disabled = true;
  refreshAllButton.textContent = "Refreshing...";

  try {
    await apiGet("/api/health");
    setApiStatus(true, "API healthy");

    await Promise.all([
      loadSummary(),
      loadServices(),
      loadTickets(),
      loadAssets(),
      loadServers(),
      loadChanges(),
      loadAudit()
    ]);

    lastRefresh.textContent = `Last refresh: ${new Date().toLocaleString()}`;
  } catch (error) {
    setApiStatus(false, "API problem");
    console.error(error);
  } finally {
    refreshAllButton.disabled = false;
    refreshAllButton.textContent = "Refresh";
  }
}

async function updateTicketStatus(ticketId, status) {
  await apiSend(`/api/tickets/${ticketId}`, "PATCH", { status });
  await refreshAll();
}

ticketForm.addEventListener("submit", async event => {
  event.preventDefault();

  const body = {
    title: document.getElementById("ticket-title").value,
    priority: document.getElementById("ticket-priority").value,
    assigned_to: document.getElementById("ticket-assigned").value || null,
    description: document.getElementById("ticket-description").value || null
  };

  await apiSend("/api/tickets", "POST", body);
  ticketForm.reset();
  document.getElementById("ticket-priority").value = "medium";
  await refreshAll();
});

changeForm.addEventListener("submit", async event => {
  event.preventDefault();

  const body = {
    title: document.getElementById("change-title").value,
    service: document.getElementById("change-service").value || null,
    risk: document.getElementById("change-risk").value,
    status: document.getElementById("change-status").value,
    description: document.getElementById("change-description").value || null
  };

  await apiSend("/api/changes", "POST", body);
  changeForm.reset();
  document.getElementById("change-risk").value = "medium";
  document.getElementById("change-status").value = "planned";
  await refreshAll();
});

refreshAllButton.addEventListener("click", refreshAll);

refreshAll();
setInterval(refreshAll, 30000);
