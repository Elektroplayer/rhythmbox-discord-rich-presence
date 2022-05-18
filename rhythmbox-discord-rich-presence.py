from gi.repository import GObject, Peas, RB
from pypresence import Presence
import time
import threading


class MyPlugin(GObject.Object, Peas.Activatable):
    object = GObject.Property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)

        self.activated = None
        self.rpc_loop = None
        self.RPC = None

    def do_activate(self):
        print("Plugin activated")

        # Возможно, можно обойтись и без этой переменной, но я не нашёл документации, поэтому писал, считай, с закрытыми глазами
        self.activated = True

        # Без этой переменной жизнь будет тяжелее
        self.sp = self.object.props.shell_player

        # Коннектимся
        self.RPC = Presence('972548831747125259')
        self.RPC.connect()

        # Создаём поток, в котором будет крутиться цикл
        self.rpc_loop = threading.Thread(target=self.change_rpc, args=())
        self.rpc_loop.start()

    def do_deactivate(self):
        print("Plugin deactivated")

        # Деактивируем плагин, в переменной указываем, что плагин выключен. В общем, вырубаемся.
        self.activated = False
        self.rpc_loop = None
        self.RPC = None

    def change_rpc(self):
        while self.activated:
            # "Внутренности" музыки
            playing_entry = None
            if self.sp:
                playing_entry = self.sp.get_playing_entry()

            if playing_entry is None:  # Если внутренности пусты
                self.RPC.update(
                    details="Бездействует",
                    large_image="big-image",
                    large_text="Rhythmbox",
                    small_image="stop",
                    small_text="Остановлено"
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
                    state = title
                    details = 'Слушает радио'
                elif artist == 'Unknown' or artist == '':  # Если неуказан артист, значит это рандомный файл. Не указываем его.
                    details = 'Слушает аудиофайл'
                else:  # Иначе это музыка. Вставляем полученную информацию
                    state = ' - '.join([artist, title])
                    details = 'Слушает музыку'

                if state and len(state) > 150:  # Максимальная допустимая длинна - 150 символов
                    state = state[:147] + "..."

                # Обновляем rpc
                self.RPC.update(
                    state=state,
                    details=details,
                    large_image="big-image",
                    large_text="Rhythmbox",
                    small_image=playing_image,
                    small_text=playing_text
                )

            time.sleep(15) # Чаще обновлять нельзя
