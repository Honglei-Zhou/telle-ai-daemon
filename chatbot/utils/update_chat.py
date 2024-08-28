from ..models import Chat
from datetime import datetime
from sqlalchemy import desc
from database.db_instance import session_scope


def update_chat(message):
    sid = message['groupId']
    online = message['online']
    dealer_id = message['dealerId']

    department = message.get('department', 'sales')
    handler = message.get('handler', 'Telle Bot')
    device_type = message.get('deviceType', 'Desktop')
    customer_name = message.get('customer', 'Customer')
    missed = message.get('missed', 'answered')

    with session_scope() as session:
        chat = session.query(Chat).filter(Chat.session_id == sid and Chat.alive == 1).order_by(desc(Chat.id)).first()

        if chat is None and online:

            new_chat = Chat()
            new_chat.session_id = sid

            new_chat.alive = 1

            new_chat.started = datetime.utcnow()

            new_chat.dealer_id = dealer_id
            new_chat.department = department
            new_chat.handler = handler
            new_chat.device_type = device_type
            new_chat.customer_name = customer_name
            new_chat.missed = missed

            duration = datetime.utcnow() - new_chat.started
            new_chat.duration = str(duration)

            new_chat.save_to_db(session)
        elif chat is not None:
            chat.started = datetime.utcnow()
            chat.save_to_db(session)

        elif chat is not None and not online:
            chat.alive = 0
            duration = datetime.utcnow() - chat.started
            chat.duration = str(duration)
            chat.save_to_db(session)
