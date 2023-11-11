#!/bin/env python3
import sys
sys.dont_write_bytecode = True
from time import sleep
from requests import get
from traceback import format_exc
from os import system
from os.path import dirname, realpath, join, isfile

sys.path.append("./../")
from utils import image_converter, skin_converter, poop_converter   
from utils.lang_manager import get_loc, set_lang, get_lang_list, lang_exists, init as init_lang

from PIL import Image

script_dir = dirname(realpath(sys.executable if getattr(sys, 'frozen', False) else __file__))

lang = "en"

lang_save_path = join(script_dir, "tric_console_lang.txt")

def save_lang(lang: str):
    with open(lang_save_path, "w") as lang_save:
        lang_save.write(lang)

if isfile(lang_save_path):
    with open(lang_save_path) as lang_save:
        lang = lang_save.read()
else:
    save_lang(lang)

try:
    init_lang(join(script_dir, "..", "lang", "console"), lang)
except Exception as e:
    print(f"Language manager initialization failed: {e}")
    sleep(5)
    exit(1)


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
    last_mode = 4
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
        save_lang(new_lang)
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
        image_path = input(get_loc("image_path_prompt"))
    if action == 2:
        skin = input(get_loc("skin_code_prompt"))
    level_path = input(get_loc("level_path_prompt"))

    system(clear_command)
    try:
        x = float(input(get_loc("x_prompt")).replace(",", "."))
        y = float(input(get_loc("y_prompt")).replace(",", "."))
    except ValueError:
        print(get_loc("float_parse_error"))
        continue

    if mode == 1 or mode == 3:
        pix_units = get_loc("units_blocks")
    if mode == 2 or mode == 4:
        pix_units = get_loc("units_text")

    system(clear_command)
    try:
        pix_size = float(input(get_loc("pixsize_prompt", pix_units)).replace(",","."))
    except ValueError:
        print(get_loc("float_parse_error"))
        continue

    if mode == 1 or mode == 3:
        system(clear_command)
        layer = int(input(get_loc("layer_prompt")))

    tol = 0
    try:
        if mode == 3 or mode == 4:
            tol = int(input(get_loc("tol_prompt")))
        if (tol < 0 or tol > 255):
            print(get_loc("wrong_tol"))
            continue
    except ValueError:
        get_loc("int_parse_error")

    if mode == 4:
        close_all_tags = input(get_loc("close_all_tags_prompt", get_loc("yes"))).lower() == get_loc("yes")
    system(clear_command)
    rewrite = input(get_loc("rewrite_prompt", get_loc("yes"))).lower()

    is_rewrite = rewrite == get_loc("yes")

    try:
        system(clear_command)
        print(get_loc("please_wait"))
        if action == 1:
            image = Image.open(image_path)
        if action == 2:
            image = skin_converter.to_image(skin)
        if mode == 1:
            image_converter.to_blocks(image.convert('RGBA'), level_path, pix_size, layer, is_rewrite, x, y)
        elif mode == 2:
            image_converter.to_text(image.convert('RGBA'), level_path, pix_size, x, y, rewrite = is_rewrite)
        elif mode == 3:
            poop_converter.to_blocks(image.convert('RGBA'), level_path, pix_size, layer, is_rewrite, x, y, tol)
        elif mode == 4:
            poop_converter.to_text(image.convert('RGBA'), level_path, pix_size, x, y, is_rewrite, tol, close_all_tags)
        print(get_loc("success"))
    except Exception as e:
        print(get_loc("error", format_exc()))
    sleep(2)
