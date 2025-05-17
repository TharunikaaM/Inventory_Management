document.addEventListener('DOMContentLoaded', () => {
    const productTable = document.querySelector('#product-table tbody');
    const totalProducts = document.getElementById('total-products');
    const addModal = document.getElementById('add-modal');
    const editModal = document.getElementById('edit-modal');
    const addBtn = document.getElementById('add-product-btn');
    const updateBtn = document.getElementById('update-product-btn');

    let selectedProductId = null;

    // Load products
    function loadProducts() {
        fetch('/api/products/')
            .then(res => res.json())
            .then(data => {
                productTable.innerHTML = '';
                totalProducts.textContent = data.length;
                data.forEach(product => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${product.p_id}</td>
                        <td>${product.p_name}</td>
                    `;
                    row.addEventListener('click', () => openEditModal(product.p_id, product.p_name));
                    productTable.appendChild(row);
                });
            });
    }

    // Add product
    addBtn.addEventListener('click', () => {
        const name = document.getElementById('add-product-name').value.trim();
        if (name) {
            fetch('/api/products/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ p_name: name })
            }).then(res => res.json()).then(() => {
                closeModal('add-modal');
                loadProducts();
                document.getElementById('add-product-name').value = '';
            });
        }
    });

    // Edit product
    updateBtn.addEventListener('click', () => {
        const name = document.getElementById('edit-product-name').value.trim();
        if (name && selectedProductId) {
            fetch(`/api/products/${selectedProductId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ p_name: name })
            }).then(res => res.json()).then(() => {
                closeModal('edit-modal');
                loadProducts();
            });
        }
    });

    // Modal handling
    document.getElementById('open-add-modal').addEventListener('click', () => {
        openModal('add-modal');
    });

    window.openEditModal = (id, name) => {
        selectedProductId = id;
        document.getElementById('edit-product-name').value = name;
        openModal('edit-modal');
    };

    window.openModal = (id) => {
        document.getElementById(id).style.display = 'flex';
    };

    window.closeModal = (id) => {
        document.getElementById(id).style.display = 'none';
        if (id === 'edit-modal') selectedProductId = null;
    };

    loadProducts();
});
