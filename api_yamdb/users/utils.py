from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

User = get_user_model()


def gen_token_and_send_code(user: User):
    """Отправляет код подтверждения на почту пользователя."""
    confirmation_code = default_token_generator.make_token(user)
    subject = 'Код подтверждения'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = 'admin@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
    return confirmation_code
