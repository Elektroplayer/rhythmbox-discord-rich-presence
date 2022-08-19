from gi.repository import GObject, Peas, RB
from pypresence import Presence
from threading import Timer
from dp_config import *


class EditingRPC:
    state        = None
    details      = "Бездействует"
    small_image  = "stop"
    small_text   = "Остановлено"

    timeout = False # False - Таймаута нет, True - Таймаут есть
    need_update = False # False - Обновление не требуется, True - Требуется

    """ Инициализация """
    def __init__(self):
        # Коннектимся
        self.RPC = Presence('972548831747125259')
        self.RPC.connect()
        self.update_rpc()

    """ Изменение переменных и отправка данных, когда это возможно """
    def change_values(self, state, details, small_image, small_text):
        print('Изменение')

        self.state        = state
        self.details      = details
        self.small_image  = small_image
        self.small_text   = small_text

        if not self.timeout:
            self.update_rpc()

            self.timeout = True

            Timer(15.5, self.timer_function).start()
        elif not self.need_update:
            self.need_update = True

    """ Функция в таймере """
    def timer_function(self):
        if self.need_update:
            self.need_update = False
            self.update_rpc()
            Timer(15.5, self.timer_function).start()
        else:
            self.timeout = False

    """ Отключение """
    def disconect(self):
        self.RPC = None

    """ Отправка данных в дискорд """
    def update_rpc(self):
        print('Обновление')

        self.RPC.update(
            state = self.state,
            details = self.details,
            large_image = "big-image",
            large_text = "Rhythmbox",
            small_image = self.small_image,
            small_text = self.small_text
        )


class MyPlugin(GObject.Object, Peas.Activatable):
    object = GObject.Property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)

        self.activated = None
        self.rpc_loop = None
        self.RPC = None

    def do_activate(self):
        print("Plugin activated")

        # Без этой переменной жизнь будет тяжелее
        self.sp = self.object.props.shell_player

        # Создаём класс
        self.RPC = EditingRPC()

        # Подключаем изменения к функции
        self.sp.connect('playing-changed', self.change_rpc)

    def do_deactivate(self):
        print("Plugin deactivated")

        # self.rpc_loop = None
        self.RPC.disconect()
        self.RPC = None

    def change_rpc(self, event, event2):
        # "Внутренности" музыки
        playing_entry = None
        if self.sp:
            playing_entry = self.sp.get_playing_entry()

        if playing_entry is None:  # Если внутренности пусты
            self.RPC.change_values(
                state = None,
                details = "Бездействует",
                small_image = "stop",
                small_text = "Остановлено"
            )
        else:  # Иначе
            # из внутренностей вынимаем...
            artist = playing_entry.get_string(RB.RhythmDBPropType.ARTIST)  # имя автора
            title = playing_entry.get_string(RB.RhythmDBPropType.TITLE)  # название музыки
            location = playing_entry.get_string(RB.RhythmDBPropType.LOCATION)  # её местоположение (в инете или на ПК)

            # Эти переменные нужны для маленькой картинки
            is_playing = self.sp.get_playing()[1]  # Воспроизводится ли сейчас музыка или нет (true если да)
            playing_image = "start" if is_playing else "pause"  # Тут указывается именно имя ассета, а не имя файла
            playing_text = "Воспроизведение" if is_playing else "Пауза"  # Текст при наведении на маленькую картинку

            # Вставляемые в rpc строки
            state = None
            details = None

            if location.startswith('http'):  # Зачастую (если не всегда) это радио
                if radio_up is not None:
                    details = radio_up.replace('{{TITLE}}', title)
                if radio_down is not None:
                    state = radio_down.replace('{{TITLE}}', title)
            elif artist == 'Unknown' or artist == '':  # Если не указан артист, значит это рандомный файл. Не указываем его.
                if file_up is not None:
                    details = file_up.replace('{{FILENAME}}', title)
                if file_down is not None:
                    state = file_down.replace('{{FILENAME}}', title)
            else:  # Иначе это музыка. Вставляем полученную информацию
                if music_up is not None:
                    details = music_up.replace('{{AUTHOR}}', artist).replace('{{TITLE}}', title)
                if music_down is not None:
                    state = music_down.replace('{{AUTHOR}}', artist).replace('{{TITLE}}', title)

            if state and len(state) > 150:  # Максимальная допустимая длинна - 150 символов
                state = state[:147] + "..."

            if details and len(details) > 150:
                details = details[:147] + "..."

            # Обновляем rpc
            self.RPC.change_values(
                state = state,
                details = details,
                small_image = playing_image,
                small_text = playing_text
            )
