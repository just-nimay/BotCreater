from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


btnInfo = InlineKeyboardButton(text='Информация📚', callback_data='btnInfo')
btnInfoInMenu = InlineKeyboardButton(text='Информация📚', callback_data='btnInfoInMenu')
btnCreateGC = InlineKeyboardButton(text='Создать🛠', callback_data='btnCreateGC')
btnAddLayer = InlineKeyboardButton(text='Новый слой❇️', callback_data='btnAddLayer')
btnLayers = InlineKeyboardButton(text='Мои слои💎', callback_data='btnLayers')
btnMenu = InlineKeyboardButton(text='Меню☕️', callback_data='btnMenu')
btnBackInLaiers = InlineKeyboardButton(text='Назад⏪', callback_data='btnBack_inLayers')
btnGenerate = InlineKeyboardButton(text='Сгенерировать⚙️', callback_data='btnGenerate')
btnConfigureLayer = InlineKeyboardButton(text='Настроить слои🔧', callback_data='btnConfigureLayer')
btnAddImage = InlineKeyboardButton(text='Добавить изображения(-е)🖼', callback_data='btnAddImage')
btnNext = InlineKeyboardButton(text='>>', callback_data='btnNextImage')
btnBack = InlineKeyboardButton(text='<<', callback_data='btnBackImage')
btnThisImage = InlineKeyboardButton(text='это👆', callback_data='btnThisImage')

btnChangeSerNum = InlineKeyboardButton(text='Изменить порядковый номер🆔', callback_data='btnChangeSerNum')
btnChangeRequired = InlineKeyboardButton(text='Изменить обязательность🔐', callback_data='btnChangeRequired')
btnDeleteLayer = InlineKeyboardButton(text='Удалить слой🗑', callback_data='btnDeleteLayer')
btnDeleteImage = InlineKeyboardButton(text='Удалить изображения(-е)✂️', callback_data='btnDeleteImage')
btnBackInLayerConfig = InlineKeyboardButton(text='Назад⏪', callback_data='btnBackInLayerConfig')
btnBackToLayers = KeyboardButton('Назад⏪')
btnAllRight = KeyboardButton('Всё 👌')
btnNotAllRight = KeyboardButton('Ой, что-то не так🙄')


mainMenu = InlineKeyboardMarkup(row_width=2)
mainMenu.insert(btnInfo)
mainMenu.insert(btnCreateGC)


inInfo = InlineKeyboardMarkup(row_width=2)
inInfo.insert(btnCreateGC)

inInfoToMenu = InlineKeyboardMarkup(row_width=2)
inInfoToMenu.insert(btnMenu)

layerReady = InlineKeyboardMarkup(row_width=2)
layerReady.insert(btnMenu)
layerReady.insert(btnAddLayer)
layerReady.insert(btnLayers)

CreateingGC = InlineKeyboardMarkup(row_width=2)
CreateingGC.add(btnAddImage)
CreateingGC.add(btnAddLayer)
CreateingGC.insert(btnLayers)
CreateingGC.add(btnMenu)

mainMenuFull = InlineKeyboardMarkup(row_width=2)
mainMenuFull.insert(btnInfoInMenu)
mainMenuFull.insert(btnAddLayer)
mainMenuFull.row(btnLayers)
mainMenuFull.add(btnGenerate)

layers = InlineKeyboardMarkup(row_width=2)
layers.add(btnBackInLaiers)
layers.insert(btnConfigureLayer)

layerConfig = InlineKeyboardMarkup()
layerConfig.add(btnChangeSerNum)
layerConfig.add(btnChangeRequired)
layerConfig.add(btnAddImage)
layerConfig.add(btnDeleteLayer)
layerConfig.add(btnDeleteImage)
layerConfig.add(btnMenu)

gallery = InlineKeyboardMarkup(row_width=3)
gallery.insert(btnBack)
gallery.insert(btnThisImage)
gallery.insert(btnNext)
gallery.add(btnBackInLayerConfig)

generating = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
generating.add(btnAllRight)
generating.add(btnNotAllRight)

def layer_buttons(layers):
    menu_layers = ReplyKeyboardMarkup(resize_keyboard=True)
    for layer in layers:
        btn = KeyboardButton(layer)
        menu_layers.add(btn)
    menu_layers.add(btnBackToLayers)
    return menu_layers





