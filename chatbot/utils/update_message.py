from ..models import Message
from datetime import datetime
import json
from database.db_instance import session_scope


def update_message(message):
    sid = message['groupId']
    dealer_id = message['dealerId']

    message_dict = message['message']

    in_message = Message()

    if message['user'] == 'customer':
        in_message.direction = 'incoming'
        in_message.message_owner = 'customer'
        in_message.from_bot = 0
    elif message['user'] == 'admin':
        in_message.direction = 'outgoing'
        in_message.message_owner = 'admin'
        in_message.from_bot = 0
    elif message['user'] == 'bot':
        in_message.direction = 'outgoing'
        in_message.message_owner = 'bot'
        in_message.from_bot = 1

    in_message.message = json.dumps(message_dict)
    in_message.session_id = sid
    in_message.dealer_id = dealer_id
    in_message.is_read = 0
    in_message.created_time = datetime.utcnow()
    with session_scope() as session:
        in_message.save_to_db(session)