from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    """Состояния пользователя"""
    main_menu = State()      # Основное меню
    guest_mode = State() 
    ai_chat = State()        # Режим AI чата
    game_mode = State()      # Режим игры
    viewing_tasks = State()  # Просмотр задач
    music_menu = State()