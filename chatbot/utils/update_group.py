from ..models import Group
from datetime import datetime
from database.db_instance import session_scope


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