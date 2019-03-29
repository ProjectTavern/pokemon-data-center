from django.shortcuts import render
from django.http import HttpResponse

import urllib
import json


def pokemon(request):
    """
    포켓몬 데이터를 전송
    :param request:
    :return:
    """
    request_data = request.GET.dict()
    if 'no' in request_data:
        pokemon_no = request_data['no']
    else:
        pokemon_no = 0

    HttpResponse()['content_type'] = 'application/json; charset=utf-8'
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRm_Lc0uln_go1zCm1kqSZ6NU2lWZzFwbVUYrda6HVE6W5r62MjDhTCTa4PkDQ6s7PP0BME01jbE23s/pub?output=csv'
    pokemon_data = urllib.request.urlopen(url).read().decode('utf-8').split('\r\n')
    result = get_pokemon(pokemon_data, int(pokemon_no))

    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


def get_pokemon(pokemon_data, pokemon_no):
    """
    포켓몬 데이터를 사전형으로 렌더링
    :param pokemon_data:
    :param pokemon_no:
    :return:
    """
    columns = []
    pokemon_result = []

    for tag in pokemon_data[0].split(','):
        columns.append(tag)

    for poke_no, row in enumerate(pokemon_data):
        if poke_no == 0:
            continue
        single = {'no': poke_no}
        status = {}
        monster = row.split(',')

        if 0 < pokemon_no < 152 and pokemon_no == poke_no:
            for monsterData in range(len(columns)):
                if columns[monsterData] == 'sum' or columns[monsterData] == 'specialAttack' or columns[monsterData] == 'captureRate' or columns[monsterData] == 'defence' or columns[monsterData] == 'speed' or columns[monsterData] == 'hp' or columns[monsterData] == 'attackDamage' or columns[monsterData] == 'specialDefence':
                    status[columns[monsterData]] = int(monster[monsterData])
                else:
                    single[columns[monsterData]] = monster[monsterData].strip('\"')
            pokemon_result.append(single)
        elif 0 >= pokemon_no or pokemon_no >= 152:
            for monsterData in range(len(columns)):
                if columns[monsterData] == 'sum' or columns[monsterData] == 'specialAttack' or columns[monsterData] == 'captureRate' or columns[monsterData] == 'defence' or columns[monsterData] == 'speed' or columns[monsterData] == 'hp' or columns[monsterData] == 'attackDamage' or columns[monsterData] == 'specialDefence':
                    status[columns[monsterData]] = int(monster[monsterData])
                else:
                    single[columns[monsterData]] = monster[monsterData].strip('\"')
            single['status'] = status
            pokemon_result.append(single)

    return {'result': pokemon_result}


def test(request):
    """
    AJAX 테스트 페이지
    :param request:
    :return:
    """

    return render(request, 'main/index.html')
