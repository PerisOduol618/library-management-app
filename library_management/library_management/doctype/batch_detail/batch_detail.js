// Copyright (c) 2024, 	Oduol Peris  and contributors
// For license information, please see license.txt

frappe.ui.form.on('Batch Detail', {
    refresh: function(frm) {
        frm.add_custom_button('Fetch Batch Data', function() {
            frappe.call({
                method: 'your_app.your_module.fetch_and_create_batch_details',
                callback: function(response) {
                    if (response.message.status === "success") {
                        frappe.msgprint("Batch data fetched successfully!");
                    } else {
                        frappe.msgprint("Failed to fetch data: " + response.message.message);
                    }
                }
            });
        });
    }
});

