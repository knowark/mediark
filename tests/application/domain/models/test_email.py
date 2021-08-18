from mediark.application.domain.models import Email


def test_email_instantiation():
    email = Email()

    assert email.id != ''
    assert email.name == ''
    assert email.template == ''
    assert email.context == {}


def test_email_attributes():
    email = Email(id='E001',
                  name='activation',
                  template='/opt/mediark/templates/mail/auth/activation.html',
                  context={
                        'type': 'activation',
                        'subject': 'New Account Activation',
                        'recipient': 'valenep@example.com',
                        'owner': 'Valentina',
                        'token': '<verification_token>'
                  })

    assert email.id == 'E001'
    assert email.name == 'activation'
    assert email.template == '/opt/mediark/templates/mail/auth/activation.html'
    assert email.context == {
                'type': 'activation',
                'subject': 'New Account Activation',
                'recipient': 'valenep@example.com',
                'owner': 'Valentina',
                'token': '<verification_token>'
                }
