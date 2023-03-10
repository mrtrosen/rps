# Generated by Django 4.1.4 on 2022-12-16 06:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_created=True,
                        blank=True,
                        null=True,
                        verbose_name="Last Player Turn",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "game_type",
                    models.IntegerField(
                        choices=[
                            (1, "Player vs. Player (PVP)"),
                            (2, "Player vs. Computer (AI)"),
                        ],
                        default=1,
                        verbose_name="Game Type",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "completed_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Game Completed At"
                    ),
                ),
                (
                    "player_one",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="games_as_player_one",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "player_two",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="games_as_player_two",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GameTurn",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "player_one_choice",
                    models.IntegerField(
                        blank=True,
                        choices=[(1, "rock"), (2, "scissor"), (3, "paper")],
                        null=True,
                        verbose_name="Player One Choice",
                    ),
                ),
                (
                    "player_two_choice",
                    models.IntegerField(
                        blank=True,
                        choices=[(1, "rock"), (2, "scissor"), (3, "paper")],
                        null=True,
                        verbose_name="Player Two Choice",
                    ),
                ),
                (
                    "turn_result",
                    models.IntegerField(
                        blank=True,
                        choices=[
                            (1, "Tie"),
                            (2, "Player One Wins"),
                            (3, "Player Two Wins"),
                        ],
                        null=True,
                        verbose_name="Turn Outcome",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="turns",
                        to="gameplay.game",
                    ),
                ),
            ],
        ),
    ]
