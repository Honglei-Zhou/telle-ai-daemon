from ..models import Lead
from datetime import datetime
from database.db_instance import session_scope


def update_lead_from_intent(data):
    message = data['message']
    email = message.get('email')
    phone = message.get('phone')

    session_id = message.get('sessionId', '')
    dealer_id = message.get('dealerId', '2019123456001')
    department = message.get('department', 'sales')
    customer = message.get('customer', 'new customer')
    notes_offer = message.get('notes', '')
    handler = message.get('handler', '')

    if session_id != '':
        with session_scope() as session:
            leads = session.query(Lead).filter_by(session_id=session_id).filter_by(status='Invalid').first()
        # leads = Lead.find_by_session(session_id, 'Invalid')
            if leads is not None:
                if email is not None:
                    leads.email = email
                if phone is not None:
                    leads.phone = phone

                leads.status = 'New'

                leads.save_to_db(session)
            else:

                leads = Lead(
                    dealer_id=dealer_id,
                    customer_name=customer,
                    created=datetime.utcnow(),
                    email=email,
                    phone=phone,
                    notes_offer=notes_offer,
                    department=department,
                    handler=handler,
                    priority=1,
                    status='New',
                    session_id=session_id
                )

                leads.save_to_db(session)