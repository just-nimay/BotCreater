from aiogram import executor, types
from config import TOKEN
from bot_creater import dp, bot
from aiogram.dispatcher import FSMContext

from info import Information, n
import db
import markups as nav

from scripts import FormLayer, FormConfigLayer, FormCollect, FormAddImage, FormLayerConfig, FormDeleteLayer, FormGenerating

@dp.message_handler(commands=['start'])
async def command_start(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.send_message(message.from_user.id, '===================\nПривет, <s>человек</s> <u>{0.username}</u>, это главное меню\n⏤⏤⏤\nТыкай кнопку <b>Информация📚</b>, если ты тут впервые (просто лучше ознакомиться, оно того стоит)'.format(message.from_user), reply_markup=nav.mainMenu)
    db.add_user(message.from_user.id)

@dp.message_handler(commands=['main'])
async def cmd_main(message: types.Message):
    await bot.send_message(message.from_user.id, f'===================\n<b>ГЛАВНОЕ МЕНЮ СОЗДАНИЯ КОЛЛЕКЦИИ <i>{db.collection_name(message.from_user.id).upper()}</i></b>\n⏤⏤⏤-\nТак, тут ты можешь посмотреть свои слои или же добавить еще один слой. Ну а если ты уже всё что надо добавил, то тыкай кнопку <b>Сгенерировать⚙️</b>', reply_markup=nav.mainMenuFull)


@dp.callback_query_handler(lambda c: c.data == 'btnMenu')
async def btnMenu(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(f'===================\n<b>ГЛАВНОЕ МЕНЮ СОЗДАНИЯ КОЛЛЕКЦИИ <i>{db.collection_name(callback_query.from_user.id).upper()}</i></b>\n⏤⏤⏤-\nТак, тут ты можешь посмотреть свои слои или же добавить еще один слой. Ну а если ты уже всё что надо добавил, то тыкай кнопку <b>Сгенерировать⚙️</b>', reply_markup=nav.mainMenuFull)


@dp.callback_query_handler(lambda c: c.data == 'btnInfo')
async def info(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(Information.INFO, reply_markup=nav.inInfo)

@dp.callback_query_handler(lambda c: c.data == 'btnInfoInMenu')
async def info(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(Information.INFO, reply_markup=nav.inInfoToMenu)


@dp.callback_query_handler(lambda c: c.data == 'btnCreateGC')
async def btnCreateGC(callback_query: types.CallbackQuery):  
    await callback_query.message.edit_text('Напиши название коллекции (только на английском)')
    await FormCollect.get_collect_name.set()


@dp.callback_query_handler(lambda c: c.data =='btnAddImage')
async def add_image(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(f'И так, изображения будут добавляться в слой <i>{db.get_current_layer(callback_query.from_user.id)}</i>\nМожешь отправлять изображения\nПосле того, как ты отправишь все нужные фотки, напиши мне: <i>готово</i>')
    await FormAddImage.get_images.set()


@dp.callback_query_handler(lambda c: c.data == 'btnAddLayer')
async def add_layer(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('Напиши название слоя (только на английском)')
    await FormLayer.get_layer_name.set()


@dp.callback_query_handler(lambda c: c.data == 'btnLayers')
async def btnLayers(callback_query: types.CallbackQuery):
    layers = db.get_layers(callback_query.from_user.id)
    await callback_query.message.edit_text(f'===================\n<b>СЛОИ</b>\n⏤⏤⏤\nВот твои слои')
    info = db.get_layers(callback_query.from_user.id, is_dict=True, with_info=True)
    for key in info:
        ser_num = info[key]['serial_num']
        req = info[key]['required']
        count_img = info[key]['count_img']
        await bot.send_message(callback_query.from_user.id, f'<b>{key.upper()}</b>\nпорядковый номер: <i>{ser_num}</i>\nобязательность: <i>{req}</i>\nколличество изображений: <i>{count_img}</i>')
    await bot.send_message(callback_query.from_user.id, 'Можешь настроить их', reply_markup=nav.layers)

@dp.callback_query_handler(lambda c: c.data == 'btnBack_inLayers')
async def btnBack_inLayers(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(f'===================\n<b>ГЛАВНОЕ МЕНЮ СОЗДАНИЯ КОЛЛЕКЦИИ <i>{db.collection_name(callback_query.from_user.id).upper()}</i></b>\n⏤⏤⏤-\nТак, тут ты можешь посмотреть свои слои или же добавить еще один слой. Ну а если ты уже всё что надо добавил, то тыкай кнопку <b>Сгенерировать⚙️</b>', reply_markup=nav.mainMenuFull)


@dp.callback_query_handler(lambda c: c.data == 'btnConfigureLayer')
async def btnConfigureLayer(callback_query: types.CallbackQuery):
    layers = db.get_layers(callback_query.from_user.id, True)
    markup = nav.layer_buttons(layers)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, f'===================\n<b>НАСТРОЙКА СЛОЕВ</b>\n⏤⏤⏤\nВыбери слой', reply_markup=markup)
    await FormConfigLayer.get_layer.set()

#button back in layer configuration
@dp.callback_query_handler(lambda c: c.data == 'btnBackInLayerConfig')
async def btnBackInLayerConfig(callback_query: types.CallbackQuery):
    layers = db.get_layers(callback_query.from_user.id, True)
    markup = nav.layer_buttons(layers)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, f'===================\n<b>НАСТРОЙКА СЛОЕВ</b>\n⏤⏤⏤\nВыбери слой', reply_markup=markup)
    await FormConfigLayer.get_layer.set()

#change serial number
@dp.callback_query_handler(lambda c: c.data == 'btnChangeSerNum')
async def btnChangeSerNum(callback_query: types.CallbackQuery):
    name = db.get_current_layer(callback_query.from_user.id)
    await callback_query.message.edit_text(f'Напиши порядковый номер для слоя <b>{name}</b>')
    await FormLayerConfig.get_serial_num.set()

#change required
@dp.callback_query_handler(lambda c: c.data == 'btnChangeRequired')
async def btnChangeRequired(callback_query: types.CallbackQuery):
    name = db.get_current_layer(callback_query.from_user.id)
    await callback_query.message.edit_text(f'Напиши требуемость слоя {name}\n"Да" или "Нет"')
    await FormLayerConfig.get_required.set()

#Delete Layer
@dp.callback_query_handler(lambda c: c.data =='btnDeleteLayer')
async def btnDeleteLayer(callback_query: types.CallbackQuery):
    layer = db.get_current_layer(callback_query.from_user.id)
    await callback_query.message.edit_text(f'Ты уверен что хочешь удалить слой {layer}?\n"Да" или "Нет"')
    await FormDeleteLayer.request.set()

#+------------------------+
#|     DELETE IMAGE       |
#+------------------------+

@dp.callback_query_handler(lambda c: c.data == 'btnDeleteImage')
async def btnDeleteImage(callback_query: types.CallbackQuery):
    images = db.get_images(callback_query.from_user.id)
    if len(images) == 0:
        await callback_query.answer(text='Нечего удалять')
    else:
        global n
        n = 0
        await callback_query.message.edit_text('Какое из?')
        await bot.send_document(callback_query.from_user.id, images[n], f'{n + 1} изображение', reply_markup=nav.gallery)

# button back
@dp.callback_query_handler(lambda c: c.data == 'btnBackImage')
async def btnBackImage(callback_query: types.CallbackQuery):
    global n
    images = db.get_images(callback_query.from_user.id)
    print('n:', n)
    if n <= 0:
        await callback_query.answer(text='Там ничего нет...')
    else:
        n -= 1
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_document(callback_query.from_user.id, images[n], f'{n + 1} изображение', reply_markup=nav.gallery)



# button next
@dp.callback_query_handler(lambda c: c.data == 'btnNextImage')
async def btnNextImage(callback_query: types.CallbackQuery):    
    global n
    images = db.get_images(callback_query.from_user.id)
    count_img = len(images) - 1
    print('count_img:', count_img)
    print('n:', n)
    if n == count_img:
        await callback_query.answer(text='Дальше некуда')
    else:
        n += 1
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_document(callback_query.from_user.id, images[n], f'{n + 1} изображение', reply_markup=nav.gallery)


# button select image
@dp.callback_query_handler(lambda c: c.data == 'btnThisImage')
async def btnThisImage(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    global n
    images = db.get_images(callback_query.from_user.id)
    cur_img = images[n]
    print('current_image:', cur_img)
    db.delete_image(cur_img)
    await bot.send_message(callback_query.from_user.id, 'Изображение было удалено!')

    name = db.get_current_layer(callback_query.from_user.id)
    info = db.get_info_layer(callback_query.from_user.id)
    serial_number = info['serial_num']
    count_img = info['count_img']
    required = info['required']

    await bot.send_message(callback_query.from_user.id, f'===================\n<b>НАСТРОЙКА СЛОЯ <i>{name.upper()}</i></b>\nЕго текущие настройки:\n<b>Порядковый номер</b>: <i>{serial_number}</i>\n<b>Обязательность</b>: <i>{required}</i>\n<b>Кол-во изображений:</b> <i>{count_img}</i>', reply_markup=nav.layerConfig)

#+========================================+
#|               GENERATION               |
#+========================================+

@dp.callback_query_handler(lambda c: c.data == 'btnGenerate')
async def btnGenerate(callback_query: types.CallbackQuery):
    info = db.get_layers(callback_query.from_user.id, is_dict=True, with_info=True)
    if len(info) < 2:
        await callback_query.answer(text='Недостаточно слоёв!')
    else:
        await callback_query.message.edit_text(f'Так, перед тем как сгенерировать изображения, убедись, что все ок')

        #geting layers
        for key in info:
            ser_num = info[key]['serial_num']
            req = info[key]['required']
            count_img = info[key]['count_img']
            await bot.send_message(callback_query.from_user.id, f'<b>{key.upper()}</b>\nпорядковый номер: <i>{ser_num}</i>\nобязательность: <i>{req}</i>\nколличество изображений: <i>{count_img}</i>')
        await bot.send_message(callback_query.from_user.id, 'Если всё ок, нажимай кнопку "Всё 👌"', reply_markup=nav.generating)

        await FormGenerating.confirm.set()





@dp.message_handler()
async def empty_handler(message: types.Message):
    if message.text == 'test':
        info = db.get_layers(message.from_user.id, is_dict=True, with_info=True)
        for key in info:
            ser_num = info[key]['serial_num']
            req = info[key]['required']
            count_img = info[key]['count_img']
            await message.answer(f'---------------------------\n<b>{key.upper()}</b>\nпорядковый номер: <i>{ser_num}</i>\nобязательность: <i>{req}</i>\nколличество изображений: <i>{count_img}</i>')
        print('---------------------------')

    await message.answer('Я не знаю что на это ответить...')     
 

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



















