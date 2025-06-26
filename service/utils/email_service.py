from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class EmailService:
    def __init__(
        self,
        subject: str,
        to: list,
        template_name: str = None,
        context: dict = None,
        body: str = None,
        cc: list = None,
        bcc: list = None,
        from_email: str = None,
        attachments: list = None
    ):
        self.subject = subject
        self.to = to
        self.template_name = template_name
        self.context = context or {}
        self.body = body or self._render_template()
        self.cc = cc or []
        self.bcc = bcc or []
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL
        self.attachments = attachments or []

    def _render_template(self):
        if self.template_name:
            return render_to_string(self.template_name, self.context)
        return ""

    def send(self):
        email = EmailMessage(
            subject=self.subject,
            body=self.body,
            from_email=self.from_email,
            to=self.to,
            cc=self.cc,
            bcc=self.bcc,
        )

        email.content_subtype = "html"

        for attachment in self.attachments:
            email.attach(*attachment)

        email.send(fail_silently=False)
