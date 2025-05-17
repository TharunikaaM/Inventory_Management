$(document).ready(function () {
    $.ajax({
        url: '/api/movements/movements',
        method: 'GET',
        success: function (data) {
            console.log("Data received:", data);
            if (data.length === 0) {
                $('#movement-table tbody').append('<tr><td colspan="6">No movements found.</td></tr>');
                return;
            }

            data.forEach(function (item) {
                $('#movement-table tbody').append(`
                    <tr>
                        <td>${item.movement_id}</td>
                        <td>${new Date(item.timestamp).toLocaleString()}</td>
                        <td>${item.product_name}</td>
                        <td>${item.from_location}</td>
                        <td>${item.to_location}</td>
                        <td>${item.qty}</td>
                    </tr>
                `);
            });
        },
        error: function (err) {
            console.error("Error loading movements:", err);
            $('#movement-table tbody').append('<tr><td colspan="6">Error loading data.</td></tr>');
        }
    });
});
