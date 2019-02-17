from django.shortcuts import render
from django.http import HttpResponse

import urllib
import json


def index(request):
    """
    포켓몬 데이터를 전송
    :param request:
    :return:
    """

    HttpResponse()['content_type'] = 'application/json; charset=utf-8'
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRm_Lc0uln_go1zCm1kqSZ6NU2lWZzFwbVUYrda6HVE6W5r62MjDhTCTa4PkDQ6s7PP0BME01jbE23s/pub?output=csv'
    pokemon_data = urllib.request.urlopen(url).read().decode('utf-8').split('\r\n')
    result = get_pokemon(pokemon_data)

    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


def get_pokemon(pokemon_data):
    """
    포켓몬 데이터를 사전형으로 렌더링
    :param pokemon_data:
    :return:
    """
    columns = []

    for tag in pokemon_data[0].split(','):
        columns.append(tag)

    pokemon = []

    for poke_no, row in enumerate(pokemon_data):
        if poke_no == 0:
            continue
        single = {'no': poke_no}
        monster = row.split(',')
        for monsterData in range(len(columns)):
            single[columns[monsterData]] = monster[monsterData]
        pokemon.append(single)

    return {'result': pokemon}


def test(request):
    """
    AJAX 테스트 페이지
    :param request:
    :return:
    """

    return render(request, 'main/index.html')
