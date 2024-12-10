from database import pool, execute_update_query, execute_select_query
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )

    builder.adjust(1)
    return builder.as_markup()

async def get_question_index(user_id):
    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(user_id)
    return current_question_index

async def get_question(current_question_index):
    current_question = f"""
        DECLARE $current_question_index AS Uint64;
        SELECT question, options, correct_option
        FROM `quiz-data-alt`
        WHERE id == $current_question_index;
    """
    results = execute_select_query(pool, current_question, current_question_index=current_question_index)
    return results

async def make_keyboard(message, current_question):
    correct_index = current_question[0]['correct_option']
    opts = str(current_question[0]['options'])
    opts_list = [x.strip() for x in opts.split(",")]
    kb = generate_options_keyboard(opts_list, opts_list[correct_index])
    await message.answer(f"{current_question[0]['question']}", reply_markup=kb)  

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    current_score = 0
    await update_quiz_index(user_id, current_question_index, current_score)
    question_index = await get_question_index(user_id)
    current_question = await get_question(question_index)
    await make_keyboard(message, current_question)

async def get_quiz_index(user_id):
    get_user_index = f"""
        DECLARE $user_id AS Uint64;

        SELECT question_index
        FROM `quiz_state`
        WHERE user_id == $user_id;
    """
    results = execute_select_query(pool, get_user_index, user_id=user_id)

    if len(results) == 0:
        return 0
    if results[0]["question_index"] is None:
        return 0
    return results[0]["question_index"]

async def get_quiz_score(user_id):
    get_user_index = f"""
        DECLARE $user_id AS Uint64;

        SELECT score
        FROM `quiz_state`
        WHERE user_id == $user_id;
    """
    results = execute_select_query(pool, get_user_index, user_id=user_id)

    if len(results) == 0:
        return 0
    if results[0]["score"] is None:
        return 0
    return results[0]["score"]  

async def update_quiz_index(user_id, question_index, score):
    set_quiz_state = f"""
        DECLARE $user_id AS Uint64;
        DECLARE $question_index AS Uint64;
        DECLARE $score AS Uint64;

        UPSERT INTO `quiz_state` (`user_id`, `question_index`,`score`)
        VALUES ($user_id, $question_index, $score);
    """

    execute_update_query(
        pool,
        set_quiz_state,
        user_id=user_id,
        question_index=question_index,
        score=score,
    )
    
def get_db_len():
    get_db_len_query = f"""
        SELECT COUNT(*)
        FROM `quiz-data-alt`
    """
    results = execute_select_query(pool, get_db_len_query)
    db_length = results[0]["column0"]
    return db_length