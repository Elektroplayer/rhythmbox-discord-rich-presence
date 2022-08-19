# rhythmbox-discord-rich-presence
Плагин для Rhythmbox, который отображает вашу музыку в статусе Discord.

## Примеры

![](https://media.discordapp.net/attachments/718825926321897504/976487450325184592/unknown.png)

![](https://media.discordapp.net/attachments/718825926321897504/976498387346133062/unknown.png)

![](https://media.discordapp.net/attachments/718825926321897504/976487631166787654/unknown.png)

![](https://media.discordapp.net/attachments/718825926321897504/976487739111399504/unknown.png)

![](https://media.discordapp.net/attachments/718825926321897504/976488160710254653/unknown.png)

## Замечание!

Чтобы плагин отображал, что вы слушаете именно музыку, а не аудиофайл, укажите в свойствах всех песен автора и название песни.

## Установка

### **Полуавтоматическая**

Просто последовательно вводите команды:

```bash
pip install pypresence
cd ~/.local/share/rhythmbox/plugins/
git clone https://github.com/Elektroplayer/rhythmbox-discord-rich-presence.git
```

*Если у вас возникла ошибка на второй команде, то возможно, такой папки не существует. Просто создайте её и продолжайте выполнение команд.*

После выполенения команд перезагрузите Rhythmbox и включите плагин *Discord Rich Presence* в настройках.

### **Автоматическая**

*TODO*

## Обноление

Зайдите в папку с плагином и напишите команду:
```bash
git pull
```
Плагин автоматически обновится до последней версии. 

## Лицензия

[GPL-3.0](./LICENSE)<br>
Copyright © 2022 Vitaliy Havanski
