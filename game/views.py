from django.shortcuts import render
from game.models import Player, Game, PlayerGameInfo
import random


def show_home(request):
    player_id = request.session.get('player_id', 'new')
    context = {}
    if isinstance(player_id, int):
        current_player = Player(pk=player_id)
        current_game = current_player.games.all().last()
        context = {
            'role': current_player.role,
            'number': current_game.number
        }

    else:
        game_check = Game.objects.all().last()

        if game_check and len(list(game_check.players.values())) == 1:
            # если игрок присоединяется к существующей игре
            new_player = Player(role='guest')
            new_player.save()
            request.session['player_id'] = new_player.id
            current_game = game_check
            many_to_many = PlayerGameInfo(players=new_player, games=current_game)
            many_to_many.save()
            context = {
                'role': new_player.role,
                'number': current_game.number
            }

        else:
            # если создаем новую игру и делаем текущего игрока хостом
            new_player = Player(role='HO')
            new_player.save()
            request.session['player_id'] = new_player.id
            number = random.randint(1, 10)
            new_game = Game(number=number)
            new_game.save()
            many_to_many = PlayerGameInfo(players=new_player, games=new_game)
            many_to_many.save()
            request.session['game_id'] = new_game.id
            context = {
                'role': new_player.role,
                'number': new_game.number
            }


    return render(
        request,
        'home.html',
        context=context
    )
