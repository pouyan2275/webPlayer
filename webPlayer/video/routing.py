from django.urls import path

from . import consumers

websocket_urlpatterns = [
   path('video/watch_to_gather/', consumers.VideoConsumer.as_asgi()),
   path('video/watching/<int:id>/', consumers.ClientConsumer.as_asgi()),
]