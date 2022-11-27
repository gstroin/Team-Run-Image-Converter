import sys
sys.dont_write_bytecode = True
from time import sleep
from requests import get
from traceback import format_exc
from os import system
from os.path import dirname, realpath, join

from utils import image_converter, skin_converter, lang_manager
from utils.lang_manager import get_loc, set_lang, get_lang_list, lang_exists, init as init_lang

from PIL import Image

init_lang(join(dirname(realpath(sys.executable if getattr(sys, 'frozen', False) else __file__)), "lang\\console\\"))


version = "0.9.0"
clear_command = "cls" if sys.platform == "win32" else "clear"


def version_check():
    last_ver = get("https://pastebin.com/raw/ba8FfNW5").text
    if version != last_ver:
        print(get_loc("new_ver", last_ver))


print(get_loc("title", version))

try:
    version_check()
except:
    pass


while True:
    action = 0
    mode = 0
    print(get_loc("main_menu"))
    last_action = 4
    last_mode = 2
    try:
        action = int(input(get_loc("action_prompt")))
    except ValueError:
        print(get_loc("int_parse_error"))
        continue
    if action > last_action or action < 1:
        print(get_loc("wrong_action"))
        continue
    if action == 3:
        break
    if action == 4:
        new_lang = None
        lang_list = get_lang_list()
        system(clear_command)
        while new_lang == None:
            print(get_loc("available_languages"))
            print('\n'.join(lang_list))
            input_result = input(get_loc("new_lang_prompt")) 
            if lang_exists(input_result):
                new_lang = input_result
            else:
                system(clear_command)
                print(get_loc("wrong_lang"))
        set_lang(new_lang)
        system(clear_command)
        continue
    
    system(clear_command)
    print(get_loc("mode_select"))
    try:
        mode = int(input(get_loc("mode_prompt")))
    except ValueError:
        print(get_loc("int_parse_error"))
        continue
    if mode > last_mode or mode < 1:
        print(get_loc("wrong_mode"))
        continue
    
    system(clear_command)
    if action == 1:
        _imagePath = input(get_loc("image_path_prompt"))
    if action == 2:
        skin = input(get_loc("skin_code_prompt"))
    _levelPath = input(get_loc("level_path_prompt"))

    system(clear_command)
    try:
        x = float(input(get_loc("x_prompt")).replace(",", "."))
        y = float(input(get_loc("y_prompt")).replace(",", "."))
    except ValueError:
        print(get_loc("float_parse_error"))
        continue

    if mode == 1:
        pixUnits = get_loc("units_blocks")
    if mode == 2:
        pixUnits = get_loc("units_text")

    system(clear_command)
    try:
        _pixSize = float(input(get_loc("pixsize_prompt", pixUnits)).replace(",","."))
    except ValueError:
        print(get_loc("float_parse_error"))

    if mode == 1:
        system(clear_command)
        _layer = int(input(get_loc("layer_prompt")))

    system(clear_command)
    rewrite = input(get_loc("rewrite_prompt", get_loc("yes"))).lower()

    isRewrite = rewrite == get_loc("yes")

    try:
        system(clear_command)
        print(get_loc("please_wait"))
        if action == 1:
            image = Image.open(_imagePath)
        if action == 2:
            image = skin_converter.to_image(skin)
        if mode == 1:
            image_converter.to_blocks(image.convert('RGBA'), _levelPath, _pixSize, _layer, isRewrite, x, y)
        elif mode == 2:
            image_converter.to_text(image.convert('RGBA'), _levelPath, _pixSize, x, y, rewrite = isRewrite)
        print(get_loc("success"))
    except Exception as e:
        print(get_loc("error", format_exc()))
    sleep(2)
