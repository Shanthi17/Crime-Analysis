import datetime

def date_sorter(listofdicts):
    date_appended_list = []

    for i, item in enumerate(listofdicts):
        date_time_str = item['FIRST_OCCURRENCE_DATE']
        date_time_obj = datetime.datetime.strptime(date_time_str, '%m/%d/%Y %I:%M:%S %p')
        date_appended_list.append([date_time_obj, item])
    date_appended_list.sort(key = lambda date_appended_list: date_appended_list[0])

    listofdicts = [item[1] for item in date_appended_list]

    return listofdicts
