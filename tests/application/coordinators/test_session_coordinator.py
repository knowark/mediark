def test_session_coordinator_creation(session_coordinator) -> None:
    assert hasattr(session_coordinator, 'set_tenant')
    assert hasattr(session_coordinator, 'get_tenant')
    assert hasattr(session_coordinator, 'set_user')


def test_session_coordinator_set_tenant(session_coordinator) -> None:

    tenant = {'id': '001', 'name': 'Default'}
    session_coordinator.set_tenant(tenant)
    assert session_coordinator


def test_session_coordinator_get_tenant(session_coordinator) -> None:

    session_coordinator.set_tenant({'id': '001', 'name': 'Default'})
    tenant = session_coordinator.get_tenant()
    assert isinstance(tenant, dict)
    assert tenant['name'] == 'Default'


def test_session_coordinator_set_user(session_coordinator) -> None:

    user = {'name': 'jdacevedo'}
    session_coordinator.set_user(user)
    assert session_coordinator.auth_provider.user.name == 'jdacevedo'
