import logging
import random

from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from rps.gameplay.models import Game, GameTurn
from rps.utils import constants

User = get_user_model()
logger = logging.getLogger(__name__)


class UserTurnForm(forms.ModelForm):
    """The form used for a user playing their part of the game"""

    user = None
    game = None

    class Meta:
        model = GameTurn
        fields = ["player_one_choice", "player_two_choice"]

    def __init__(self, *args, **kwargs):
        # pass the logged in user and the game into the form for security/non-cheat reasons
        self.user = kwargs.pop("user")
        self.game = kwargs.pop("game")
        super().__init__(*args, **kwargs)

        if self.user == self.game.player_one:
            self.fields["player_two_choice"].widget = forms.HiddenInput()
        else:
            self.fields["player_one_choice"].widget = forms.HiddenInput()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.game = self.game

        if self.game.game_type == Game.PLAYER_VERSUS_COMPUTER:
            # autoplay the turn for the computer
            computer_choice = random.choice(
                [constants.ROCK, constants.SCISSOR, constants.PAPER]
            )
            instance.player_two_choice = computer_choice

        if (
            instance.player_one_choice is not None
            and instance.player_two_choice is not None
        ):
            # if they chose the same option, it's a TIE
            if instance.player_one_choice == instance.player_two_choice:
                instance.turn_result = GameTurn.PLAYER_TIE

            # check the scenarios for player one beating player two:
            # ROCK     beats    SCISSORS
            # SCISSORS beats    PAPER
            # PAPER    beats    ROCK
            elif (
                instance.player_one_choice == constants.ROCK
                and instance.player_two_choice == constants.SCISSOR
            ):
                instance.turn_result = GameTurn.PLAYER_ONE_WINS
            elif (
                instance.player_one_choice == constants.SCISSOR
                and instance.player_two_choice == constants.PAPER
            ):
                instance.turn_result = GameTurn.PLAYER_ONE_WINS
            elif (
                instance.player_one_choice == constants.PAPER
                and instance.player_two_choice == constants.ROCK
            ):
                instance.turn_result = GameTurn.PLAYER_ONE_WINS

            # If player one didn't beat player two on any of the choices, then player two wins by default!
            else:
                instance.turn_result = GameTurn.PLAYER_TWO_WINS

        if instance.turn_result is not None:
            if instance.turn_result in [
                GameTurn.PLAYER_ONE_WINS,
                GameTurn.PLAYER_TWO_WINS,
            ]:
                self.game.completed_at = timezone.now()

        # save the game so that the modified_date updates to reflect that we have had some action performed on it

        self.game.save()

        if commit:
            instance.save()

        return instance
