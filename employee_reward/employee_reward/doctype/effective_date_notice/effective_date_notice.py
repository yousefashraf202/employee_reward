# Copyright (c) 2024, Yousef Ashraf and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EffectiveDateNotice(Document):
    def validate(self):
        employee_leave = frappe.db.get_all(
            'Leave Application',
            filters={'employee': self.employee, 'status': 'Approved',"docstatus": 1, 'custom_is_annual_leave': 1},
            fields=['from_date', 'to_date', 'total_leave_days'],
            order_by='from_date desc'
        )
        if len(employee_leave):
            self.last_annual_leave_start_date = employee_leave[0]['from_date']
            self.last_annual_leave_end_date = employee_leave[0]['to_date']
            self.total_leave_days = employee_leave[0]['total_leave_days']

    def on_submit(self):
        frappe.db.set_value("Employee", self.employee, "last_working_date", self.start_working_at, update_modified=False)
        frappe.db.commit()
        frappe.msgprint(msg="Last Working Date Updated")

    def on_cancel(self):
        frappe.db.set_value("Employee", self.employee, "last_working_date", self.current_last_working_date, update_modified=False)
        frappe.db.commit()
        frappe.msgprint(msg="Last Working Date Cancelled")