from .start import router as start_router
from .menu import router as menu_router
from .tasks import router as tasks_router
from .games import router as games_router
from .ai_chat import router as ai_router
from .help import router as help_router
from .music import router as music_router  # ← ДОБАВЬ
from .weather import router as weather_router  # ← ДОБАВЬ
from .currency import router as currency_router  # ← ДОБАВЬ

__all__ = [
    'start_router', 'menu_router', 'tasks_router', 
    'games_router', 'ai_router', 'help_router',
    'music_router', 'weather_router', 'currency_router'  # ← ДОБАВЬ
]