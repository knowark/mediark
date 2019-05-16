from flask import Flask
from flask_restful import Api
from ..config import Registry
from mediark.infrastructure.web.resources import (ImageResource,
                                                  AudiolResource,
                                                  )
from mediark.application.repositories.audio_repository import (
    MemoryAudioRepository)
from mediark.application.repositories.image_repository import (
    MemoryImageRepository)
from mediark.application.coordinators.audio_storage_coordinator import (
    AudioStorageCoordinator)
from mediark.application.coordinators.image_storage_coordinator import (
    ImageStorageCoordinator)


def set_routes(app: Flask, registry: Registry) -> None:

    @app.route('/')
    def index() -> str:
        return 'Welcome to Mediark!'

    # Restful API
    api = Api(app)

    # Services
    notification_coordinator = registry['NotificationCoordinator']
    subscription_coordinator = registry['SubscriptionCoordinator']


    # Audio resource
    api.add_resource(
        AudioResource,
        '/register', '/signup',
        resource_class_kwargs={
            'notification_coordinator': notification_coordinator
        })

    # Image resource
    api.add_resource(
        ImageResource,
        '/register', '/signup',
        resource_class_kwargs={
            'subscription_coordinator': subscription_coordinator
        })

   