from data.loader import db




def show_time(time):
    time = int(time)
    minute = 60
    hour = minute * 60
    day = hour * 24
    week = day * 7
    month = day * 31
    year = day * 365

    if time >= year:
        date = time // year
        if date == 1 or (date > 20 and int(str(date)[-1]) == 1):
            return f'{date} год'
        elif date <= 4 or (date > 20 and (int(str(date)[-1]) <= 4 and int(str(date)[-1]) >= 1)):
            return f'{date} года'
        else:
            return f'{date} лет'
    elif time >= month:
        date = time // month
        if date == 1 or (date > 20 and int(str(date)[-1]) == 1):
            return f'{date} месяц'
        elif date <= 4 or (date > 20 and (int(str(date)[-1]) <= 4 and int(str(date)[-1]) >= 1)):
            return f'{date} месяца'
        else:
            return f'{date} месяцев'
    elif time >= week:
        date = time // week
        if date == 1 or (date > 20 and int(str(date)[-1]) == 1):
            return f'{date} неделя'
        elif date <= 4 or (date > 20 and (int(str(date)[-1]) <= 4 and int(str(date)[-1]) >= 1)):
            return f'{date} недели'
        else:
            return f'{date} недель'
    elif time >= day:
        date = time // day
        if date == 1 or (date > 20 and int(str(date)[-1]) == 1):
            return f'{date} день'
        elif date <= 4 or (date > 20 and (int(str(date)[-1]) <= 4 and int(str(date)[-1]) >= 1)):
            return f'{date} дня'
        else:
            return f'{date} дней'
    elif time >= hour:
        date = time // hour
        if date == 1 or (date > 20 and int(str(date)[-1]) == 1):
            return f'{date} час'
        elif date <= 4 or (date > 20 and (int(str(date)[-1]) <= 4 and int(str(date)[-1]) >= 1)):
            return f'{date} часа'
        else:
            return f'{date} часов'
    elif time >= minute:
        date = time // minute
        if date == 1 or (date > 20 and int(str(date)[-1]) == 1):
            return f'{date} минута'
        elif date <= 4 or (date > 20 and (int(str(date)[-1]) <= 4 and int(str(date)[-1]) >= 1)):
            return f'{date} минуты'
        else:
            return f'{date} минут'
    else:
        if time == 1 or (time > 20 and int(str(time)[-1]) == 1):
            return f'{time} секунда'
        elif time <= 4 or (time > 20 and (int(str(time)[-1]) <= 4 and int(str(time)[-1]) >= 1)):
            return f'{time} секунды'
        else:
            return f'{time} секунд'




def check_time(text):

    minute = 60
    hour = minute * 60
    day = hour * 24
    week = day * 7
    month = day * 31
    year = day * 365

    text = str(text)
    try:
        if 'year' == text[-4:]:
            return int(text[:-4]) * year

        elif 'month' == text[-5:]:
            return int(text[:-5]) * month

        elif 'week' == text[-4:]:
            return int(text[:-4]) * week

        elif 'day' == text[-3:]:
            return int(text[:-3]) * day

        elif 'hour' == text[-4:]:
            return int(text[:-4]) * hour

        elif 'minute' == text[-6:]:
            return int(text[:-6]) * minute
        else:
            return int(text)
    except:
        return False


# 1692985841