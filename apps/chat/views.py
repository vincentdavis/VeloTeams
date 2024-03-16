from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render

class ChatRoomView(TemplateView):
    template_name = 'chat_room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_name'] = self.kwargs['room_name']
        return context