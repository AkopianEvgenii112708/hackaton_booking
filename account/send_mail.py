from django.core.mail import send_mail

def send_confirmation_email(user, code):
    full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}/'
    send_mail(
        'Здравствуйте! Активируйте ваш аккаунт',
        f'Чтобы активировать ваш аккаунт нужно перейти по ссылке: \n{full_link}',
        'eakopian2002ml@gmail.com',
        [user],
        fail_silently=False
    )