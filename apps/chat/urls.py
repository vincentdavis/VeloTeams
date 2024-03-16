from django.urls import path
from .views import ChatRoomView
app_name = "teams"
urlpatterns = [
    path('chat/<str:room_name>/', ChatRoomView.as_view(), name='chat_room'),
]