from gi.repository import GObject, Peas, RB
from pypresence import Presence
import time
import threading


class MyPlugin(GObject.Object, Peas.Activatable):
    object = GObject.Property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)

        self.activated = None
        self.rpc_while = None
        self.RPC = None

    def do_activate(self):
        print("Plugin activated")

        # Возможно можно обойтись и без этой переменной, но я не нашёл документации, поэтому писал, считай, с закрытыми глазами
        self.activated = True

        # Без этой переменной жизнь будет тяжелее
        self.sp = self.object.props.shell_player

        # Коннектимся
        self.RPC = Presence('972548831747125259')
        self.RPC.connect()

        # Создаём поток, в котором будет крутиться цикл
        self.rpc_while = threading.Thread(target=self.change_rpc, args=())
        self.rpc_while.start()

    def do_deactivate(self):
        print("Plugin deactivated")

        # Деактивируем плагин, в переменной указываем, что плагин выключен. В общем, вырубаемся.
        self.activated = False
        self.rpc_while = None
        self.RPC = None

    def change_rpc(self):
        while self.activated:
            playing_entry = None
            if self.sp:
                playing_entry = self.sp.get_playing_entry()

            if playing_entry is None:
                self.RPC.update(
                    details="Бездействует",
                    large_image="big-image",
                    large_text="Rhythmbox",
                    small_image="stop",
                    small_text="Остановлено"
                )
            else:
                artist = playing_entry.get_string(RB.RhythmDBPropType.ARTIST)  # Имя артиста
                title = playing_entry.get_string(RB.RhythmDBPropType.TITLE)  # Имя музыки
                playing_location = playing_entry.get_string(RB.RhythmDBPropType.LOCATION)  # Её местоположение (в инете или тут)
                playing_type = self.sp.get_playing()[1]  # Воспроизводится ли сейчас музыка или нет
                playing_image = None  # Инициализируем заранее
                playing_text = None

                # Это нужно для маленьких картинок
                if playing_type:
                    playing_image = "start"
                    playing_text = "Воспроизведение"
                else:
                    playing_image = "pause"
                    playing_text = "Пауза"

                if not (artist == '' or artist == 'Unknown') and (title is not None):
                    text = artist + " - " + title
                    if len(text) > 150:
                        text = text[:147] + "..."

                    self.RPC.update(
                        details="Слушает музыку",
                        state=text,
                        large_image="big-image",
                        large_text="Rhythmbox",
                        small_image=playing_image,
                        small_text=playing_text
                    )
                elif playing_location[:4] == 'http':  # Зачастую (если не всегда) это радио
                    if len(title) > 150:
                        title = title[:147] + "..."

                    self.RPC.update(
                        details="Слушает радио",
                        state=title,
                        large_image="big-image",
                        large_text="Rhythmbox",
                        small_image=playing_image,
                        small_text=playing_text
                    )
                else:  # Если это файл и мы не знаем его автора, то это какой-то рандом файл, название которого указывать, думаю, не стоит.
                    self.RPC.update(
                        details="Слушает аудиофайл",
                        large_image="big-image",
                        large_text="Rhythmbox",
                        small_image=playing_image,
                        small_text=playing_text
                    )

            time.sleep(15)
