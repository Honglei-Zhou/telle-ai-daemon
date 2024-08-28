from .create_lead_inquiry import create_lead_inquiry
from .create_appt_intent import create_appt_intent
from .create_lead_from_intent import create_lead_from_intent
from .update_lead import update_lead
from .update_user import update_user
from .update_message import update_message
from .update_group import update_group
from .update_chat import update_chat
from .update_pageview import update_pageview
from .update_lead_from_intent import update_lead_from_intent

handler = {
    'UPDATE_MSG': update_message,
    'UPDATE_GROUP': update_group,
    'UPDATE_CHAT': update_chat,
    'UPDATE_LEAD': update_lead,
    'CREATE_LEAD_INTENT': create_lead_from_intent,
    'UPDATE_LEAD_INTENT': update_lead_from_intent,
    'CREATE_LEAD_INQUIRY': create_lead_inquiry,
    'CREATE_APPT_INTENT': create_appt_intent,
    'UPDATE_USER': update_user,
    'UPDATE_USER_PV': update_pageview
}