from json import load as json_load
from os import walk
from os.path import join

langs = {}
current_lang = "en"

def set_lang(lang: str):
    global current_lang
    if lang in langs:
        current_lang = lang
    else:
        raise Exception("Language not found")


def init(lang_path: str, lang: str = "en"):
    walk_result = walk(lang_path)
    for (dirpath, dirnames, filenames) in walk_result:
        for filename in filenames:
            file_path = join(lang_path, filename)
            with open(file_path, encoding="utf-8") as lang_file:
                langs[filename.removesuffix(".json")] = json_load(lang_file)
    set_lang(lang)

def get_loc(key: str, *format_args):
    if (key not in langs[current_lang]):
        raise Exception("Key not found")
    if len(format_args) > 0:
        try:
            return str.format(langs[current_lang][key], *format_args)
        except IndexError:
            pass
    return str(langs[current_lang][key])

def get_lang_list():
    return [f"{lang}{(' (' + langs[lang]['lang_name'] + ')') if 'lang_name' in langs[lang] else ''}" for lang in langs]

def lang_exists(lang):
    return lang in langs