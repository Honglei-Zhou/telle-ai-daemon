from ..models import Lead
from datetime import datetime
from database.db_instance import session_scope


def create_appt_intent(data):
    keys = {
        "VehicleType": "VehicleType",
        "VehicleDrivetrain": "VehicleDrivetrain",
        "VehicleBudget": "VehicleBudget",
        "VehicleColor": "VehicleColor",
        "VehicleMake": "VehicleMake",
        "VehicleModel": "VehicleModel",
        "VehicleFeatures": "VehicleFeatures",  # list
        "VehicleYear": "VehicleYear",
        "test_drive_date": "test_drive_date",
        "test_drive_time": "test_drive_time",
    }

    message = data['message']
    dealer_id = message.get('dealerId', '2019123456001')
    customer_name = message.get('person', 'customer')
    email = message.get('email', '')
    phone = message.get('phone-number', '')
    notes_offer = message.get('note', '')

    session_id = message.get('sessionId', '')

    handler = message.get('handleBy', 'not available')

    department = message.get('department', 'sales')
    priority = message.get('importance', 1)

    status = message.get('status', 'New')

    for key in keys:
        val = message.get(key)
        if val:
            if key == 'VehicleFeatures':
                val = ','.join(val)
            notes_offer = '{} {}'.format(notes_offer, '{}:{}'.format(key, val))

    leads = Lead(
        dealer_id=dealer_id,
        customer_name=customer_name,
        created=datetime.utcnow(),
        email=email,
        phone=phone,
        session_id=session_id,
        notes_offer=notes_offer,
        department=department,
        handler=handler,
        priority=priority,
        status=status
    )

    print(leads)
    with session_scope() as session:
        leads.save_to_db(session)