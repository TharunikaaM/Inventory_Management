document.addEventListener('DOMContentLoaded', () => {
    const locationTable = document.querySelector('#location-table tbody');
    const totalLocations = document.getElementById('total-locations');
    const addModal = document.getElementById('add-modal');
    const editModal = document.getElementById('edit-modal');
    const addBtn = document.getElementById('add-location-btn');
    const updateBtn = document.getElementById('update-location-btn');

    let selectedLocationId = null;

    // Load locations
    function loadLocations() {
        fetch('/api/locations/')
            .then(res => res.json())
            .then(data => {
                locationTable.innerHTML = '';
                totalLocations.textContent = data.length;
                data.forEach(location => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${location.l_id}</td>
                        <td>${location.l_name}</td>
                    `;
                    row.addEventListener('click', () => openEditModal(location.l_id, location.l_name));
                    locationTable.appendChild(row);
                });
            });
    }

    // Add location
    addBtn.addEventListener('click', () => {
        const name = document.getElementById('add-location-name').value.trim();
        if (name) {
            fetch('/api/locations/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ l_name: name })
            }).then(res => res.json()).then(() => {
                closeModal('add-modal');
                loadLocations();
                document.getElementById('add-location-name').value = '';
            });
        }
    });

    // Edit location
    updateBtn.addEventListener('click', () => {
        const name = document.getElementById('edit-location-name').value.trim();
        if (name && selectedLocationId) {
            fetch(`/api/locations/${selectedLocationId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ l_name: name })
            }).then(res => res.json()).then(() => {
                closeModal('edit-modal');
                loadLocations();
            });
        }
    });

    // Modal handling
    document.getElementById('open-add-modal').addEventListener('click', () => {
        openModal('add-modal');
    });

    window.openEditModal = (id, name) => {
        selectedLocationId = id;
        document.getElementById('edit-location-name').value = name;
        openModal('edit-modal');
    };

    window.openModal = (id) => {
        document.getElementById(id).style.display = 'flex';
    };

    window.closeModal = (id) => {
        document.getElementById(id).style.display = 'none';
        if (id === 'edit-modal') selectedLocationId = null;
    };

    loadLocations();
});
