import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

class EmailService:
    """Envía correos usando tu propio servidor SMTP Postal (autogestionado)."""

    @staticmethod
    async def send_payment_confirmation(to_email: str, order_id: str, artwork_title: str, amount: str, currency: str):
        subject = f"Pago confirmado - {artwork_title}"
        html_body = f"""
        <h2>Pago confirmado!</h2>
        <p>Tu pago de <strong>{amount} {currency}</strong> por la obra <strong>{artwork_title}</strong> ha sido confirmado.</p>
        <p>La ONG Pont Culturel verificara la transaccion y liberara los fondos al artista.</p>
        <p>Orden: {order_id}</p>
        <hr>
        <p>Gracias por apoyar el arte cubano</p>
        """
        await EmailService._send_email(to_email, subject, html_body)

    @staticmethod
    async def _send_email(to_email: str, subject: str, html_body: str):
        msg = MIMEMultipart("alternative")
        msg["From"] = "Pont Culturel <notificaciones@pontculturel.art>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_body, "html"))

        try:
            await asyncio.to_thread(EmailService._smtp_send, msg)
            print(f"Correo enviado a {to_email}")
        except Exception as e:
            print(f"Error al enviar correo a {to_email}: {e}")

    @staticmethod
    def _smtp_send(msg: MIMEMultipart):
        smtp_host = settings.POSTAL_SMTP_HOST or "localhost"
        smtp_port = settings.POSTAL_SMTP_PORT or 2525
        smtp_user = settings.POSTAL_SMTP_USER or ""
        smtp_pass = settings.POSTAL_SMTP_PASS or ""

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            if smtp_user and smtp_pass:
                server.login(smtp_user, smtp_pass)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
