import datetime
from api import api

def get_datetime_str(value):
    data_value = datetime.datetime.strptime(value, '%d/%m/%y')
    data = {'day':data_value.date().day,
            'month':data_value.date().month,
            'year':data_value.date().year}
    return data

def get_id_region(data):
    # print(data["gaiaId"]["day"])
    print(data)
    print(api.api_request('properties/v2/list',data,'POST'))


