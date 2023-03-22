from telebot.handler_backends import State, StatesGroup

class UserState(StatesGroup):
    city = State()  # выбор города
    city_received = State()  # город найден
    number_of_hotels = State() # количество отелей
    checkInDate = State() #дата заезда
    checkOutDate = State() # дата выезда
    adults = State() # кол-во взрослых
    children = State() # кол-во дитей
    check_in = State()  # выбор даты заезда
    check_out = State()  # выбор даты выезда
    all = State()  # все данные получены
    # price = State()
