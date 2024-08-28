from ..models import Lead
from datetime import datetime
from database.db_instance import session_scope


def create_lead_inquiry(data):
    message = data['message']
    dealer_id = message.get('dealerId', '2019123456001')
    customer_name = message.get('customer', 'customer')
    email = message.get('email', '')
    phone = message.get('phone', '')
    notes_offer = message.get('note', '')

    session_id = message.get('sessionId', '')

    handler = message.get('handleBy', 'not available')

    department = message.get('department', 'sales')
    priority = message.get('importance', 1)

    status = message.get('status', 'New')

    zipcode = message.get('zipcode', '')
    vin = message.get('vin', '')
    stock = message.get('stock', '')

    notes_offer = '{} zipcode: {} vin: {} stock: {}'.format(notes_offer, zipcode, vin, stock)

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