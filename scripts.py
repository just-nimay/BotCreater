
from bot_creater import dp, bot, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types
from markups import CreateingGC, layerConfig, mainMenuFull, inInfoToMenu
import markups as nav
import db

import os

from time import time

from config import CONFIG

from nft import main

# добавление коллекции
class FormCollect(StatesGroup):
    get_collect_name = State()

@dp.message_handler(state=FormCollect.get_collect_name)
async def get_collect_name(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['get_layer_name'] = message.text
        existing = db.check_exist_collect(message.from_user.id, message.text)
        if existing == 1:
            await message.answer(f'У тебя уже есть коллекция <i>{message.text}</i>, побробуй другое имя')
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id - 1)
        else:
            db.add_collection(message.from_user.id, message.text)
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id - 1)
            await state.finish()
            await bot.send_message(message.from_user.id, f'===================\n<b>ГЛАВНОЕ МЕНЮ СОЗДАНИЯ КОЛЛЕКЦИИ <i>{db.collection_name(message.from_user.id).upper()}</i></b>\n⏤⏤⏤-\nТак, тут ты можешь посмотреть свои слои или же добавить еще один слой. Ну а если ты уже всё что надо добавил, то тыкай кнопку <b>Сгенерировать⚙️</b>', reply_markup=mainMenuFull)

# добавление слоя
class FormLayer(StatesGroup):
    get_layer_name = State()
    get_serial_num = State()
    get_required = State()
    request_image = State()
    get_image = State()


@dp.message_handler(state=FormLayer.get_layer_name)
async def get_layer_name(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        check = db.checking_layer_name(message.from_user.id, message.text)
        if check == 1:
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id - 1 )
            await message.answer('Ой, кажется слой с таким именем уже есть, побробуй другое')
        else:
            data['get_layer_name'] = message.text
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id - 1)
            await FormLayer.next()
            await message.answer(f'Так, теперь напиши порядковый номер для слоя <b>{message.text}</b>')

@dp.message_handler(state=FormLayer.get_serial_num)
async def get_serial_num(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        try:
            serial_num = int(message.text)
            check = db.checking_serial_num(message.from_user.id, serial_num)
            if check == 1:
                await bot.delete_message(message.from_user.id, message.message_id)
                await bot.delete_message(message.from_user.id, message.message_id - 1)
                await message.answer('Хм, слой с таким пордковым номером уже есть.')
            else:
                data['get_serial_num']= serial_num
                await bot.delete_message(message.from_user.id, message.message_id)
                await bot.delete_message(message.from_user.id, message.message_id - 1)
                await FormLayer.next()
                await message.answer('А сейчас мне нужна требуемость слоя\n"Yes" или "No"')
        except ValueError:
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id - 1)
            await message.answer(f'Я не думаю, что "{message.text}" это число...')



@dp.message_handler(state=FormLayer.get_required)
async def get_required(message: types.Message, state:FSMContext):

    async with state.proxy() as data:
        if message.text.lower() == 'yes':
            data['get_required'] = 1
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id - 1)

            db.add_layer(data['get_layer_name'], data['get_serial_num'], data['get_required'],  message.from_user.id) #добавление слоя в таблицу layer
            await message.answer('Нус, слой добавлен\nMожешь добавить изображения, ну или создать еще один слой\n...ну или перейти в меню, ты тут сам решай)', reply_markup=CreateingGC)
            await state.finish()
        elif message.text.lower() == 'no':
            data['get_required'] = 0
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id - 1)

            db.add_layer(data['get_layer_name'], data['get_serial_num'], data['get_required'],  message.from_user.id) #добавление слоя в таблицу layer
            await message.answer('Нус, слой добавлен\nMожешь добавить изображения, ну или создать еще один слой\n...ну или перейти в меню, ты тут сам решай)', reply_markup=CreateingGC)
            await state.finish()
        else:
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id - 1)
            await message.answer('Ну понятно же написано: <b>yes</b> или <b>no</b>...')
 
 # добавление изображений
class FormAddImage(StatesGroup):
     get_images = State()


@dp.message_handler(content_types=['text', 'document'], state=FormAddImage)
@dp.message_handler(state=FormAddImage)
async def get_images(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == 'document':
            data['photo'] = message.document['file_id']
            print(message.document)
            extension = message.document['file_name'][-3:]
            print(extension)
            if extension == 'png':
                db.add_media(data['photo'], message.from_user.id)
                print('photo was added into media')
                await message.answer('Фото добавлено')
            else:
                await bot.delete_message(message.from_user.id, message.message_id)
                await message.answer('Нужен формат <i>png</i>')

        elif message.content_type == 'text':
            if message.text.lower() == 'готово':
                await bot.delete_message(message.from_user.id, message.message_id)
                await bot.delete_message(message.from_user.id, message.message_id - 1)
                await message.answer('Фото были успешно загружены!\nТеперь, я думаю, уже точно можно зайти в меню, ну или же создать еще один слой', reply_markup=CreateingGC)
                await state.finish()
            else:
                await bot.delete_message(message.from_user.id, message.message_id)
                await bot.delete_message(message.from_user.id, message.message_id - 1)
                await message.answer(f'кожанный, если ты уже все что надо добавил, пиши мне: <i>готово</i>\nНу если, конечно, твоё <i>"{message.text}"</i> это для тебя <i>"готово"</i>, то тогда сорян, я просто железяка')




# настройка слоя
class FormConfigLayer(StatesGroup):
    get_layer = State()


@dp.message_handler(state=FormConfigLayer.get_layer)
async def get_layer(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.delete_message(message.from_user.id, message.message_id - 1)

    async with state.proxy() as data:
        data['get_layer'] = message.text
    await state.finish()
    if message.text == 'Назад⏪':
        layers = db.get_layers(message.from_user.id)
        await bot.delete_message(message.from_user.id, message.message_id)

        await message.answer(f'===================\n<b>СЛОИ</b>\n⏤⏤⏤\nВот твои слои')
        info = db.get_layers(message.from_user.id, is_dict=True, with_info=True)
        for key in info:
            ser_num = info[key]['serial_num']
            req = info[key]['required']
            count_img = info[key]['count_img']
            await bot.send_message(message.from_user.id, f'<b>{key.upper()}</b>\nпорядковый номер: <i>{ser_num}</i>\nобязательность: <i>{req}</i>\nколличество изображений: <i>{count_img}</i>')
        await bot.send_message(message.from_user.id, 'Можешь настроить их', reply_markup=nav.layers)
    else:
        db.change_current_layer(message.from_user.id, message.text)
        info = db.get_info_layer(message.from_user.id)
        serial_number = info['serial_num']
        required = info['required']
        count_img = info['count_img']
        await message.answer(f'===================\n<b>НАСТРОЙКА СЛОЯ <i>{message.text.upper()}</i></b>\nЕго текущие настройки:\n<b>Порядковый номер</b>: <i>{serial_number}</i>\n<b>Обязательность</b>: <i>{required}</i>\n<b>Кол-во изображений:</b> <i>{count_img}</i>', reply_markup=layerConfig)


class FormLayerConfig(StatesGroup):
    get_serial_num = State()
    get_required = State()

@dp.message_handler(state=FormLayerConfig.get_serial_num)
async def get_serial_num(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['get_serial_num'] = int(message.text)
            db.change_serial_number(message.from_user.id, data['get_serial_num'])

            await state.finish()

            name = db.get_current_layer(message.from_user.id)
            info = db.get_info_layer(message.from_user.id)
            serial_number = info['serial_num']
            required = info['required']
            count_img = info['count_img']
            
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id - 1)
            await message.answer(f'Порядковый номер для слоя {name} был изменен на {serial_number}')

            await message.answer(f'===================\n<b>НАСТРОЙКА СЛОЯ <i>{name.upper()}</i></b>\nЕго текущие настройки:\n<b>Порядковый номер</b>: <i>{serial_number}</i>\n<b>Обязательность</b>: <i>{required}</i>\n<b>Кол-во изображений:</b> <i>{count_img}</i>', reply_markup=layerConfig)


        except ValueError:
            await bot.delete_message(message.from_user.id, message.message_id)
            await message.answer(f'Я не думаю, что "{message.text}" это число...')


@dp.message_handler(state=FormLayerConfig.get_required)
async def get_required(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        name = db.get_current_layer(message.from_user.id)
        info = db.get_info_layer(message.from_user.id)
        serial_number = info['serial_num']
        count_img = info['count_img']

        if message.text.lower() == 'да':           
            db.change_required(message.from_user.id, 1)
            await state.finish()
            required = db.get_info_layer(message.from_user.id)['required']
            
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id - 1)
            await message.answer(f'Обязательность для слоя {name} была изменена на {serial_number}')
            await message.answer(f'===================\n<b>НАСТРОЙКА СЛОЯ <i>{name.upper()}</i></b>\nЕго текущие настройки:\n<b>Порядковый номер</b>: <i>{serial_number}</i>\n<b>Обязательность</b>: <i>{required}</i>\n<b>Кол-во изображений:</b> <i>{count_img}</i>', reply_markup=layerConfig)

        elif message.text.lower() == 'нет':
            await state.finish()
            db.change_required(message.from_user.id, 0)
            required = db.get_info_layer(message.from_user.id)['required']
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id - 1)
            await message.answer(f'Обязательность для слоя {name} была изменена на {required}')
            await message.answer(f'===================\n<b>НАСТРОЙКА СЛОЯ <i>{name.upper()}</i></b>\nЕго текущие настройки:\n<b>Порядковый номер</b>: <i>{serial_number}</i>\n<b>Обязательность</b>: <i>{required}</i>\n<b>Кол-во изображений:</b> <i>{count_img}</i>', reply_markup=layerConfig)
            
        else:
            await bot.delete_message(message.from_user.id, message.message_id)
            await message.answer('Ну понятно же написано: <b>да</b> или <b>нет</b>...')
 
#удалить слой

class FormDeleteLayer(StatesGroup):
    request = State()

@dp.message_handler(state=FormDeleteLayer.request)
async def request(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        answ = message.text
        layer = db.get_current_layer(message.from_user.id)
        if answ.lower() == 'да':
            db.delete_layer(message.from_user.id)
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id - 1)
            await message.answer(f'Слой {layer} был удалён!')
            await state.finish()
            await message.answer(f'===================\n<b>ГЛАВНОЕ МЕНЮ СОЗДАНИЯ КОЛЛЕКЦИИ <i>{db.collection_name(message.from_user.id).upper()}</i></b>\n⏤⏤⏤-\nТак, тут ты можешь посмотреть свои слои или же добавить еще один слой. Ну а если ты уже всё что надо добавил, то тыкай кнопку <b>Сгенерировать⚙️</b>', reply_markup=mainMenuFull)
     
        else:
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.delete_message(message.from_user.id, message.message_id - 1)
            await state.finish()
            await message.answer('Ладно, как-нибудь в другой раз...')
            info = db.get_info_layer(message.from_user.id)
            serial_number = info['serial_num']
            required = info['required']
            count_img = info['count_img']
            await message.answer(f'===================\n<b>НАСТРОЙКА СЛОЯ <i>{layer.upper()}</i></b>\nЕго текущие настройки:\n<b>Порядковый номер</b>: <i>{serial_number}</i>\n<b>Обязательность</b>: <i>{required}</i>\n<b>Кол-во изображений:</b> <i>{count_img}</i>', reply_markup=layerConfig)


#+================================================+
#|              ГЕНЕРАЦИЯ  КОЛЛЕЦИИ               |
#+================================================+



async def create_config(telegram_id):
    config = []

    layers_info = db.get_info_layers(telegram_id)
    for layer in layers_info:
        layer_name = layer['name']

        layer_id = layer['serial_num']

        layer_required = layer['get_required']
        if layer_required == 1:
            layer_required = True
        else:
            layer_required = False

        layer_directory = layer_name

        layer_rarity_weights = None
        
        dict_val = {}
        dict_val['id'] = layer_id
        dict_val['name'] = layer_name
        dict_val['directory'] = layer_directory
        dict_val['required'] = layer_required
        dict_val['rarity_weights'] = layer_rarity_weights

        config.append(dict_val)

    return config




async def create_dirs(path):
    path_assets = f'{path}/assets'
    print('PATH ASSETS:', path_assets)

    is_dir = os.path.isdir(path_assets)
    if is_dir == False:
        os.mkdir(path_assets)

    with open(f'{path}/config.py', 'r') as config:
        lines = config.readlines()
        print('READING CONFIG FILE...')
        for line in lines:
            directory = ''
            if "'directory'" in line:
                directory = line[15:-3]
                
            path_direct = f'{path_assets}/{directory}'
            print('PATH DIRECT:', path_direct)
            is_dir = os.path.isdir(path_direct)
            if is_dir == False:
                os.mkdir(path_direct)

async def download_images(path, telegram_id, bot):
    path_assets = f'{path}/assets'
    photos_dict = db.get_image_info(telegram_id)


    for root, dirs, files in os.walk(path_assets):
        print('first for start') 
        dir_name = root[22:]
        if len(dir_name) > 0:
            print('DIR_NAME:', dir_name)
            dir_name = dir_name.split('/')
            print('DIR_NAME:', dir_name)
            if len(dir_name) > 1:
                dir_name = dir_name[1]
                print('DIR_NAME:', dir_name)

        print('first for end')
        for key in photos_dict:
            print('second for start')
            print('key:', key)
            print('dir_name:', dir_name)

            if dir_name == key:
                photos = photos_dict[key]
                print('second for end')
                for file_id in photos:
                    print('third for start')
                    file = await bot.get_file(file_id)
                    
                    file_name = file['file_path']
                    print(file_name)
                    file_name = file_name.split('/')
                    print(file_name)
                    file_name = file_name[1]
                    print(file_name)
                    download_file_photo = await bot.download_file(file.file_path)

                    src = f'{path_assets}/{dir_name}/{file_name}'

                    with open(src, 'wb') as new_file:
                        new_file.write((download_file_photo).read())

                    print('photo was downloaded!')
                    print('third for end')

class FormGenerating(StatesGroup):
    confirm = State()

@dp.message_handler(state=FormGenerating.confirm)
async def confirm(message: types.Message, state: FSMContext):
    if message.text == 'Всё 👌':
        await state.finish()
        
        await bot.delete_message(message.from_user.id, message.message_id)
        await bot.delete_message(message.from_user.id, message.message_id - 1)
        await message.answer('Начало создания коллекции...')
        col_name = db.collection_name(message.from_user.id)
        CONFIG = await create_config(message.from_user.id)
        telegram_id = message.from_user.id
        
        is_dir = os.path.isdir(str(telegram_id))
        print(is_dir)
        if is_dir == False:
            os.mkdir(str(telegram_id))
            os.mkdir(f'{telegram_id}/{col_name}')

        path = f'{telegram_id}/{col_name}'

        with open(f'{path}/config.py', 'w') as config:
            CONFIG = str(CONFIG)
            CONFIG = CONFIG.replace('[', '[\n')
            CONFIG = CONFIG.replace('{', '{\n')
            CONFIG = CONFIG.replace(',', ',\n')
            CONFIG = CONFIG.replace('},', '\n},')
            config.write(f'CONFIG = {CONFIG}')
        
        print('starting create_dirs...')
        await create_dirs(path)
        print('finish create_dirs!')

        print('starting downloading...')
        await download_images(path, message.from_user.id, bot)
        print('finish download!')

        print('starting generating...')
        config = await create_config(telegram_id)
        await main(path, col_name, config, message)
        print('finish generating!')

    else:
        await state.finish()
        await message.answer('Если что-то не так, нажми кнопку "Меню☕️"', reply_markup=inInfoToMenu)

 

