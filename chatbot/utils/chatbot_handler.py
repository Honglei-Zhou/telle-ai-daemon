import os
from ..models import Group, Message, Chat, Lead, WebUserModel, WebUserPageView
from datetime import datetime, timezone
import json
import pytz
import ipinfo
from database.config import ipinfo_access_token
from sqlalchemy import desc
from database.db_instance import session_scope

local_tz = pytz.timezone('America/Chicago')

dirpath = os.path.dirname(os.path.realpath(__file__))


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(local_tz)


def update_group(message):
    dealer_id = message['dealerId']
    sid = message['groupId']
    alive = 1 if message['online'] is True else 0

    with session_scope() as session:
        group = session.query(Group).filter(Group.session_id == sid).first()

        if group is None:

            new_group = Group()
            new_group.session_id = sid

            new_group.alive = alive

            new_group.dealer_id = dealer_id

            new_group.created = datetime.utcnow()

            new_group.save_to_db(session)

        else:
            group.alive = alive
            group.save_to_db(session)


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


def update_chat(message):
    sid = message['groupId']
    close = message['online']
    dealer_id = message['dealerId']

    department = message.get('department', 'sales')
    handler = message.get('handler', 'Telle Bot')
    device_type = message.get('deviceType', 'Desktop')
    customer_name = message.get('customer', 'Customer')
    missed = message.get('missed', 'answered')

    with session_scope() as session:
        chat = session.query(Chat).filter(Chat.session_id == sid and Chat.alive == 1).order_by(desc(Chat.id)).first()

        if chat is None and not close:

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

        elif chat is not None and close:
            print(chat)
            chat.alive = 0
            duration = datetime.utcnow() - chat.started
            chat.duration = str(duration)
            chat.save_to_db(session)


def update_lead(data):
    message = data['message']
    dealer_id = message.get('dealerId', '2019123456001')
    customer_name = message.get('customer', 'customer')
    email = message.get('email', '')
    phone = message.get('phone', '')
    notes_offer = message.get('note', 'Submitted from SMS text.')
    appointment = message.get('appointment', None)

    session_id = message.get('sessionId', '')

    department = message.get('department', '')
    handler = message.get('handleBy', 'not available')

    priority = message.get('importance', 1)

    status = message.get('status', 'New')

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

    if appointment:
        leads.appointment = appointment

    print(leads)
    with session_scope() as session:
        leads.save_to_db(session)

    # Send notifications


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
    # Send notification


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


def get_ip_address(ip):
    try:
        handler = ipinfo.getHandler(ipinfo_access_token)
        details = handler.getDetails(ip)
        return details.all
    except Exception as e:
        print(e)
        return {}


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
