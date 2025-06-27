# notifications/services.py

from .providers.email import send_email
from .providers.sms import send_sms
from .providers.push import send_push
from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_ENV = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))
)

def render_template(type, name, context):
    template_path = f"{type}/{name}.txt"
    template = TEMPLATE_ENV.get_template(template_path)
    return template.render(context)

def send_notification(type, recipient, subject, message):
    context = {
        "subject": subject,
        "message": message
    }

    rendered = render_template(type, "default", context)

    if type == "email":
        return send_email(recipient, subject, rendered)
    elif type == "sms":
        return send_sms(recipient, rendered)
    elif type == "push":
        return send_push(recipient, rendered)
    else:
        raise ValueError("Unsupported notification type")
