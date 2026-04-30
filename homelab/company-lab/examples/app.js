async function fetchJson(path) {
    const response = await fetch(path);

    if (!response.ok) {
        throw new Error(`HTTP ${response.status} for ${path}`);
    }

    return await response.json();
}

function setText(id, value) {
    document.getElementById(id).innerText = value;
}

function ticketBadge(status) {
    if (status === "open") {
        return '<span class="badge badge-open">open</span>';
    }

    if (status === "in_progress") {
        return '<span class="badge badge-progress">in progress</span>';
    }

    if (status === "closed") {
        return '<span class="badge badge-closed">closed</span>';
    }

    return `<span class="badge">${status}</span>`;
}

function serverBadge(status) {
    if (status === "online") {
        return '<span class="badge badge-online">online</span>';
    }

    return `<span class="badge badge-open">${status}</span>`;
}

async function loadStatus() {
    try {
        const status = await fetchJson("/api/status");
        setText("backend-status", status.status.toUpperCase());
        document.getElementById("backend-status").className = "number status-ok";
    } catch (error) {
        setText("backend-status", "ERROR");
        document.getElementById("backend-status").className = "number status-bad";
        console.error(error);
    }
}

async function loadSummary() {
    const summary = await fetchJson("/api/summary");

    setText("employees-count", summary.employees);
    setText("open-tickets-count", summary.open_tickets);
    setText("assets-count", summary.assets);
    setText("servers-count", summary.servers);
}

async function loadEmployees() {
    const employees = await fetchJson("/api/employees");
    const tbody = document.getElementById("employees-table");

    tbody.innerHTML = employees.map(employee => `
        <tr>
            <td>${employee.full_name}</td>
            <td>${employee.department}</td>
            <td>${employee.position}</td>
            <td>${employee.email}</td>
        </tr>
    `).join("");
}

async function loadTickets() {
    const tickets = await fetchJson("/api/tickets");
    const tbody = document.getElementById("tickets-table");

    tbody.innerHTML = tickets.map(ticket => `
        <tr>
            <td>#${ticket.id}</td>
            <td>${ticket.title}</td>
            <td>${ticketBadge(ticket.status)}</td>
            <td>${ticket.priority}</td>
            <td>${ticket.assigned_to}</td>
        </tr>
    `).join("");
}

async function loadAssets() {
    const assets = await fetchJson("/api/assets");
    const tbody = document.getElementById("assets-table");

    tbody.innerHTML = assets.map(asset => `
        <tr>
            <td>${asset.asset_type}</td>
            <td>${asset.name}</td>
            <td>${asset.owner}</td>
            <td>${asset.status}</td>
        </tr>
    `).join("");
}

async function loadServers() {
    const servers = await fetchJson("/api/servers");
    const tbody = document.getElementById("servers-table");

    tbody.innerHTML = servers.map(server => `
        <tr>
            <td>${server.hostname}</td>
            <td>${server.ip_address}</td>
            <td>${server.role}</td>
            <td>${server.os}</td>
            <td>${serverBadge(server.status)}</td>
        </tr>
    `).join("");
}

async function loadDashboard() {
    await loadStatus();
    await loadSummary();
    await loadEmployees();
    await loadTickets();
    await loadAssets();
    await loadServers();
}

loadDashboard().catch(error => {
    console.error("Dashboard loading failed:", error);
});
