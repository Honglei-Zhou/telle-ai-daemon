from ..models import WebUserPageView
from datetime import datetime
from database.db_instance import session_scope


def update_pageview(data):
    message = data['message']
    session_id = message.get('sessionId', '')

    dealer_id = message.get('dealerId', '2019123456001')

    ip_addr = message.get('ip_addr', '127.0.0.1')

    page = message.get('page', ''),
    bot_clicked = message.get('bot_clicked')

    new_pageview = WebUserPageView(
        dealer_id=dealer_id,
        created=datetime.utcnow(),
        ip_addr=ip_addr,
        page=page,
        bot_clicked=bot_clicked,
        session_id=session_id)
    with session_scope() as session:
        new_pageview.save_to_db(session)
