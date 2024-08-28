from ..models import WebUserModel
from datetime import datetime
from database.db_instance import session_scope
from .tools import get_ip_address


def update_user(data):
    sid = data['groupId']
    message = data['message']
    device_type = message.get('deviceType', 'Desktop')
    device_detail = message.get('deviceDetail', 'Desktop')
    session_id = message.get('sessionId', sid)

    dealer_id = message.get('dealerId', '2019123456001')
    dealer_name = message.get('dealerName', 'telle')

    ip_addr = message.get('ip_addr', '127.0.0.1')

    ip_details = get_ip_address(ip_addr)
    city = ip_details.get('city', 'NA')
    state = ip_details.get('region', 'NA')

    new_user = WebUserModel(dealer_id=dealer_id,
                            dealer_name=dealer_name,
                            device_detail=device_detail,
                            device_type=device_type,
                            created=datetime.utcnow(),
                            ip_addr=ip_addr,
                            city=city,
                            state=state,
                            session_id=session_id)
    with session_scope() as session:
        new_user.save_to_db(session)