from django.db import models


class Player(models.Model):
    game = models.ManyToManyField('Game', through='PlayerGameInfo', related_name='player')
    name = models.CharField(max_length=20)


class Game(models.Model):
    players = models.ManyToManyField('Player', through='PlayerGameInfo', related_name='games')
    number = models.SmallIntegerField


class PlayerGameInfo(models.Model):
    players = models.ForeignKey(Player, on_delete=models.CASCADE)
    games = models.ForeignKey(Game, on_delete=models.CASCADE)

# Заходим на сайт, дергаем последнюю запись гаме из БД
# len(list(game1.players.values()))
# Если 1, то подцепляемся
# Если 2, создаем новую в качестве хоста
# Номер загадывает хост (автоматически)

