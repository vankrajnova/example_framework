from datetime import datetime, timezone


def convert_to_full_xml_format(date, time='T00:00:00.000', zone='Z'):
    pieces_of_date = date.split(".")
    return rf'{pieces_of_date[2]}-{pieces_of_date[1]}-{pieces_of_date[0]}{time}{zone}'

def convert_utc_to_local(dt_as_str):
    utc_datetime = datetime.strptime(dt_as_str, "%Y-%m-%dT%H:%M:%S.000Z")
    return utc_datetime.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%d.%m.%Y")

def format_date_for_hr(date):
    day, month, year = date.split(".")
    return f"{year}-{month}-{day}"

def full_date_to_short(date_as_str):
    dict_month = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
                  'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10',
                  'ноября': '11', 'декабря': '12'}
    day, month, year = date_as_str.split(' ')
    new_month = dict_month.get(month)
    return ".".join([day, new_month, year])
