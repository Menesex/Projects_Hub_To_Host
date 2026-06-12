// Sanitize user data before inserting into innerHTML to prevent XSS
function escapeHtml(value) {
    if (value === null || value === undefined) return '';
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// 1. Load employees on page load
window.onload = () => loadEmployees();

// 2. Fetch employees from API with current filters
async function loadEmployees() {
    const status     = document.getElementById('statusFilter').value;
    const search     = document.getElementById('searchInput').value;
    const searchType = document.getElementById('searchType').value;

    // encodeURIComponent prevents broken URLs if the user types &, ?, etc.
    const url = `/employees?status=${encodeURIComponent(status)}&search=${encodeURIComponent(search)}&search_type=${encodeURIComponent(searchType)}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const employees = await response.json();
        renderTable(employees);
    } catch (error) {
        console.error("Error cargando empleados:", error);
        document.getElementById('employeeBody').innerHTML =
            '<tr><td colspan="8" style="text-align:center;color:#dc2626;padding:20px">Error al cargar los datos. Intenta de nuevo.</td></tr>';
    }
}

// 3. Render employees table dynamically
function renderTable(employees) {
    const tableBody = document.getElementById('employeeBody');

    if (employees.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:20px;color:#64748b">No se encontraron empleados.</td></tr>';
        return;
    }

    tableBody.innerHTML = employees.map(emp => {
        const isActive = emp.active;
        // escapeHtml on every field that comes from the database
        const id       = escapeHtml(emp.id);
        const name     = escapeHtml(emp.name);
        const access   = escapeHtml(emp.access_id) || 'LIBRE';
        const area     = escapeHtml(emp.area);
        const position = escapeHtml(emp.position);
        const hour     = escapeHtml(emp.entry_hour);

        return `
            <tr id="row-${id}" class="${isActive ? '' : 'row-retired'}">
                <td>${id}</td>
                <td class="col-name">${name}</td>
                <td class="col-access">${access}</td>
                <td class="col-area">${area}</td>
                <td class="col-position">${position}</td>
                <td class="col-hour">${hour}</td>
                <td>
                    <span class="${isActive ? 'status-active' : 'status-inactive'}">
                        ${isActive ? 'Activo' : 'Retirado'}
                    </span>
                </td>
                <td>
                    ${isActive
                        ? `<button onclick="editMode(${emp.id})">Editar</button>
                           <button onclick="handleRetire(${emp.id})" style="background-color:#ff4d4d;color:white;border:none;border-radius:4px;cursor:pointer;">Retirar</button>`
                        : `<span style="color:gray">Sin acciones</span>`
                    }
                </td>
            </tr>
        `;
    }).join('');
}

// 4. Switch a row to edit mode (inputs instead of text)
function editMode(id) {
    const row = document.getElementById(`row-${id}`);

    // Read current values from the cells
    const name   = row.querySelector('.col-name').innerText;
    const access = row.querySelector('.col-access').innerText;
    const area   = row.querySelector('.col-area').innerText;
    const pos    = row.querySelector('.col-position').innerText;
    const hour   = row.querySelector('.col-hour').innerText;

    // escapeHtml prevents broken inputs if values contain quotes or angle brackets
    row.innerHTML = `
        <td>${id}</td>
        <td><input type="text" id="editName-${id}"   value="${escapeHtml(name)}"                          style="width:90%"></td>
        <td><input type="text" id="editAccess-${id}" value="${escapeHtml(access === 'LIBRE' ? '' : access)}" style="width:80%"></td>
        <td><input type="text" id="editArea-${id}"   value="${escapeHtml(area)}"                          style="width:90%"></td>
        <td><input type="text" id="editPos-${id}"    value="${escapeHtml(pos)}"                           style="width:90%"></td>
        <td><input type="time" id="editHour-${id}"   value="${escapeHtml(hour)}"></td>
        <td>Activo</td>
        <td>
            <button onclick="saveEdit(${id})" style="background-color:#28a745;color:white;">Guardar</button>
            <button onclick="loadEmployees()"  style="background-color:#6c757d;color:white;">Cancelar</button>
        </td>
    `;
}

// 5. Save edits (PUT)
async function saveEdit(id) {
    const updatedEmp = {
        name:       document.getElementById(`editName-${id}`).value.trim(),
        access_id:  document.getElementById(`editAccess-${id}`).value.trim() || null,
        area:       document.getElementById(`editArea-${id}`).value.trim(),
        position:   document.getElementById(`editPos-${id}`).value.trim(),
        entry_hour: document.getElementById(`editHour-${id}`).value,
        active:     true,
    };

    if (!updatedEmp.name || !updatedEmp.area || !updatedEmp.position) {
        alert("Nombre, área y cargo son obligatorios");
        return;
    }

    try {
        const response = await fetch(`/employees/${id}`, {
            method:  'PUT',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(updatedEmp),
        });

        if (!response.ok) {
            const data = await response.json().catch(() => ({}));
            alert(`Error: ${data.detail || 'No se pudo actualizar'}`);
            return;
        }
        loadEmployees();
    } catch {
        alert("Error de conexión al actualizar");
    }
}

// 6. Create new employee (POST)
async function saveEmployee() {
    const newEmp = {
        name:       document.getElementById('newName').value.trim(),
        access_id:  document.getElementById('newAccessId').value.trim() || null,
        area:       document.getElementById('newArea').value.trim(),
        position:   document.getElementById('newPosition').value.trim(),
        entry_hour: document.getElementById('newEntryHour').value,
        active:     true,
    };

    if (!newEmp.name || !newEmp.area || !newEmp.position) {
        alert("Nombre, área y cargo son obligatorios");
        return;
    }

    try {
        const response = await fetch('/employees', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(newEmp),
        });

        if (!response.ok) {
            const data = await response.json().catch(() => ({}));
            alert(`Error: ${data.detail || 'No se pudo crear el empleado'}`);
            return;
        }
        closeModal();
        loadEmployees();
    } catch {
        alert("Error de conexión al crear el empleado");
    }
}

// 7. Retire employee (PATCH)
async function handleRetire(id) {
    if (!confirm("¿Estás seguro de retirar a este empleado? La tarjeta quedará libre.")) return;

    try {
        const response = await fetch(`/employees/${id}/retire`, { method: 'PATCH' });
        if (!response.ok) {
            const data = await response.json().catch(() => ({}));
            alert(`Error: ${data.detail || 'No se pudo retirar el empleado'}`);
            return;
        }
        loadEmployees();
    } catch {
        alert("Error de conexión al retirar el empleado");
    }
}

// 8. Live search
function searchEmployees() {
    loadEmployees();
}

// --- Modal helpers ---
function openModal() {
    document.getElementById('employeeModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('employeeModal').style.display = 'none';
    document.getElementById('newName').value       = "";
    document.getElementById('newAccessId').value   = "";
    document.getElementById('newArea').value       = "";
    document.getElementById('newPosition').value   = "";
    document.getElementById('newEntryHour').value  = "08:00";
}
