from django.shortcuts import render
from django.http import HttpResponse
from game.models import Player, Game, PlayerGameInfo
import random


def show_home(request):
    player_id = request.session.get('player_id', 'new')
    context = {}

    if request.method == 'POST':
        player_id = request.session.get('player_id', 'new')
        if player_id == 'new':
            return HttpResponse('Ошибка сессии')
        game_id = request.session.get('game_id')
        guess = int(request.POST.get('guess'))
        current_game = Game.objects.get(pk=game_id)
        current_player = Player.objects.get(pk=player_id)
        number = current_game.number
        context = {
            'role': current_player.role,
            'game': current_game,
            'guess': guess
        }
        if guess == number:
            current_game.solved = True
            current_game.try_count += 1
            current_game.save()
        else:
            current_game.try_count += 1
            current_game.save()

    elif isinstance(player_id, int):
        # игрок уже есть в базе
        current_player = Player.objects.get(pk=player_id)
        current_game = current_player.games.all().last()
        context = {
            'role': current_player.role,
            'game': current_game
        }

    else:
        game_check = Game.objects.all().last()

        if game_check and len(list(game_check.players.values())) == 1:
            # игрок присоединяется к существующей игре в роли гостя
            new_player = Player(role='GU')
            new_player.save()
            request.session['player_id'] = new_player.id
            current_game = game_check
            request.session['game_id'] = current_game.id
            many_to_many = PlayerGameInfo(players=new_player, games=current_game)
            many_to_many.save()
            context = {
                'role': new_player.role,
                'game': current_game
            }

        else:
            # создаем новую игру и делаем текущего игрока хостом
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
                'game': new_game
            }


    return render(request, 'home.html', context)
