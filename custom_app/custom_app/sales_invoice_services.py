import frappe
from frappe.utils import nowdate
from .service_item_details import *

def create_sales_invoice_for_lab_test(doc, method):
    
    if not doc.patient:
        frappe.throw("Patient information is required to add to the Sales Invoice.")

    service_name, item_code, rate = get_lab_test_item_details(doc)

    sales_invoices = frappe.get_all("Sales Invoice", filters={"customer": doc.patient, "docstatus": 0})
    if sales_invoices:
        sales_invoice = frappe.get_doc("Sales Invoice", sales_invoices[0].name)
    else:
        frappe.throw("No draft Sales Invoice found for this patient.")

    sales_invoice.append("items", {
        "item_code": item_code,
        "qty": 1,
        "rate": rate,
        "description": service_name
    })

    sales_invoice.save()
    frappe.msgprint(f"Service {service_name} added to Sales Invoice {sales_invoice.name} (Service ID: {doc.name})")

    submit_or_update_service_request(doc.patient, "Lab Test", doc.name)



def create_sales_invoice_for_medication(doc, method):
    if not doc.patient:
        frappe.throw("Patient information is required to add to the Sales Invoice.")

    service_name, item_code, rate = get_medication_item_details(doc)

    sales_invoices = frappe.get_all("Sales Invoice", filters={"customer": doc.patient, "docstatus": 0})
    if sales_invoices:
        sales_invoice = frappe.get_doc("Sales Invoice", sales_invoices[0].name)
    else:
        frappe.throw("No draft Sales Invoice found for this patient.")

    sales_invoice.append("items", {
        "item_code": item_code,
        "qty": 1,
        "rate": rate,
        "description": service_name
    })

    sales_invoice.save()
    frappe.msgprint(f"Service {service_name} added to Sales Invoice {sales_invoice.name} (Service ID: {doc.name})")
    submit_or_update_service_request(doc.patient, "Medication Request", doc.name)


def create_sales_invoice_for_procedure(doc, method):
    
    if not doc.patient:
        frappe.throw("Patient information is required to add to the Sales Invoice.")

    service_name, item_code, rate = get_procedure_item_details(doc)

    sales_invoices = frappe.get_all("Sales Invoice", filters={"customer": doc.patient, "docstatus": 0})
    if sales_invoices:
        sales_invoice = frappe.get_doc("Sales Invoice", sales_invoices[0].name)
    else:
        frappe.throw("No draft Sales Invoice found for this patient.")

    
    sales_invoice.append("items", {
        "item_code": item_code,
        "qty": 1,
        "rate": rate,
        "description": service_name
    })

    sales_invoice.save()
    frappe.msgprint(f"Service {service_name} added to Sales Invoice {sales_invoice.name} (Service ID: {doc.name})")
    submit_or_update_service_request(doc.patient, "Medication Request", doc.name)



def submit_or_update_service_request(patient, service_type, service_name):
    """
    This function will either submit a new service request or update an existing one
    if it has already been submitted. The service request will be marked as 'Completed'.
    """

    status_code_value = frappe.get_value("Code Value", 
        {
            "code_value": "completed",  
            "code_system": "Request Status"  
        }, 
        "name"
    )

    existing_service_request = frappe.get_all("Service Request", filters={
        "patient": patient,
        "template_dt": service_type,
        "template_dn": service_name
    })

    if existing_service_request:
        
        for request in existing_service_request:
            service_request_doc = frappe.get_doc("Service Request", request.name)
            if service_request_doc.docstatus == 1:  
                if service_request_doc.status != "Completed":
                    service_request_doc.status = status_code_value
                    service_request_doc.save(ignore_permissions=True)
                    frappe.msgprint(f"Existing service request {service_request_doc.name} has been updated to Completed.")
            else:
                frappe.throw(f"Service request {service_request_doc.name} is not submitted yet.")
    # else:
    #     # Create a new service request if it doesn't exist
    #     new_service_request = frappe.get_doc({
    #         "doctype": "Service Request",
    #         "patient": patient,
    #         "template_dt": service_type,
    #         "template_dn": service_name,
    #         "status": "Completed",
    #         "docstatus": 1  # Marking it as submitted
    #     })
    #     new_service_request.insert(ignore_permissions=True)
    #     frappe.msgprint(f"New service request {new_service_request.name} has been created and marked as Completed.")
