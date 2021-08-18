from .auth_provider import AuthProvider, StandardAuthProvider
from .user import User

ZeroID = '00000000-0000-0000-0000-000000000000'


anonymous_user = User(id=ZeroID, name='anonymous')


OneID = '11111111-1111-1111-1111-111111111111'


system_user = User(id=OneID, name='system')
