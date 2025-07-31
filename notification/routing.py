from django.urls import re_path, path

from notification import consumer

websocket_urlpatterns = [
    # re_path(r'ws/notifications/(?P<room_name>\w+)/$', consumer.NotificationConsumer.as_asgi()),
    re_path('ws/notifications/admin/' , consumer.NotificationRVM.as_asgi()),
    re_path('ws/notifications/user/' , consumer.NotificationUser.as_asgi()),
]  