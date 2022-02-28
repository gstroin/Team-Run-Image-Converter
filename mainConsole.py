#Импорт стандартных библиотек.
import sys
import time
import requests
import traceback

#Импорт собственных библиотек
from utils import ImgConv, skinConverter

#Импорт сторонних библиотек.
from PIL import Image

version = "0.8.0"


def VersionCheck(ver):
    lastVer = requests.get("https://pastebin.com/raw/ba8FfNW5").text
    if version != lastVer:
        print("Вышла новая версия: " + lastVer + "!")


print("Team Run Image Converter by gstroin (Console) v. " + version)

#Проверяем версию, ачё.
try:
    VersionCheck(version)
except:
    #И срём на неё, в случае ошибки как отсутствие подключения.
    pass

time.sleep(2)
print()

#Дальше мне ООООЧЕНЬ лень что-либо комментировать.
#это говнокод.

while True:
    action = 0
    mode = 0
    print("1. Конвертировать изображение\n2. Конвертировать скин\n3. Выйти\n")
    lastAction = 3
    lastMode = 2
    try:
        action = int(input("Что вы хотите сделать?: "))
    except ValueError:
        print("\nПожалуйста, введите число, а не слово\n")
        continue
    if action > lastAction or action < 1:
        print("\nНеверное действие!\n")
        continue
    if action == 3:
        break

    print("\nВыберите режим:\n1. Блоки (можно настроить слой, весит меньше, лагает на слабых устройствах, быстрее загружается)\n2. Текст (всего один объект, нельзя настроить слой, загружается дольше, вес больше, можно использовать в никах и названиях этажей)\n")
    try:
        mode = int(input("Режим: "))
    except ValueError:
        print("\nРежим должен быть целым числом.\n")
        continue
    if mode > lastMode or mode < 1:
        print("Неверный номер режима!")
        continue
    
    if action == 1:
        _imagePath = input("Путь к изображению: ")
    if action == 2:
        skin = input("Код скина: ")
    print()
    _levelPath = input("Путь к уровню: ")
    print()

    try:
        x = float(input("Координата X, на которой будет размещено изображение: ").replace(",", "."))
        print()
        y = float(input("Координата Y, на которой будет размещено изображение: ").replace(",", "."))
        print()
    except ValueError:
        print("\nОшибка: Координаты должны быть числами.\n")
        continue

    if mode == 1:
        pixUnits = "в блоках"
    if mode == 2:
        pixUnits = "в пикселях"
    _pixSize = float(input("Размер каждого пикселя изображения (" + pixUnits + "): ").replace(",","."))
    print()

    if mode == 1:
        _layer = int(input("Слой: "))
        print()

    rewrite = input("Перезаписать уровень? (да или нет): ").lower()
    print()

    if rewrite == "да":
        isRewrite = True
    else:
        isRewrite = False

    try:
        print("Пожалуйста, подождите...")
        if action == 1:
            image = Image.open(_imagePath)
        if action == 2:
            image = skinConverter.toPNG(skin)
        if mode == 1:
            ImgConv.Convert(image.convert('RGBA'), _levelPath, _pixSize, _layer, isRewrite, x, y)
        elif mode == 2:
            ImgConv.pictureToText(image.convert('RGBA'), _levelPath, _pixSize, x, y, isRewrite)
        print("Успешно!")
        time.sleep(2)
    except Exception as e:
        print("Ошибка:\n" + traceback.format_exc())
        time.sleep(2)
