import frappe
from frappe.utils import nowdate


def create_sales_invoice_on_patient_creation(doc, method):
    customer_name = create_customer_for_patient(doc)
    
    si = frappe.new_doc("Sales Invoice")
    si.customer = customer_name
    si.due_date = frappe.utils.nowdate()
    
    si.append("items", {
        "item_code": "inpatient service",
        "qty": 1,
        "rate": 0.00 
    })
    
    si.insert()
    # si.submit()

def create_customer_for_patient(patient):
    customer_name = patient.patient_name
    existing_customer = frappe.db.get_value("Customer", {"customer_name": customer_name})
    if existing_customer:
        return existing_customer
    else:
        customer = frappe.new_doc("Customer")
        customer.customer_name = customer_name
        customer.customer_group = "Individual" 
        customer.territory = "All Territories" 
        customer.customer_type = "Individual"
        customer.save()
        return customer.name



# def create_empty_sales_invoice_for_patient(doc, method):
#     frappe.logger().info(f"Creating Sales Invoice for Patient: {doc.name}")

#     # Ensure the Patient has a linked Customer
#     if not doc.customer:
#         # Create a new Customer for the Patient
#         customer_name = f"{doc.first_name} {doc.middle_name or ''} {doc.last_name} ({doc.identification_number or doc.date_of_birth or doc.name})".strip()
#         if frappe.db.exists("Customer", {"customer_name": customer_name}):
#             frappe.logger().info(f"Customer with name {customer_name} already exists. Linking to Patient {doc.name}")
#             customer = frappe.get_doc("Customer", {"customer_name": customer_name})
#         else:
#             customer = frappe.get_doc({
#                 "doctype": "Customer",
#                 "customer_name": customer_name,
#                 "customer_group": "All Customer Groups",  # Replace with the appropriate customer group
#                 "customer_type": "Individual",
#                 "territory": "All Territories",  # Replace with the appropriate territory
#             })
#             customer.insert(ignore_permissions=True)
#             frappe.logger().info(f"Created Customer {customer.name} for Patient {doc.name}")

#         # Link the Customer to the Patient
#         doc.customer = customer.name
#         doc.db_update()
#     else:
#         customer = frappe.get_doc("Customer", doc.customer)

#     # Get the default receivable account for the company
#     company_name = frappe.defaults.get_user_default("Company")
#     if not company_name:
#         frappe.throw("Company is not set as a default")

#     debit_to = frappe.get_value("Company", company_name, "default_receivable_account")
#     if not debit_to:
#         frappe.throw(f"No default Receivable Account found for the company {company_name}")

#     # Get the default income account for the company
#     income_account = frappe.get_value("Company", company_name, "default_income_account")
#     if not income_account:
#         frappe.throw(f"No default Income Account found for the company {company_name}")

#     # Create a new Sales Invoice with an item having default values
#     try:
#         sales_invoice = frappe.get_doc({
#             "doctype": "Sales Invoice",
#             "patient": doc.name,
#             "customer": customer.name,
#             "due_date": nowdate(),
#             "company": company_name,
#             "debit_to": debit_to,
#             "items": [{
#                     "item_code": "inpatient service",  # Replace with a valid Item Code
#                     "item_name": "Inpatient Service",
#                     "qty": 1,
#                     "rate": 0.0,
#                     "amount": 0.0,
#                     "uom": "Nos",
#                     "conversion_factor": 1.0,
#                     "income_account": income_account,
#                     "expense_account": frappe.get_value("Company", company_name, "default_expense_account"),
#                 }
#             ]
#         })

#         # Insert and submit the Sales Invoice
#         sales_invoice.insert(ignore_permissions=True)
#         sales_invoice.submit()
#         frappe.logger().info(f"Sales Invoice {sales_invoice.name} created successfully for Patient: {doc.name}")

#     except Exception as e:
#         frappe.logger().error(f"Failed to create Sales Invoice: {str(e)}")
#         frappe.throw(f"Failed to create Sales Invoice: {str(e)}")