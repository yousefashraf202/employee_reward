// Copyright (c) 2024, Yousef Ashraf and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Effective Date Notice", {
//   refresh(frm) {
//     console.log("Document saved successfully:", frm.doc.name);
//   },
// });

// frappe.ui.form.on("Effective Date Notice", {
//   after_save(frm) {
//     // Fetch the latest values from the server (you can use frm.doc to get the updated values)
//     if (frm.doc.last_annual_leave_start_date) {
//       // Setting the values from the backend to the frontend fields
//       frm.set_value(
//         "last_annual_leave_start_date",
//         frm.doc.last_annual_leave_start_date
//       );
//       frm.set_value(
//         "last_annual_leave_end_date",
//         frm.doc.last_annual_leave_end_date
//       );
//       frm.set_value("total_leave_days", frm.doc.total_leave_days);
//     }
//   },
// });

// frappe.ui.form.on("Effective Date Notice", {
//   after_save(frm) {
//     console.log(frm.doc.name);
//   },
// });
