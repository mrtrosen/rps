import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from rps.gameplay.forms import UserTurnForm
from rps.gameplay.models import Game

User = get_user_model()
logger = logging.getLogger(__name__)


def index(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    """The main gameplay page
    This page displays information about gameplay options and allows a
    user to select what type of game they wish to play
    """
    template = "gameplay/index.html"
    past_games = None
    count_past_games = 0

    if request.user.is_authenticated:
        past_games = request.user.past_games
        count_past_games = past_games.count()

    return render(
        request,
        template,
        {
            "count_past_games": count_past_games,
            "past_games": past_games,
        },
    )


@login_required
def new_game(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    """Create a new game depending on which option the user chose to play"""
    game_type = kwargs.get("game_type", None)
    user = request.user

    if game_type is not None and game_type in [
        Game.PLAYER_VERSUS_COMPUTER,
        Game.PLAYER_VERSUS_PLAYER,
    ]:
        try:
            game = Game.objects.create(game_type=game_type, player_one=user)
            messages.success(request, "Your new game is ready to play, good luck!")
            return redirect(reverse("gameplay:play", kwargs={"game_uuid": game.id}))
        except Exception as ex:
            logger.error(ex)
            messages.error(
                request,
                "There was an issue creating a new game, the site admins have been alerted, please try again later.",
            )
            return redirect(reverse("gameplay:index"))
    else:
        messages.error(
            request,
            "The requested new game type could not be located, please verify and retry.",
        )
        return redirect(reverse("gameplay:index"))


@login_required
def play(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    """The main gameplay page
    Allows the user to select their choice, and then waits for second user to play their turn
    """
    template = "gameplay/play.html"
    game_id = kwargs.get("game_uuid", None)
    user = request.user

    if Game.objects.filter(id=game_id).exists():
        game = Game.objects.get(id=game_id)
    else:
        messages.error(
            request,
            "The requested game could not be located, please verify you have the correct URL.",
        )
        return redirect(reverse("gameplay:index"))

    if request.method == "POST":
        form = UserTurnForm(request.POST, user=user, game=game)
        if form.is_valid():
            form.save()
            messages.success(request, "Your turn has been played!")
            return redirect(reverse("gameplay:play", kwargs={"game_uuid": game.id}))
    else:
        form = UserTurnForm(user=user, game=game)

    # get the winner of the game, if any, so we don't query the db multiple times in the html
    game_winner_info = game.game_winner_info

    return render(
        request,
        template,
        {
            "user": user,
            "game": game,
            "form": form,
            "game_winner_info": game_winner_info,
        },
    )
