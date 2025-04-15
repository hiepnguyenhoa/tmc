from PyPDF2 import PdfReader
from .models import Registration, RetreatDuration

def extract_and_create_registration(pdf_path, retreat_duration_id):
    """
    Extracts information from a fillable PDF file and creates a registration.

    Args:
        pdf_path (str): The path to the PDF file.
        retreat_duration_id (int): The ID of the retreat duration to associate with the registration.

    Returns:
        Registration: The created registration object.
    """
    # Open the PDF file with PyPDF2
    reader = PdfReader(pdf_path)
    form_data = {}
    if "/AcroForm" in reader.trailer["/Root"]:
        fields = reader.trailer["/Root"]["/AcroForm"]["/Fields"]
        for field in fields:
            field_obj = field.get_object()
            field_name = field_obj.get("/T")  # Field name
            field_value = field_obj.get("/V")  # Field value
            if field_name and field_value:
                form_data[field_name] = field_value

    # Debug: Print extracted form data
    print("DEBUG: Extracted form data from PDF:")
    print(form_data)

    # Map extracted data to registration fields
    first_name = form_data.get("First", "").strip()
    last_name = form_data.get("Last", "").strip()
    sex = form_data.get("Sex", "").strip()
    address = f'{form_data.get("Number and Stree", "").strip()}, {form_data.get("City", "").strip()}, {form_data.get("State", "").strip()} {form_data.get("Zip Code", "").strip()}'
    phone = form_data.get("Text6", "").strip()
    email = form_data.get("Over 80", "").strip()
    age = form_data.get("Age", "").strip()
    emergency_contact_name = form_data.get("Text7", "").strip()
    emergency_contact_phone = form_data.get("Text8", "").strip()
    emergency_contact_relation = form_data.get("Relation", "").strip()

    # Get the retreat duration
    retreat_duration = RetreatDuration.objects.get(id=retreat_duration_id)

    # Create the registration
    registration = Registration.objects.create(
        retreat_duration=retreat_duration,
        first_name=first_name,
        last_name=last_name,
        sex=sex,
        address=address,
        phone=phone,
        email=email,
        age=age,
        emergency_contact_name=emergency_contact_name,
        emergency_contact_phone=emergency_contact_phone,
        emergency_contact_relation=emergency_contact_relation,
        pdf_path=pdf_path,  # Save the PDF path
    )

    print(f"DEBUG: Created registration for {first_name} {last_name}")
    return registration