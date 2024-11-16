# Copyright (c) 2024, Yousef Ashraf and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RewardAllocation(Document):
    frappe.msgprint(msg="test")
    def after_save(self):
         frappe.msgprint(msg=self.employee)
         # employee_leave = frappe.db.get_list(
         #     'Leave Application',
         #     filters={'employee': self.employee, 'status': 'Approved', 'custom_is_annual_leave': 1},
         #     fields=['from_date', 'to_date', 'total_leave_days'],
         #     order_by='from_date desc'
         # )
         # frappe.db.set_value("Reward Allocation",self.name,self.last_annual_leave_start_date,employee_leave[0]['from_date'])
         # frappe.db.set_value("Reward Allocation",self.name,self.last_annual_leave_end_date,employee_leave[0]['to_date'])
         # frappe.db.set_value("Reward Allocation",self.name,self.total_leave_days,employee_leave[0]['total_leave_days'])
         # frappe.db.commit()
         
        


    
