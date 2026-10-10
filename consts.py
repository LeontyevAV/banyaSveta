ACTION_ABOUT_MASTER_BANYA = '👩🏼🏠 О Мастере и бане'
ACTION_INLINE_ABOUT_MASTER = '👩🏼 О Мастере'
ACTION_INLINE_ABOUT_BANYA = '🏠 О Бане'
ACTION_INLINE_REVIEWS = '📝 Отзывы'
ACTION_INLINE_LEAVE_REVIEWS = 'Оставить свой отзывы'
ACTION_INLINE_ASK_QUESTION = '❓ Задать вопрос'
ACTION_INLINE_CONTACTS = '📞 Контакты, соц. сети'
ACTION_INLINE_CONTACT = '✏️ Связаться'

ACTION_INLINE_SERVICES = '📋 Услуги'
ACTION_INLINE_WARM_INSIDE = 'Программа «Тепло внутри» 4 чел'
ACTION_INLINE_HARMONY_IN_COUPLE = 'Программа «Гармония в паре» 2 чел'
ACTION_INLINE_TOTAL_CARE = 'Программа «Тотальная забота» 1 чел'
ACTION_INLINE_BANYA_ON_LITE = 'Программа «Баня на лайте» 5 чел'
ACTION_INLINE_CERTIFICATE = '💌 Подарочный сертификат'
ACTION_INLINE_SCHEDULE = '🗓️ Расписание'
ACTION_INLINE_BOOKING_RULES = '📜 Правила бронирования'
ACTION_INLINE_REGISTER = '✏️ Записаться'

ACTION_INLINE_SUBSCRIBE_CHANNEL = '✅ Подписаться на канал'
ACTION_INLINE_GOTO_CHANEL = '🚶🏼 Перейти на канал'

ACTION_INLINE_MAILING_BY_MESSAGE = 'Разослать сообщение по номеру'
ACTION_INLINE_MAILING_BY_TEXT = 'Разослать текст'
ACTION_INLINE_MOD_USERS = '👥 Список пользователей'
ACTION_INLINE_BACK = '<< Назад'

CALLBACK_MOD_MAILING_MESSAGE = 'mod:mailing:message'
CALLBACK_MOD_MAILING_TEXT = 'mod:mailing:text'
CALLBACK_MOD_USERS = 'mod:users'
CALLBACK_MOD_BACK = 'mod:back'

ACTION_SERVICES = '📋 Услуги'
ACTION_SCHEDULE = '🗓️ Расписание'
ACTION_CERTIFICATE = '💌 Подарочный сертификат'
ACTION_GET_PRESENT = '🎁 Получить подарок'
ACTION_MODERATION = '💻 Модерация'
ACTION_SUBSCRIBE_CHANNEL = '✅ Подписаться на канал "БАНЯ СВЕТА"'
ACTION_BOOKING_RULES = '📜 Правила бронирования'
ACTION_REVIEWS = '📝 Отзывы'
ACTION_ASK_QUESTION = '❓ Задать вопрос'
ACTION_CONTACTS = '📞 Контакты, соц. сети'
ACTION_GET_LOCATION = 'Моё местоположение'

HTTP_PATH_FILE_FOR_BOT = 'https://api.telegram.org/file/bot'

ERROR_CHANEL_NOT_FOUND = (
    'Канал {chanelUserName} не найден или бот в нём не администратор'
)

BOT_ADMIN_NAME = '@LeontyevAV'
BOT_MODERATOR_NAME = '@LeontyevaSvetlana'
BOT_MASTER_NAME = '@LeontyevaSvetlana'
BOT_ADMIN_ID = 123298974
BOT_MODERATOR_ID = 137048427

URL_MASTER = f'https://t.me/{BOT_MASTER_NAME.replace("@", "")}'
URL_USER_TELEGRAM = 'https://t.me/{userTelegramName}'

BOT_CONTENT_START_TEXT = f"""Приветствую вас в своем пространстве. 

Меня зовут Светлана Леонтьева ({BOT_MASTER_NAME}). Я - пар-мастер. Провожу СПА-девичники, программы для пары и индивидуальные парения в своей домашней бане в пос. Северный (г. Краснодар)."""

BOT_NOT_FOUND_ERROR = 'Бот {botUserName} не найден'
USER_TELEGRAM_FOR_BOT_NOT_FOUND_ERROR = (
    'Пользователь телеграмм с ID {userIdForTelegram} не найден'
)
