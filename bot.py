import asyncio
import html
import re
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


# ============================================================
# НАСТРОЙКИ
# ============================================================

# ВСТАВЬ СЮДА НОВЫЙ ТОКЕН БОТА
# Новый токен мне НЕ присылай.
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "Не найден BOT_TOKEN. "
        "Добавь переменную BOT_TOKEN в Railway."
    )


# ============================================================
# 4 БАРИСТА
# ============================================================
# Каждый бариста должен сначала открыть бота
# и нажать /start.
#
# Чтобы узнать ID:
# бариста пишет боту /myid
#
# Потом вставляешь 4 ID сюда.
# ============================================================

BARISTA_IDS = [
    8197518132,
    5679849857,
    6474157578,
    6336578302,
]


# ============================================================
# ОПЛАТА
# ============================================================

CARD_NUMBER = "9860 3901 0178 4366"
CARD_OWNER = "AZIZBEK MUSTANOV"


# ============================================================
# КОФЕЙНЯ
# ============================================================

COFFEE_NAME = "Profi Kofi"
COFFEE_ADDRESS = "Ташкент, улица Айбека 65/4"
COFFEE_PHONE = "+998 97 761 00 37"
COFFEE_MAP = "https://maps.app.goo.gl/MDHivFNcqvyWLmR27"

DELIVERY_INFO = "Бесплатная доставка, Пн–Пт 08:00–17:00"


# ============================================================
# МЕНЮ
# ============================================================

MENU = {

    # --------------------------------------------------------
    # КОФЕ
    # --------------------------------------------------------

    "coffee": {
        "title": "☕ Кофе",
        "items": [
            ("Эспрессо", "24/28k"),
            ("Американо", "24/28/42k"),
            ("Капучино", "29/34/52k"),
            ("Латте", "29/52k"),
            ("Тыквенный латте", "48/84k"),
            ("Флэт уайт", "34/56k"),
            ("Раф", "38/72k"),
            ("Раф с халвой", "42/84k"),
            ("Раф тыквенный", "46/84k"),
            ("Мокко с шоколадом", "38/67k"),
            ("Мокко с карамелью", "38/67k"),
        ],
    },

    # --------------------------------------------------------
    # МАТЧА
    # --------------------------------------------------------

    "matcha": {
        "title": "🍵 Матча",
        "items": [
            ("Матча на молоке", "36k"),
            ("Матча на безлактозном", "44k"),
            ("Матча тоник", "67k"),
            ("Матча бамбл", "67k"),
        ],
    },

    # --------------------------------------------------------
    # ЛИМОНАДЫ
    # --------------------------------------------------------

    "lemonades": {
        "title": "🥤 Лимонады",
        "items": [
            ("Манго маракуйя", "60k"),
            ("Тархун киви", "50k"),
            ("Мохито", "40k"),
            ("Клубника-апельсин", "50k"),
            ("Твист ред-гранат", "48k"),
            ("Твист ред-милк", "48k"),
            ("Твист грейпфрут sugar free", "48k"),
            ("Черника юдзу", "60k"),
        ],
    },

    # --------------------------------------------------------
    # ФРЕШИ
    # --------------------------------------------------------

    "juices": {
        "title": "🧃 Фреши",
        "items": [
            ("Морковный", "25/40k"),
            ("Яблочный", "37/50k"),
            ("Апельсиновый", "60/80k"),
            ("Яблоко сельдерей", "52/70k"),
            ("Яблоко морковь", "37/50k"),
            ("Фреш грейпфрут", "80k"),
        ],
    },

    # --------------------------------------------------------
    # МОЛОЧНЫЕ КОКТЕЙЛИ
    # --------------------------------------------------------

    "milkshakes": {
        "title": "🥛 Молочные коктейли",
        "items": [
            ("Матча шейк", "62k"),
            ("Йогурт клубника банан", "56k"),
            ("Йогурт банан", "62k"),
            ("Йогурт клубника манго", "62k"),
            ("Розовый кокос", "60k"),
        ],
    },

    # --------------------------------------------------------
    # ДЕТОКС
    # --------------------------------------------------------

    "detox": {
        "title": "🍹 Детокс",
        "items": [
            ("Зеленый детокс", "54k"),
            ("Ягодный детокс", "70k"),
            ("Ананас-матча", "52k"),
            ("Цитрус щавель", "52k"),
            ("Шпинат киви", "48k"),
            ("Манго авокадо", "65k"),
        ],
    },

    # --------------------------------------------------------
    # АВТОРСКИЕ ЧАИ
    # --------------------------------------------------------

    "tea": {
        "title": "🍵 Авторские чаи",
        "items": [
            ("Марокканский", "28k"),
            ("Цитрусовый", "28k"),
            ("Пуэр", "20k"),
            ("Ташкентский чай", "15k"),
            ("Имбирный", "24k"),
            ("Травяной сбор", "22k"),
            ("Облепиховый", "26k"),
            ("Бергамот", "20k"),
            ("Вишнёвый глинтвейн", "42k"),
            ("Клюква маракуйя", "28k"),
            ("Пряный манго глинтвейн", "42k"),
        ],
    },

    # --------------------------------------------------------
    # СМУЗИ
    # --------------------------------------------------------

    "smoothies": {
        "title": "🥭 Смузи",
        "items": [
            ("Манго", "70k"),
            ("Черника малина", "65k"),
            ("Юдзу лимон", "70k"),
        ],
    },

    # --------------------------------------------------------
    # ХОЛОДНЫЙ КОФЕ
    #
    # ВАЖНО:
    # первая цена = обычный размер
    # вторая цена = большой размер
    # --------------------------------------------------------

    "iced_coffee": {
        "title": "🧊 Холодный кофе",
        "items": [
            ("Айс американо", "38/45k"),
            ("Айс капучино", "42/50k"),
            ("Айс латте", "42/50k"),
            ("Айс какао", "50/70k"),
            ("Айс раф", "38/72k"),
            ("Кофе Тоник", "58/82k"),
            ("Фрапучино йогурт", "58/70k"),
            ("Бамбл апельсиновый", "56/82k"),
            ("Бамбл вишневый", "56/82k"),
            ("Бамбл грейпфрутовый", "56/82k"),
        ],
    },

    # --------------------------------------------------------
    # АЙС-ТИ
    # --------------------------------------------------------

    "iced_tea": {
        "title": "🫖 Айс-ти",
        "items": [
            ("Классический", "35k"),
            ("Малиновый", "40k"),
            ("Маракуйя", "45k"),
            ("Клубника", "40k"),
            ("Вишневый", "40k"),
        ],
    },

    # --------------------------------------------------------
    # ПЕРЕКУСЫ
    # --------------------------------------------------------

    "snacks": {
        "title": "🥐 Перекусы",
        "items": [
            ("Ватрушка", "25 000 сум"),
            ("Батончик Nattys", "30 000 сум"),
            ("Печенье COOKIES", "15 000 сум"),
        ],
    },

    # --------------------------------------------------------
    # ДОБАВКИ
    # --------------------------------------------------------

    "additions": {
        "title": "➕ Добавки",
        "items": [
            ("Сироп добавка", "7k"),
            ("Топпинг", "10k"),
            ("Молоко добавка", "5k"),
            ("Апельсин", "5k"),
            ("Пюре", "10k"),
            ("Лимон", "5k"),
            ("Имбирь", "5k"),
            ("Мёд", "10k"),
            ("Джус Баббл", "15k"),
            ("Сельдерей", "10k"),
            ("Юдзу", "10k"),
            ("5YES альтернативное молоко", "25k"),
            ("Schweppes", "10k"),
            ("Вода с/г", "5k"),
        ],
    },
}


# ============================================================
# ХРАНЕНИЕ
# ============================================================

# user_id -> корзина
carts = {}

# (user_id, category_id, index) -> выбранное количество
quantities = {}

# (user_id, category_id, index) -> выбранная цена
selected_prices = {}

# (user_id, category_id, index) -> выбранный вариант
selected_variants = {}

# user_id -> комментарий
cart_comments = {}

# order_id -> заказ
orders = {}

# user_id -> заказ, ожидающий оплату
pending_orders = {}

# Номер заказа
next_order_id = 1001


# ============================================================
# СОСТОЯНИЯ ОФОРМЛЕНИЯ
# ============================================================

class OrderForm(StatesGroup):
    comment = State()
    name = State()
    phone = State()
    delivery = State()
    address = State()


# ============================================================
# BOT
# ============================================================

bot = Bot(TOKEN)

dp = Dispatcher(
    storage=MemoryStorage()
)


# ============================================================
# АДРЕС
# ============================================================

@dp.message(F.text == "📍 АДРЕС")
async def address_button(
    message: types.Message,
):
    await message.answer(
        f"📍 <b>{COFFEE_NAME}</b>\n\n"
        f"{COFFEE_ADDRESS}\n\n"
        f"📞 {COFFEE_PHONE}\n"
        f"🗺 <a href=\"{COFFEE_MAP}\">Открыть карту</a>",
        parse_mode="HTML",
    )


# ============================================================
# ДОСТАВКА
# ============================================================

@dp.message(F.text == "🚚 ДОСТАВКА")
async def delivery_button(
    message: types.Message,
):
    await message.answer(
        "🚚 <b>Доставка</b>\n\n"
        f"{DELIVERY_INFO}\n\n"
        f"📞 {COFFEE_PHONE}",
        parse_mode="HTML",
    )



# ============================================================
# ЦЕНЫ
# ============================================================

def parse_prices(text):
    text = text.lower()
    text = text.replace("сум", "")
    text = text.replace(" ", "")

    has_k = "k" in text

    text = text.replace("k", "")

    prices = []

    for part in text.split("/"):
        digits = re.sub(
            r"\D",
            "",
            part,
        )

        if not digits:
            continue

        price = int(digits)

        if has_k:
            price *= 1000

        prices.append(price)

    return prices


def format_price(price):
    return (
        f"{price:,}"
        .replace(",", " ")
        + " сум"
    )


# ============================================================
# НАЗВАНИЕ ВАРИАНТА
# ============================================================

def variant_name(
    category_id,
    variant_index,
    total_variants,
):
    """
    Для холодного кофе:
    1 = Обычный
    2 = Большой

    Для остальных товаров с несколькими ценами
    показываем нейтральные Вариант 1/2/3.
    """

    if (
        category_id == "iced_coffee"
        and total_variants == 2
    ):
        if variant_index == 0:
            return "Обычный"

        if variant_index == 1:
            return "Большой"

    return f"Вариант {variant_index + 1}"


# ============================================================
# КОРЗИНА
# ============================================================

def get_cart(user_id):
    if user_id not in carts:
        carts[user_id] = []

    return carts[user_id]


def copy_cart(user_id):
    return [
        item.copy()
        for item in get_cart(user_id)
    ]


def find_cart_item(
    user_id,
    category_id,
    index,
    price,
):
    for item in get_cart(user_id):

        if (
            item["category_id"] == category_id
            and item["index"] == index
            and item["price"] == price
        ):
            return item

    return None


def quantity_for_variant(
    user_id,
    category_id,
    index,
    price,
):
    item = find_cart_item(
        user_id,
        category_id,
        index,
        price,
    )

    if item:
        return item["quantity"]

    return 0


def add_to_cart(
    user_id,
    category_id,
    index,
    price,
    quantity,
    variant,
):
    cart = get_cart(user_id)

    name = MENU[
        category_id
    ]["items"][index][0]

    item = find_cart_item(
        user_id,
        category_id,
        index,
        price,
    )

    if item:
        item["quantity"] += quantity
        return

    cart.append(
        {
            "category_id": category_id,
            "index": index,
            "name": name,
            "price": price,
            "quantity": quantity,
            "variant": variant,
        }
    )


def change_cart(
    user_id,
    category_id,
    index,
    price,
    delta,
):
    item = find_cart_item(
        user_id,
        category_id,
        index,
        price,
    )

    if not item:
        return

    item["quantity"] += delta

    if item["quantity"] <= 0:

        cart = get_cart(user_id)

        if item in cart:
            cart.remove(item)


def cart_total(user_id):
    total = 0

    for item in get_cart(user_id):
        total += (
            item["price"]
            * item["quantity"]
        )

    return total


def reset_cart(user_id):

    carts[user_id] = []

    for key in list(
        quantities.keys()
    ):
        if key[0] == user_id:
            quantities.pop(
                key,
                None,
            )

    for key in list(
        selected_prices.keys()
    ):
        if key[0] == user_id:
            selected_prices.pop(
                key,
                None,
            )

    for key in list(
        selected_variants.keys()
    ):
        if key[0] == user_id:
            selected_variants.pop(
                key,
                None,
            )

    cart_comments.pop(
        user_id,
        None,
    )


# ============================================================
# ГЛАВНОЕ МЕНЮ
# ============================================================

def main_keyboard():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="☕ МЕНЮ"
                ),
                KeyboardButton(
                    text="🛒 КОРЗИНА"
                ),
            ],
            [
                KeyboardButton(
                    text="📍 АДРЕС"
                ),
                KeyboardButton(
                    text="🚚 ДОСТАВКА"
                ),
            ],
        ],
        resize_keyboard=True,
    )


# ============================================================
# КАТЕГОРИИ
# ============================================================

def categories_keyboard():

    rows = []

    for category_id, category in MENU.items():

        rows.append(
            [
                InlineKeyboardButton(
                    text=category["title"],
                    callback_data=(
                        f"cat:{category_id}"
                    ),
                )
            ]
        )

    rows.append(
        [
            InlineKeyboardButton(
                text="🛒 Корзина",
                callback_data="cart",
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=rows
    )


# ============================================================
# КНОПКИ ТОВАРОВ
# ============================================================

def product_keyboard(
    user_id,
    category_id,
    opened_price=None,
):

    rows = []

    items = MENU[
        category_id
    ]["items"]

    for index, (
        name,
        price_text,
    ) in enumerate(items):

        prices = parse_prices(
            price_text
        )

        # ----------------------------------------
        # НАЗВАНИЕ
        # ----------------------------------------

        rows.append(
            [
                InlineKeyboardButton(
                    text=(
                        f"{name} — "
                        f"{price_text}"
                    ),
                    callback_data=(
                        f"p:"
                        f"{category_id}:"
                        f"{index}"
                    ),
                )
            ]
        )

        # ----------------------------------------
        # КОЛИЧЕСТВО
        # ----------------------------------------

        # Если одна цена
        if len(prices) == 1:

            current_price = prices[0]

            quantity = quantity_for_variant(
                user_id,
                category_id,
                index,
                current_price,
            )

        else:

            current_price = selected_prices.get(
                (
                    user_id,
                    category_id,
                    index,
                )
            )

            if current_price is None:
                quantity = 0
            else:
                quantity = quantity_for_variant(
                    user_id,
                    category_id,
                    index,
                    current_price,
                )

        rows.append(
            [
                InlineKeyboardButton(
                    text="➖",
                    callback_data=(
                        f"-:"
                        f"{category_id}:"
                        f"{index}"
                    ),
                ),

                InlineKeyboardButton(
                    text=str(quantity),
                    callback_data="nothing",
                ),

                InlineKeyboardButton(
                    text="➕",
                    callback_data=(
                        f"+:"
                        f"{category_id}:"
                        f"{index}"
                    ),
                ),
            ]
        )

        # ----------------------------------------
        # ВЫБОР РАЗМЕРА / ЦЕНЫ
        # ----------------------------------------

        if (
            opened_price
            and
            opened_price[0] == category_id
            and
            opened_price[1] == index
        ):

            price_buttons = []

            for variant_index, price in enumerate(
                prices
            ):

                label = variant_name(
                    category_id,
                    variant_index,
                    len(prices),
                )

                price_buttons.append(
                    InlineKeyboardButton(
                        text=(
                            f"{label} — "
                            f"{format_price(price)}"
                        ),
                        callback_data=(
                            f"v:"
                            f"{category_id}:"
                            f"{index}:"
                            f"{price}:"
                            f"{variant_index}"
                        ),
                    )
                )

            rows.append(
                price_buttons
            )

    rows.append(
        [
            InlineKeyboardButton(
                text="⬅️ Категории",
                callback_data="categories",
            ),
            InlineKeyboardButton(
                text="🛒 Корзина",
                callback_data="cart",
            ),
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=rows
    )


def category_text(category_id):

    return (
        f"<b>{MENU[category_id]['title']}</b>\n\n"
        "Выберите количество 👇"
    )


# ============================================================
# ТЕКСТ КОРЗИНЫ
# ============================================================

def cart_text(user_id):

    cart = get_cart(user_id)

    if not cart:

        return (
            "🛒 <b>ВАША КОРЗИНА ПУСТА</b>\n\n"
            "Выберите товары из меню ☕"
        )

    text = (
        "🛒 <b>ВАША КОРЗИНА</b>\n\n"
    )

    for item in cart:

        subtotal = (
            item["price"]
            * item["quantity"]
        )

        item_name = item["name"]

        if item.get("variant"):
            item_name += (
                f" ({item['variant']})"
            )

        text += (
            f"☕ {html.escape(item_name)}\n"
            f"{item['quantity']} × "
            f"{format_price(item['price'])} = "
            f"<b>{format_price(subtotal)}</b>\n\n"
        )

    comment = cart_comments.get(
        user_id,
        "",
    ).strip()

    if comment:

        text += (
            "📝 <b>Комментарий:</b>\n"
            f"{html.escape(comment)}\n\n"
        )

    else:

        text += (
            "📝 <b>Комментарий:</b> "
            "не добавлен\n\n"
        )

    text += (
        f"💰 <b>Итого: "
        f"{format_price(cart_total(user_id))}</b>"
    )

    return text


# ============================================================
# КНОПКИ КОРЗИНЫ
# ============================================================

def cart_keyboard(user_id):

    cart = get_cart(user_id)

    rows = []

    for index, item in enumerate(cart):

        rows.append(
            [
                InlineKeyboardButton(
                    text="➖",
                    callback_data=(
                        f"cm-:{index}"
                    ),
                ),

                InlineKeyboardButton(
                    text=str(
                        item["quantity"]
                    ),
                    callback_data="nothing",
                ),

                InlineKeyboardButton(
                    text="➕",
                    callback_data=(
                        f"cm+:{index}"
                    ),
                ),

                InlineKeyboardButton(
                    text="🗑",
                    callback_data=(
                        f"cd:{index}"
                    ),
                ),
            ]
        )

    if cart:

        if cart_comments.get(
            user_id,
            "",
        ).strip():

            rows.append(
                [
                    InlineKeyboardButton(
                        text="✏️ Изменить комментарий",
                        callback_data="comment:add",
                    ),
                    InlineKeyboardButton(
                        text="❌ Удалить комментарий",
                        callback_data="comment:delete",
                    ),
                ]
            )

        else:

            rows.append(
                [
                    InlineKeyboardButton(
                        text="📝 Добавить комментарий",
                        callback_data="comment:add",
                    )
                ]
            )

        rows.append(
            [
                InlineKeyboardButton(
                    text="✅ Оформить заказ",
                    callback_data="checkout",
                )
            ]
        )

        rows.append(
            [
                InlineKeyboardButton(
                    text="🗑 Очистить корзину",
                    callback_data="clearcart",
                )
            ]
        )

    rows.append(
        [
            InlineKeyboardButton(
                text="☕ Меню",
                callback_data="categories",
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=rows
    )


# ============================================================
# START
# ============================================================

@dp.message(CommandStart())
async def start(
    message: types.Message,
):

    await message.answer(
        f"☕ <b>Добро пожаловать в "
        f"{COFFEE_NAME}!</b>\n\n"
        "Выберите раздел:",
        reply_markup=main_keyboard(),
        parse_mode="HTML",
    )


# ============================================================
# MY ID
# ============================================================

@dp.message(Command("myid"))
async def myid(
    message: types.Message,
):

    await message.answer(
        "🆔 Ваш Telegram ID:\n\n"
        f"<code>{message.from_user.id}</code>",
        parse_mode="HTML",
    )


# ============================================================
# МЕНЮ
# ============================================================

@dp.message(
    F.text == "☕ МЕНЮ"
)
async def menu(
    message: types.Message,
):

    await message.answer(
        "☕ <b>Меню Profi Kofi</b>\n\n"
        "Выберите категорию:",
        reply_markup=categories_keyboard(),
        parse_mode="HTML",
    )


# ============================================================
# ОТКРЫТЬ КАТЕГОРИЮ
# ============================================================

@dp.callback_query(
    F.data.startswith("cat:")
)
async def open_category(
    callback: types.CallbackQuery,
):

    category_id = (
        callback.data
        .split(":")[1]
    )

    if category_id not in MENU:
        await callback.answer(
            "Категория не найдена.",
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        category_text(category_id),
        reply_markup=product_keyboard(
            callback.from_user.id,
            category_id,
        ),
        parse_mode="HTML",
    )

    await callback.answer()


# ============================================================
# НАЗАД К КАТЕГОРИЯМ
# ============================================================

@dp.callback_query(
    F.data == "categories"
)
async def back_categories(
    callback: types.CallbackQuery,
):

    await callback.message.edit_text(
        "☕ <b>Меню Profi Kofi</b>\n\n"
        "Выберите категорию:",
        reply_markup=categories_keyboard(),
        parse_mode="HTML",
    )

    await callback.answer()


# ============================================================
# НАЖАТИЕ НА НАЗВАНИЕ ТОВАРА
# ============================================================

@dp.callback_query(
    F.data.startswith("p:")
)
async def product_click(
    callback: types.CallbackQuery,
):

    _, category_id, index = (
        callback.data.split(":")
    )

    index = int(index)

    if category_id not in MENU:
        await callback.answer(
            "Товар не найден.",
            show_alert=True,
        )
        return

    user_id = callback.from_user.id

    prices = parse_prices(
        MENU[category_id]["items"][index][1]
    )

    # Одна цена
    if len(prices) == 1:

        selected_prices[
            (
                user_id,
                category_id,
                index,
            )
        ] = prices[0]

        await callback.answer(
            "Цена выбрана. Нажимайте ➕"
        )

        return

    # Несколько цен
    await callback.message.edit_reply_markup(
        reply_markup=product_keyboard(
            user_id,
            category_id,
            opened_price=(
                category_id,
                index,
            ),
        )
    )

    await callback.answer(
        "Выберите размер"
        if category_id == "iced_coffee"
        else "Выберите вариант"
    )


# ============================================================
# ВЫБОР ЦЕНЫ / РАЗМЕРА
# ============================================================

@dp.callback_query(
    F.data.startswith("v:")
)
async def choose_variant(
    callback: types.CallbackQuery,
):

    _, category_id, index, price, variant_index = (
        callback.data.split(":")
    )

    index = int(index)
    price = int(price)
    variant_index = int(variant_index)

    user_id = callback.from_user.id

    prices = parse_prices(
        MENU[category_id]["items"][index][1]
    )

    variant = variant_name(
        category_id,
        variant_index,
        len(prices),
    )

    selected_prices[
        (
            user_id,
            category_id,
            index,
        )
    ] = price

    selected_variants[
        (
            user_id,
            category_id,
            index,
        )
    ] = variant

    await callback.message.edit_reply_markup(
        reply_markup=product_keyboard(
            user_id,
            category_id,
        )
    )

    await callback.answer(
        f"{variant}: {format_price(price)}"
    )


# ============================================================
# PLUS
# ============================================================

@dp.callback_query(
    F.data.startswith("+:" )
)
async def product_plus(
    callback: types.CallbackQuery,
):

    _, category_id, index = (
        callback.data.split(":")
    )

    index = int(index)

    user_id = callback.from_user.id

    prices = parse_prices(
        MENU[category_id]["items"][index][1]
    )

    # Одна цена
    if len(prices) == 1:

        price = prices[0]

        variant = ""

    # Несколько цен
    else:

        price = selected_prices.get(
            (
                user_id,
                category_id,
                index,
            )
        )

        variant = selected_variants.get(
            (
                user_id,
                category_id,
                index,
            )
        )

        if price is None:

            await callback.answer(
                "Сначала выберите размер.",
                show_alert=True,
            )

            return

    add_to_cart(
        user_id,
        category_id,
        index,
        price,
        1,
        variant,
    )

    await callback.message.edit_reply_markup(
        reply_markup=product_keyboard(
            user_id,
            category_id,
        )
    )

    await callback.answer(
        "Добавлено ➕"
    )


# ============================================================
# MINUS
# ============================================================

@dp.callback_query(
    F.data.startswith("-:")
)
async def product_minus(
    callback: types.CallbackQuery,
):

    _, category_id, index = (
        callback.data.split(":")
    )

    index = int(index)

    user_id = callback.from_user.id

    prices = parse_prices(
        MENU[category_id]["items"][index][1]
    )

    if len(prices) == 1:

        price = prices[0]

    else:

        price = selected_prices.get(
            (
                user_id,
                category_id,
                index,
            )
        )

        if price is None:

            await callback.answer(
                "Сначала выберите размер.",
                show_alert=True,
            )

            return

    current = quantity_for_variant(
        user_id,
        category_id,
        index,
        price,
    )

    if current <= 0:

        await callback.answer()
        return

    change_cart(
        user_id,
        category_id,
        index,
        price,
        -1,
    )

    await callback.message.edit_reply_markup(
        reply_markup=product_keyboard(
            user_id,
            category_id,
        )
    )

    await callback.answer(
        "Убрано ➖"
    )


# ============================================================
# КОРЗИНА
# ============================================================

@dp.message(
    F.text == "🛒 КОРЗИНА"
)
async def cart_button(
    message: types.Message,
):

    user_id = message.from_user.id

    await message.answer(
        cart_text(user_id),
        reply_markup=cart_keyboard(user_id),
        parse_mode="HTML",
    )


@dp.callback_query(
    F.data == "cart"
)
async def cart_callback(
    callback: types.CallbackQuery,
):

    user_id = callback.from_user.id

    await callback.message.edit_text(
        cart_text(user_id),
        reply_markup=cart_keyboard(user_id),
        parse_mode="HTML",
    )

    await callback.answer()


# ============================================================
# PLUS В КОРЗИНЕ
# ============================================================

@dp.callback_query(
    F.data.startswith("cm+:")
)
async def cart_plus(
    callback: types.CallbackQuery,
):

    index = int(
        callback.data.split(":")[1]
    )

    user_id = callback.from_user.id

    cart = get_cart(user_id)

    if index < len(cart):

        cart[index]["quantity"] += 1

    await callback.message.edit_text(
        cart_text(user_id),
        reply_markup=cart_keyboard(user_id),
        parse_mode="HTML",
    )

    await callback.answer()


# ============================================================
# MINUS В КОРЗИНЕ
# ============================================================

@dp.callback_query(
    F.data.startswith("cm-:")
)
async def cart_minus(
    callback: types.CallbackQuery,
):

    index = int(
        callback.data.split(":")[1]
    )

    user_id = callback.from_user.id

    cart = get_cart(user_id)

    if index < len(cart):

        item = cart[index]

        item["quantity"] -= 1

        if item["quantity"] <= 0:

            cart.pop(index)

    await callback.message.edit_text(
        cart_text(user_id),
        reply_markup=cart_keyboard(user_id),
        parse_mode="HTML",
    )

    await callback.answer()


# ============================================================
# УДАЛИТЬ ИЗ КОРЗИНЫ
# ============================================================

@dp.callback_query(
    F.data.startswith("cd:")
)
async def cart_delete(
    callback: types.CallbackQuery,
):

    index = int(
        callback.data.split(":")[1]
    )

    user_id = callback.from_user.id

    cart = get_cart(user_id)

    if index < len(cart):

        cart.pop(index)

    await callback.message.edit_text(
        cart_text(user_id),
        reply_markup=cart_keyboard(user_id),
        parse_mode="HTML",
    )

    await callback.answer(
        "Удалено"
    )


# ============================================================
# ОЧИСТИТЬ КОРЗИНУ
# ============================================================

@dp.callback_query(
    F.data == "clearcart"
)
async def clear_cart(
    callback: types.CallbackQuery,
):

    user_id = callback.from_user.id

    reset_cart(user_id)

    await callback.message.edit_text(
        cart_text(user_id),
        reply_markup=cart_keyboard(user_id),
        parse_mode="HTML",
    )

    await callback.answer(
        "Корзина очищена"
    )


# ============================================================
# ДОБАВИТЬ КОММЕНТАРИЙ
# ============================================================

@dp.callback_query(
    F.data == "comment:add"
)
async def comment_add(
    callback: types.CallbackQuery,
    state: FSMContext,
):

    user_id = callback.from_user.id

    if not get_cart(user_id):

        await callback.answer(
            "Корзина пустая.",
            show_alert=True,
        )

        return

    await state.set_state(
        OrderForm.comment
    )

    await callback.message.answer(
        "📝 <b>Комментарий к заказу</b>\n\n"
        "Напишите, что нужно добавить, "
        "убрать или изменить.\n\n"
        "Например:\n"
        "• без сахара\n"
        "• меньше льда\n"
        "• без сиропа\n"
        "• добавить молока",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="➡️ Без комментария"
                    )
                ],
                [
                    KeyboardButton(
                        text="❌ Отмена"
                    )
                ],
            ],
            resize_keyboard=True,
        ),
        parse_mode="HTML",
    )

    await callback.answer()


# ============================================================
# СОХРАНИТЬ КОММЕНТАРИЙ
# ============================================================

@dp.message(
    OrderForm.comment
)
async def get_comment(
    message: types.Message,
    state: FSMContext,
):

    user_id = message.from_user.id

    if message.text == "❌ Отмена":

        await state.clear()

        await message.answer(
            cart_text(user_id),
            reply_markup=cart_keyboard(user_id),
            parse_mode="HTML",
        )

        return

    if message.text == "➡️ Без комментария":

        cart_comments[user_id] = ""

    else:

        comment = (message.text or "").strip()

        if len(comment) > 500:

            await message.answer(
                "Комментарий должен быть максимум "
                "500 символов."
            )

            return

        cart_comments[user_id] = comment

    await state.clear()

    await message.answer(
        cart_text(user_id),
        reply_markup=cart_keyboard(user_id),
        parse_mode="HTML",
    )


# ============================================================
# УДАЛИТЬ КОММЕНТАРИЙ
# ============================================================

@dp.callback_query(
    F.data == "comment:delete"
)
async def delete_comment(
    callback: types.CallbackQuery,
):

    user_id = callback.from_user.id

    cart_comments[user_id] = ""

    await callback.message.edit_text(
        cart_text(user_id),
        reply_markup=cart_keyboard(user_id),
        parse_mode="HTML",
    )

    await callback.answer(
        "Комментарий удалён"
    )


# ============================================================
# НАЧАТЬ ОФОРМЛЕНИЕ
# ============================================================

@dp.callback_query(
    F.data == "checkout"
)
async def checkout(
    callback: types.CallbackQuery,
    state: FSMContext,
):

    user_id = callback.from_user.id

    if not get_cart(user_id):

        await callback.answer(
            "Корзина пустая.",
            show_alert=True,
        )

        return

    await state.set_state(
        OrderForm.name
    )

    await callback.message.answer(
        "📝 <b>Оформление заказа</b>\n\n"
        "Как вас зовут?",
        parse_mode="HTML",
    )

    await callback.answer()


# ============================================================
# ИМЯ
# ============================================================

@dp.message(
    OrderForm.name
)
async def get_name(
    message: types.Message,
    state: FSMContext,
):

    if message.text == "❌ Отмена":

        await state.clear()

        await message.answer(
            "Оформление отменено.",
            reply_markup=main_keyboard(),
        )

        return

    name = (message.text or "").strip()

    if len(name) < 2:

        await message.answer(
            "Пожалуйста, напишите имя."
        )

        return

    await state.update_data(
        name=name
    )

    await state.set_state(
        OrderForm.phone
    )

    await message.answer(
        "📞 Напишите номер телефона:"
    )


# ============================================================
# ТЕЛЕФОН
# ============================================================

@dp.message(
    OrderForm.phone
)
async def get_phone(
    message: types.Message,
    state: FSMContext,
):

    if message.text == "❌ Отмена":

        await state.clear()

        await message.answer(
            "Оформление отменено.",
            reply_markup=main_keyboard(),
        )

        return

    phone = (message.text or "").strip()

    if len(phone) < 5:
        await message.answer(
            "Пожалуйста, напишите номер телефона."
        )
        return

    await state.update_data(
        phone=phone
    )

    await state.set_state(
        OrderForm.delivery
    )

    await message.answer(
        "Как хотите получить заказ?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="🚚 Доставка"
                    ),
                    KeyboardButton(
                        text="🏠 Самовывоз"
                    ),
                ],
                [
                    KeyboardButton(
                        text="❌ Отмена"
                    )
                ],
            ],
            resize_keyboard=True,
        ),
    )


# ============================================================
# ДОСТАВКА / САМОВЫВОЗ
# ============================================================

@dp.message(
    OrderForm.delivery
)
async def get_delivery(
    message: types.Message,
    state: FSMContext,
):

    if message.text == "❌ Отмена":

        await state.clear()

        await message.answer(
            "Оформление отменено.",
            reply_markup=main_keyboard(),
        )

        return

    if message.text == "🏠 Самовывоз":

        await state.update_data(
            delivery="Самовывоз",
            address=COFFEE_ADDRESS,
        )

        await ask_payment(
            message,
        )

        return

    if message.text == "🚚 Доставка":

        await state.update_data(
            delivery="Доставка"
        )

        await state.set_state(
            OrderForm.address
        )

        await message.answer(
            "📍 Напишите адрес доставки:"
        )

        return

    await message.answer(
        "Выберите Доставку или Самовывоз."
    )


# ============================================================
# АДРЕС
# ============================================================

@dp.message(
    OrderForm.address
)
async def get_address(
    message: types.Message,
    state: FSMContext,
):

    if message.text == "❌ Отмена":

        await state.clear()

        await message.answer(
            "Оформление отменено.",
            reply_markup=main_keyboard(),
        )

        return

    address = (message.text or "").strip()

    if len(address) < 5:

        await message.answer(
            "Пожалуйста, напишите полный адрес."
        )

        return

    await state.update_data(
        address=address
    )

    await ask_payment(
        message,
    )


# ============================================================
# СПОСОБ ОПЛАТЫ
# ============================================================

async def ask_payment(
    message,
):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💵 Наличными",
                    callback_data="pay:cash",
                )
            ],
            [
                InlineKeyboardButton(
                    text="💳 Переводом",
                    callback_data="pay:transfer",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data="pay:cancel",
                )
            ],
        ]
    )

    await message.answer(
        "💳 <b>Выберите способ оплаты</b>",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


# ============================================================
# СОЗДАНИЕ ЗАКАЗА
# ============================================================

async def create_order(
    user_id,
    state,
    payment_method,
    username,
):

    global next_order_id

    if not get_cart(user_id):
        return None

    data = await state.get_data()

    order_id = next_order_id
    next_order_id += 1

    if payment_method == "Наличными":

        status = "Ожидает принятия"

    else:

        status = "Ожидает проверки оплаты"

    return {

        "order_id": order_id,

        "user_id": user_id,

        "username": username,

        "name": data.get(
            "name",
            "",
        ),

        "phone": data.get(
            "phone",
            "",
        ),

        "delivery": data.get(
            "delivery",
            "",
        ),

        "address": data.get(
            "address",
            "",
        ),

        "comment": cart_comments.get(
            user_id,
            "",
        ),

        "payment_method": payment_method,

        "items": copy_cart(
            user_id
        ),

        "total": cart_total(
            user_id
        ),

        "status": status,

        "barista_messages": [],
    }


# ============================================================
# НАЛИЧНЫЕ
# ============================================================

@dp.callback_query(
    F.data == "pay:cash"
)
async def pay_cash(
    callback: types.CallbackQuery,
    state: FSMContext,
):

    user_id = callback.from_user.id

    order = await create_order(
        user_id,
        state,
        "Наличными",
        callback.from_user.username,
    )

    if not order:

        await callback.answer(
            "Корзина пустая.",
            show_alert=True,
        )

        return

    orders[
        order["order_id"]
    ] = order

    success, sent_count = (
        await send_cash_order_to_baristas(
            order
        )
    )

    if not success:

        await callback.message.answer(
            "⚠️ Не удалось отправить "
            "заказ баристам.\n\n"
            "Проверь BARISTA_IDS."
        )

        await callback.answer()

        return

    reset_cart(user_id)

    await state.clear()

    username = (
        f"@{callback.from_user.username}"
        if callback.from_user.username
        else "без username"
    )

    await callback.message.edit_text(
        f"✅ <b>Заказ №{order['order_id']} принят!</b>\n\n"
        f"💵 Оплата: наличными\n"
        f"💬 Telegram: {html.escape(username)}\n\n"
        f"Заказ отправлен {sent_count} бариста.",
        parse_mode="HTML",
    )

    await callback.message.answer(
        "Спасибо! ☕\n\n"
        "Мы сообщим вам статус заказа.",
        reply_markup=main_keyboard(),
    )

    await callback.answer()


# ============================================================
# ПЕРЕВОД
# ============================================================

@dp.callback_query(
    F.data == "pay:transfer"
)
async def pay_transfer(
    callback: types.CallbackQuery,
    state: FSMContext,
):

    user_id = callback.from_user.id

    order = await create_order(
        user_id,
        state,
        "Переводом",
        callback.from_user.username,
    )

    if not order:

        await callback.answer(
            "Корзина пустая.",
            show_alert=True,
        )

        return

    orders[
        order["order_id"]
    ] = order

    pending_orders[
        user_id
    ] = order

    await state.clear()

    await callback.message.edit_text(
        f"💳 <b>ОПЛАТА ЗАКАЗА "
        f"№{order['order_id']}</b>\n\n"

        f"💰 Сумма: "
        f"<b>{format_price(order['total'])}</b>\n\n"

        f"💳 <b>Номер карты:</b>\n"
        f"<code>{html.escape(CARD_NUMBER)}</code>\n\n"

        f"👤 <b>Получатель:</b>\n"
        f"{html.escape(CARD_OWNER)}\n\n"

        "После перевода отправьте "
        "<b>скриншот оплаты</b> 📸",
        parse_mode="HTML",
    )

    await callback.message.answer(
        "📸 Отправьте сюда скриншот оплаты.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="❌ Отменить заказ"
                    )
                ]
            ],
            resize_keyboard=True,
        ),
    )

    await callback.answer()


# ============================================================
# ОТМЕНА ОПЛАТЫ
# ============================================================

@dp.callback_query(
    F.data == "pay:cancel"
)
async def pay_cancel(
    callback: types.CallbackQuery,
    state: FSMContext,
):

    await state.clear()

    await callback.message.edit_text(
        "❌ Заказ отменён."
    )

    await callback.message.answer(
        "Возвращаемся в меню.",
        reply_markup=main_keyboard(),
    )

    await callback.answer()


# ============================================================
# ОТМЕНА ОЖИДАНИЯ СКРИНА
# ============================================================

@dp.message(
    F.text == "❌ Отменить заказ"
)
async def cancel_pending(
    message: types.Message,
):

    user_id = message.from_user.id

    if user_id not in pending_orders:
        return

    order = pending_orders.pop(
        user_id,
        None,
    )

    if order:
        order["status"] = "Отменён"

    await message.answer(
        "❌ Заказ отменён.",
        reply_markup=main_keyboard(),
    )


# ============================================================
# ТЕКСТ ЗАКАЗА БАРИСТУ
# ============================================================

def make_barista_text(order):

    username = order.get(
        "username"
    )

    if username:

        telegram_text = (
            f"@{html.escape(username)}"
        )

    else:

        telegram_text = (
            "без username"
        )

    text = (

        f"☕ <b>ЗАКАЗ №"
        f"{order['order_id']}</b>\n\n"

        f"👤 Клиент: "
        f"{html.escape(order['name'])}\n"

        f"📞 Телефон: "
        f"{html.escape(order['phone'])}\n"

        f"💬 Telegram: "
        f"{telegram_text}\n\n"

        f"🚚 Получение: "
        f"{html.escape(order['delivery'])}\n"

        f"📍 Адрес: "
        f"{html.escape(order['address'])}\n\n"

        f"💳 Оплата: "
        f"<b>{html.escape(order['payment_method'])}</b>\n\n"

        "🛒 <b>ЗАКАЗ:</b>\n"
    )

    for item in order["items"]:

        item_name = item["name"]

        if item.get("variant"):

            item_name += (
                f" ({item['variant']})"
            )

        subtotal = (
            item["price"]
            * item["quantity"]
        )

        text += (
            f"• {html.escape(item_name)} × "
            f"{item['quantity']} — "
            f"{format_price(subtotal)}\n"
        )

    comment = (
        order.get(
            "comment",
            "",
        )
        .strip()
    )

    if comment:

        text += (
            "\n📝 <b>КОММЕНТАРИЙ:</b>\n"
            f"{html.escape(comment)}\n"
        )

    text += (
        f"\n💰 <b>ИТОГО: "
        f"{format_price(order['total'])}</b>\n\n"

        f"⏳ <b>Статус: "
        f"{html.escape(order['status'])}</b>"
    )

    # Реквизиты показываем в заказе
    # только если выбран перевод.
    if order["payment_method"] == "Переводом":

        text += (
            "\n\n"
            f"💳 Карта: "
            f"<code>{html.escape(CARD_NUMBER)}</code>\n"
            f"👤 Получатель: "
            f"{html.escape(CARD_OWNER)}"
        )

    return text


# ============================================================
# КНОПКИ БАРИСТА
# ============================================================

def barista_keyboard(
    order_id,
    status,
):

    if status == "Ожидает проверки оплаты":

        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💳 Оплата подтверждена",
                        callback_data=(
                            f"status:paid:{order_id}"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Оплата не подтверждена",
                        callback_data=(
                            f"status:reject:{order_id}"
                        ),
                    )
                ],
            ]
        )

    if status == "Ожидает принятия":

        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="👨‍🍳 Принять заказ",
                        callback_data=(
                            f"status:accepted:{order_id}"
                        ),
                    )
                ]
            ]
        )

    if status == "Оплата подтверждена":

        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="👨‍🍳 Принять заказ",
                        callback_data=(
                            f"status:accepted:{order_id}"
                        ),
                    )
                ]
            ]
        )

    if status == "Заказ принят":

        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔥 Готовится",
                        callback_data=(
                            f"status:cooking:{order_id}"
                        ),
                    )
                ]
            ]
        )

    if status == "Готовится":

        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Готов",
                        callback_data=(
                            f"status:ready:{order_id}"
                        ),
                    )
                ]
            ]
        )

    if status == "Готов":

        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🏁 Завершить",
                        callback_data=(
                            f"status:done:{order_id}"
                        ),
                    )
                ]
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[]
    )


# ============================================================
# ID БАРИСТОВ
# ============================================================

def valid_barista_ids():

    return [
        value
        for value in BARISTA_IDS
        if isinstance(value, int)
        and value != 0
    ]


# ============================================================
# НАЛИЧНЫЕ -> 4 БАРИСТА
# ============================================================

async def send_cash_order_to_baristas(
    order,
):

    barista_ids = (
        valid_barista_ids()
    )

    if not barista_ids:

        return False, 0

    order[
        "barista_messages"
    ] = []

    text = make_barista_text(
        order
    )

    keyboard = barista_keyboard(
        order["order_id"],
        order["status"],
    )

    sent_count = 0

    for barista_id in barista_ids:

        try:

            msg = await bot.send_message(
                chat_id=barista_id,
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )

            order[
                "barista_messages"
            ].append(
                {
                    "chat_id": barista_id,
                    "message_id": msg.message_id,
                    "type": "text",
                }
            )

            sent_count += 1

        except Exception as error:

            print(
                f"Ошибка у бариста "
                f"{barista_id}: {error}"
            )

    return (
        sent_count > 0,
        sent_count,
    )


# ============================================================
# ПЕРЕВОД + СКРИН -> 4 БАРИСТА
# ============================================================

async def send_transfer_to_baristas(
    order,
    file_id,
    is_document=False,
):

    barista_ids = (
        valid_barista_ids()
    )

    if not barista_ids:

        return False, 0

    order[
        "barista_messages"
    ] = []

    caption = make_barista_text(
        order
    )

    keyboard = barista_keyboard(
        order["order_id"],
        order["status"],
    )

    sent_count = 0

    for barista_id in barista_ids:

        try:

            if is_document:

                msg = await bot.send_document(
                    chat_id=barista_id,
                    document=file_id,
                    caption=caption,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )

                msg_type = "document"

            else:

                msg = await bot.send_photo(
                    chat_id=barista_id,
                    photo=file_id,
                    caption=caption,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )

                msg_type = "photo"

            order[
                "barista_messages"
            ].append(
                {
                    "chat_id": barista_id,
                    "message_id": msg.message_id,
                    "type": msg_type,
                }
            )

            sent_count += 1

        except Exception as error:

            print(
                f"Ошибка у бариста "
                f"{barista_id}: {error}"
            )

    return (
        sent_count > 0,
        sent_count,
    )


# ============================================================
# СКРИНШОТ ОПЛАТЫ
#
# FSM здесь специально НЕ используется.
# Поэтому после отказа оплаты можно снова
# отправить новый скрин.
# ============================================================

@dp.message(F.photo)
async def payment_photo(
    message: types.Message,
):

    user_id = (
        message.from_user.id
    )

    order = pending_orders.get(
        user_id
    )

    if not order:

        return

    order["username"] = (
        message.from_user.username
    )

    order["status"] = (
        "Ожидает проверки оплаты"
    )

    orders[
        order["order_id"]
    ] = order

    success, sent_count = (
        await send_transfer_to_baristas(
            order,
            message.photo[-1].file_id,
            False,
        )
    )

    if not success:

        await message.answer(
            "⚠️ Не удалось отправить "
            "скриншот баристам.\n\n"
            "Проверь BARISTA_IDS."
        )

        return

    reset_cart(
        user_id
    )

    pending_orders.pop(
        user_id,
        None,
    )

    await message.answer(
        f"✅ <b>Скриншот получен!</b>\n\n"
        f"Заказ №{order['order_id']} "
        f"отправлен {sent_count} бариста.\n\n"
        "Ожидайте проверки оплаты.",
        reply_markup=main_keyboard(),
        parse_mode="HTML",
    )


# ============================================================
# СКРИНШОТ ФАЙЛОМ
# ============================================================

@dp.message(F.document)
async def payment_document(
    message: types.Message,
):

    user_id = (
        message.from_user.id
    )

    order = pending_orders.get(
        user_id
    )

    if not order:

        return

    order["username"] = (
        message.from_user.username
    )

    order["status"] = (
        "Ожидает проверки оплаты"
    )

    orders[
        order["order_id"]
    ] = order

    success, sent_count = (
        await send_transfer_to_baristas(
            order,
            message.document.file_id,
            True,
        )
    )

    if not success:

        await message.answer(
            "⚠️ Не удалось отправить "
            "скриншот баристам."
        )

        return

    reset_cart(
        user_id
    )

    pending_orders.pop(
        user_id,
        None,
    )

    await message.answer(
        f"✅ <b>Скриншот получен!</b>\n\n"
        f"Заказ №{order['order_id']} "
        f"отправлен {sent_count} бариста.",
        reply_markup=main_keyboard(),
        parse_mode="HTML",
    )


# ============================================================
# СТАТУСЫ
# ============================================================

STATUS_NAMES = {

    "paid":
        "Оплата подтверждена",

    "accepted":
        "Заказ принят",

    "cooking":
        "Готовится",

    "ready":
        "Готов",

    "done":
        "Завершён",
}


CLIENT_MESSAGES = {

    "paid":
        "💳 Оплата подтверждена!\n\n"
        "Ваш заказ передан в работу.",

    "accepted":
        "👨‍🍳 Бариста принял ваш заказ.",

    "cooking":
        "🔥 Ваш заказ готовится!",

    "ready":
        "✅ Ваш заказ готов!",

    "done":
        "🏁 Заказ завершён.\n\n"
        "Спасибо, что выбрали Profi Kofi ☕",
}


ALLOWED_ACTIONS = {

    "Ожидает проверки оплаты": [
        "paid",
        "reject",
    ],

    "Ожидает принятия": [
        "accepted",
    ],

    "Оплата подтверждена": [
        "accepted",
    ],

    "Заказ принят": [
        "cooking",
    ],

    "Готовится": [
        "ready",
    ],

    "Готов": [
        "done",
    ],

    "Оплата не подтверждена": [],

    "Завершён": [],
}


# ============================================================
# ОБНОВИТЬ ВСЕ СООБЩЕНИЯ БАРИСТОВ
# ============================================================

async def update_barista_messages(
    order,
):

    text = make_barista_text(
        order
    )

    keyboard = barista_keyboard(
        order["order_id"],
        order["status"],
    )

    for info in order.get(
        "barista_messages",
        [],
    ):

        try:

            if info["type"] == "text":

                await bot.edit_message_text(
                    chat_id=info["chat_id"],
                    message_id=info["message_id"],
                    text=text,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )

            else:

                await bot.edit_message_caption(
                    chat_id=info["chat_id"],
                    message_id=info["message_id"],
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )

        except Exception as error:

            print(
                f"Ошибка обновления "
                f"{info['chat_id']}: {error}"
            )


# ============================================================
# СТАТУСЫ БАРИСТА
# ============================================================

@dp.callback_query(
    F.data.startswith("status:")
)
async def change_status(
    callback: types.CallbackQuery,
):

    # Только 4 бариста
    if callback.from_user.id not in (
        valid_barista_ids()
    ):

        await callback.answer(
            "У вас нет доступа.",
            show_alert=True,
        )

        return

    _, action, order_id_text = (
        callback.data.split(":")
    )

    order_id = int(
        order_id_text
    )

    order = orders.get(
        order_id
    )

    if not order:

        await callback.answer(
            "Заказ не найден.",
            show_alert=True,
        )

        return

    current_status = order[
        "status"
    ]

    # Не даём нажимать старые кнопки
    if action not in (
        ALLOWED_ACTIONS.get(
            current_status,
            [],
        )
    ):

        await callback.answer(
            "Этот статус уже обработан.",
            show_alert=True,
        )

        return

    # ========================================================
    # ОПЛАТА НЕ ПОДТВЕРЖДЕНА
    # ========================================================

    if action == "reject":

        order[
            "status"
        ] = "Оплата не подтверждена"

        await update_barista_messages(
            order
        )

        # Старые сообщения закрыты.
        # Новый скрин = новые сообщения.
        order[
            "barista_messages"
        ] = []

        orders[
            order_id
        ] = order

        # Снова ждём новый скрин
        pending_orders[
            order["user_id"]
        ] = order

        try:

            await bot.send_message(
                order["user_id"],

                f"❌ <b>Оплата по заказу "
                f"№{order_id} не подтверждена.</b>\n\n"

                "Проверьте перевод и "
                "отправьте новый скриншот.\n\n"

                f"💰 Сумма: "
                f"<b>{format_price(order['total'])}</b>\n\n"

                f"💳 Карта:\n"
                f"<code>{html.escape(CARD_NUMBER)}</code>\n\n"

                f"👤 Получатель:\n"
                f"<b>{html.escape(CARD_OWNER)}</b>",

                parse_mode="HTML",
            )

        except Exception as error:

            print(
                "Ошибка сообщения клиенту:",
                error,
            )

        await callback.answer(
            "Клиент может отправить новый скриншот."
        )

        return

    # ========================================================
    # ОБЫЧНЫЙ СТАТУС
    # ========================================================

    new_status = STATUS_NAMES[
        action
    ]

    order[
        "status"
    ] = new_status

    order[
        "last_barista_id"
    ] = callback.from_user.id

    try:

        await bot.send_message(
            order["user_id"],

            f"☕ <b>Заказ №{order_id}</b>\n\n"
            f"{CLIENT_MESSAGES[action]}",

            parse_mode="HTML",
        )

    except Exception as error:

        print(
            "Ошибка уведомления клиента:",
            error,
        )

    # Обновляем всех четырёх бариста
    await update_barista_messages(
        order
    )

    await callback.answer(
        f"Статус: {new_status}"
    )


# ============================================================
# НЕАКТИВНАЯ КНОПКА
# ============================================================

@dp.callback_query(
    F.data == "nothing"
)
async def nothing(
    callback: types.CallbackQuery,
):

    await callback.answer()


# ============================================================
# ЗАПУСК
# ============================================================

async def main():

    print()
    print(
        "======================================"
    )
    print(
        "☕ PROFI KOFI BOT"
    )
    print(
        "✅ БОТ ЗАПУЩЕН"
    )
    print(
        "======================================"
    )
    print()

    # Удаляем старый webhook перед запуском polling.
    # Иначе Telegram отвечает: can't use getUpdates while webhook is active.
    await bot.delete_webhook(
        drop_pending_updates=True
    )

    await dp.start_polling(
        bot
    )


if __name__ == "__main__":
    asyncio.run(main())
