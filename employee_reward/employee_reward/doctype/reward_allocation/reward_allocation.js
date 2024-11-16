// Copyright (c) 2024, Yousef Ashraf and contributors
// For license information, please see license.txt

frappe.ui.form.on("Reward Allocation", {
  after_save(frm) {
    // frappe.msgprint((msg = "test measssage"));
    console.log("test console");
  },
});
