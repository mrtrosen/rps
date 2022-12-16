import logging
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from rps.utils import constants

User = get_user_model()
logger = logging.getLogger(__name__)


class Game(models.Model):
    PLAYER_VERSUS_PLAYER = 1
    PLAYER_VERSUS_COMPUTER = 2
    GAME_TYPE_CHOICES = (
        (PLAYER_VERSUS_PLAYER, "Player vs. Player (PVP)"),
        (PLAYER_VERSUS_COMPUTER, "Player vs. Computer (AI)"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game_type = models.IntegerField(
        "Game Type", choices=GAME_TYPE_CHOICES, default=PLAYER_VERSUS_PLAYER
    )

    player_one = models.ForeignKey(
        User,
        related_name="games_as_player_one",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    player_two = models.ForeignKey(
        User,
        related_name="games_as_player_two",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField("Created At", auto_now_add=True)
    modified_at = models.DateTimeField(
        "Last Player Turn", auto_now=True, blank=True, null=True
    )
    completed_at = models.DateTimeField("Game Completed At", blank=True, null=True)

    @property
    def game_winner_info(self):
        """Return the winner of a game
        Since the computer player is not an actual user, we need to determine who won based on the results of the Turns
        :return: User who won game, else None
        """
        winning_player = None
        name = None
        if self.turns.filter(turn_result=GameTurn.PLAYER_ONE_WINS).count() > 0:
            if self.player_one is None:
                name = "Computer"
                winning_player = None
            else:
                name = self.player_one.name
                winning_player = self.player_one
        elif self.turns.filter(turn_result=GameTurn.PLAYER_TWO_WINS).count() > 0:
            if self.player_two is None:
                name = "Computer"
                winning_player = None
            else:
                name = self.player_two.name
                winning_player = self.player_two

        # if there is a winning player, return their info
        if name is not None:
            return {
                "name": name,
                "user": winning_player,
            }

        # there is not yet a winning player!
        return None

    def which_players_turn(self):
        """Determine which player's turn it is.
        If there are no turns, or the same number of turns for each player has been completed,
        either player can play, so we return None

        If Player one has played more turns, then it's player two's turn
        Otherwise it's Player One's turn
        """
        # if there have been no turns made, either player can play
        if self.turns.count() == 0:
            return None

        player_one_turn_count = self.turns.filter(
            player_one_choice__isnull=False
        ).count()
        player_two_turn_count = self.turns.filter(
            player_two_choice__isnull=False
        ).count()

        player_user = None
        if player_one_turn_count == player_two_turn_count:

            return None

        if player_one_turn_count > player_two_turn_count:
            if self.player_two is None:
                player_name = "Computer"
            else:
                player_name = self.player_two.name
                player_user = self.player_two

        else:
            if self.player_one is None:
                player_name = "Computer"
            else:
                player_name = self.player_one.name
                player_user = self.player_one

        return {
            "name": player_name,
            "user": player_user,
        }

    def get_absolute_url(self):
        """Get url for game's play view

        Returns:
            str: URL for game's play view.

        """
        return reverse("gameplay:play", kwargs={"uuid": self.id})

    def __str__(self):
        return str(self.id)


class GameTurn(models.Model):
    TURN_PLAY_CHOICES = tuple(
        [
            (key, option["name"])
            for key, option in constants.GAMEPLAY_OPTIONS_DICT.items()
        ]
    )

    PLAYER_TIE = 1
    PLAYER_ONE_WINS = 2
    PLAYER_TWO_WINS = 3
    TURN_OUTCOME_CHOICES = (
        (PLAYER_TIE, "Tie"),
        (PLAYER_ONE_WINS, "Player One Wins"),
        (PLAYER_TWO_WINS, "Player Two Wins"),
    )

    game = models.ForeignKey("Game", related_name="turns", on_delete=models.CASCADE)
    player_one_choice = models.IntegerField(
        "Player One Choice", choices=TURN_PLAY_CHOICES, blank=True, null=True
    )
    player_two_choice = models.IntegerField(
        "Player Two Choice", choices=TURN_PLAY_CHOICES, blank=True, null=True
    )

    turn_result = models.IntegerField(
        "Turn Outcome", choices=TURN_OUTCOME_CHOICES, blank=True, null=True
    )

    created_at = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        if self.game.player_one is not None:
            player_one_name = self.game.player_one.name
        else:
            player_one_name = "Computer"

        if self.game.player_two is not None:
            player_two_name = self.game.player_two.name
        else:
            player_two_name = "Computer"

        if self.player_one_choice is not None:
            player_one_info = f"played {self.get_player_one_choice_display()}"
        else:
            player_one_info = "has not yet picked a choice"

        if self.player_two_choice is not None:
            player_two_info = f"played {self.get_player_two_choice_display()}"
        else:
            player_two_info = "has not yet picked a choice"

        return f"{player_one_name} {player_one_info} vs {player_two_name} {player_two_info}"
