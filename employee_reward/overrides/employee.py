import frappe
from erpnext.setup.doctype.employee.employee import Employee
from datetime import datetime, timedelta
from frappe.utils import getdate, add_to_date, today


class CustomEmployee(Employee):
   def validate(self):
      if self.designation == "Accountant":
         frappe.msgprint(msg="You Are Accountant")
      else:
         frappe.msgprint(msg="You Are not an Accountant")
      
      # Call external function and pass self
      import_salary_details(self)
      calculate_reward(self)
      calculate_flying_ticket(self)
      calculate_last_working_period(self)
      calculate_leave_allocation(self)
      
      # Ensure original validate logic is called
      super().validate()


def run_employee_validations():
    employees = frappe.get_all("Employee", filters={"status": "Active"})
    for employee in employees:
        employee_doc = frappe.get_doc("Employee", employee.name)
        
        # Call the external functions to update fields
        import_salary_details(employee_doc)
        calculate_reward(employee_doc)
        calculate_flying_ticket(employee_doc)
        calculate_last_working_period(employee_doc)
        calculate_leave_allocation(employee_doc)
        
        # Save the document to persist changes
        employee_doc.save()

    # Commit the transaction to ensure all changes are saved
    frappe.db.commit()



# Define an external function
def import_salary_details(doc):
   employee_salary = frappe.db.get_all(
      "Salary Structure Assignment",
      filters={'employee': doc.employee, 'docstatus':1},
      fields=["name","base","custom_housing_allowance","custom_transportation_allowance","custom_other_allowances","from_date"],
      order_by='from_date desc'
      )
   
   if len(employee_salary):
      doc.custom_base = employee_salary[0]["base"]
      doc.custom_housing_allowance = employee_salary[0]["custom_housing_allowance"]
      doc.custom_transportation_allowance = employee_salary[0]["custom_transportation_allowance"]
      doc.custom_other_allowances = employee_salary[0]["custom_other_allowances"]        
      doc.custom_total_salary = doc.custom_base + doc.custom_housing_allowance + doc.custom_transportation_allowance + doc.custom_other_allowances



def calculate_reward(doc):
   date_of_joining = getdate(doc.date_of_joining)  # Assuming date_of_joining is a string
   current_date = getdate(today())

   
   years_of_service = current_date.year - date_of_joining.year
   if (current_date.month, current_date.day) < (date_of_joining.month, date_of_joining.day):
      years_of_service -= 1
   
   months_of_service = current_date.month - date_of_joining.month
   if current_date.day < date_of_joining.day:
      months_of_service -= 1

   if months_of_service < 0:
      months_of_service += 12

   if current_date.day >= date_of_joining.day:
      days_of_service = current_date.day - date_of_joining.day
   else:
      previous_month = (current_date.replace(day=1) - timedelta(days=1)).day
      days_of_service = previous_month - date_of_joining.day + current_date.day
   
   doc.custom_years = years_of_service
   doc.custom_months = months_of_service
   doc.custom_days = days_of_service


   # Reward Calculation Logic
   if years_of_service >= 5 and months_of_service:
      reward = round((((doc.custom_total_salary / 2) * 5) + ((years_of_service - 5) * doc.custom_total_salary) + (months_of_service * (doc.custom_total_salary / 12)) + (days_of_service * (doc.custom_total_salary / 360))), 2)
   elif years_of_service < 5:
      reward = round(((years_of_service * (doc.custom_total_salary / 2)) + (months_of_service * (doc.custom_total_salary / 2 / 12)) + (days_of_service * (doc.custom_total_salary / 2 / 360))), 2)
   
   # Adjust reward based on reason for ending the contract
   if doc.custom_reason_for_termination == "فسخ خلال التجربة" or doc.custom_reason_for_termination == "فسخ العقد بموجب المادة (80)":
      reward = 0  # No reward for these reasons
   elif doc.custom_reason_for_termination == "الاستقالة":
      if years_of_service < 2:
         reward = 0  # No reward for less than 2 years of service
      elif 2 <= years_of_service <= 5:
         reward *= 1 / 3  # 1/3 of the reward for 2 to 5 years
      elif 5 < years_of_service <= 10:
         reward *= 2 / 3  # 2/3 of the reward for 5 to 10 years
      else:
         reward = reward  # Full reward for more than 10 years
   else:
      # All other reasons will get full reward
      reward = reward

   doc.custom_final_reward_amount = reward



def calculate_difference(start_date, end_date):
    # Calculate years
    years = end_date.year - start_date.year
    if (end_date.month, end_date.day) < (start_date.month, start_date.day):
        years -= 1  # Adjust years if the end date is before the anniversary date

    # Calculate months
    months = end_date.month - start_date.month
    if end_date.day < start_date.day:
        months -= 1  # Adjust months if the end day is before the start day
    if months < 0:
        months += 12  # Ensure months is not negative

    # Calculate days
    if end_date.day >= start_date.day:
        days = end_date.day - start_date.day
    else:
        # Get the number of days in the previous month
        previous_month = (end_date.replace(day=1) - timedelta(days=1)).day
        days = previous_month - start_date.day + end_date.day

    return years, months, days


# last_date_of work is today is current_date
#last_working_date is اخر مباشرة


def calculate_last_working_period(doc):
   last_working_date = getdate(doc.last_working_date)  # Assuming last_working_date is a string
   current_date = getdate(today())

   
   years_of_last_service = current_date.year - last_working_date.year
   if (current_date.month, current_date.day) < (last_working_date.month, last_working_date.day):
      years_of_last_service -= 1
   
   months_of_last_service = current_date.month - last_working_date.month
   if current_date.day < last_working_date.day:
      months_of_last_service -= 1

   if months_of_last_service < 0:
      months_of_last_service += 12

   if current_date.day >= last_working_date.day:
      days_of_last_service = current_date.day - last_working_date.day
   else:
      previous_month = (current_date.replace(day=1) - timedelta(days=1)).day
      days_of_last_service = previous_month - last_working_date.day + current_date.day
   
   doc.custom_years_1 = years_of_last_service
   doc.custom_months_1 = months_of_last_service
   doc.custom_days_1 = days_of_last_service







# Leave allocation calculation
def calculate_leave_allocation(doc):

   last_working_date = getdate(doc.last_working_date)  # Assuming last_working_date is a string
   current_date = getdate(today())
   five_year_mark = getdate(add_to_date(doc.date_of_joining,years=5))

   # Last period calculation
   if last_working_date < five_year_mark and current_date > five_year_mark:
      years_before, months_before, days_before = calculate_difference(last_working_date, five_year_mark)
      years_after, months_after, days_after = calculate_difference(five_year_mark, current_date)
   elif last_working_date < five_year_mark and current_date < five_year_mark:
      years_before, months_before, days_before = calculate_difference(last_working_date, current_date)
      years_after = 0
      months_after = 0
      days_after = 0
   elif last_working_date > five_year_mark and current_date > five_year_mark:
      years_before = 0
      months_before = 0
      days_before = 0
      years_after, months_after, days_after = calculate_difference(last_working_date, current_date)
            
    
   # Total days before and after
   total_days_before = years_before * 360 + months_before * 30 + days_before
   total_days_after = years_after * 360 + months_after * 30 + days_after

   # Leave allocation
   leave_before_mark = total_days_before * (1.75 / 30)  # 21 days per year
   leave_after_mark = total_days_after * (2.5 / 30)  # 30 days per year

   leave_applications = frappe.db.get_all(
	   'Leave Application',
        filters={'employee': doc.employee, 'status': 'Approved',"docstatus": 1, 'custom_is_annual_leave': 1,'from_date': ['>=', last_working_date]},
        fields=['from_date', 'to_date' , 'total_leave_days'],
        order_by='from_date desc'

   )
   total_leave_used = sum(leave.get('total_leave_days', 0) for leave in leave_applications)

   total_leave_amount = ((leave_before_mark + leave_after_mark) - total_leave_used) * (doc.custom_total_salary / 30)
    
   doc.custom_annual_leave_balance = leave_before_mark + leave_after_mark
   doc.custom_annual_leave_used = total_leave_used
   doc.custom_accrued_leave_balance = doc.custom_annual_leave_balance - doc.custom_annual_leave_used
   doc.custom_annual_leave_entitlment = total_leave_amount
   





def calculate_flying_ticket(doc):
   if doc.custom_years_1 > 0:
      ticket_allocation = doc.custom_ticket_value
   elif doc.custom_years_1 <= 0:
      ticket_allocation = ((doc.custom_ticket_value / 12) * doc.custom_months_1) + ( ((doc.custom_ticket_value / 12) / 30) * doc.custom_days_1 )
      
   doc.custom_ticket_amount_entitlment = ticket_allocation

