import frappe

def create_lab_test_or_medication_or_procedure(doc, method):
    # Check Medications
    if hasattr(doc, 'drug_prescription'):
        for medication in doc.drug_prescription:
            create_medication(doc.patient, doc.name, medication.drug_name, medication.dosage_form, medication.dosage)

    # Check Investigations
    if hasattr(doc, 'lab_test_prescription'):
        for lab_test in doc.lab_test_prescription:
            create_lab_test(doc.patient, doc.name, lab_test.lab_test_code)

    # Check Procedures
    if hasattr(doc, 'procedure_prescription'):
        for procedure in doc.procedure_prescription:
            create_clinical_procedure(doc.patient, doc.name, procedure.procedure_name, procedure.procedure_name)


def create_lab_test(patient, inpatient_record, lab_test_code):

    # Retrieve the Inpatient Record to get relevant details
    inpatient_record_doc = frappe.get_doc("Inpatient Record", inpatient_record)

    # Map gender to patient_sex
    patient_sex = "Male" if inpatient_record_doc.gender == "Male" else "Female"

    # Create a new Lab Test
    new_lab_test = frappe.get_doc({
        "doctype": "Lab Test",
        "patient": patient,
        "inpatient_record": inpatient_record,
        "template": lab_test_code,
        "patient_sex": patient_sex,
        "status": "Draft"
    })
    new_lab_test.insert(ignore_permissions=True)
    frappe.msgprint(f"Lab Test '{lab_test_code}' has been created.")

def create_medication(patient, inpatient_record, medication_name, dosage_form, dosage):
    # Retrieve the Inpatient Record to get relevant details
    inpatient_record_doc = frappe.get_doc("Inpatient Record", inpatient_record)

    print(inpatient_record_doc)
    # Extract information needed for the Medication Request
    practitioner = inpatient_record_doc.primary_practitioner

    # Create a new Medication Record
    new_medication = frappe.get_doc({
        "doctype": "Medication Request",
        "patient": patient,
        "inpatient_record": inpatient_record,
        "medication_item": medication_name,
        "practitioner": practitioner,
        "dosage_form": dosage_form,
        "dosage": dosage,
    })
    new_medication.insert(ignore_permissions=True)
    frappe.msgprint(f"Medication '{medication_name}' has been created.")

def create_clinical_procedure(patient, inpatient_record, procedure_name, template_name):
    # Create a new Clinical Procedure
    new_procedure = frappe.get_doc({
        "doctype": "Clinical Procedure",
        "patient": patient,
        "inpatient_record": inpatient_record,
        "procedure_name": procedure_name,
        "procedure_template": template_name,
        "status": "Draft"
    })
    new_procedure.insert(ignore_permissions=True)
    frappe.msgprint(f"Clinical Procedure '{procedure_name}' has been created.")