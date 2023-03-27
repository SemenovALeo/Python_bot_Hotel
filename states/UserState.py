from telebot.handler_backends import State, StatesGroup

class User_State(StatesGroup):
    city = State()  # выбор города
    city_received = State()  # город найден
    number_of_hotels = State() # количество отелей
    checkInDate = State() #дата заезда
    checkOutDate = State() # дата выезда
    adults = State() # кол-во взрослых
    children = State() # кол-во дитей
    check_in = State()  # выбор даты заезда
    check_out = State()  # выбор даты выезда
    history = State()
    all = State()  # все данные получены
    # price = State()
