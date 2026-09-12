import datetime


def get_time():
    return f"{datetime.date.today().year}/{datetime.date.today().month}/{datetime.date.today().day}"

print(get_time())