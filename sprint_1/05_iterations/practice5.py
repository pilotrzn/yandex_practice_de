races_data = [
    {'Ferrari': 20, 'Mercedes': 5, 'Aston Martin': 10, 'Williams': 15},
    {'Mercedes': 15, 'Aston Martin': 20, 'Ferrari': 10, 'Williams': 0},
    {'Ferrari': 20, 'Williams': 15, 'Aston Martin': 10, 'Mercedes': 5}
]


def get_competition_data(races_data):
    command_names = {}
    command_scores = {}
    for race in races_data:
        for command, count in race.items():
            if command not in command_names:
                command_names[command] = command
                command_scores[command] = 0
            command_scores[command] += count

        #bubble sort
        winteam = None
        winscore = 0
        for command, count in command_scores.items():
             if count > winscore:
                  winscore = count
                  winteam = command

        print('Команды, участвовавшие в гонке: '+ ', '.join(sorted(dict.keys(command_names))))
        print(f'В гонке победила команда {winteam} с результатом {winscore} баллов')

get_competition_data(races_data)