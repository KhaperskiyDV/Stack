from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

class Keyboards:
    def __init__(self, is_admin: bool = False):
        self.is_admin = is_admin

    def main_kb(self):
        if self.is_admin:
            return InlineKeyboardMarkup(inline_keyboard = [
            [ InlineKeyboardButton(text="Добавить устройство", callback_data='add_device')],
            [ InlineKeyboardButton(text="Поиск устройства", callback_data='search_device')],],)
        else:
            return InlineKeyboardMarkup(inline_keyboard = [            
            [ InlineKeyboardButton(text="Поиск устройства", callback_data='search_device')],],)

    def object_actions_kb(self):
        if self.is_admin:
            return InlineKeyboardMarkup(inline_keyboard = [
                [InlineKeyboardButton(text="Добавить еще одно устройство", callback_data="add_another_device")],
                [InlineKeyboardButton(text="В главное меню", callback_data="main_menu")],])
        else: 
            return InlineKeyboardMarkup(inline_keyboard = [
                [InlineKeyboardButton(text="В главное меню", callback_data="main_menu")],
        ])

    def device_actions_kb(self):
        if self.is_admin: 
            return InlineKeyboardMarkup (inline_keyboard =  [
            [InlineKeyboardButton(text="Редактировать", callback_data="edit_device")],
            [InlineKeyboardButton(text="Назад к списку устройств", callback_data="back_to_device_list")],
        ])
        else:
            return InlineKeyboardMarkup (inline_keyboard =  [
            [InlineKeyboardButton(text="Назад к списку устройств", callback_data="back_to_device_list")],
        ])



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
        [InlineKeyboardButton(text="Назад к списку устройств", callback_data="back_to_device_list")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def cancel_edit_kb():
    buttons = [
        [InlineKeyboardButton(text="Отменить редактирование", callback_data="cancel_edit")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_device_edit_kb():
    buttons = [
            [
                InlineKeyboardButton(text="Название", callback_data="edit_name"),
                InlineKeyboardButton(text="Модель", callback_data="edit_model")
            ],
            [
                InlineKeyboardButton(text="IP", callback_data="edit_ip"),
                InlineKeyboardButton(text="Логин", callback_data="edit_login")
            ],
            [
                InlineKeyboardButton(text="Пароль", callback_data="edit_password"),
                InlineKeyboardButton(text="Отменить", callback_data="cancel_edit")
            ]
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_cancel_edit_kb():
    buttons = [
        [InlineKeyboardButton(text="Отменить редактирование", callback_data="cancel_edit")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)