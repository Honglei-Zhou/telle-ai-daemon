import sqlalchemy_jsonfield
import ujson
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text
from database.db_instance import Base, TelleModelMixin, session_scope


class Message(Base, TelleModelMixin):

    __tablename__ = 'telle_message'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String(80), nullable=True)

    dealer_id = Column(String(100))
    dealer_name = Column(Text)

    session_id = Column(String(120), nullable=False)
    direction = Column(String(20), nullable=False)
    message = Column(
        sqlalchemy_jsonfield.JSONField(
            # MariaDB does not support JSON for now
            enforce_string=True,
            # MariaDB connector requires additional parameters for correct UTF-8
            enforce_unicode=False,
            json=ujson
        ),
        nullable=True
    )

    dialogflow_resp = Column(
        sqlalchemy_jsonfield.JSONField(
            # MariaDB does not support JSON for now
            enforce_string=True,
            # MariaDB connector requires additional parameters for correct UTF-8
            enforce_unicode=False,
            json=ujson
        ),
        nullable=True
    )
    is_read = Column(Integer)
    from_bot = Column(Integer)
    message_owner = Column(String(80), nullable=True)

    created_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs)

    # def save_to_db(self):
    #     session.add(self)
    #     session.commit()

    def __repr__(self):
        return '<Message %r>' % self.id


class Chat(Base, TelleModelMixin):

    __tablename__ = 'telle_chat'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String(80), nullable=True)

    device_type = Column(String(80))
    device_detail = Column(String(80))

    session_id = Column(String(120), nullable=False)

    started = Column(DateTime, default=datetime.datetime.utcnow)

    duration = Column(Text)

    lead = Column(Integer)

    handler = Column(String(50))

    dealer_id = Column(String(100))
    dealer_name = Column(Text)

    department = Column(String(50))

    alive = Column(Integer, default=0)

    missed = Column(String(10))

    def __init__(self, **kwargs):
        super(Chat, self).__init__(**kwargs)

    # def save_to_db(self):
    #     session.add(self)
    #     session.commit()


class Lead(Base, TelleModelMixin):
    __tablename__ = 'telle_lead'

    id = Column(Integer, primary_key=True)

    dealer_id = Column(String(100))
    customer_name = Column(String(80), nullable=True)

    created = Column(DateTime, default=datetime.datetime.utcnow)

    session_id = Column(String(120))

    email = Column(String(50))
    phone = Column(String(50))

    notes_offer = Column(Text)

    appointment = Column(DateTime)

    department = Column(String(50))

    handler = Column(String(50))

    priority = Column(Integer)

    status = Column(String(20))

    def __init__(self, **kwargs):
        super(Lead, self).__init__(**kwargs)

    # def save_to_db(self):
    #     session.add(self)
    #     session.commit()

    @classmethod
    def find_by_session(cls, session_id, status):
        return cls.query.filter_by(session_id=session_id).filter_by(status=status).first()

    def __repr__(self):
        return '<Lead %r>' % self.id


class Group(Base, TelleModelMixin):
    __tablename__ = 'telle_group'

    id = Column(Integer, primary_key=True)

    session_id = Column(String(120), nullable=False)

    alive = Column(Integer, default=0)

    created = Column(DateTime, default=datetime.datetime.utcnow)

    dealer_id = Column(String(100))
    dealer_name = Column(Text)

    department = Column(String(50))

    # def save_to_db(self):
    #     session.add(self)
    #     session.commit()
    def __init__(self, **kwargs):
        super(Group, self).__init__(**kwargs)

    def __repr__(self):
        return '<Group %r>' % self.session_id


class WebUserModel(Base, TelleModelMixin):

    __tablename__ = 'telle_webuser'

    id = Column(Integer, primary_key=True)

    session_id = Column(String(120), nullable=False)

    ip_addr = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))

    device_type = Column(String(80))
    device_detail = Column(String(80))

    created = Column(DateTime, default=datetime.datetime.utcnow)

    dealer_id = Column(String(100))
    dealer_name = Column(Text)

    def __init__(self, **kwargs):
        super(WebUserModel, self).__init__(**kwargs)


class WebUserPageView(Base, TelleModelMixin):

    __tablename__ = 'telle_pageview'

    id = Column(Integer, primary_key=True)

    session_id = Column(String(120), nullable=False)
    ip_addr = Column(String(100))

    created = Column(DateTime, default=datetime.datetime.utcnow)

    dealer_id = Column(String(100))
    dealer_name = Column(Text)

    bot_clicked = Column(Integer, default=0)

    page = Column(Text)

    def __init__(self, **kwargs):
        super(WebUserPageView, self).__init__(**kwargs)


class IPModel(Base, TelleModelMixin):

    __tablename__ = 'telle_visitors_ip'

    id = Column(Integer, primary_key=True)
    ip_addr = Column(String(40))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    bot_id = Column(String(255))

    def __init__(self, **kwargs):
        super(IPModel, self).__init__(**kwargs)