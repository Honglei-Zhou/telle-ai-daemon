from ..models import Lead
from datetime import datetime
from database.db_instance import session_scope


def create_lead_from_intent(data):
    message = data['message']
    dealer_id = message.get('dealerId', '2019123456001')
    customer_name = message.get('customer', 'customer')
    email = message.get('email', '')
    phone = message.get('phone', '')
    notes_offer = message.get('note', '')
    appointment = message.get('appointment', None)

    session_id = message.get('sessionId', '')

    department = message.get('department', '')
    handler = message.get('handleBy', 'not available')

    priority = message.get('importance', 1)

    status = message.get('status', 'Invalid')

    new_leads = Lead(
        dealer_id=dealer_id,
        customer_name=customer_name,
        created=datetime.utcnow(),
        email=email,
        phone=phone,
        notes_offer=notes_offer,
        department=department,
        handler=handler,
        priority=priority,
        status=status,
        session_id=session_id
    )

    if appointment:
        new_leads.appointment = appointment

    print(new_leads)
    with session_scope() as session:
        new_leads.save_to_db(session)