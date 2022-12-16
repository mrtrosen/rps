from django.urls import path

from rps.gameplay.views import index, new_game, play

app_name = "gameplay"
urlpatterns = [
    path("", view=index, name="index"),
    path("<uuid:game_uuid>/play/", view=play, name="play"),
    path("new/<int:game_type>/", view=new_game, name="new_game"),
]
