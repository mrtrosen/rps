from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for Rock Paper Scissors.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def past_games(self):
        """Return a query set of all the games played by this user
        :return: QuerySet
        """
        as_player_one = self.games_as_player_one.all()
        as_player_two = self.games_as_player_two.all()

        # now that we have them all, sort them by descending created_at
        all_games = (as_player_one | as_player_two).order_by("-created_at")

        return all_games

    @property
    def winning_games(self):
        """Return a list of games this user has won
        :return: QuerySet
        """
        return self.past_games.filter(winner=self)
