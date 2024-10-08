import frappe
from frappe.utils import nowdate

def create_empty_sales_invoice(doc, method):
    frappe.logger().info(f"Creating Sales Invoice for Inpatient Record: {doc.name}")

    # Check if a patient exists
    if not doc.patient:
        frappe.throw("Patient is required to create a Sales Invoice")

    # Get the default receivable account for the company
    company_name = "test (Demo)"
    debit_to = frappe.get_value("Company", {"company_name": company_name}, "default_receivable_account")
    if not debit_to:
        frappe.throw(f"No default Receivable Account found for the company {company_name}")

    # Get the default income account for the company
    income_account = frappe.get_value("Company", {"company_name": company_name}, "default_income_account")
    if not income_account:
        frappe.throw(f"No default Income Account found for the company {company_name}")

    # Create a new Sales Invoice with an item having default values
    try:
        sales_invoice = frappe.get_doc({
            "doctype": "Sales Invoice",
            "patient": doc.patient,
            "customer": doc.patient_name,
            "due_date": nowdate(),
            "inpatient_record": doc.name,
            "company": company_name,
            "debit_to": debit_to,
            "grand_total": 0.0,
            "outstanding_amount": 0.0,
            "total": 0.0,
            "net_total": 0.0,
            "total_taxes_and_charges": 0.0,
            "paid_amount": 0.0,
            "base_grand_total": 0.0,
            "base_total": 0.0,
            "base_net_total": 0.0,
            "base_total_taxes_and_charges": 0.0,
            "posting_date": nowdate(),
            "items": [
                {
                    "item_code": "SKU001",  # Replace with a valid Item Code if necessary
                    "item_name": "T-shirt",
                    "qty": 1,
                    "rate": 800.0,
                    "amount": 800.0,
                    "uom": "Nos",
                    "conversion_factor": 1.0,
                    "income_account": income_account,  # Set the income account to ensure it's not None
                    "expense_account": frappe.get_value("Company", {"company_name": company_name}, "default_expense_account"),
                }
            ]
        })

        # Insert and submit the sales invoice
        sales_invoice.insert(ignore_permissions=True)
        sales_invoice.submit()
        frappe.logger().info(f"Sales Invoice created successfully for Inpatient Record: {doc.name}")

    except Exception as e:
        frappe.logger().error(f"Failed to create Sales Invoice: {str(e)}")
        frappe.throw(f"Failed to create Sales Invoice: {str(e)}")
