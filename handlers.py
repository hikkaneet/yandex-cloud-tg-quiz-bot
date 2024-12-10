from aiogram import types, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart, StateFilter, CommandObject, CREATOR
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from service import generate_options_keyboard, get_question, new_quiz, get_quiz_index, update_quiz_index, get_question_index, make_keyboard, get_db_len, get_quiz_score
from aiogram.methods import SendPhoto

DB_LEN = get_db_len()
IMG_URL = "https://storage.yandexcloud.net/quiz-storage/_6d3c2ad4-68f1-4839-ae75-0ed35841292b.webp"

router = Router()

@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    await callback.message.answer("Верно!")
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_score = await get_quiz_score(callback.from_user.id)
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    current_score += 1
    await update_quiz_index(callback.from_user.id, current_question_index, current_score)

    if current_question_index < DB_LEN:
        question_index = await get_question_index(callback.from_user.id)
        current_question = await get_question(question_index)
        await make_keyboard(callback.message, current_question)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await callback.message.answer(f"Вы ответили правильно на {current_score} из {current_question_index} вопросов!")
        await callback.message.answer(f"Точность Ваших ответов {round(current_score / current_question_index * 100, 2)}%!")

  
@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    # Получение текущего вопроса из словаря состояний пользователя
    question_index = await get_question_index(callback.from_user.id)
    current_question = await get_question(question_index)
    correct_option = current_question[0]['correct_option']
    opts = str(current_question[0]['options'])
    opts_list = [x.strip() for x in opts.split(",")]

    await callback.message.answer(f"Неправильно. Правильный ответ: {opts_list[correct_option]}")

    current_question_index = await get_quiz_index(callback.from_user.id)
    current_score = await get_quiz_score(callback.from_user.id)
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    current_score += 0
    await update_quiz_index(callback.from_user.id, current_question_index, current_score)


    if current_question_index < DB_LEN:
        question_index = await get_question_index(callback.from_user.id)
        current_question = await get_question(question_index)
        await make_keyboard(callback.message, current_question)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await callback.message.answer(f"Вы ответили правильно на {current_score} из {current_question_index} вопросов!")
        await callback.message.answer(f"Точность Ваших ответов {round(current_score / current_question_index * 100, 2)}%!")

# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer_photo(photo=IMG_URL)
    await message.answer(f"Количество вопросов: {DB_LEN}")
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

# Хэндлер на команду /quiz
@router.message(F.text=="Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    
    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)
    