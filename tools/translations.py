# MIT License
#
# Copyright (c) 2017 GiveMeAllYourCats
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Thanks to https://www.thegrove3d.com/learn/how-to-translate-a-blender-addon/ for the idea

import os
import csv
import bpy
import json
import pathlib
from bpy.app.translations import locale

from .register import register_wrap

main_dir = pathlib.Path(os.path.dirname(__file__)).parent.resolve()
resources_dir = os.path.join(str(main_dir), "resources")
translations_file = os.path.join(resources_dir, "translations.csv")

dictionary = {}
languages = []
verbose = True


def load_translations():
    global dictionary, languages
    dictionary = {}
    languages = ["auto"]

    # Check the settings which translation to load
    language = get_language_from_settings()

    with open(translations_file, 'r', encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        if not csv_reader:
            return

        for i, row in enumerate(csv_reader):
            # print(row)
            text = row.get(language)
            if not text:
                text = row.get('en_US')
            dictionary[row['name']] = text

            # get all current languages
            if i == 0:
                for key in row.keys():
                    if '_' in key:
                        languages.append(key)

    check_missing_translations()


def t(phrase: str, *args, **kwargs):
    # Translate the given phrase into Blender's current language.
    output = dictionary.get(phrase)
    if output is None:
        if verbose:
            print('Warning: Unknown phrase: ' + phrase)
        return phrase

    return output.format(*args, **kwargs)


def check_missing_translations():
    for key, value in dictionary.items():
        if not value and verbose:
            print('Translations en_US: Value missing for key: ' + key)


def get_languages_list(self, context):
    choices = []

    for language in languages:
        # 1. Will be returned by context.scene
        # 2. Will be shown in lists
        # 3. will be shown in the hover description (below description)
        choices.append((language, language, language))

    bpy.types.Object.Enum = choices
    return bpy.types.Object.Enum


def update_ui(self, context):
    from . import settings
    lang_changed = (settings.settings_data or {}).get('ui_lang') != context.scene.ui_lang
    settings.update_settings(self, context)
    if lang_changed:
        reload_scripts()


def get_language_from_settings():
    # Compute the settings path here instead of importing tools/settings.py.
    # That module imports tools/translate.py, which imports this module, so
    # importing it while load_translations() runs during module init would be
    # a circular import and leave the dictionary empty while translate.py's
    # class attributes are being evaluated.
    try:
        settings_file = bpy.utils.extension_path_user(
            __package__.rpartition('.')[0] or __package__, path="settings.json")
    except (AttributeError, ValueError, TypeError):
        settings_file = os.path.join(resources_dir, "settings.json")

    # Load settings file
    try:
        with open(settings_file, encoding="utf8") as file:
            settings_data = json.load(file)
    except FileNotFoundError:
        print("SETTINGS FILE NOT FOUND!")
        return
    except json.decoder.JSONDecodeError:
        print("ERROR FOUND IN SETTINGS FILE")
        return

    if not settings_data:
        print("NO DATA IN SETTINGS FILE")
        return

    lang = settings_data.get("ui_lang")
    if not lang or "auto" in lang.lower():
        return locale

    return lang


def reload_scripts():
    bpy.ops.script.reload()


load_translations()