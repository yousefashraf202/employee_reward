# Copyright (c) 2024, Yousef Ashraf and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EffectiveDateNotice(Document):
    # frappe.msgprint(msg="test inside the class validate1111", title="test title")

    def after_save(self):
        frappe.msgprint(msg="test inside the class validate2222", title="test title")
        employee_leave = frappe.db.get_list(
            'Leave Application',
            filters={'employee': self.employee, 'status': 'Approved', 'custom_is_annual_leave': 1},
            fields=['from_date', 'to_date', 'total_leave_days'],
            order_by='from_date desc'
        )

        if employee_leave:
            self.last_annual_leave_start_date = employee_leave[0]['from_date']
            self.last_annual_leave_end_date = employee_leave[0]['to_date']
            self.total_leave_days = employee_leave[0]['total_leave_days']
        frappe.msgprint(msg="test inside the class validate3333", title="test title")
        


# def after_save(doc):
#     employee_leave = frappe.db.get_list(
#         'Leave Application',
#         filters={'employee': doc.employee, 'status': 'Approved', 'custom_is_annual_leave': 1},
#         fields=['from_date', 'to_date', 'total_leave_days'],
#         order_by='from_date desc'
#     )

#     if employee_leave:
#         doc.last_annual_leave_start_date = employee_leave[0]['from_date']
#         doc.last_annual_leave_end_date = employee_leave[0]['to_date']
#         doc.total_leave_days = employee_leave[0]['total_leave_days']

# def after_submit(doc):
#     frappe.db.set_value("Employee", doc.employee, 'last_working_date', doc.start_working_at, update_modified=False)
#     frappe.db.commit()
#     frappe.msgprint(f"Last Working Date Updated for Employee {doc.employee_name}")