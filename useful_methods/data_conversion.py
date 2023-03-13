def convert_to_full_xml_format(date, time='T00:00:00.000', zone='Z'):
    pieces_of_date = date.split(".")
    return rf'{pieces_of_date[2]}-{pieces_of_date[1]}-{pieces_of_date[0]}{time}{zone}'
