from mediark.application.domain.models import Email


def test_email_instantiation():
    email = Email()

    assert email.id != ''
    assert email.name == ''
    assert email.recipient == ''
    assert email.subject == ''
    assert email.type == ''
    assert email.template == ''
    assert email.context == {}


def test_email_attributes():
    email = Email(id='E001',
                  name='registered',
                  template='mail/auth/registered.html',
                  recipient='info@example.com',
                  subject='New Register',
                  type='registered',
                  context={
                    "user_name": "Info",
                    "shop_url": "https://www.tempos.site",
                    "unsubscribe_link": "https://www.tempos.site"
                  })

    assert email.id == 'E001'
    assert email.name == 'registered'
    assert email.recipient == 'info@example.com'
    assert email.subject == 'New Register'
    assert email.type == 'registered'
    assert email.template == 'mail/auth/registered.html'
    assert email.context == {
                "user_name": "Info",
                "shop_url": "https://www.tempos.site",
                "unsubscribe_link": "https://www.tempos.site"
                }
