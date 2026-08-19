import asyncio
import os
import sqlite3

from aiohttp import web  # <--- শুধু এই নতুন লাইনটা এখানে বসিয়ে দিন

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)


# =========================================================
# BOT SETUP
# =========================================================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN পাওয়া যায়নি")
    exit()

bot = Bot(
    BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()

print("Bot setup complete")


# =========================================================
# FSM STATES
# =========================================================

class MenuState(StatesGroup):
    CLASS = State()
    PLATFORM = State()
    ACS = State()
    UDVASH = State()
    SSC27 = State()
    SSC28 = State()
    COLLEGE_ADM = State()
    HSC28_PLATFORM = State()
    HSC28_SUB_PLATFORM = State()

# =========================================================
# DATABASE
# =========================================================

DB_NAME = "bot.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            username TEXT,
            points INTEGER DEFAULT 0,
            referrals INTEGER DEFAULT 0,
            referred_by INTEGER
        )
    """)

    conn.commit()
    conn.close()


create_database()


# =========================================================
# REQUIRED CHANNELS
# =========================================================

CHANNELS = [
    "@TGCoursesOfficial",
    "@TGCoursesPaid"
]


# =========================================================
# ADMIN
# =========================================================

ADMIN_ID = 8629243439

# =========================================================
# COURSE POINTS
# =========================================================

# =========================================================
# COURSE POINTS
# =========================================================

COURSE_POINTS = {
    # HSC-27
    "🧬 ACS Physics": 5, "🧪 ACS Chemistry": 5, "📐 ACS Math": 5,
    "🔬 ACS Biology": 5, "📖 ACS English": 3, "📖 ACS Bangla": 3,
    "💻 ACS ICT": 3, "🔥 ACS Full Combo": 15,
    "🎓 Udvash 1st Year Prime Batch": 10, "📚 Udvash English-Bangla": 5, "💻 Udvash ICT": 5,
    
    # HSC-28
    "🔬 HSC-28 ACS Physics": 5, "🧪 HSC-28 ACS Chemistry": 5, "📐 HSC-28 ACS Math": 5,
    "🧬 HSC-28 ACS Biology": 5, "📖 HSC-28 ACS EBI": 5, "🔥 HSC-28 ACS Combo": 20,
    "🔬 HSC-28 Udvash Physics": 5, "🧪 HSC-28 Udvash Chemistry": 5, "📐 HSC-28 Udvash Math": 5,
    "🧬 HSC-28 Udvash Biology": 5, "📖 HSC-28 Udvash EBI": 5, "🔥 HSC-28 Udvash Combo": 20,
    "🔬 HSC-28 RM Physics": 5, "🧪 HSC-28 RM Chemistry": 5, "📐 HSC-28 RM Math": 5,
    "🧬 HSC-28 RM Biology": 5, "📖 HSC-28 RM EBI": 5, "🔥 HSC-28 RM Combo": 20,
    "📚 HSC-28 FT PCMB": 5, "📖 HSC-28 FT EBI 4.0": 5,
    "🧬 HSC-28 Biology Haters": 5, "📖 HSC-28 Banglabaz 8.0": 5,
    
    # SSC-27
    "📘 RM B2P 3.0": 5, "📘 RM FRPB 27": 5, "🔰 ACS FRB": 5,
    "💡 FT Academic": 5, "💡 FT FRC": 5, "🔥 RM FRPB 27 + B2P 3.0": 10,

    # SSC-28
    "📘 RM SSC-28 B2P 3.0": 5,

    # College Admission (Free)
    "🆓 FT College Admission": 0,
    "🆓 Udvash College Admission": 0,
    "🆓 Momit College Admission": 0
}

# =========================================================
# COURSE GROUP IDs
# =========================================================

COURSE_CHAT_IDS = {
    # HSC-27
    "🧬 ACS Physics": -1004417399917, "🧪 ACS Chemistry": -1004432616301, "📐 ACS Math": -1003754195447,
    "🔬 ACS Biology": -1003902592947, "📖 ACS English": -1003809262369, "📖 ACS Bangla": -1004408437595,
    "💻 ACS ICT": -1003889984967, "🎓 Udvash 1st Year Prime Batch": -1004325357898,
    "📚 Udvash English-Bangla": -1003912205576, "💻 Udvash ICT": -1004307468812,

    # HSC-28
    "🔬 HSC-28 ACS Physics": -1004379805642, "🧪 HSC-28 ACS Chemistry": -1004384787466,
    "📐 HSC-28 ACS Math": -1004377477480, "🧬 HSC-28 ACS Biology": -1004442866830, "📖 HSC-28 ACS EBI": -1004364249237,
    "🔬 HSC-28 Udvash Physics": -1004430305863, "🧪 HSC-28 Udvash Chemistry": -1003978547160,
    "📐 HSC-28 Udvash Math": -1003940475910, "🧬 HSC-28 Udvash Biology": -1003947339208, "📖 HSC-28 Udvash EBI": -1003749761957,
    "🔬 HSC-28 RM Physics": -1003949266673, "🧪 HSC-28 RM Chemistry": -1004292838640,
    "📐 HSC-28 RM Math": -1003578406989, "🧬 HSC-28 RM Biology": -1004460124967, "📖 HSC-28 RM EBI": -1004347215700,
    "📚 HSC-28 FT PCMB": -1004320388177, "📖 HSC-28 FT EBI 4.0": -1004409001270,
    "🧬 HSC-28 Biology Haters": -1004431839453, "📖 HSC-28 Banglabaz 8.0": -1004441373692,
    
    # SSC-27
    "📘 RM B2P 3.0": -1004433054061, "📘 RM FRPB 27": -1004402125191, "🔰 ACS FRB": -1003551363988,
    "💡 FT Academic": -1004471423035, "💡 FT FRC": -1004317549708,

    # SSC-28
    "📘 RM SSC-28 B2P 3.0": -1004411083808,

    # College Admission
    "🆓 FT College Admission": -1003917862107,
    "🆓 Udvash College Admission": -1004273492074,
    "🆓 Momit College Admission": -1004291611293
}

# =========================================================
# CALLBACK TO COURSE
# =========================================================

CALLBACK_TO_COURSE = {
    # HSC-27
    "buy_acs_physics": "🧬 ACS Physics", "buy_acs_chemistry": "🧪 ACS Chemistry", "buy_acs_math": "📐 ACS Math",
    "buy_acs_biology": "🔬 ACS Biology", "buy_acs_english": "📖 ACS English", "buy_acs_bangla": "📖 ACS Bangla",
    "buy_acs_ict": "💻 ACS ICT", "buy_acs_combo": "🔥 ACS Full Combo", "buy_udvash_prime": "🎓 Udvash 1st Year Prime Batch",
    "buy_udvash_english_bangla": "📚 Udvash English-Bangla", "buy_udvash_ict": "💻 Udvash ICT",

    # HSC-28
    "buy_h28_acs_phy": "🔬 HSC-28 ACS Physics", "buy_h28_acs_chem": "🧪 HSC-28 ACS Chemistry", 
    "buy_h28_acs_math": "📐 HSC-28 ACS Math", "buy_h28_acs_bio": "🧬 HSC-28 ACS Biology", 
    "buy_h28_acs_ebi": "📖 HSC-28 ACS EBI", "buy_h28_acs_combo": "🔥 HSC-28 ACS Combo",
    
    "buy_h28_ud_phy": "🔬 HSC-28 Udvash Physics", "buy_h28_ud_chem": "🧪 HSC-28 Udvash Chemistry", 
    "buy_h28_ud_math": "📐 HSC-28 Udvash Math", "buy_h28_ud_bio": "🧬 HSC-28 Udvash Biology", 
    "buy_h28_ud_ebi": "📖 HSC-28 Udvash EBI", "buy_h28_ud_combo": "🔥 HSC-28 Udvash Combo",
    
    "buy_h28_rm_phy": "🔬 HSC-28 RM Physics", "buy_h28_rm_chem": "🧪 HSC-28 RM Chemistry", 
    "buy_h28_rm_math": "📐 HSC-28 RM Math", "buy_h28_rm_bio": "🧬 HSC-28 RM Biology", 
    "buy_h28_rm_ebi": "📖 HSC-28 RM EBI", "buy_h28_rm_combo": "🔥 HSC-28 RM Combo",
    
    "buy_h28_ft_pcmb": "📚 HSC-28 FT PCMB", "buy_h28_ft_ebi": "📖 HSC-28 FT EBI 4.0",
    "buy_h28_bio_haters": "🧬 HSC-28 Biology Haters", "buy_h28_banglabaz": "📖 HSC-28 Banglabaz 8.0",

    # SSC-27
    "buy_s27_rm_b2p": "📘 RM B2P 3.0",
    "buy_s27_rm_frpb": "📘 RM FRPB 27",
    "buy_s27_acs_frb": "🔰 ACS FRB",
    "buy_s27_ft_acad": "💡 FT Academic",
    "buy_s27_ft_frc": "💡 FT FRC",
    "buy_s27_rm_combo": "🔥 RM FRPB 27 + B2P 3.0",

    # SSC-28
    "buy_s28_rm_b2p": "📘 RM SSC-28 B2P 3.0",

    # College Admission
    "get_ca_ft": "🆓 FT College Admission",
    "get_ca_udvash": "🆓 Udvash College Admission",
    "get_ca_momit": "🆓 Momit College Admission"
}

# =========================================================
# COMBO LISTS
# =========================================================

ACS_COMBO_COURSES = [
    "🧬 ACS Physics", "🧪 ACS Chemistry", "📐 ACS Math",
    "🔬 ACS Biology", "📖 ACS English", "📖 ACS Bangla", "💻 ACS ICT"
]
HSC28_ACS_COMBO = [
    "🔬 HSC-28 ACS Physics", "🧪 HSC-28 ACS Chemistry", "📐 HSC-28 ACS Math", "🧬 HSC-28 ACS Biology", "📖 HSC-28 ACS EBI"
]
HSC28_UDVASH_COMBO = [
    "🔬 HSC-28 Udvash Physics", "🧪 HSC-28 Udvash Chemistry", "📐 HSC-28 Udvash Math", "🧬 HSC-28 Udvash Biology", "📖 HSC-28 Udvash EBI"
]
HSC28_RM_COMBO = [
    "🔬 HSC-28 RM Physics", "🧪 HSC-28 RM Chemistry", "📐 HSC-28 RM Math", "🧬 HSC-28 RM Biology", "📖 HSC-28 RM EBI 2.0"
]
SSC27_RM_COMBO = [
    "📘 RM B2P 3.0", "📘 RM FRPB 27"
]

# =========================================================
# JOIN KEYBOARD
# =========================================================

def join_keyboard():

    buttons = [

        [
            InlineKeyboardButton(
                text="📚 TG Courses Official",
                url="https://t.me/TGCoursesOfficial"
            )
        ],

        [
            InlineKeyboardButton(
                text="🔐 TG Courses Paid",
                url="https://t.me/TGCoursesPaid"
            )
        ],

        [
            InlineKeyboardButton(
                text="✅ Check",
                callback_data="check_join"
            )
        ]

    ]

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


# =========================================================
# MAIN MENU
# =========================================================

def main_menu():

    buttons = [

        [
            KeyboardButton(text="👤 Profile"),
            KeyboardButton(text="⚡ Referral")
        ],

        [
            KeyboardButton(text="📚 Redeem Courses"),
            KeyboardButton(text="🏆 Leaderboard")
        ],

        [
            KeyboardButton(text="কোর্স কিভাবে নিবে 🛠️")
        ]

    ]

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )


# =========================================================
# CLASS MENU
# =========================================================

def class_menu():

    buttons = [

        [
            KeyboardButton(text="🎓 HSC-27"),
            KeyboardButton(text="🎓 HSC-28")
        ],

        [
            KeyboardButton(text="🎓 SSC-27"),
            KeyboardButton(text="🎓 SSC-28")
        ],

        [
            # এখানে নামটা ঠিক করে দেওয়া হয়েছে
            KeyboardButton(
                text="🎓 College Admission Course" 
            )
        ],

        [
            KeyboardButton(text="⬅️ Back"),
            KeyboardButton(text="🔝 Main Menu")
        ]

    ]

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )

# =========================================================
# HSC-27 PLATFORM MENU
# =========================================================

def hsc27_platform_menu():

    buttons = [

        [
            KeyboardButton(text="🔰 ACS"),
            KeyboardButton(text="🎓 Udvash")
        ],

        [
            KeyboardButton(text="⬅️ Back"),
            KeyboardButton(text="🔝 Main Menu")
        ]

    ]

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )


# =========================================================
# START
# =========================================================

@dp.message(F.text.startswith("/start"))
async def start_command(message):

    user_id = message.from_user.id
    name = message.from_user.full_name
    username = message.from_user.username

    args = message.text.split()

    referred_by = None

    if len(args) > 1:

        try:
            referred_by = int(args[1])
        except ValueError:
            referred_by = None

    if referred_by == user_id:
        referred_by = None

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:

        cursor.execute(
            """
            INSERT INTO users
            (
                user_id,
                name,
                username,
                referred_by
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                name,
                username,
                referred_by
            )
        )

        if referred_by:

            cursor.execute(
                """
                UPDATE users
                SET
                    referrals = referrals + 1,
                    points = points + 1
                WHERE user_id=?
                """,
                (referred_by,)
            )

    else:

        cursor.execute(
            """
            UPDATE users
            SET
                name=?,
                username=?
            WHERE user_id=?
            """,
            (
                name,
                username,
                user_id
            )
        )

    conn.commit()
    conn.close()

    await message.answer(

        "👋 <b>Welcome to TG COURSES!</b>\n\n"

        "🎁 <b>Free Premium Courses</b>\n\n"

        "রেফার করে আমাদের Premium Course গুলো "
        "ফ্রিতে পেতে পারো! 🎓🔥\n\n"

        "📢 প্রথমে আমাদের দুইটি চ্যানেলে Join করো।\n\n"

        "তারপর নিচের <b>✅ Check</b> বাটনে ক্লিক করো।",

        reply_markup=join_keyboard()
    )


# =========================================================
# CHECK JOIN
# =========================================================

@dp.callback_query(F.data == "check_join")
async def check_join(callback):

    user_id = callback.from_user.id

    not_joined = []

    for channel in CHANNELS:

        try:

            member = await bot.get_chat_member(
                chat_id=channel,
                user_id=user_id
            )

            if member.status in ["left", "kicked"]:
                not_joined.append(channel)

        except Exception as e:

            print(
                f"Check Join Error {channel}:",
                e
            )

            not_joined.append(channel)

    if not not_joined:

        await callback.message.answer(

            "✅ <b>Verification Successful!</b>\n\n"

            "🎉 Welcome to TG COURSES!\n\n"

            "আপনি এখন বটটি ব্যবহার করতে পারবেন।\n\n"

            "🚀 এখন থেকে আপনি:\n"
            "• Referral করতে পারবেন\n"
            "• Points earn করতে পারবেন\n"
            "• Course options দেখতে পারবেন",

            reply_markup=main_menu()
        )

    else:

        await callback.message.answer(

            "❌ <b>Access Denied!</b>\n\n"

            "বটটি ব্যবহার করতে হলে আপনাকে অবশ্যই "
            "আমাদের সব চ্যানেলে Join থাকতে হবে।\n\n"

            "👇 আগে Join করুন এবং আবার Check করুন।",

            reply_markup=join_keyboard()
        )

    await callback.answer()


# =========================================================
# PROFILE
# =========================================================

@dp.message(F.text == "👤 Profile")
async def profile_command(message):

    user_id = message.from_user.id
    name = message.from_user.full_name

    username = message.from_user.username

    if username:
        username = "@" + username
    else:
        username = "Not set"

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT points FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    points = user[0] if user else 0

    await message.answer(

        f"🙍‍♂️ <b>Your Name:</b> {name}\n"
        f"🔥 <b>Username:</b> {username}\n"
        f"🚀 <b>User ID:</b> <code>{user_id}</code>\n"
        f"💰 <b>Balance:</b> {points} Point\n\n"

        "বন্ধুদের আপনার Refer Link দিয়ে Invite করুন "
        "এবং ফ্রিতে Premium Course জিতে নাও! 😊✅"
    )


# =========================================================
# REFERRAL
# =========================================================

@dp.message(F.text == "⚡ Referral")
async def referral_command(message):

    user_id = message.from_user.id

    referral_link = (
        f"https://t.me/TGCoursesRefer_bot?start={user_id}"
    )

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT referrals FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    referrals = user[0] if user else 0

    await message.answer(

        f"💁‍♂️ <b>Your Total Referrals:</b> "
        f"{referrals} টি\n\n"

        f"📎 <b>Your Referral Link:</b>\n"
        f"{referral_link}\n\n"

        "🎁 প্রতি রেফারে <b>1 Point</b> Add হবে! ✅"
    )


# =========================================================
# REDEEM COURSES
# =========================================================

@dp.message(F.text == "📚 Redeem Courses")
async def redeem_courses(message, state: FSMContext):

    await state.set_state(MenuState.CLASS)

    photo = (
        "AgACAgUAAxkBAAIUV2qBwlb1yodVyjkdkzpGyZMfebJ4"
        "AAJiE2sb9VsRVN6uv6EUZeS3AQADAgADeQADPQQ"
    )

    await message.answer_photo(

        photo=photo,

        caption=(
            "📚 আপনি যে ক্লাসের কোর্স নিতে চান,\n"
            "সেটি সিলেক্ট করুন 👇"
        ),

        reply_markup=class_menu()
    )


# =========================================================
# HSC-27
# =========================================================

@dp.message(F.text == "🎓 HSC-27")
async def hsc27_command(message, state: FSMContext):

    await state.set_state(MenuState.PLATFORM)

    photo = (
        "AgACAgUAAxkBAAIUVWqBwk2om5Q7FDV_8ziqbutItiX5"
        "AAJhE2sb9VsRVIdaOFFA0fJvAQADAgADeQADPQQ"
    )

    await message.answer_photo(

        photo=photo,

        caption=(
            "🎓 <b>HSC-27</b>\n\n"
            "আপনি যে প্ল্যাটফর্মের কোর্স নিতে চান, "
            "সেটি সিলেক্ট করুন 📚👇"
        ),

        reply_markup=hsc27_platform_menu()
    )


# =========================================================
# ACS MENU
# =========================================================

@dp.message(F.text == "🔰 ACS")
async def acs_menu(message, state: FSMContext):

    await state.set_state(MenuState.ACS)

    photo = (
        "AgACAgUAAxkBAAIUU2qBwfF2AAFgSUfJ6Z7mTzVjPa8-3w"
        "ACYBNrG_VbEVQxy2tQDj5SRgEAAwIAA3gAAz0E"
    )

    buttons = [

        [
            KeyboardButton(text="🧬 ACS Physics"),
            KeyboardButton(text="🧪 ACS Chemistry")
        ],

        [
            KeyboardButton(text="📐 ACS Math"),
            KeyboardButton(text="🔬 ACS Biology")
        ],

        [
            KeyboardButton(text="📖 ACS English"),
            KeyboardButton(text="📖 ACS Bangla"),
            KeyboardButton(text="💻 ACS ICT")
        ],

        [
            KeyboardButton(text="🔥 ACS Full Combo")
        ],

        [
            KeyboardButton(text="⬅️ Back"),
            KeyboardButton(text="🔝 Main Menu")
        ]

    ]

    await message.answer_photo(

        photo=photo,

        caption="🔰 <b>ACS Course List 👇</b>",

        reply_markup=ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True
        )
    )


# =========================================================
# UDVASH MENU
# =========================================================

@dp.message(F.text == "🎓 Udvash")
async def udvash_menu(message, state: FSMContext):

    await state.set_state(MenuState.UDVASH)

    photo = (
        "AgACAgUAAxkBAAIUT2qBwap8XciI6bgKUtBKTr1tZxXV"
        "AAJdE2sb9VsRVPDLDkWrPRrHAQADAgADeAADPQQ"
    )

    buttons = [

        [
            KeyboardButton(
                text="🎓 Udvash 1st Year Prime Batch"
            )
        ],

        [
            KeyboardButton(text="📚 Udvash English-Bangla"),
            KeyboardButton(text="💻 Udvash ICT")
        ],

        [
            KeyboardButton(text="⬅️ Back"),
            KeyboardButton(text="🔝 Main Menu")
        ]

    ]

    await message.answer_photo(

        photo=photo,

        caption="🎓 <b>Udvash Course List 👇</b>",

        reply_markup=ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True
        )
    )

# =========================================================
# ACS PHYSICS
# =========================================================

@dp.message(F.text == "🧬 ACS Physics")
async def acs_physics(message):

    photo = (
        "AgACAgUAAxkBAAIWemqCOShig8iLcFcI2rpC2I85dpkH"
        "AALXEWsb9VsZVCQQ4WTwl6BQAQADAgADbQADPQQ"
    )

    await message.answer_photo(

        photo=photo,

        caption=(
            "📘 🔥 <b>HSC-27 ACS PHYSICS</b> 🔥\n"
            "1st & 2nd All Cycle\n\n"

            "👨‍🏫 <b>ইন্সট্রাক্টর:</b>\n"
            "💠 অপূর্ব ভাই\n"
            "💠 মাশরুর ভাই\n\n"

            "⚪️ <b>PHYSICS CYCLE 01</b>\n"
            "• ভৌতজগৎ ও পরিমাপ\n"
            "• ভেক্টর\n"
            "• গতিবিদ্যা\n\n"

            "⚪️ <b>PHYSICS CYCLE 02</b>\n"
            "• নিউটনিয়ান বলবিদ্যা\n"
            "• কাজ, ক্ষমতা ও শক্তি\n"
            "• মহাকর্ষ ও অভিকর্ষ\n\n"

            "⚪️ <b>PHYSICS CYCLE 03</b>\n"
            "• পর্যাবৃত্ত গতি\n"
            "• তরঙ্গ\n"
            "• জ্যামিতিক আলোকবিজ্ঞান\n\n"

            "⚪️ <b>PHYSICS CYCLE 04</b>\n"
            "• আদর্শ গ্যাস গতিতত্ত্ব\n"
            "• তাপগতিবিদ্যা\n"
            "• পরমাণুর মডেল\n\n"

            "⚪️ <b>PHYSICS CYCLE 05</b>\n"
            "• স্থির তড়িৎ\n"
            "• চল তড়িৎ\n"
            "• সেমিকন্ডাক্টর ও ইলেকট্রনিক্স\n\n"

            "⚪️ <b>PHYSICS CYCLE 06</b>\n"
            "• তড়িৎ প্রবাহের ক্রিয়া\n"
            "• তড়িৎ চুম্বক আবেশ\n"
            "• আধুনিক পদার্থবিজ্ঞান\n\n"

            "🎁 <b>কোর্সের সাথে পাবেন:</b>\n"
            "📍 টপিকভিত্তিক ক্লাস\n"
            "📍 Lecture Sheet\n"
            "📍 PDF Materials\n"
            "📍 Practice Sheet\n"
            "📍 Doubt Solve Class\n"
            "📍 Lifetime Access\n\n"

            "💰 <b>মূল্য: 5 Points</b>"
        ),

        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Buy Course — 5 Points",
                        callback_data="buy_acs_physics"
                    )
                ]
            ]
        )
    )


# =========================================================
# ACS CHEMISTRY
# =========================================================

@dp.message(F.text == "🧪 ACS Chemistry")
async def acs_chemistry(message):

    photo = (
        "AgACAgUAAxkBAAIWfGqCOT5pe4_YWRjw8F6p55heuQ6"
        "AAALYEWsb9VsZVIQOZ2cp4bUdAQADAgADeAADPQQ"
    )

    await message.answer_photo(

        photo=photo,

        caption=(
            "📘 🔥 <b>HSC-27 ACS HEMEL CHEMISTRY ALL CYCLE (1-5)</b> 🔥\n\n"

            "📋 <b>HSC 2027 ACS HEMEL CHEMISTRY ALL CYCLE</b>\n\n"

            "📖 <b>ইন্সট্রাক্টর:</b> 👉🏻 হিমেল ভাইয়া\n\n"

            "⚪️ <b>কেমিস্ট্রি সাইকেল ০১</b>\n"
            "• ল্যাবরেটরী নিরাপদ ব্যবহার\n"
            "• গুণগত রসায়ন\n\n"

            "⚪️ <b>কেমিস্ট্রি সাইকেল ০২</b>\n"
            "• মৌলের পর্যায়বৃত্ত ধর্ম\n"
            "• কর্মমুখী রসায়ন\n\n"

            "⚪️ <b>কেমিস্ট্রি সাইকেল ০৩</b>\n"
            "• পরিবেশ রসায়ন\n"
            "• রাসায়নিক পরিবর্তন\n\n"

            "⚪️ <b>কেমিস্ট্রি সাইকেল ০৪</b>\n"
            "• জৈব রসায়ন\n\n"

            "⚪️ <b>কেমিস্ট্রি সাইকেল ০৫</b>\n"
            "• পরিমাণগত রসায়ন\n"
            "• অর্থনৈতিক রসায়ন\n"
            "• তড়িৎ রসায়ন\n\n"

            "🎁 <b>কোর্সের সাথে পাবেন:</b>\n"
            "📍 টপিক ভিত্তিক ক্লাস (720p)\n"
            "📍 ক্লাসের লেকচার শীট\n"
            "📍 বাড়ির কাজের PDF\n"
            "📍 প্র্যাকটিস শীট\n"
            "📍 ডাউট সলভ ক্লাস\n"
            "📍 লাইফটাইম এক্সেস\n\n"

            "💰 <b>মূল্য: 5 Points</b>"
        ),

        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Buy Course — 5 Points",
                        callback_data="buy_acs_chemistry"
                    )
                ]
            ]
        )
    )


# =========================================================
# ACS MATH
# =========================================================

@dp.message(F.text == "📐 ACS Math")
async def acs_math(message):

    photo = (
        "AgACAgUAAxkBAAIWgGqCOWgvQ_yZriR1zf0bUuxWxj2W"
        "AALaEWsb9VsZVJWuVLa-4EzhAQADAgADeAADPQQ"
    )

    await message.answer_photo(

        photo=photo,

        caption=(
            "📘 🔥 <b>HSC-27 ACS MATH All Cycle (1-6)</b> 🔥\n\n"

            "📋 <b>HSC 2027 ACS MATH ALL CYCLE</b>\n\n"

            "<b>ইন্সট্রাক্টর সমূহ</b>\n"
            "▫️ অভিদত্ত তুশার\n"
            "▫️ রকিবুল ভাইয়া\n\n"

            "⚪️ <b>ম্যাথ সাইকেল ০১</b>\n"
            "• ম্যাট্রিক্স ও নির্ণায়ক\n"
            "• ভেক্টর\n"
            "• সরলরেখা\n"
            "• বৃত্ত\n\n"

            "⚪️ <b>ম্যাথ সাইকেল ০২</b>\n"
            "• বিন্যাস ও সমাবেশ\n"
            "• ত্রিকোণমিতিক অনুপাত\n"
            "• সংযুক্ত কোণের ত্রিকোণমিতি\n\n"

            "⚪️ <b>ম্যাথ সাইকেল ০৩</b>\n"
            "• অন্তরীকরণ\n"
            "• যোগজীকরণ\n\n"

            "⚪️ <b>ম্যাথ সাইকেল ০৪</b>\n"
            "• বাস্তব সংখ্যা ও অসমতা\n"
            "• যোগাশ্রয়ী প্রোগ্রাম\n"
            "• জটিল সংখ্যা\n"
            "• বহুপদী ও বহুপদী সমীকরণ\n\n"

            "⚪️ <b>ম্যাথ সাইকেল ০৫</b>\n"
            "• দ্বিপদী বিস্তৃতি\n"
            "• কণিক\n"
            "• বিপরীত ত্রিকোণমিতি\n\n"

            "⚪️ <b>ম্যাথ সাইকেল ০৬</b>\n"
            "• স্থিতিবিদ্যা\n"
            "• সমতলে বস্তুকণার গতি\n"
            "• বিস্তার পরিমাপ ও সম্ভাবনা\n\n"

            "🎁 <b>কোর্সের সাথে পাবেন:</b>\n"
            "📍 টপিক ভিত্তিক ক্লাস\n"
            "📍 ক্লাসের লেকচার শীট\n"
            "📍 বাড়ির কাজের PDF\n"
            "📍 প্র্যাকটিস শীট\n"
            "📍 ডাউট সলভ ক্লাস\n"
            "📍 লাইফটাইম এক্সেস\n\n"

            "💰 <b>মূল্য: 5 Points</b>"
        ),

        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Buy Course — 5 Points",
                        callback_data="buy_acs_math"
                    )
                ]
            ]
        )
    )


# =========================================================
# ACS BIOLOGY
# =========================================================

@dp.message(F.text == "🔬 ACS Biology")
async def acs_biology(message):

    photo = (
        "AgACAgUAAxkBAAIWfmqCOVEBD2Y3dcYPOl6HAAG6Koyi"
        "0QAC2RFrG_VbGVR-9ITQRrFGsQEAAwIAA3kAAz0E"
    )

    await message.answer_photo(

        photo=photo,

        caption=(
            "📘 🔥 <b>HSC-27 ACS BIO-MISSION BIOLOGY ALL CYCLE (1-6)</b> 🔥\n\n"

            "📋 <b>HSC 2027 ACS BIO-MISSION BIOLOGY ALL CYCLE</b>\n\n"

            "📖 <b>ইন্সট্রাক্টর:</b> 👉🏻 শুভ্র ভাই\n\n"

            "⚪️ <b>বায়োলজি সাইকেল ০১</b>\n"
            "• কোষ ও কোষের গঠন\n"
            "• কোষ বিভাজন\n"
            "• কোষ রসায়ন\n\n"

            "⚪️ <b>বায়োলজি সাইকেল ০২</b>\n"
            "• প্রাণীর বিভিন্নতা ও শ্রেণীবিন্যাস\n"
            "• প্রাণীর পরিচিতি\n"
            "• পরিপাক ও শোষণ\n\n"

            "⚪️ <b>বায়োলজি সাইকেল ০৩</b>\n"
            "• অণুজীব\n"
            "• শৈবাল ও ছত্রাক\n"
            "• ব্রায়োফাইটা ও টেরিডোফাইটা\n"
            "• জীব প্রযুক্তি\n\n"

            "⚪️ <b>বায়োলজি সাইকেল ০৪</b>\n"
            "• রক্ত ও সংবহন\n"
            "• শ্বসন শাসক্রিয়া\n"
            "• বর্জ্য ও নিষ্কাশন\n"
            "• চলন অঙ্গচলনা\n\n"

            "⚪️ <b>বায়োলজি সাইকেল ০৫</b>\n"
            "• নগ্নবীজী ও আবৃতবীজী উদ্ভিদ\n"
            "• টিস্যু ও টিস্যুতন্ত্র\n"
            "• উদ্ভিদ শরীরতত্ত্ব\n"
            "• জীবের পরিবেশ বিস্তার ও সংরক্ষণ\n\n"

            "⚪️ <b>বায়োলজি সাইকেল ০৬</b>\n"
            "• সমন্বয় ও নিয়ন্ত্রণ\n"
            "• মানব জীবনের ধারাবাহিকতা\n"
            "• মানবদেহের প্রতিরক্ষা\n"
            "• জিনতত্ত্ব ও বিবর্তন\n"
            "• প্রাণীর আচরণ\n\n"

            "🎁 <b>কোর্সের সাথে পাবেন:</b>\n"
            "📍 ক্লাসের লেকচার শীট\n"
            "📍 দাগানো বই PDF\n"
            "📍 প্র্যাকটিস শীট\n"
            "📍 লাইফটাইম এক্সেস\n\n"

            "💰 <b>মূল্য: 5 Points</b>"
        ),

        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Buy Course — 5 Points",
                        callback_data="buy_acs_biology"
                    )
                ]
            ]
        )
    )


# =========================================================
# ACS ENGLISH
# =========================================================

@dp.message(F.text == "📖 ACS English")
async def acs_english(message):

    photo = (
        "AgACAgUAAxkBAAIWgmqCOYZrRinwwRLpZ1_211iUpMJa"
        "AALbEWsb9VsZVHTJsrc-JqbHAQADAgADeAADPQQ"
    )

    await message.answer_photo(

        photo=photo,

        caption=(
            "📘 🔥 <b>HSC-27 English by Crowning English</b> 🔥\n\n"

            "📋 <b>HSC 2027 CROWNING ENGLISH</b>\n\n"

            "👨‍🏫 <b>Teacher:</b>\n"
            "▫️ Shampod Bhowmick\n\n"

            "📚 <b>Course Syllabus:</b>\n"
            "▫️ English 1st Paper\n"
            "▫️ English 2nd Paper\n"
            "▫️ HSC to Admission\n\n"

            "🎁 <b>কোর্সের সাথে পাবেন</b>\n"
            "📍 HSC English 1st Paper\n"
            "📍 HSC English 2nd Paper\n"
            "📍 Admission Preparation\n"
            "📍 Topic Based Classes\n"
            "📍 Lecture Materials\n"
            "📍 Lifetime Access\n\n"

            "💰 <b>মূল্য: 3 Points</b>"
        ),

        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Buy Course — 3 Points",
                        callback_data="buy_acs_english"
                    )
                ]
            ]
        )
    )


# =========================================================
# ACS BANGLA
# =========================================================

@dp.message(F.text == "📖 ACS Bangla")
async def acs_bangla(message):

    photo = (
        "AgACAgUAAxkBAAIWhGqCOZ7WP-OIxRDSKRL7W51hQgRS"
        "AALcEWsb9VsZVDTWp3Jkn7YiAQADAgADeAADPQQ"
    )

    await message.answer_photo(

        photo=photo,

        caption=(
            "📘 🔥 <b>অনুসর্গের ব্যঞ্জন</b> 🔥\n\n"

            "📋 <b>HSC 2027 বাংলা কোর্স</b>\n\n"

            "👨‍🏫 <b>ইন্সট্রাক্টর সমূহ</b>\n"
            "▫️ Abida Parvin Choudhuri\n"
            "▫️ Tanvir Ahmed\n\n"

            "🎓 <b>HSC-27 Batch এর জন্য</b>\n"
            "📚 সর্বমোট 60+ ক্লাস\n\n"

            "📖 <b>কোর্সের বিশেষত্ব</b>\n"
            "📍 HSC-27 Batch এর জন্য সম্পূর্ণ কোর্স\n"
            "📍 সর্বমোট 60+ টি ক্লাস\n"
            "📍 অভিজ্ঞ ইন্সট্রাক্টরদের ক্লাস\n"
            "📍 বাংলা বিষয়ের পূর্ণাঙ্গ প্রস্তুতি\n"
            "📍 HSC পরীক্ষার জন্য প্রস্তুতিমূলক ক্লাস\n\n"

            "🔥 <b>অনুসর্গের ব্যঞ্জন</b>\n"
            "🎯 HSC-27 শিক্ষার্থীদের বাংলা প্রস্তুতির জন্য\n\n"

            "💰 <b>মূল্য: 3 Points</b>"
        ),

        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Buy Course — 3 Points",
                        callback_data="buy_acs_bangla"
                    )
                ]
            ]
        )
    )


# =========================================================
# ACS ICT
# =========================================================

@dp.message(F.text == "💻 ACS ICT")
async def acs_ict(message):

    photo = (
        "AgACAgUAAxkBAAIWhmqCObww7OM9xAxpfQ2QW5czLp1i"
        "AALdEWsb9VsZVHmseobKwvq1AQADAgADeAADPQQ"
    )

    await message.answer_photo(

        photo=photo,

        caption=(
            "📘 🔥 <b>ACS ICT 2027</b> 🔥\n\n"

            "📋 <b>ACS ICT BATCH DECODER — HSC 27</b>\n\n"

            "📚 <b>অধ্যায় ডিসট্রিবিউশন</b>\n"
            "💡 Chapter 1, 3: Kazi Rakibul Hasan\n"
            "💡 Chapter 2, 4: Abhi Datta Tushar\n"
            "💡 Chapter 5, 6: Md Sharoare Hosan Emon\n\n"

            "⚔️ <b>কোর্সের সাথে যা যা পাবে</b>\n"
            "🔘 টপিক ভিত্তিক ক্লাস (HD)\n"
            "🔘 লেকচার শীট + প্র্যাকটিস শীট\n"
            "🔘 বাড়ির কাজের পিডিএফ\n"
            "🔘 অধ্যায় শেষে রিভিশন ক্লাস\n"
            "🔘 লাইফটাইম এক্সেস পাবে\n\n"

            "💰 <b>মূল্য: 3 Points</b>"
        ),

        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Buy Course — 3 Points",
                        callback_data="buy_acs_ict"
                    )
                ]
            ]
        )
    )


# =========================================================
# ACS FULL COMBO
# =========================================================

@dp.message(F.text == "🔥 ACS Full Combo")
async def acs_full_combo(message):

    photo = (
        "AgACAgUAAxkBAAIWiGqCOdPQ3zS9zr0jYCsKTZr51qOb"
        "AALeEWsb9VsZVI1YenP5ThBDAQADAgADeQADPQQ"
    )

    await message.answer_photo(

        photo=photo,

        caption=(
            "🔰 <b>HSC-27 ACS Full Combo</b>\n\n"

            "➪ ACS Physics Cycle 1 - 6\n"
            "➪ ACS Chemistry Cycle 1 - 5\n"
            "➪ ACS Biology Cycle 1 - 6\n"
            "➪ ACS Math Cycle 1 - 6\n"
            "➪ ACS ICT Decoder\n"
            "➪ ACS English Galacticos 1.0 - 2.0\n"
            "➪ ACS Bangla অনুসর্গের ব্যঞ্জন\n\n"

            "✅ Group Organized Class\n"
            "✅ All PDF Materials\n"
            "✅ Lifetime Access\n"
            "✅ 24/7 Admin Support\n\n"

            "💰 <b>মূল্য: 15 Points</b>"
        ),

        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Buy Course — 15 Points",
                        callback_data="buy_acs_combo"
                    )
                ]
            ]
        )
    )


# =========================================================
# UDVASH PRIME
# =========================================================

@dp.message(F.text == "🎓 Udvash 1st Year Prime Batch")
async def udvash_prime(message, state: FSMContext):

    await state.set_state(MenuState.UDVASH)

    photo = (
        "AgACAgUAAxkBAAIWimqCOeXhvW_QE6N_0gUAAWNaiwKSq"
        "wAC3xFrG_VbGVQast1rLZwmmgEAAwIAA20AAz0E"
    )

    await message.answer_photo(

        photo=photo,

        caption=(
            "📘 🔥 <b>UDVASH HSC 1st Year Prime Batch</b> 🔥\n\n"

            "📋 <b>UDVASH HSC 1st YEAR PRIME BATCH</b>\n\n"

            "🎓 <b>HSC 2027 Batch এর জন্য</b>\n\n"

            "📚 <b>যে বিষয়গুলো থাকছে</b>\n"
            "🔵 Physics\n"
            "🟢 Chemistry\n"
            "🟣 Biology\n"
            "🟠 Higher Mathematics\n\n"

            "⚔️ <b>কোর্সের সাথে যা যা পাবে</b>\n"
            "🏷️ HD রেজুলেশন ক্লাস\n"
            "🏷️ টপিক ভিত্তিক ক্লাস\n"
            "🏷️ গোছানো ক্লাস PDF\n"
            "🏷️ লাইফটাইম এক্সেস\n\n"

            "💰 <b>মূল্য: 10 Points</b>"
        ),

        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Buy Course — 10 Points",
                        callback_data="buy_udvash_prime"
                    )
                ]
            ]
        )
    )


# =========================================================
# UDVASH ENGLISH + BANGLA
# =========================================================

@dp.message(F.text == "📚 Udvash English-Bangla")
async def udvash_english_bangla(message, state: FSMContext):

    await state.set_state(MenuState.UDVASH)

    photo = (
        "AgACAgUAAxkBAAIWjGqCOfy3ZJjxHanwq86GIk1q1fi_A"
        "ALgEWsb9VsZVAMI-drj34G9AQADAgADeAADPQQ"
    )

    await message.answer_photo(

        photo=photo,

        caption=(
            "📘 🔥 <b>UDVASH HSC-27 ENGLISH & BANGLA</b> 🔥\n\n"

            "📋 <b>UDVASH HSC 2027 ENGLISH & BANGLA COURSE</b>\n\n"

            "📚 <b>বিষয়সমূহ</b>\n"
            "🔵 বাংলা ১ম পত্র\n"
            "🔵 বাংলা ২য় পত্র\n"
            "🟢 ইংরেজি ১ম পত্র\n"
            "🟢 ইংরেজি ২য় পত্র\n\n"

            "🎓 <b>HSC-27 Batch এর জন্য</b>\n"
            "✨ বাংলা ও ইংরেজির পূর্ণাঙ্গ প্রস্তুতি\n\n"

            "⚔️ <b>কোর্সের সাথে যা যা পাবে</b>\n"
            "🏷️ HD রেজুলেশন ক্লাস\n"
            "🏷️ টপিক ভিত্তিক ক্লাস\n"
            "🏷️ গোছানো ক্লাস PDF\n"
            "🏷️ গুরুত্বপূর্ণ Lecture Materials\n"
            "🏷️ Practice & Exam Preparation\n"
            "🏷️ লাইফটাইম এক্সেস\n\n"

            "💰 <b>মূল্য: 5 Points</b>"
        ),

        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Buy Course — 5 Points",
                        callback_data="buy_udvash_english_bangla"
                    )
                ]
            ]
        )
    )


# =========================================================
# UDVASH ICT
# =========================================================

@dp.message(F.text == "💻 Udvash ICT")
async def udvash_ict(message, state: FSMContext):

    await state.set_state(MenuState.UDVASH)

    photo = (
        "AgACAgUAAxkBAAIWjmqCOhVY5LAgq_Ri461JzBHOkd3W"
        "AALhEWsb9VsZVGWoYbwMSRtMAQADAgADeQADPQQ"
    )

    await message.answer_photo(

        photo=photo,

        caption=(
            "📘 🔥 <b>UDVASH HSC-27 ICT</b> 🔥\n\n"

            "📋 <b>UDVASH HSC 2027 ICT COURSE</b>\n\n"

            "💻 <b>ICT এর সম্পূর্ণ প্রস্তুতি</b>\n"
            "🔹 HSC ICT Syllabus Coverage\n"
            "🔹 Chapter-wise Classes\n"
            "🔹 Topic-based Preparation\n"
            "🔹 CQ & MCQ Preparation\n\n"

            "🎓 <b>HSC-27 Batch এর জন্য</b>\n"
            "✨ ICT বিষয়ে পূর্ণাঙ্গ প্রস্তুতি\n\n"

            "⚔️ <b>কোর্সের সাথে যা যা পাবে</b>\n"
            "🏷️ HD রেজুলেশন ক্লাস\n"
            "🏷️ টপিক ভিত্তিক ক্লাস\n"
            "🏷️ গোছানো ক্লাস PDF\n"
            "🏷️ Lecture Sheet & Practice Materials\n"
            "🏷️ CQ + MCQ Preparation\n"
            "🏷️ লাইফটাইম এক্সেস\n\n"

            "💰 <b>মূল্য: 5 Points</b>"
        ),

        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🛒 Buy Course — 5 Points",
                        callback_data="buy_udvash_ict"
                    )
                ]
            ]
        )
    )

# =========================================================
# HSC-28 MENUS
# =========================================================

def hsc28_platform_menu():
    buttons = [
        [KeyboardButton(text="🔰 HSC-28 ACS"), KeyboardButton(text="🎓 HSC-28 Udvash")],
        [KeyboardButton(text="🔥 Redwan's Method"), KeyboardButton(text="💡 Fahad's Tutorial")],
        [KeyboardButton(text="🧬 Biology Haters"), KeyboardButton(text="📖 Banglabaz 8.0")],
        [KeyboardButton(text="⬅️ Back"), KeyboardButton(text="🔝 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def hsc28_sub_menu(platform_name):
    buttons = [
        [KeyboardButton(text=f"🔬 {platform_name} Physics"), KeyboardButton(text=f"🧪 {platform_name} Chemistry")],
        [KeyboardButton(text=f"📐 {platform_name} Math"), KeyboardButton(text=f"🧬 {platform_name} Biology")],
        [KeyboardButton(text=f"📖 {platform_name} EBI")],
        [KeyboardButton(text=f"🔥 {platform_name} Combo")],
        [KeyboardButton(text="⬅️ Back"), KeyboardButton(text="🔝 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(F.text == "🎓 HSC-28")
async def hsc28_command(message, state: FSMContext):
    await state.set_state(MenuState.HSC28_PLATFORM)
    
    # এখানে প্ল্যাটফর্ম সিলেক্ট করার ছবি দেওয়া হলো
    photo = "AgACAgUAAxkBAAIUVWqBwk2om5Q7FDV_8ziqbutItiX5AAJhE2sb9VsRVIdaOFFA0fJvAQADAgADeQADPQQ"
    
    await message.answer_photo(
        photo=photo,
        caption=(
            "🎓 <b>HSC-28</b>\n\n"
            "আপনি যে প্ল্যাটফর্মের কোর্স নিতে চান, "
            "সেটি সিলেক্ট করুন 📚👇"
        ),
        reply_markup=hsc28_platform_menu()
    )

@dp.message(F.text == "🔰 HSC-28 ACS")
async def hsc28_acs_menu(message, state: FSMContext):
    await state.set_state(MenuState.HSC28_SUB_PLATFORM)
    photo = "AgACAgUAAxkBAAIaqWqEpngOs6x5ONZ0E9mqRxL1ZlcWAAJKFGsby_UoVHrtMAWn2Go2AQADAgADeQADPQQ"
    await message.answer_photo(photo=photo, caption="🔰 <b>HSC-28 ACS Course List 👇</b>", reply_markup=hsc28_sub_menu("HSC-28 ACS"))

@dp.message(F.text == "🎓 HSC-28 Udvash")
async def hsc28_udvash_menu(message, state: FSMContext):
    await state.set_state(MenuState.HSC28_SUB_PLATFORM)
    photo = "AgACAgUAAxkBAAIaq2qEptFrgMwVFft7be6M0-2i3I3oAAJLFGsby_UoVO527OSwSfBZAQADAgADeAADPQQ"
    await message.answer_photo(photo=photo, caption="🎓 <b>HSC-28 Udvash Course List 👇</b>", reply_markup=hsc28_sub_menu("HSC-28 Udvash"))

@dp.message(F.text == "🔥 Redwan's Method")
async def hsc28_rm_menu(message, state: FSMContext):
    await state.set_state(MenuState.HSC28_SUB_PLATFORM)
    photo = "AgACAgUAAxkBAAIarWqEpukF3eWsd09uIAip4RtvcgcbAAJMFGsby_UoVApdZ2RRn-LdAQADAgADeAADPQQ"
    await message.answer_photo(photo=photo, caption="🔥 <b>Redwan's Method Course List 👇</b>", reply_markup=hsc28_sub_menu("HSC-28 RM"))

@dp.message(F.text == "💡 Fahad's Tutorial")
async def hsc28_ft_menu(message, state: FSMContext):
    await state.set_state(MenuState.HSC28_SUB_PLATFORM)
    photo = "AgACAgUAAxkBAAIar2qEpywI_zAhEMZQz40IPgihhx-bAAJNFGsby_UoVMqB2T1-Bh-fAQADAgADeQADPQQ"
    buttons = [[KeyboardButton(text="📚 HSC-28 FT PCMB"), KeyboardButton(text="📖 HSC-28 FT EBI 4.0")], [KeyboardButton(text="⬅️ Back"), KeyboardButton(text="🔝 Main Menu")]]
    await message.answer_photo(photo=photo, caption="💡 <b>Fahad's Tutorial Course List 👇</b>", reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))

# =========================================================
# HSC-28 COURSE HANDLERS (ACS)
# =========================================================

@dp.message(F.text == "🔬 HSC-28 ACS Physics")
async def hsc28_acs_phy(message):
    photo = "AgACAgUAAxkBAAIaf2qEnyF3o0Sm34PAx7I0Sq0kTj-cAAI6FGsby_UoVA26IhTTCnrwAQADAgADeQADPQQ"
    caption = "📖 <b>𝗔𝗖𝗦 𝗣𝗛𝗬𝗦𝗜𝗖𝗦 𝗖𝗬𝗖𝗟𝗘 (𝗛𝗦𝗖 𝟮𝟴)</b>\n\n🗃 <b>শিক্ষক প্যানেল:</b>\n👤 অপূর্ব ভাই\n👤 মাশরুর ভাই\n\n📖 <b>Available Cycles:</b>\n◉ Cycle 1, 2, 3, 4, 5 & 6\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Trusted ✅\n✅ After Sales Service 🍑\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n✅ Best Service At Unbeatable Price 📊\n\n─────────♡─────────────\n📖 <b>কোর্সের মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_acs_phy")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "🧪 HSC-28 ACS Chemistry")
async def hsc28_acs_chem(message):
    photo = "AgACAgUAAxkBAAIagWqEn5wjVVOayJZSjVsi1bAn1i8nAAI7FGsby_UoVJb5yFg6LCSmAQADAgADeQADPQQ"
    caption = "📖 <b>𝗔𝗖𝗦 𝗔𝗹𝗼𝗿𝗼𝗻 𝗖𝗵𝗲𝗺𝗶𝘀𝘁𝗿𝘆 (𝗛𝗦𝗖 𝟮𝟴)</b>\n\n🗃 <b>Instructor:</b>\n👤 𝗠𝗼𝘁𝘁𝗮𝘀𝗶𝗻 𝗣𝗮𝗵𝗹𝗼𝘃𝗶\n👤 𝗛𝗲𝗺𝗲𝗹 𝗕𝗵𝗮𝗶\n\n📖 <b>Available Cycles:</b>\n◉ Cycle 1, 2, 3, 4 & 5\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n\n─────────♡─────────────\n📖 <b>কোর্সের মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_acs_chem")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "📐 HSC-28 ACS Math")
async def hsc28_acs_math(message):
    photo = "AgACAgUAAxkBAAIag2qEn_5ISBwVxV9qWjcvc2q9CJZBAAI8FGsby_UoVFrqVEx_n0aSAQADAgADeQADPQQ"
    caption = "📖 <b>𝗔𝗖𝗦 𝗠𝗮𝘁𝗵 𝗔𝗹𝗹 𝗖𝘆𝗰𝗹𝗲 (𝗛𝗦𝗖 𝟮𝟴)</b>\n\n🗃 <b>Instructor:</b>\n👤 𝗔𝗯𝗵𝗶 𝗗𝗮𝗱𝗮\n👤 𝗥𝗮𝗸𝗶𝗯 𝗕𝗵𝗮𝗶\n\n📖 <b>Available Cycles:</b>\n◉ Cycle 1, 2, 3, 4, 5 & 6\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n\n─────────♡─────────────\n📖 <b>কোর্সের মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_acs_math")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "🧬 HSC-28 ACS Biology")
async def hsc28_acs_bio(message):
    photo = "AgACAgUAAxkBAAIahWqEoCtmA6hfEpuC_o3OzN-ngdw-AAI9FGsby_UoVBkK8Ia9XXaPAQADAgADeQADPQQ"
    caption = "📖 <b>𝗔𝗖𝗦 𝗕𝗶𝗼𝗹𝗼𝗴𝘆 𝗖𝘆𝗰𝗹𝗲 (𝗛𝗦𝗖 𝟮𝟴)</b>\n\n🗃 <b>Instructor:</b>\n👤 𝗦𝗵𝘂𝘃𝗿𝗼 𝗕𝗵𝗮𝗶\n\n📖 <b>Available Cycles:</b>\n◉ Cycle 1, 2, 3, 4, 5 & 6\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n\n─────────♡─────────────\n📖 <b>কোর্সের মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_acs_bio")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "📖 HSC-28 ACS EBI")
async def hsc28_acs_ebi(message):
    photo = "AgACAgUAAxkBAAIah2qEoEd8tdJ9wZZf2dkYOrrEdTiKAAI-FGsby_UoVPw9mCdKeOU7AQADAgADeQADPQQ"
    caption = "📖 <b>𝗔𝗖𝗦 𝗘𝗕𝗜 𝗖𝗼𝘂𝗿𝘀𝗲 (𝗛𝗦𝗖 𝟮𝟴)</b>\n\n🗃 <b>Instructor:</b>\n👤 𝗔𝗯𝗵𝗶 𝗗𝗮𝘁𝘁𝗮 𝗧𝘂𝘀𝗵𝗮𝗿\n👤 𝗔𝗼𝗵𝗶𝗻 𝗕𝗵𝗮𝗶\n👤 𝗥𝗮𝗸𝗶𝗯 𝗕𝗵𝗮𝗶\n👤 𝗙𝗮𝗿𝘂𝗸 𝗕𝗵𝗮𝗶\n👤 𝗝𝗮𝗹𝗮𝗹 𝗦𝘂𝗺𝗼𝗻\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n\n─────────♡─────────────\n📖 <b>কোর্সের মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_acs_ebi")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "🔥 HSC-28 ACS Combo")
async def hsc28_acs_combo(message):
    photo = "AgACAgUAAxkBAAIaiWqEo_hu-XqqTyTTv7pamnpsCLJuAAI_FGsby_UoVFEuiPy7dPYGAQADAgADeQADPQQ"
    caption = "🔰 <b>𝐇𝐒𝐂-𝟐𝟖 (𝐀𝐂𝐒) 𝐂𝐨𝐦𝐛𝐨</b> 🔰\n\n➪ 𝐀𝐂𝐒 𝐏𝐡𝐲𝐬𝐢𝐜𝐬 𝐂𝐲𝐜𝐥𝐞 𝟏 - 𝟔\n➪ 𝐀𝐂𝐒 𝐂𝐡𝐞𝐦𝐢𝐬𝐭𝐫𝐲 𝐂𝐲𝐜𝐥𝐞 𝟏 - 𝟔\n➪ 𝐀𝐂𝐒 𝐁𝐢𝐨𝐥𝐨𝐠𝐲 𝐂𝐲𝐜𝐥𝐞 𝟏 - 𝟔 ⁽ˢʰᵘᵛʳᵒ ⱽᵃⁱ⁾\n➪ 𝐀𝐂𝐒 𝐌𝐚𝐭𝐡 𝐂𝐲𝐜𝐥𝐞 𝟏 - 𝟔\n➪ 𝐀𝐂𝐒 𝐄𝐧𝐠𝐥𝐢𝐬𝐡 𝐁𝐚𝐧𝐠𝐥𝐚 𝐈𝐂𝐓\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ গ্রুপে সাজানো ক্লাস ▶️\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n\n┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n📖 <b>সবগুলো কম্বো মূল্য: 20 Point</b> 🔥🔥\n┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 20 Points", callback_data="buy_h28_acs_combo")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

# =========================================================
# HSC-28 COURSE HANDLERS (UDVASH)
# =========================================================

@dp.message(F.text == "🔬 HSC-28 Udvash Physics")
async def hsc28_ud_phy(message):
    photo = "AgACAgUAAxkBAAIac2qEndJJC3Km2-SbQdbnoAO6mt5WAAIxFGsby_UoVBMoh1AGuAJ3AQADAgADeQADPQQ"
    caption = "📖 <b>𝗨𝗱𝘃𝗮𝘀𝗵 𝗣𝗛𝗬𝗦𝗜𝗖𝗦 (𝗛𝗦𝗖 𝟮𝟴)</b>\n\n📖 <b>Available Subject:</b>\n◉ Physics 1st and 2nd Paper\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_ud_phy")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "🧪 HSC-28 Udvash Chemistry")
async def hsc28_ud_chem(message):
    photo = "AgACAgUAAxkBAAIadWqEnfdKXovT-tKUsYyKLwGG8ygFAAIyFGsby_UoVAH2KxE69onXAQADAgADeQADPQQ"
    caption = "📖 <b>𝗨𝗱𝘃𝗮𝘀𝗵 𝗖𝗵𝗲𝗺𝗶𝘀𝘁𝗿𝘆 (𝗛𝗦𝗖 𝟮𝟴)</b>\n\n📖 <b>Available Subject:</b>\n◉ Chemistry 1st and 2nd Paper\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_ud_chem")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "📐 HSC-28 Udvash Math")
async def hsc28_ud_math(message):
    photo = "AgACAgUAAxkBAAIad2qEnhKmWCCA6C3-JrZle8pANp3HAAIzFGsby_UoVDDHzqYNbgABCgEAAwIAA3kAAz0E"
    caption = "📖 <b>𝗨𝗱𝘃𝗮𝘀𝗵 𝗛𝗶𝗴𝗵𝗲𝗿 𝗠𝗮𝘁𝗵 (𝗛𝗦𝗖 𝟮𝟴)</b>\n\n📖 <b>Available Subject:</b>\n◉ Higher Math 1st and 2nd\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_ud_math")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "🧬 HSC-28 Udvash Biology")
async def hsc28_ud_bio(message):
    photo = "AgACAgUAAxkBAAIaeWqEnivMmzjdLXPDCqHc7acg-VAJAAI0FGsby_UoVGM9aO7IWp4AAQEAAwIAA3kAAz0E"
    caption = "📖 <b>𝗨𝗱𝘃𝗮𝘀𝗵 𝗕𝗶𝗼𝗹𝗼𝗴𝘆 (𝗛𝗦𝗖 𝟮𝟴)</b>\n\n📖 <b>Available Subject:</b>\n◉ Biology 1st and 2nd Paper\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_ud_bio")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "📖 HSC-28 Udvash EBI")
async def hsc28_ud_ebi(message):
    photo = "AgACAgUAAxkBAAIae2qEnkA6nf3NmlYFhLn7rLgGcIiMAAI2FGsby_UoVCJSEhaRvPGUAQADAgADeQADPQQ"
    caption = "📖 <b>𝗨𝗱𝘃𝗮𝘀𝗵 𝗘𝗕𝗜 (𝗛𝗦𝗖 𝟮𝟴)</b>\n\n📖 <b>𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗦𝘂𝗯𝗷𝗲𝗰𝘁:</b>\n◉ 𝗘𝗻𝗴𝗹𝗶𝘀𝗵 𝗕𝗮𝗻𝗴𝗹𝗮 𝗜𝗖𝗧\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_ud_ebi")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "🔥 HSC-28 Udvash Combo")
async def hsc28_ud_combo(message):
    photo = "AgACAgUAAxkBAAIafWqEnlvI8Nw7A_eyrzpPZGIrVu-VAAI4FGsby_UoVDX-a3HxyUakAQADAgADeQADPQQ"
    caption = "🔰 <b>𝗨𝗱𝘃𝗮𝘀𝗵 𝐇𝐒𝐂-𝟐𝟖 𝐂𝐨𝐦𝐛𝐨</b> 🔰\n\n➪ 𝗨𝗱𝘃𝗮𝘀𝗵 𝗣𝗵𝘆𝘀𝗶𝗰𝘀\n➪ 𝗨𝗱𝘃𝗮𝘀𝗵 𝗖𝗵𝗲𝗺𝗶𝘀𝘁𝗿𝘆\n➪ 𝗨𝗱𝘃𝗮𝘀𝗵 𝗠𝗮𝘁𝗵\n➪ 𝗨𝗱𝘃𝗮𝘀𝗵 𝗕𝗶𝗼𝗹𝗼𝗴𝘆\n➪ 𝗨𝗱𝘃𝗮𝘀𝗵 𝗘𝗕𝗜\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ গ্রুপে সাজানো ক্লাস ▶️\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Lifetime Access 🎓\n\n─────────♡─────────────\n📖 <b>সবগুলো কম্বো মূল্য: 20 Point</b> 🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 20 Points", callback_data="buy_h28_ud_combo")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

# =========================================================
# HSC-28 COURSE HANDLERS (REDWAN'S METHOD)
# =========================================================

@dp.message(F.text == "🔬 HSC-28 RM Physics")
async def hsc28_rm_phy(message):
    photo = "AgACAgUAAxkBAAIal2qEpLZ744vXTIUwBMHkb0Hwm4xAAAJBFGsby_UoVNvGW90pEavrAQADAgADeQADPQQ"
    caption = "📖 <b>𝗥𝗠 𝗣𝗵𝘆𝘀𝗶𝗰𝘀 𝟭𝘀𝘁 𝗣𝗮𝗽𝗲𝗿 (𝗛𝗦𝗖-𝟮𝟴)</b>\n\n🗃 <b>শিক্ষক প্যানেল:</b>\n👤 𝗥𝗲𝗱𝘄𝗮𝗻 𝗛𝘂𝘀𝗵𝗲𝗻\n👤 𝗣𝗲𝗿𝘃𝗲𝘇 𝗔𝗵𝗺𝗺𝗲𝗱\n👤 𝗡𝗶𝗮𝘇𝗺𝗼𝗿𝘀𝗵𝗲𝗱 𝗙𝗮𝘆𝘀𝗮𝗹\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_rm_phy")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "🧪 HSC-28 RM Chemistry")
async def hsc28_rm_chem(message):
    photo = "AgACAgUAAxkBAAIamWqEpNRXj1JTFWGV2apTkJSycdFQAAJCFGsby_UoVMPhEz5StZVVAQADAgADeQADPQQ"
    caption = "📖 <b>𝗥𝗠 𝗖𝗵𝗲𝗺𝗶𝘀𝘁𝗿𝘆 𝟭𝘀𝘁 𝗣𝗮𝗽𝗲𝗿 𝗛𝗦𝗖𝟮𝟴</b>\n\n🗃 <b>Instructor:</b>\n👤 𝗛𝗮𝘀𝗮𝗻 𝗔𝗻𝗮𝗺\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_rm_chem")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "📐 HSC-28 RM Math")
async def hsc28_rm_math(message):
    photo = "AgACAgUAAxkBAAIam2qEpPGyR0B24dO1XQPe30GBgPqkAAJDFGsby_UoVBWVDklOTJv9AQADAgADeQADPQQ"
    caption = "📖 <b>𝗥𝗠 Higher 𝗠𝗮𝘁𝗵 𝟭𝘀𝘁 𝗣𝗮𝗽𝗲𝗿 (𝗛𝗦𝗖-𝟮𝟴)</b>\n\n🗃 <b>Instructor:</b>\n👤 𝗙𝗮𝗵𝗮𝗱 𝗛𝗼𝘀𝘀𝗮𝗶𝗻 𝗦𝗵𝗼𝘃𝗼𝗻\n👤 𝗔𝘀𝗶𝗳 𝗙𝗮𝘆𝘀𝗮𝗹 𝗥𝗶𝗳𝗮𝘁\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_rm_math")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "🧬 HSC-28 RM Biology")
async def hsc28_rm_bio(message):
    photo = "AgACAgUAAxkBAAIanWqEpSdBLLY37LN9b4bOVN4fIX2EAAJEFGsby_UoVL8tJ3Xp-vgzAQADAgADeQADPQQ"
    caption = "📖 <b>𝗥𝗠 𝗕𝗶𝗼𝗹𝗼𝗴𝘆 𝟭𝘀𝘁 𝗣𝗮𝗽𝗲𝗿 (𝗛𝗦𝗖-𝟮𝟴)</b>\n\n🗃 <b>Instructor:</b>\n👤 𝗝𝘂𝗻𝗻𝘂𝗿𝗮𝗶𝗻 𝗞𝗵𝗮𝗻\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_rm_bio")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "📖 HSC-28 RM EBI")
async def hsc28_rm_ebi(message):
    photo = "AgACAgUAAxkBAAIan2qEpUH7J07bYSO4gs_xJ3OXjkbJAAJFFGsby_UoVGKlNIrlFuv_AQADAgADeQADPQQ"
    caption = "📖 <b>𝗥𝗠 𝗘𝗕𝗜 𝟮.𝟬 (𝗛𝗦𝗖-𝟮𝟴)</b>\n\n🗃 <b>Instructor:</b>\n👤 𝗥𝗲𝗱𝘄𝗮𝗻 𝗦𝗶𝗿, 𝗛𝗮𝗺𝗷𝗮 𝗦𝗶𝗿, 𝗧𝗶𝗽𝘂 𝗦𝗶𝗿, 𝗝𝗶𝗹𝗮𝗻𝗶 𝗦𝗶𝗿, 𝗢𝗺𝗶 𝗦𝗶𝗿\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_rm_ebi")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "🔥 HSC-28 RM Combo")
async def hsc28_rm_combo(message):
    photo = "AgACAgUAAxkBAAIaoWqEpWMokPQcV090FWgdD8nMwhF2AAJGFGsby_UoVEU4PjM1djjjAQADAgADeQADPQQ"
    caption = "🔰 <b>𝗥𝗲𝗱𝘄𝗮𝗻'𝘀 𝗠𝗲𝘁𝗵𝗼𝗱 𝐇𝐒𝐂-𝟐𝟖 𝐂𝐨𝐦𝐛𝐨</b> 🔰\n\n➪ 𝗥𝗠 𝗣𝗵𝘆𝘀𝗶𝗰𝘀 𝟭𝘀𝘁 𝗣𝗮𝗽𝗲𝗿\n➪ 𝗥𝗠 𝗖𝗵𝗲𝗺𝗶𝘀𝘁𝗿𝘆 𝟭𝘀𝘁 𝗣𝗮𝗽𝗲𝗿\n➪ 𝗥𝗠 𝗠𝗮𝘁𝗵 𝟭𝘀𝘁 𝗣𝗮𝗽𝗲𝗿\n➪ 𝗥𝗠 𝗕𝗶𝗼𝗹𝗼𝗴𝘆 𝟭𝘀𝘁 𝗣𝗮𝗽𝗲𝗿\n➪ 𝗥𝗠 𝗘𝗕𝗜 𝟮.𝟬\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ গ্রুপে সাজানো ক্লাস ▶️\n✅ Everyday Class Update 🕔\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n\n─────────♡─────────────\n📖 <b>সবগুলো কম্বো মূল্য: 20 Point</b>\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 20 Points", callback_data="buy_h28_rm_combo")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

# =========================================================
# HSC-28 COURSE HANDLERS (OTHERS)
# =========================================================

@dp.message(F.text == "📚 HSC-28 FT PCMB")
async def hsc28_ft_pcmb(message):
    photo = "AgACAgUAAxkBAAIao2qEpdSpw77gsiIoiI8isLBhaBhwAAJHFGsby_UoVEZ81fbBJ6iQAQADAgADeQADPQQ"
    caption = "📖 <b>𝗙𝗮𝗵𝗮𝗱'𝘀 𝗧𝘂𝘁𝗼𝗿𝗶𝗮𝗹 PCMB (HSC-28)</b>\n\n📖 <b>𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗦𝘂𝗯𝗷𝗲𝗰𝘁:</b>\n◉ Physics Chemistry Higher Math Biology\n\n🗃 <b>Instructor:</b>\n👤 Imam Reza Ali Muzahid, Rahul Saha, Md. Fahad Hossain ও অন্যান্য\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Archive EBI 3.0 Free\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ Lifetime Access 🎓\n\n─────────♡─────────────\n📖 <b>সবগুলো কম্বো মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_ft_pcmb")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "📖 HSC-28 FT EBI 4.0")
async def hsc28_ft_ebi(message):
    photo = "AgACAgUAAxkBAAIapWqEpd74Rkd0nUKZh9Ia2wZqpWcnAAJIFGsby_UoVI9mGxa6S2foAQADAgADeAADPQQ"
    caption = "📖 <b>𝗙𝗮𝗵𝗮𝗱'𝘀 𝗧𝘂𝘁𝗼𝗿𝗶𝗮𝗹 𝗘𝗕𝗜 4.0</b>\n\n📖 <b>𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗦𝘂𝗯𝗷𝗲𝗰𝘁:</b>\n◉ 𝗘𝗻𝗴𝗹𝗶𝘀𝗵 𝗕𝗮𝗻𝗴𝗹𝗮 𝗜𝗖𝗧\n\n🗃 <b>Instructor:</b>\n👤 𝗦𝗮𝗶𝗳𝘂𝗹 𝗦𝗶𝗿, 𝗦𝗮𝗸𝗶𝗯 𝗦𝗶𝗿, 𝗦𝗮𝗻𝗶 𝗦𝗶𝗿, 𝗥𝗮𝘀𝗲𝗹 𝗦𝗶𝗿\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Archive EBI 3.0 Free\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ Lifetime Access 🎓\n\n─────────♡─────────────\n📖 <b>সবগুলো কম্বো মূল্য: 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_ft_ebi")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "🧬 Biology Haters")
async def hsc28_bio_haters(message):
    photo = "AgACAgUAAxkBAAIap2qEpk5Bsfa_Xn68zkpD6A5Yp_O4AAJJFGsby_UoVAMCXJZOGV5kAQADAgADeQADPQQ"
    caption = "📖 <b>𝗕𝗶𝗼𝗹𝗼𝗴𝘆 𝗛𝗮𝘁𝗲𝗿𝘀 (𝗛𝗦𝗖 𝟮𝟴)</b>\n\n🗃 <b>শিক্ষক প্যানেল:</b>\n👤 Dr. Rajib Sarkar\n\n📖 <b>Available Cycles:</b>\n◉ Cycle 1, 2, 3, 4, 5 & 6\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ Lifetime Access 🎓\n\n─────────♡─────────────\n📖 <b>সবগুলো কম্বো মূল্য: 5 Point</b>🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_bio_haters")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "📖 Banglabaz 8.0")
async def hsc28_banglabaz(message):
    photo = "AgACAgUAAxkBAAIatmqEuSPAykMU2FB2mnvuvP6XDvXGAAJVFGsby_UoVJvqV7fAsdiUAQADAgADeQADPQQ"
    caption = "📖 <b>Banglabaz 8.0 (HSC-28)</b>\n\n📖 <b>𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗦𝘂𝗯𝗷𝗲𝗰𝘁:</b>\n◉ Bangla 1st & 2nd Paper\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ Lifetime Access 🎓\n\n─────────♡─────────────\n📖 <b>সবগুলো কম্বো মূল্য: 5 Point</b>🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_h28_banglabaz")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

# =========================================================
# SSC-27 MENUS & COURSES
# =========================================================

def ssc27_menu():
    buttons = [
        [KeyboardButton(text="🔥 RM FRPB 27 + B2P 3.0")],
        [KeyboardButton(text="📘 RM B2P 3.0"), KeyboardButton(text="📘 RM FRPB 27")],
        [KeyboardButton(text="🔰 ACS FRB")],
        [KeyboardButton(text="💡 FT Academic"), KeyboardButton(text="💡 FT FRC")],
        [KeyboardButton(text="⬅️ Back"), KeyboardButton(text="🔝 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(F.text == "🎓 SSC-27")
async def ssc27_command(message, state: FSMContext):
    await state.set_state(MenuState.SSC27)
    photo = "AgACAgUAAxkBAAIcYGqE17iI5aPvj7AUTebTxbgBLNypAAJtFGsby_UoVLSqgPSSJbZ7AQADAgADeQADPQQ"
    await message.answer_photo(
        photo=photo,
        caption="🎓 <b>SSC-27</b>\n\nআপনি যে প্ল্যাটফর্মের কোর্স নিতে চান, সেটি সিলেক্ট করুন 📚👇",
        reply_markup=ssc27_menu()
    )

@dp.message(F.text == "🔥 RM FRPB 27 + B2P 3.0")
async def ssc27_rm_combo(message):
    photo = "AgACAgUAAxkBAAIcLGqEz43H9lPwlV44ILJ0iodQkHFRAAJjFGsby_UoVFRPIIpyBbebAQADAgADeQADPQQ"
    caption = "×̷̷͜×̷ <b>Redwan's Method SSC 27 Combo</b> ×̷̷͜×̷\n\n⌯⌲ <b>কি কি পাবেন:</b>\n◉ RM FRPB 27 (SSC 27)\n◉ RM B2P 3.0 (SSC 27)\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য : 10 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 10 Points", callback_data="buy_s27_rm_combo")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "📘 RM B2P 3.0")
async def ssc27_rm_b2p(message):
    photo = "AgACAgUAAxkBAAIcLmqEz5k-Fp--TOL_4hjZko_IlNOwAAJkFGsby_UoVDT2zbUwAAG1JwEAAwIAA3kAAz0E"
    caption = "×̷̷͜×̷ <b>RM SSC 27 B2P 3.0</b> ×̷̷͜×̷\n\n🔰 <b>কেন আমাদের থেকে নিবে:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update🕔\n✅ All PDF Materials 📄\n✅ Trusted✅\n✅ After Sales Service 🤝\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n✅ Best Service At Unbeatable Price📊\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য : 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_s27_rm_b2p")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "📘 RM FRPB 27")
async def ssc27_rm_frpb(message):
    photo = "AgACAgUAAxkBAAIcMGqEz6X9L_Y1mw-AS2AqKxFmsUKQAAJlFGsby_UoVEcgwMgUT7XJAQADAgADeQADPQQ"
    caption = "×̷̷͜×̷ <b>Redwan's Method FRPB 27</b> ×̷̷͜×̷\n\n🔰 <b>কেন আমাদের থেকে নিবে:</b>\n✅ YouTube এ সাজানো ক্লাস\n✅ Everyday Class Update🕔\n✅ All PDF Materials 📄\n✅ Trusted✅\n✅ After Sales Service 🤝\n✅ Lifetime Access 🧑‍🎓\n✅ 24/7 Admin Support 👤\n✅ Best Service At Unbeatable Price📊\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য : 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_s27_rm_frpb")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "🔰 ACS FRB")
async def ssc27_acs_frb(message):
    photo = "AgACAgUAAxkBAAIcMmqE0BEu20EO0RQnVPrnqoFOZg9aAAJmFGsby_UoVI6MEbjhvke4AQADAgADeAADPQQ"
    caption = "×̷̷͜×̷ <b>ACS FRB 27</b> ×̷̷͜×̷\n\n🔰 <b>কেন আমাদের থেকে নিবে:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update🕔\n✅ All PDF Materials 📄\n✅ Trusted✅\n✅ After Sales Service 🤝\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n✅ Best Service At Unbeatable Price📊\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য : 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_s27_acs_frb")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "💡 FT Academic")
async def ssc27_ft_acad(message):
    photo = "AgACAgUAAxkBAAIcNGqE0FjpZbd0TJFfjuOw-fK6s3auAAJnFGsby_UoVJYRSuM7TTFKAQADAgADeQADPQQ"
    caption = "×̷̷͜×̷ <b>FT Academic</b> ×̷̷͜×̷\n\n🔰 <b>কেন আমাদের থেকে নিবে:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update🕔\n✅ All PDF Materials 📄\n✅ Trusted✅\n✅ After Sales Service 🤝\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n✅ Best Service At Unbeatable Price📊\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য : 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_s27_ft_acad")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "💡 FT FRC")
async def ssc27_ft_frc(message):
    photo = "AgACAgUAAxkBAAIcNmqE0G_TdXppwwGOILhSm5enfpkUAAJoFGsby_UoVDb-3vNsjKQYAQADAgADeQADPQQ"
    caption = "×̷̷͜×̷ <b>FT FRC</b> ×̷̷͜×̷\n\n🔰 <b>কেন আমাদের থেকে নিবে:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update🕔\n✅ All PDF Materials 📄\n✅ Trusted✅\n✅ After Sales Service 🤝\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n✅ Best Service At Unbeatable Price📊\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য : 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_s27_ft_frc")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

# =========================================================
# SSC-28 MENUS & COURSES
# =========================================================

def ssc28_menu():
    buttons = [
        [KeyboardButton(text="📘 RM SSC-28 B2P 3.0")],
        [KeyboardButton(text="⬅️ Back"), KeyboardButton(text="🔝 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(F.text == "🎓 SSC-28")
async def ssc28_command(message, state: FSMContext):
    await state.set_state(MenuState.SSC28)
    photo = "AgACAgUAAxkBAAIcQGqE1yV9dTVzQjhN1sGKCrT5wv9aAAJsFGsby_UoVMSx5Tn2WnaKAQADAgADeQADPQQ"
    await message.answer_photo(
        photo=photo,
        caption="🎓 <b>SSC-28</b>\n\nআপনি যে কোর্সটি নিতে চান, সেটি সিলেক্ট করুন 📚👇",
        reply_markup=ssc28_menu()
    )

@dp.message(F.text == "📘 RM SSC-28 B2P 3.0")
async def ssc28_rm_b2p(message):
    photo = "AgACAgUAAxkBAAIcQGqE1yV9dTVzQjhN1sGKCrT5wv9aAAJsFGsby_UoVMSx5Tn2WnaKAQADAgADeQADPQQ"
    caption = "×̷̷͜×̷ <b>RM SSC 28 B2P 3.0</b> ×̷̷͜×̷\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Trusted ✅\n✅ After Sales Service 🤝\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n✅ Best Service At Unbeatable Price 📊\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য : 5 Point</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🛒 Buy Course — 5 Points", callback_data="buy_s28_rm_b2p")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

# =========================================================
# COLLEGE ADMISSION MENUS & COURSES
# =========================================================

def college_adm_menu():
    buttons = [
        [KeyboardButton(text="🆓 FT College Admission"), KeyboardButton(text="🆓 Udvash College Admission")],
        [KeyboardButton(text="🆓 Momit College Admission")],
        [KeyboardButton(text="⬅️ Back"), KeyboardButton(text="🔝 Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(F.text == "🎓 College Admission Course")
async def college_adm_command(message, state: FSMContext):
    await state.set_state(MenuState.COLLEGE_ADM)
    photo = "AgACAgUAAxkBAAIce2qE3I5-C9gFQ1XxRiq5p3Va5Sm2AAJuFGsby_UoVG9Aox0P9X15AQADAgADeQADPQQ"
    await message.answer_photo(
        photo=photo,
        caption="🎓 <b>College Admission (Free Courses)</b>\n\nআপনি যে ফ্রি কোর্সটি নিতে চান, সেটি সিলেক্ট করুন 📚👇",
        reply_markup=college_adm_menu()
    )

@dp.message(F.text == "🆓 FT College Admission")
async def ca_ft(message):
    photo = "AgACAgUAAxkBAAIc_2qFAV5gxeNMxaqq6ifsO-K-LBKpAAKLFGsby_UoVFjkC4mtAXqNAQADAgADeQADPQQ"
    caption = "×̷̷͜×̷ <b>Fahad's Tutorial College Admission</b> ×̷̷͜×̷\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Trusted ✅\n✅ After Sales Service 🍑\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n✅ Best Service At Unbeatable Price 📊\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য : Free</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🎁 Get Course (Free)", callback_data="get_ca_ft")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "🆓 Udvash College Admission")
async def ca_udvash(message):
    photo = "AgACAgUAAxkBAAIchGqE3k0k_O7uz9G6vUXzLVInDCoNAAJwFGsby_UoVP3IYvvI8oPhAQADAgADeQADPQQ"
    caption = "×̷̷͜×̷ <b>Udvash College Admissions Course</b> ×̷̷͜×̷\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Trusted ✅\n✅ After Sales Service 🍑\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n✅ Best Service At Unbeatable Price 📊\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য : Free</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🎁 Get Course (Free)", callback_data="get_ca_udvash")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

@dp.message(F.text == "🆓 Momit College Admission")
async def ca_momit(message):
    photo = "AgACAgUAAxkBAAIciWqE3qDNcHurmEPFvPEIJRxPXsaeAAJxFGsby_UoVHaM8ZjRkzGBAQADAgADeAADPQQ"
    caption = "×̷̷͜×̷ <b>Momit College Admissions Course</b> ×̷̷͜×̷\n\n🔰 <b>কেন আমাদের থেকে নিবেন:</b>\n✅ Telegram সাজানো ক্লাস\n✅ Everyday Class Update 🕔\n✅ All PDF Materials 📄\n✅ Trusted ✅\n✅ After Sales Service 🍑\n✅ Archive Class 🗑\n✅ Lifetime Access 🎓\n✅ 24/7 Admin Support 👤\n✅ Best Service At Unbeatable Price 📊\n\n─────────♡─────────────\n📖 <b>কোর্সের বিশেষ মূল্য : Free</b> 🔥🔥\n─────────♡─────────────"
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🎁 Get Course (Free)", callback_data="get_ca_momit")]])
    await message.answer_photo(photo=photo, caption=caption, reply_markup=markup)

# =========================================================
# BACK BUTTON
# =========================================================

# =========================================================
# BACK BUTTON
# =========================================================

@dp.message(F.text == "⬅️ Back")
async def back_button(message, state: FSMContext):
    current_state = await state.get_state()
    class_photo = "AgACAgUAAxkBAAIUV2qBwlb1yodVyjkdkzpGyZMfebJ4AAJiE2sb9VsRVN6uv6EUZeS3AQADAgADeQADPQQ"
    hsc27_photo = "AgACAgUAAxkBAAIUVWqBwk2om5Q7FDV_8ziqbutItiX5AAJhE2sb9VsRVIdaOFFA0fJvAQADAgADeQADPQQ"

    if current_state == MenuState.HSC28_SUB_PLATFORM.state:
        await state.set_state(MenuState.HSC28_PLATFORM)
        await message.answer_photo(photo=hsc27_photo, caption="🎓 <b>HSC-28</b>\n\nআপনি যে প্ল্যাটফর্মের কোর্স নিতে চান, সেটি সিলেক্ট করুন 📚👇", reply_markup=hsc28_platform_menu())
    elif current_state == MenuState.HSC28_PLATFORM.state:
        await state.set_state(MenuState.CLASS)
        await message.answer_photo(photo=class_photo, caption="📚 আপনি যে ক্লাসের কোর্স নিতে চান,\nসেটি সিলেক্ট করুন 👇", reply_markup=class_menu())
    elif current_state in [MenuState.ACS.state, MenuState.UDVASH.state]:
        await state.set_state(MenuState.PLATFORM)
        await message.answer_photo(photo=hsc27_photo, caption="🎓 <b>HSC-27</b>\n\nআপনি যে প্ল্যাটফর্মের কোর্স নিতে চান, সেটি সিলেক্ট করুন 📚👇", reply_markup=hsc27_platform_menu())
    elif current_state in [MenuState.PLATFORM.state, MenuState.SSC27.state, MenuState.SSC28.state, MenuState.COLLEGE_ADM.state]:
        await state.set_state(MenuState.CLASS)
        await message.answer_photo(photo=class_photo, caption="📚 আপনি যে ক্লাসের কোর্স নিতে চান,\nসেটি সিলেক্ট করুন 👇", reply_markup=class_menu())
    elif current_state == MenuState.CLASS.state:
        await state.clear()
        await message.answer("🏠 <b>Main Menu</b>", reply_markup=main_menu())

# =========================================================
# MAIN MENU BUTTON
# =========================================================

@dp.message(F.text == "🔝 Main Menu")
async def back_main_menu(message, state: FSMContext):

    await state.clear()

    await message.answer(
        "🏠 <b>Main Menu</b>",
        reply_markup=main_menu()
    )

# =========================================================
# LEADERBOARD
# =========================================================

@dp.message(F.text == "🏆 Leaderboard")
async def leaderboard(message):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name, username, referrals, points
        FROM users
        ORDER BY referrals DESC, points DESC
        LIMIT 10
        """
    )

    users = cursor.fetchall()

    conn.close()

    if not users:
        await message.answer(
            "🏆 <b>Referral Leaderboard</b>\n\n"
            "এখনো কোনো user নেই।"
        )
        return

    text = "🏆 <b>Referral Leaderboard</b>\n\n"

    medals = {
        1: "🥇",
        2: "🥈",
        3: "🥉"
    }

    for index, (name, username, referrals, points) in enumerate(users, start=1):

        medal = medals.get(index, "")

        if not name:
            name = "Unknown"

        if not username:
            username = "Not Set"
        elif not username.startswith("@"):
            username = f"@{username}"

        referrals = referrals or 0
        points = points or 0

        text += (
            f"{medal} <b>{index}. {name}</b>\n"
            f"👤 Username: {username}\n"
            f"👥 Referrals: {referrals}\n"
            f"💰 Points: {points}\n\n"
        )

    await message.answer(text)


# =========================================================
# HOW TO GET COURSE
# =========================================================

@dp.message(F.text == "কোর্স কিভাবে নিবে 🛠️")
async def how_to_get_course(message):

    await message.answer(

        "🛠️ <b>কোর্স কিভাবে নিবে?</b>\n\n"

        "1️⃣ প্রথমে আমাদের required channel-গুলোতে Join করুন।\n\n"
        "2️⃣ Referral করে Points সংগ্রহ করুন।\n\n"
        "3️⃣ <b>📚 Redeem Courses</b> থেকে আপনার পছন্দের "
        "course select করুন।\n\n"
        "4️⃣ Course-এর required Points দেখে তারপর "
        "পরবর্তী নির্দেশনা অনুসরণ করুন।"
    )

# =========================================================
# ADMIN CONTROLS (TESTING)
# =========================================================

@dp.message(F.text.startswith("/addpoint"))
async def add_point_command(message):
    
    # অ্যাডমিন ভেরিফিকেশন
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ You are not authorized to use this command.")
        return

    args = message.text.split()
    
    # সঠিক ফরম্যাট চেক করা
    if len(args) != 3:
        await message.answer("⚠️ <b>সঠিক নিয়ম:</b>\n/addpoint <user_id> <amount>")
        return

    try:
        target_user_id = int(args[1])
        points_to_add = int(args[2])
    except ValueError:
        await message.answer("❌ User ID এবং Amount অবশ্যই সংখ্যা হতে হবে।")
        return

    # ডাটাবেসে পয়েন্ট আপডেট করা
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT points FROM users WHERE user_id=?", (target_user_id,))
    user = cursor.fetchone()

    if user:
        new_points = user[0] + points_to_add
        cursor.execute(
            "UPDATE users SET points=? WHERE user_id=?",
            (new_points, target_user_id)
        )
        conn.commit()
        
        await message.answer(
            f"✅ <b>পয়েন্ট অ্যাড করা হয়েছে!</b>\n\n"
            f"👤 User ID: <code>{target_user_id}</code>\n"
            f"🎁 Added: {points_to_add} Points\n"
            f"💰 New Balance: {new_points} Points"
        )
        
        # ইউজারকে নোটিফিকেশন পাঠানো (যদি বট তাকে মেসেজ দিতে পারে)
        try:
            await bot.send_message(
                target_user_id,
                f"🎁 <b>Congratulations!</b>\nAdmin আপনাকে {points_to_add} Points উপহার দিয়েছে!\n"
                f"💰 আপনার বর্তমান ব্যালেন্স: {new_points} Points"
            )
        except Exception as e:
            await message.answer("⚠️ ইউজারকে নোটিফিকেশন পাঠানো যায়নি (হয়তো সে বট ব্লক করেছে)।")
            
    else:
        await message.answer("❌ এই User ID ডাটাবেসে পাওয়া যায়নি।")
        
    conn.close()

# =========================================================
# BUY COURSE / PURCHASE FLOW
# =========================================================

# কোন callback_data এর জন্য কোন কোর্স তা চেনার জন্য ডিকশনারি

# =========================================================
# CALLBACK TO COURSE
# =========================================================

CALLBACK_TO_COURSE = {
    # HSC-27
    "buy_acs_physics": "🧬 ACS Physics", "buy_acs_chemistry": "🧪 ACS Chemistry", "buy_acs_math": "📐 ACS Math",
    "buy_acs_biology": "🔬 ACS Biology", "buy_acs_english": "📖 ACS English", "buy_acs_bangla": "📖 ACS Bangla",
    "buy_acs_ict": "💻 ACS ICT", "buy_acs_combo": "🔥 ACS Full Combo", "buy_udvash_prime": "🎓 Udvash 1st Year Prime Batch",
    "buy_udvash_english_bangla": "📚 Udvash English-Bangla", "buy_udvash_ict": "💻 Udvash ICT",

    # HSC-28
    "buy_h28_acs_phy": "🔬 HSC-28 ACS Physics", "buy_h28_acs_chem": "🧪 HSC-28 ACS Chemistry", 
    "buy_h28_acs_math": "📐 HSC-28 ACS Math", "buy_h28_acs_bio": "🧬 HSC-28 ACS Biology", 
    "buy_h28_acs_ebi": "📖 HSC-28 ACS EBI", "buy_h28_acs_combo": "🔥 HSC-28 ACS Combo",
    
    "buy_h28_ud_phy": "🔬 HSC-28 Udvash Physics", "buy_h28_ud_chem": "🧪 HSC-28 Udvash Chemistry", 
    "buy_h28_ud_math": "📐 HSC-28 Udvash Math", "buy_h28_ud_bio": "🧬 HSC-28 Udvash Biology", 
    "buy_h28_ud_ebi": "📖 HSC-28 Udvash EBI", "buy_h28_ud_combo": "🔥 HSC-28 Udvash Combo",
    
    "buy_h28_rm_phy": "🔬 HSC-28 RM Physics", "buy_h28_rm_chem": "🧪 HSC-28 RM Chemistry", 
    "buy_h28_rm_math": "📐 HSC-28 RM Math", "buy_h28_rm_bio": "🧬 HSC-28 RM Biology", 
    "buy_h28_rm_ebi": "📖 HSC-28 RM EBI", "buy_h28_rm_combo": "🔥 HSC-28 RM Combo",
    
    "buy_h28_ft_pcmb": "📚 HSC-28 FT PCMB", "buy_h28_ft_ebi": "📖 HSC-28 FT EBI 4.0",
    "buy_h28_bio_haters": "🧬 HSC-28 Biology Haters", "buy_h28_banglabaz": "📖 HSC-28 Banglabaz 8.0",

    # SSC-27
    "buy_s27_rm_b2p": "📘 RM B2P 3.0",
    "buy_s27_rm_frpb": "📘 RM FRPB 27",
    "buy_s27_acs_frb": "🔰 ACS FRB",
    "buy_s27_ft_acad": "💡 FT Academic",
    "buy_s27_ft_frc": "💡 FT FRC",
    "buy_s27_rm_combo": "🔥 RM FRPB 27 + B2P 3.0",

    # SSC-28
    "buy_s28_rm_b2p": "📘 RM SSC-28 B2P 3.0",

    # College Admission
    "get_ca_ft": "🆓 FT College Admission",
    "get_ca_udvash": "🆓 Udvash College Admission",
    "get_ca_momit": "🆓 Momit College Admission"
}

@dp.callback_query(F.data.startswith("buy_") | F.data.startswith("get_"))
async def handle_buy_course(callback):
    
    user_id = callback.from_user.id
    course_name = CALLBACK_TO_COURSE.get(callback.data)
    
    if not course_name:
        await callback.answer("❌ Course not found!", show_alert=True)
        return
        
    required_points = COURSE_POINTS.get(course_name)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT points FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        await callback.answer("⚠️ దয়া করে আগে /start কমান্ড দিন।", show_alert=True)
        return
        
    current_points = user[0]
    
    # ১. পয়েন্ট চেক
    if current_points < required_points:
        conn.close()
        shortfall = required_points - current_points
        await callback.answer(
            f"❌ আপনার পর্যাপ্ত পয়েন্ট নেই!\n\n"
            f"আপনার আছে: {current_points} Points\n"
            f"প্রয়োজন: {required_points} Points\n"
            f"আরও {shortfall} Points লাগবে।",
            show_alert=True
        )
        return
        
    # ২. পয়েন্ট কেটে নেওয়া
    new_points = current_points - required_points
    cursor.execute("UPDATE users SET points=? WHERE user_id=?", (new_points, user_id))
    conn.commit()
    conn.close()
    
    # ৩. ইনভাইট লিংক জেনারেট এবং মেসেজ পাঠানো
    await callback.message.answer("⏳ আপনার কোর্সের অ্যাক্সেস লিংক তৈরি করা হচ্ছে... দয়া করে অপেক্ষা করুন।")
    
    try:
        # Full Combo-এর জন্য স্পেশাল লজিক (HSC-27 & HSC-28)
        combo_lists = {
            "🔥 ACS Full Combo": ACS_COMBO_COURSES,
            "🔥 HSC-28 ACS Combo": HSC28_ACS_COMBO,
            "🔥 HSC-28 Udvash Combo": HSC28_UDVASH_COMBO,
            "🔥 HSC-28 RM Combo": HSC28_RM_COMBO,
            "🔥 RM FRPB 27 + B2P 3.0": SSC27_RM_COMBO
        }

        if course_name in combo_lists:
            links_text = ""
            courses_in_combo = combo_lists[course_name]
            
            for sub_course in courses_in_combo:
                chat_id = COURSE_CHAT_IDS.get(sub_course)
                if chat_id:
                    invite = await bot.create_chat_invite_link(chat_id, member_limit=1)
                    links_text += f"🔹 <b>{sub_course}</b>:\n{invite.invite_link}\n\n"
                
            msg = (
                f"✅ <b>Purchase Successful!</b> 🎉\n\n"
                f"🎯 <b>Course:</b> {course_name}\n"
                f"💰 <b>পয়েন্ট কাটা হয়েছে:</b> {required_points}\n"
                f"💳 <b>বর্তমান ব্যালেন্স:</b> {new_points} Points\n\n"
                f"🔗 <b>Your Access Links (One-time use):</b>\n\n{links_text}\n"
                f"⚠️ <i>লিংকগুলো শুধুমাত্র একবার কাজ করবে, তাই অন্য কাউকে শেয়ার করবেন না!</i>"
            )
            
        # সাধারণ (সিঙ্গেল) কোর্সের জন্য
        else:
            chat_id = COURSE_CHAT_IDS.get(course_name)
            invite = await bot.create_chat_invite_link(chat_id, member_limit=1)
            
            msg = (
                f"✅ <b>Purchase Successful!</b> 🎉\n\n"
                f"🎯 <b>Course:</b> {course_name}\n"
                f"💰 <b>পয়েন্ট কাটা হয়েছে:</b> {required_points}\n"
                f"💳 <b>বর্তমান ব্যালেন্স:</b> {new_points} Points\n\n"
                f"🔗 <b>Your Access Link (One-time use):</b>\n{invite.invite_link}\n\n"
                f"⚠️ <i>লিংকটি শুধুমাত্র একবার কাজ করবে, তাই অন্য কাউকে শেয়ার করবেন না!</i>"
            )
            
        await callback.message.answer(msg)
        await callback.answer()
        
    except Exception as e:
        # যদি বট গ্রুপে অ্যাডমিন না হয় বা অন্য কোনো কারণে লিংক তৈরি করতে না পারে
        print(f"Error creating invite link: {e}")
        
        # যেহেতু লিংক দিতে পারেনি, তাই ইউজারের পয়েন্ট ফেরত দেওয়া
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET points=? WHERE user_id=?", (current_points, user_id))
        conn.commit()
        conn.close()
        
        await callback.message.answer(
            "❌ <b>দুঃখিত! টেকনিক্যাল সমস্যার কারণে লিংক তৈরি করা যায়নি।</b>\n"
            "আপনার পয়েন্ট রিফান্ড করা হয়েছে। অনুগ্রহ করে অ্যাডমিনের সাথে যোগাযোগ করুন।"
        )
        
    except Exception as e:
        # যদি বট গ্রুপে অ্যাডমিন না হয় বা অন্য কোনো কারণে লিংক তৈরি করতে না পারে
        print(f"Error creating invite link: {e}")
        
        # যেহেতু লিংক দিতে পারেনি, তাই ইউজারের পয়েন্ট ফেরত দেওয়া
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET points=? WHERE user_id=?", (current_points, user_id))
        conn.commit()
        conn.close()
        
        await callback.message.answer(
            "❌ <b>দুঃখিত! টেকনিক্যাল সমস্যার কারণে লিংক তৈরি করা যায়নি।</b>\n"
            "আপনার পয়েন্ট রিফান্ড করা হয়েছে। অনুগ্রহ করে অ্যাডমিনের সাথে যোগাযোগ করুন।"
        )
# =========================================================
# MORE ADMIN COMMANDS
# =========================================================

# --- ১. পয়েন্ট কেটে নেওয়া (ভুল ঠিক করার জন্য) ---
@dp.message(F.text.startswith("/removepoint"))
async def remove_point_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    args = message.text.split()
    if len(args) != 3:
        await message.answer("⚠️ <b>সঠিক নিয়ম:</b>\n/removepoint <user_id> <amount>")
        return

    try:
        target_user_id = int(args[1])
        points_to_remove = int(args[2])
    except ValueError:
        await message.answer("❌ User ID এবং Amount সংখ্যা হতে হবে।")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT points FROM users WHERE user_id=?", (target_user_id,))
    user = cursor.fetchone()

    if user:
        # পয়েন্ট যেন মাইনাস (0 এর নিচে) না হয়ে যায়
        current_points = user[0]
        new_points = max(0, current_points - points_to_remove)
        
        cursor.execute("UPDATE users SET points=? WHERE user_id=?", (new_points, target_user_id))
        conn.commit()
        
        await message.answer(
            f"✅ <b>পয়েন্ট মাইনাস করা হয়েছে!</b>\n\n"
            f"👤 User ID: <code>{target_user_id}</code>\n"
            f"➖ Removed: {points_to_remove} Points\n"
            f"💰 New Balance: {new_points} Points"
        )
    else:
        await message.answer("❌ এই User ID ডাটাবেসে পাওয়া যায়নি।")
    conn.close()


# --- ২. ইউজারের বিস্তারিত তথ্য দেখা ---
@dp.message(F.text.startswith("/userinfo"))
async def userinfo_command(message):
    if message.from_user.id != ADMIN_ID:
        return
        
    args = message.text.split()
    if len(args) != 2:
        await message.answer("⚠️ <b>সঠিক নিয়ম:</b>\n/userinfo <user_id>")
        return
        
    try:
        target_id = int(args[1])
    except ValueError:
        await message.answer("❌ User ID সংখ্যা হতে হবে।")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, username, points, referrals FROM users WHERE user_id=?", (target_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        name, username, points, referrals = user
        username_text = username if username else "Not Set"
        await message.answer(
            f"👤 <b>User Information</b>\n\n"
            f"📛 Name: {name}\n"
            f"🔗 Username: {username_text}\n"
            f"🆔 ID: <code>{target_id}</code>\n"
            f"💰 Points: {points}\n"
            f"👥 Total Referrals: {referrals}"
        )
    else:
        await message.answer("❌ ইউজার ডাটাবেসে পাওয়া যায়নি।")


# --- ৩. বটের টোটাল স্ট্যাটাস দেখা ---
@dp.message(F.text == "/stats")
async def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    conn.close()
    
    await message.answer(
        f"📊 <b>Bot Statistics</b>\n\n"
        f"👥 Total Users: <b>{total_users}</b>"
    )


# --- ৪. ব্রডকাস্ট (সবাইকে মেসেজ পাঠানো) ---
@dp.message(F.text.startswith("/broadcast"))
async def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        return
        
    text_to_send = message.text.replace("/broadcast", "").strip()
    
    if not text_to_send:
        await message.answer("⚠️ <b>সঠিক নিয়ম:</b>\n/broadcast <আপনার মেসেজ>")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    conn.close()

    await message.answer(f"📢 Broadcast শুরু হয়েছে... (Total users: {len(users)})\nদয়া করে অপেক্ষা করুন।")
    
    success_count = 0
    for user in users:
        try:
            await bot.send_message(chat_id=user[0], text=text_to_send)
            success_count += 1
            await asyncio.sleep(0.05)  # টেলিগ্রামের স্প্যাম লিমিট থেকে বাঁচতে
        except Exception:
            pass  # ইউজার বট ব্লক করে দিলে এরর ইগনোর করবে
            
    await message.answer(
        f"✅ <b>Broadcast সম্পন্ন হয়েছে!</b>\n\n"
        f"সাফল্যজনকভাবে মেসেজ পাঠানো হয়েছে: {success_count} জনকে।"
    )

# =========================================================
# RUN BOT
# =========================================================

@dp.message(F.photo)
async def get_photo_id(message):
    file_id = message.photo[-1].file_id

    print("================================")
    print("PHOTO FILE ID:")
    print(file_id)
    print("================================")

    await message.answer(
        f"✅ Photo received!\n\n"
        f"File ID:\n{file_id}"
    )

async def handle_ping(request):
    return web.Response(text="Bot is alive and running!")

async def main():
    print("🚀 Bot is running...")
    
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', 10000) 
    await site.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
