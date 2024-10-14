import frappe

def get_lab_test_item_details(doc):
    lab_test_template = frappe.get_doc("Lab Test Template", doc.template)
    return doc.lab_test_name, doc.lab_test_name, lab_test_template.lab_test_rate

def get_medication_item_details(doc):
    item = frappe.get_doc("Item", doc.medication_item)
    return doc.medication, doc.medication_item, item.valuation_rate

def get_procedure_item_details(doc):
    return doc.procedure_name, doc.item_code, doc.rate