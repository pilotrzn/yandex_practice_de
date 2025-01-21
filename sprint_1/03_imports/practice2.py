from datetime import datetime as dt, time as t


# Напишите код функции, следуя плану из задания.
def get_results(leader, participant):
    t_lead = dt.strptime(leader, '%H:%M:%S')
    t_partic = dt.strptime(participant, '%H:%M:%S')
    diff = (t_partic - t_lead).total_seconds()

    if diff <= 0:
        print('Вы пробежали за {0} и победили!'.format(participant))
    else:
        hours = int(diff // (60 * 60))
        diff_format = t(hours % 24, int(diff // 60) % 60, int(diff % 60))
        mes = str(hours) + ':' + diff_format.strftime("%M:%S")
        print('Вы пробежали за {0} с отставанием от лидера {1}'.format(
            participant, mes)
            )


# Проверьте работу программы, можете подставить свои значения.
get_results('03:03:03', '03:03:03')
get_results('02:02:02', '03:04:05')
get_results('02:02:02', '02:00:05')
