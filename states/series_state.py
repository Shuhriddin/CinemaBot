from aiogram.fsm.state import StatesGroup, State

class SeriesState(StatesGroup):
    waiting_for_title = State()
    uploading_episodes = State()
