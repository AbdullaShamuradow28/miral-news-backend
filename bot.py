import aiogram
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, FSInputFile
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types, F, Router
from aiogram.client.default import DefaultBotProperties 

BOT_TOKEN = "7758326963:AAE8Lhrs4RJwRJRUXy-nszsoVfC1Cmb7OAA"
MIRAL_STUDIO_CHANNEL_ID = -1002255895973
IDEAS_FILE = "ideas.txt"

class UserState(StatesGroup):
    waiting_for_idea = State()
    waiting_for_bug_description = State()

router = Router()

async def check_channel_subscription(bot: Bot, user_id: int, channel_id: int) -> bool:
    """Проверяет подписку пользователя на канал."""
    try:
        chat_member = await bot.get_chat_member(channel_id, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False

@router.message(aiogram.filters.Command("start"))
async def start_bot(msg: types.Message, bot: Bot):
    user_id = msg.from_user.id
    is_subscribed = await check_channel_subscription(bot, user_id, MIRAL_STUDIO_CHANNEL_ID)

    if not is_subscribed:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Подписаться на Miral Studio", url="https://t.me/miralstudio")]
        ])
        await msg.answer(
            text="Привет! 👋 Я бот Miral News. \n\n"
                 "Для начала работы, пожалуйста, подпишись на наш канал **Miral Studio**, "
                 "чтобы быть в курсе всех новостей и обновлений!",
            reply_markup=markup
        )
        await msg.answer("После подписки, пожалуйста, нажми /start ещё раз.")
    else:
        main_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Предложить идею 💡")],
                [KeyboardButton(text="Сообщить об ошибке 🐞")]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )
        await msg.answer(
            text="Привет! 👋 Я официальный бот Miral News! \n\n"
                 "Здесь ты можешь предложить идею для обновления или сообщить об ошибке. \n"
                 "Выбери действие, нажав на одну из кнопок ниже:",
            reply_markup=main_keyboard
        )

@router.message(F.text == "Предложить идею 💡")
async def suggest_idea_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Отлично! Напиши свою идею или список идей (можешь их пронумеровать или пометить символом • ).")
    await state.set_state(UserState.waiting_for_idea)

@router.message(UserState.waiting_for_idea)
async def process_idea(msg: types.Message, state: FSMContext):
    idea_text = msg.text
    user_info = f"@{msg.from_user.username}" if msg.from_user.username else f"ID: {msg.from_user.id}"

    with open(IDEAS_FILE, "a", encoding="utf-8") as f:
        f.write(f"Идея от {user_info}:\n{idea_text}\n---\n")

    await msg.answer("Спасибо! Твоя идея успешно записана. Мы обязательно её рассмотрим.")
    await state.clear()

@router.message(F.text == "Сообщить об ошибке 🐞")
async def report_bug_handler(msg: types.Message):
    bug_type_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Критическая ошибка (блокирует работу)", callback_data="report_critical")],
        [InlineKeyboardButton(text="Значительная ошибка (мешает, но можно обойти)", callback_data="report_major")],
        [InlineKeyboardButton(text="Мелкий баг/Опечатка", callback_data="report_minor")]
    ])
    await msg.answer("Выберите тип вашей проблемы:", reply_markup=bug_type_markup)

@router.callback_query(F.data.startswith("report_"))
async def process_bug_report_type(callback: types.CallbackQuery, state: FSMContext):
    report_type_code = callback.data.split("_")[1]
    
    report_type_name = {
        "critical": "Критическая ошибка",
        "major": "Значительная ошибка",
        "minor": "Мелкий баг/Опечатка"
    }.get(report_type_code, "Неизвестный тип")

    await state.update_data(bug_type=report_type_name)

    response_text = ""
    if report_type_code == "critical":
        response_text = f"Вы выбрали '{report_type_name}'. Пожалуйста, **подробно** опишите проблему: как её воспроизвести, что пошло не так. Если есть скриншоты или видео, приложите их следующим сообщением."
    elif report_type_code == "major":
        response_text = f"Вы выбрали '{report_type_name}'. Опишите, пожалуйста, проблему, как часто она возникает, и как она влияет на работу."
    elif report_type_code == "minor":
        response_text = f"Вы выбрали '{report_type_name}'. Укажите, пожалуйста, где вы обнаружили это."

    await callback.message.edit_text(response_text)
    await callback.answer()

    await state.set_state(UserState.waiting_for_bug_description)

@router.message(UserState.waiting_for_bug_description)
async def process_bug_description(msg: types.Message, state: FSMContext):
    bug_description = msg.text
    user_info = f"@{msg.from_user.username}" if msg.from_user.username else f"ID: {msg.from_user.id}"
    
    data = await state.get_data()
    bug_type = data.get("bug_type", "Неизвестный тип ошибки")

    # Отправка отчета мне в лс:
    # ADMIN_CHAT_ID = YOUR_ADMIN_ID
    # if ADMIN_CHAT_ID:
    #     await msg.bot.send_message(
    #         ADMIN_CHAT_ID,
    #         f"🚨 **НОВЫЙ БАГ-РЕПОРТ!** 🚨\n"
    #         f"**От:** {user_info}\n"
    #         f"**Тип:** {bug_type}\n"
    #         f"**Описание:**\n{bug_description}",
    #         parse_mode=ParseMode.MARKDOWN
    #     )
    # else:
    #     print(f"Новый баг-репорт от {user_info} ({bug_type}): {bug_description}")


    await msg.answer("Спасибо! Твоё описание ошибки получено. Мы постараемся исправить её как можно скорее.")
    await state.clear()

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())