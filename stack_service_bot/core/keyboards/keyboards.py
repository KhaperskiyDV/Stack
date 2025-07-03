from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [ InlineKeyboardButton(text="Добавить устройство", callback_data='add_device')],
            [ InlineKeyboardButton(text="Поиск устройства", callback_data='search_device')],
    ],
   
)

add_device_finish_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [ InlineKeyboardButton(text="Записать в базу", callback_data='post_device')],
            [ InlineKeyboardButton(text="Отмена", callback_data='cancel')],
    ],
   
)

DEVICE_TYPES = {
    "switch": "Коммутатор",
    "registrator": "Регистратор",
    "server": "Сервер",
    "camera": "Камера",
    
}

def get_device_types_kb(data: list[dict]) -> InlineKeyboardMarkup:
    """Генерирует инлайн-клавиатуру с типами устройств"""
    buttons = []
    for object in data:
        buttons.append([InlineKeyboardButton(text=f"{object['name']}", callback_data=str(object['id']))])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_object_search_kb(data: list[dict]) -> InlineKeyboardMarkup:
    buttons = []
    for object in data:
        buttons.append([InlineKeyboardButton(text=f"{object['name']} - {object['adress']}", callback_data=str(object['id']))])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_device_list_kb(data: list[dict]) -> InlineKeyboardMarkup:
    buttons = []
    for object in data:
        buttons.append([InlineKeyboardButton(text=f"{object['name']} - {object['ip']}", callback_data=str(object['id']))])
    return InlineKeyboardMarkup(inline_keyboard=buttons)



# __________________________________________________

# В core/keyboards/keyboards.py

def get_object_actions_kb():
    buttons = [
        [InlineKeyboardButton(text="Добавить еще одно устройство", callback_data="add_another_device")],
        [InlineKeyboardButton(text="В главное меню", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_device_actions_kb():
    buttons = [
        [InlineKeyboardButton(text="Редактировать", callback_data="edit_device")],
        # [InlineKeyboardButton(text="Добавить еще устройство", callback_data="add_another_device")],
        [InlineKeyboardButton(text="Назад к списку устройств", callback_data="back_to_device_list")],
        # [InlineKeyboardButton(text="В главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def cancel_edit_kb():
    buttons = [
        [InlineKeyboardButton(text="Отменить редактирование", callback_data="cancel_edit")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_device_edit_kb():
    buttons = [
        [InlineKeyboardButton(text="Название", callback_data="edit_name")],
        [InlineKeyboardButton(text="Модель", callback_data="edit_model")],
        [InlineKeyboardButton(text="IP", callback_data="edit_ip")],
        [InlineKeyboardButton(text="Логин", callback_data="edit_login")],
        [InlineKeyboardButton(text="Пароль", callback_data="edit_password")],
        [InlineKeyboardButton(text="Описание", callback_data="edit_description")],
        [InlineKeyboardButton(text="Отменить", callback_data="cancel_edit")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_cancel_edit_kb():
    buttons = [
        [InlineKeyboardButton(text="Отменить редактирование", callback_data="cancel_edit")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)