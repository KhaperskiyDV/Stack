import asyncio
import requests as req
from core.keyboards.keyboards import *
from core.utils.utils import generate_password
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from core.settings import settings
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

user_private_router = Router()
url_prefix = settings.bots.prod_url
# Вспомогательные функции
async def get_user_status_api(user_name: str):
    url = f"http://{url_prefix}:8000/api/users/is-superuser/{user_name}/"
    response = req.get(url)
    return response.json()

async def search_objects_api(search_text: str):
    url = f"http://{url_prefix}:8000/api/objects/?search={search_text}"
    response = req.get(url)
    return response.json()

async def get_device_types_api():
    url = f"http://{url_prefix}:8000/api/device-types/"
    response = req.get(url)
    return response.json()

async def get_object_devices_api(object_id: int):
    url = f"http://{url_prefix}:8000/api/objects/{object_id}/devices/"
    response = req.get(url)
    return response.json()

async def get_device_type_api(device_type_id: int):
    url = f"http://{url_prefix}:8000/api/device-types/{device_type_id}/"
    response = req.get(url)
    return response.json()

async def post_device_api(device_data: dict):
    return req.post(f'http://{url_prefix}:8000/api/devices/', data=device_data)


async def update_device_api(id:int, device_data:dict):
    return req.patch(f'http://{url_prefix}:8000/api/devices/{id}/', data=device_data)



@user_private_router.message(Command('start', 'run'))
async def get_start(message: Message, bot: Bot):
    user_status = await get_user_status_api(message.from_user.id)
    if  user_status['registred']:
        main_kb = Keyboards(user_status['is_superuser']).main_kb()
        await message.answer(f'Привет, {message.from_user.first_name}! ', reply_markup=main_kb)
    else:
        await message.answer(f'Привет, {message.from_user.first_name}!\n'
                             f'Для работы с ботом обратитесь к администратору.\n\n'
                             f'Передайте ему свой ID: {message.from_user.id}')

class ObjectStates(StatesGroup):
    user_name = State()
    object_search_text = State()
    object_search_result = State()
    object_selected = State()

class DeviceAdd(ObjectStates):
    device_type = State()
    device_name = State()
    device_model = State()
    device_ip = State()
    device_login = State()
    device_password = State()
    device_description = State()
    finish = State()

class DeviceInfo(ObjectStates):
    device_list = State()
    device_selected = State()
    device_actions = State()
    device_edit = State()

# Обработчики для разных действий (добавление/поиск)
@user_private_router.callback_query(F.data == 'add_device')
async def start_adding_device(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ObjectStates.object_search_text)
    await state.update_data(action='add')  # Сохраняем тип действия
    await callback.message.answer('Введите текст для поиска объекта для добавления устройства:')
    await callback.answer()

@user_private_router.callback_query(F.data == 'search_device')
async def start_searching_device(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ObjectStates.object_search_text)
    await state.update_data(action='search')  # Сохраняем тип действия
    await callback.message.answer('Введите текст для поиска объекта с устройствами:')
    await callback.answer()

# Общий обработчик для поиска объектов
@user_private_router.message(ObjectStates.object_search_text)
async def process_search_text(message: Message, state: FSMContext):
    search_text = message.text.strip()
    if not search_text:
        await message.answer("Текст поиска не может быть пустым. Попробуйте снова.")
        return
    
    objects = await search_objects_api(search_text)
    
    if not objects:
        await message.answer("Объекты не найдены. Попробуйте снова.")
        return
    
    await state.update_data(object_search_text=search_text, 
                            object_search_result=objects,
                            user_name=message.from_user.id)
    await state.set_state(ObjectStates.object_search_result)
    await message.answer(
        f'Найдено объектов: {len(objects)}\nВыберите нужный:',
        reply_markup=get_object_search_kb(objects)
    )

# Обработчик выбора объекта с ветвлением по типу действия
@user_private_router.callback_query(ObjectStates.object_search_result)
async def process_selected_object(callback: CallbackQuery, state: FSMContext):
    selected_object_id = int(callback.data)
    data = await state.get_data()
    objects = data['object_search_result']
    action = data.get('action')  # Получаем сохраненное действие
    
    selected_object = next((obj for obj in objects if obj['id'] == selected_object_id), None)
    
    if not selected_object:
        await callback.answer("Объект не найден!")
        return
    
    await state.update_data(object_selected=selected_object)
    await callback.answer()
    
    # Ветвление по типу действия
    if action == 'add':
        await process_add_device_after_object_selection(callback, state)
    elif action == 'search':
        await process_info_device_after_object_selection(callback, state)

async def process_add_device_after_object_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_object = data['object_selected']
    
    types_json = await get_device_types_api()
    await state.set_state(DeviceAdd.device_type)
    
    await callback.message.edit_text(
        f'Выбран объект:\n'
        f'Название: {selected_object["name"]}\n'
        f'Адрес: {selected_object["adress"]}\n\n'
        f'Теперь выберите тип устройства:',
        reply_markup=get_device_types_kb(types_json)
    )

async def process_info_device_after_object_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_object = data['object_selected']
    
    object_devices_list = await get_object_devices_api(selected_object['id'])
    await state.update_data(device_list=object_devices_list)
    
    if not object_devices_list:
        
        user_status = await get_user_status_api(data['user_name'])
        object_actions_kb = Keyboards(user_status['is_superuser']).object_actions_kb()

        await callback.message.edit_text(
            f'Выбран объект:\n'
            f'Название: {selected_object["name"]}\n'
            f'Адрес: {selected_object["adress"]}\n\n'
            f'У данного объекта нет устройств.',
            reply_markup=object_actions_kb
        )
        await state.set_state(DeviceInfo.device_actions)
    else:
        await state.set_state(DeviceInfo.device_list)
        await callback.message.edit_text(
            f'Выбран объект:\n'
            f'Название: {selected_object["name"]}\n'
            f'Адрес: {selected_object["adress"]}\n\n'
            f'Выберите устройство:',
            reply_markup=get_device_list_kb(object_devices_list)
        )

# Добавление устройства (продолжение)
@user_private_router.callback_query(DeviceAdd.device_type)
async def process_device_type(callback: CallbackQuery, state: FSMContext):
    device_type_id = int(callback.data)
    types_json = await get_device_types_api()
    
    device_type = next((t for t in types_json if t['id'] == device_type_id), None)
    
    if not device_type:
        await callback.answer("Неизвестный тип устройства!")
        return
    
    await state.update_data(device_type=device_type)
    await state.set_state(DeviceAdd.device_name)
    
    await callback.message.answer(
        f"Выбран тип: {device_type['name']}\n\nВведите название устройства:"
    )
    await callback.answer()

@user_private_router.message(DeviceAdd.device_name)
async def process_device_name(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Название не может быть пустым. Попробуйте снова.")
        return
    
    await state.update_data(device_name=message.text.strip())
    await state.set_state(DeviceAdd.device_model)
    await message.answer('Введите модель устройства:')

@user_private_router.message(DeviceAdd.device_model)
async def process_device_model(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Наименование модели не может быть пустым. Попробуйте снова.")
        return
    
    await state.update_data(device_model=message.text.strip())
    await state.set_state(DeviceAdd.device_ip)
    await message.answer('Введите IP устройства:')

@user_private_router.message(DeviceAdd.device_ip)
async def process_device_ip(message: Message, state: FSMContext):
    if not message.text.replace('.', '').isdigit():
        await message.answer("Неверный формат IP. Попробуйте снова.")
        return
    
    await state.update_data(device_ip=message.text)
    await state.set_state(DeviceAdd.device_login)
    await message.answer('Введите логин устройства:')

@user_private_router.message(DeviceAdd.device_login)
async def process_device_login(message: Message, state: FSMContext):
    if not message.text.strip():
        await message.answer("Логин не может быть пустым. Попробуйте снова.")
        return
    
    await state.update_data(device_login=message.text.strip())
    await message.delete()
    await state.set_state(DeviceAdd.device_password)
    
    suggested_password = generate_password(8)
    await message.answer(
        f'Введите пароль устройства:\n'
    )

@user_private_router.message(DeviceAdd.device_password)
async def process_device_password(message: Message, state: FSMContext):
    await state.update_data(device_password=message.text)
    await message.delete()
    await state.set_state(DeviceAdd.device_description)
    await message.answer('Введите описание устройства:')

@user_private_router.message(DeviceAdd.device_description)
async def process_device_description(message: Message, state: FSMContext):
    await state.update_data(device_description=message.text)
    data = await state.get_data()
    
    result_message = (
        f"Подтвердите ввод данных:\n\n"
        f"Объект: {data['object_selected']['name']}\n"
        f"Адрес: {data['object_selected']['adress']}\n\n"
        f"Тип устройства: {data['device_type']['name']}\n"
        f"Модель: {data['device_model']}\n"
        f"Название: {data['device_name']}\n"
        f"IP: {data['device_ip']}\n"
        f"Логин: {data['device_login']}\n"
        f"Пароль: {data['device_password']}\n"
        f"Описание: {data.get('device_description', 'не указано')}"
    )
    await state.set_state(DeviceAdd.finish)
    await message.answer(result_message, reply_markup=add_device_finish_kb)

@user_private_router.callback_query(DeviceAdd.finish)
async def process_finish(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'post_device':
        data = await state.get_data()
        post_data = {
            'type': data['device_type']['id'],
            'name': data['device_name'],
            'model': data['device_model'],
            'ip': data['device_ip'],
            'login': data['device_login'],
            'password': data['device_password'],
            'description': data['device_description'],
            'object': data['object_selected']['id'],
        }
        
        response = await post_device_api(post_data)
        if response.status_code == 201:
            await callback.message.edit_text(
                'Устройство успешно добавлено!',
                reply_markup=get_object_actions_kb()
            )
            await state.set_state(DeviceInfo.device_actions)
        else:
            await callback.message.answer(
                f'Произошла ошибка при добавлении устройства: {response.text}',
                reply_markup=main_kb
            )
            await state.clear()
    else:
        await callback.message.answer('Ввод данных отменен.', reply_markup=main_kb)
        await state.clear()
    await callback.answer()

# Поиск и работа с устройствами
@user_private_router.callback_query(DeviceInfo.device_list)
async def process_device_list(callback: CallbackQuery, state: FSMContext):
    selected_device_id = int(callback.data)
    data = await state.get_data()
    object_devices_list = data['device_list']
    
    selected_device = next((device for device in object_devices_list if device['id'] == selected_device_id), None)
    
    if not selected_device:
        await callback.answer("Устройство не найдено!")
        return
    
    await state.update_data(device_selected=selected_device)
    device_type = await get_device_type_api(selected_device['type'])
    user_status = await get_user_status_api(data['user_name'])
    device_actions_kb = Keyboards(user_status['is_superuser']).device_actions_kb()
    await callback.message.edit_text(
        f'Выбрано устройство:\n'
        f'Тип: {device_type["name"]}\n'
        f'Название: {selected_device["name"]}\n'
        f'Модель: {selected_device["model"]}\n'
        f'IP: {selected_device["ip"]}\n'
        f'Логин: {selected_device["login"]}\n'
        f'Пароль: {selected_device["password"]}\n'
        f'Описание: {selected_device["description"]}',
        reply_markup=device_actions_kb
    )
    await state.set_state(DeviceInfo.device_actions)
    await callback.answer()



@user_private_router.callback_query(DeviceInfo.device_actions, F.data == 'edit_device')
async def start_edit_device(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DeviceInfo.device_edit)
    await callback.message.edit_text(
        "Выберите, что хотите изменить:",
        reply_markup=get_device_edit_kb()
    )
    await callback.answer()

@user_private_router.callback_query(DeviceInfo.device_edit, F.data.startswith('edit_'))
async def select_field_to_edit(callback: CallbackQuery, state: FSMContext):
    field = callback.data.replace('edit_', '')
    await state.update_data(edit_field=field)
    
    field_names = {
        'name': "название",
        'model': "модель",
        'ip': "IP-адрес",
        'login': "логин",
        'password': "пароль",
        'description': "описание"
    }
    
    await callback.message.edit_text(
        f"Введите новое значение для {field_names.get(field, field)}:",
        reply_markup=get_cancel_edit_kb()
    )
    await callback.answer()

@user_private_router.message(DeviceInfo.device_edit)
async def process_edit_value(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data.get('edit_field')
    device = data['device_selected']
    
    if not field:
        await message.answer("Не выбрано поле для редактирования. Попробуйте снова.")
        return
    
    # Обновляем данные устройства
    new_data = {field: message.text}
    
    try:
        # API запрос для обновления устройства
        response = await update_device_api(device['id'], new_data)
        if response.status_code != 200:
            raise ValueError
        
        # Обновляем данные в состоянии
        updated_device = {**device, **new_data}
        await state.update_data(device_selected=updated_device)
        
        device_type = await get_device_type_api(updated_device['type'])
        
        await message.answer(
            f"Устройство успешно обновлено!\n\n"
            f"Тип: {device_type['name']}\n"
            f"Название: {updated_device['name']}\n"
            f"Модель: {updated_device['model']}\n"
            f"IP: {updated_device['ip']}\n"
            f"Логин: {updated_device['login']}\n"
            f"Пароль: {updated_device['password']}\n"
            f"Описание: {updated_device['description']}",
            reply_markup=get_device_actions_kb()
        )
        await state.set_state(DeviceInfo.device_actions)
        
    except Exception as e:
        await message.answer(
            f"Ошибка при обновлении устройства: {str(e)}",
            reply_markup=get_device_actions_kb()
        )
        await state.set_state(DeviceInfo.device_actions)

@user_private_router.callback_query(DeviceInfo.device_edit, F.data == 'cancel_edit')
async def cancel_editing(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    device = data['device_selected']
    device_type = await get_device_type_api(device['type'])
    
    await callback.message.edit_text(
        f'Редактирование отменено. Текущие данные устройства:\n\n'
        f'Тип: {device_type["name"]}\n'
        f'Название: {device["name"]}\n'
        f'Модель: {device["model"]}\n'
        f'IP: {device["ip"]}\n'
        f'Логин: {device["login"]}\n'
        f'Пароль: {device["password"]}\n'
        f'Описание: {device["description"]}',
        reply_markup=get_device_actions_kb()
    )
    await state.set_state(DeviceInfo.device_actions)
    await callback.answer()


@user_private_router.callback_query(DeviceInfo.device_actions, F.data == 'add_another_device')
async def add_another_device(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    types_json = await get_device_types_api()
    await state.set_state(DeviceAdd.device_type)
    
    await callback.message.answer(
        f'Выбран объект:\n'
        f'Название: {data["object_selected"]["name"]}\n'
        f'Адрес: {data["object_selected"]["adress"]}\n\n'
        f'Выберите тип нового устройства:',
        reply_markup=get_device_types_kb(types_json)
    )
    await callback.answer()

@user_private_router.callback_query(DeviceInfo.device_actions, F.data == 'back_to_device_list')
async def back_to_device_list(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    object_devices_list = await get_object_devices_api(data['object_selected']['id'])
    await state.update_data(device_list=object_devices_list)
    
    if object_devices_list:
        await state.set_state(DeviceInfo.device_list)
        await callback.message.edit_text(
            f'Выбран объект:\n'
            f'Название: {data["object_selected"]["name"]}\n'
            f'Адрес: {data["object_selected"]["adress"]}\n\n'
            f'Выберите устройство:',
            reply_markup=get_device_list_kb(object_devices_list)
        )
    else:
        await callback.message.edit_text(
            f'Выбран объект:\n'
            f'Название: {data["object_selected"]["name"]}\n'
            f'Адрес: {data["object_selected"]["adress"]}\n\n'
            f'У данного объекта нет устройств.',
            reply_markup=get_object_actions_kb()
        )
        await state.set_state(DeviceInfo.device_actions)
    await callback.answer()

@user_private_router.callback_query(DeviceInfo.device_actions, F.data == 'back_to_objects')
async def back_to_objects(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(ObjectStates.object_search_result)
    await callback.message.edit_text(
        f'Найдено объектов: 1\nВыберите нужный:',
        reply_markup=get_object_search_kb([data['object_selected']])
    )
    await callback.answer()

@user_private_router.callback_query(DeviceInfo.device_actions, F.data == 'main_menu')
async def back_to_objects(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_data = await get_user_status_api(data['user_name'])
    main_kb = Keyboards(user_data['is_superuser']).main_kb()
    await callback.message.answer('Вы вернулись в главное меню', reply_markup=main_kb)
    await state.clear()
    await callback.answer()