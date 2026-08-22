# MIT License

# Copyright (c) 2017 GiveMeAllYourCats

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Code author: GiveMeAllYourCats
# Repo: https://github.com/michaeldegroot/cats-blender-plugin
# Edits by: GiveMeAllYourCats, Hotox
import re
import os
import bpy
import copy
import json
import pathlib
import traceback
import collections

from collections import OrderedDict

from . import common as Common
from .register import register_wrap
from .. import globs
from .translations import t

dictionary = {}

main_dir = pathlib.Path(os.path.dirname(__file__)).parent.resolve()
resources_dir = os.path.join(str(main_dir), "resources")
dictionary_file = os.path.join(resources_dir, "dictionary.json")


@register_wrap
class TranslateShapekeyButton(bpy.types.Operator):
    bl_idname = 'cats_translate.shapekeys'
    bl_label = t('TranslateShapekeyButton.label')
    bl_description = t('TranslateShapekeyButton.desc')
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):

        saved_data = Common.SavedData()

        to_translate = []

        for mesh in Common.get_meshes_objects(mode=2):
            if Common.has_shapekeys(mesh):
                for shapekey in mesh.data.shape_keys.key_blocks:
                    if 'vrc.' not in shapekey.name and shapekey.name not in to_translate:
                        to_translate.append(shapekey.name)

        update_dictionary(to_translate, translating_shapes=True, self=self)

        Common.update_shapekey_orders()

        i = 0
        for mesh in Common.get_meshes_objects(mode=2):
            if Common.has_shapekeys(mesh):
                for shapekey in mesh.data.shape_keys.key_blocks:
                    if 'vrc.' not in shapekey.name:
                        shapekey.name, translated = translate(shapekey.name, add_space=True, translating_shapes=True)
                        if translated:
                            i += 1

        Common.ui_refresh()

        saved_data.load()

        self.report({'INFO'}, t('TranslateShapekeyButton.success', number=str(i)))
        return {'FINISHED'}


@register_wrap
class TranslateBonesButton(bpy.types.Operator):
    bl_idname = 'cats_translate.bones'
    bl_label = t('TranslateBonesButton.label')
    bl_description = t('TranslateBonesButton.desc')
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if not Common.get_armature():
            return False
        return True

    def execute(self, context):
        to_translate = []
        for armature in Common.get_armature_objects():
            for bone in armature.data.bones:
                to_translate.append(bone.name)

        update_dictionary(to_translate, self=self)

        count = 0
        for armature in Common.get_armature_objects():
            for bone in armature.data.bones:
                bone.name, translated = translate(bone.name)
                if translated:
                    count += 1

        self.report({'INFO'}, t('TranslateBonesButton.success', number=str(count)))
        return {'FINISHED'}


@register_wrap
class TranslateObjectsButton(bpy.types.Operator):
    bl_idname = 'cats_translate.objects'
    bl_label = t('TranslateObjectsButton.label')
    bl_description = t('TranslateObjectsButton.desc')
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        to_translate = []
        for obj in Common.get_objects():
            if obj.name not in to_translate:
                to_translate.append(obj.name)
            if obj.type == 'ARMATURE':
                if obj.data and obj.data.name not in to_translate:
                    to_translate.append(obj.data.name)
                if obj.animation_data and obj.animation_data.action:
                    to_translate.append(obj.animation_data.action.name)

        update_dictionary(to_translate, self=self)

        i = 0
        for obj in Common.get_objects():
            obj.name, translated = translate(obj.name)
            if translated:
                i += 1

            if obj.type == 'ARMATURE':
                if obj.data:
                    obj.data.name, translated = translate(obj.data.name)
                    if translated:
                        i += 1

                if obj.animation_data and obj.animation_data.action:
                    obj.animation_data.action.name, translated = translate(obj.animation_data.action.name)
                    if translated:
                        i += 1

        self.report({'INFO'}, t('TranslateObjectsButton.success', number=str(i)))
        return {'FINISHED'}


@register_wrap
class TranslateMaterialsButton(bpy.types.Operator):
    bl_idname = 'cats_translate.materials'
    bl_label = t('TranslateMaterialsButton.label')
    bl_description = t('TranslateMaterialsButton.desc')
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        saved_data = Common.SavedData()

        to_translate = []
        for mesh in Common.get_meshes_objects(mode=2):
            for matslot in mesh.material_slots:
                if matslot.name not in to_translate:
                    to_translate.append(matslot.name)

        update_dictionary(to_translate, self=self)

        i = 0
        for mesh in Common.get_meshes_objects(mode=2):
            Common.set_active(mesh)
            for index, matslot in enumerate(mesh.material_slots):
                mesh.active_material_index = index
                if bpy.context.object.active_material:
                    bpy.context.object.active_material.name, translated = translate(bpy.context.object.active_material.name)
                    if translated:
                        i += 1

        saved_data.load()
        self.report({'INFO'}, t('TranslateMaterialsButton.success', number=str(i)))
        return {'FINISHED'}


@register_wrap
class TranslateAllButton(bpy.types.Operator):
    bl_idname = 'cats_translate.all'
    bl_label = t('TranslateAllButton.label')
    bl_description = t('TranslateAllButton.desc')
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):

        error_shown = False

        try:
            if Common.get_armature():
                bpy.ops.cats_translate.bones('INVOKE_DEFAULT')
        except RuntimeError as e:
            self.report({'ERROR'}, str(e).replace('Error: ', ''))
            error_shown = True

        try:
            bpy.ops.cats_translate.shapekeys('INVOKE_DEFAULT')
        except RuntimeError as e:
            if not error_shown:
                self.report({'ERROR'}, str(e).replace('Error: ', ''))
                error_shown = True

        try:
            bpy.ops.cats_translate.objects('INVOKE_DEFAULT')
        except RuntimeError as e:
            if not error_shown:
                self.report({'ERROR'}, str(e).replace('Error: ', ''))
                error_shown = True

        try:
            bpy.ops.cats_translate.materials('INVOKE_DEFAULT')
        except RuntimeError as e:
            if not error_shown:
                self.report({'ERROR'}, str(e).replace('Error: ', ''))
                error_shown = True

        if error_shown:
            return {'CANCELLED'}
        self.report({'INFO'}, t('TranslateAllButton.success'))
        return {'FINISHED'}


# Loads the dictionaries at the start of blender
def load_translations():
    global dictionary
    dictionary = OrderedDict()
    temp_dict = OrderedDict()
    dict_found = False

    # Load internal dictionary
    try:
        with open(dictionary_file, encoding="utf8") as file:
            temp_dict = json.load(file, object_pairs_hook=collections.OrderedDict)
            dict_found = True
    except FileNotFoundError:
        print('DICTIONARY NOT FOUND!')
        pass
    except json.decoder.JSONDecodeError:
        print("ERROR FOUND IN DICTIONARY")
        pass

    # Sort temp dictionary by length and put it into the global dict
    for key in sorted(temp_dict, key=lambda k: len(k), reverse=True):
        dictionary[key] = temp_dict[key]

    return dict_found


def update_dictionary(to_translate_list, translating_shapes=False, self=None):
    global dictionary

    # Check if single string is given and put it into an array
    if type(to_translate_list) is str:
        to_translate_list = [to_translate_list]

    # Translate everything using the offline dictionary only
    for to_translate in to_translate_list:
        to_translate = fix_jp_chars(to_translate)

        for key, value in dictionary.items():
            if key in to_translate:
                if value:
                    to_translate = to_translate.replace(key, value)

    return


def translate(to_translate, add_space=False, translating_shapes=False):
    global dictionary

    pre_translation = to_translate
    length = len(to_translate)
    translated_count = 0

    # Add space for shape keys
    addition = ''
    if add_space:
        addition = ' '

    # Convert half chars into full chars
    to_translate = fix_jp_chars(to_translate)

    # Translate with internal dictionary
    for key, value in dictionary.items():
        if key in to_translate:
            # If string is empty, don't replace it. This will be done at the end
            if not value:
                continue

            to_translate = to_translate.replace(key, addition + value)

            # Check if string is fully translated
            translated_count += len(key)
            if translated_count >= length:
                break

    to_translate = to_translate.replace('.L', '_L').replace('.R', '_R').replace('  ', ' ').replace('し', '').replace('っ', '').strip()

    return to_translate, pre_translation != to_translate


# Half-width to full-width Japanese character mapping
_jp_half_to_full = {
    0xFF61: 0x3002, 0xFF62: 0x300C, 0xFF63: 0x300D, 0xFF64: 0x3001,
    0xFF65: 0x30FB, 0xFF66: 0x30F2, 0xFF67: 0x30A1, 0xFF68: 0x30A3,
    0xFF69: 0x30A5, 0xFF6A: 0x30A7, 0xFF6B: 0x30A9, 0xFF6C: 0x30E3,
    0xFF6D: 0x30E5, 0xFF6E: 0x30E7, 0xFF6F: 0x30C3, 0xFF70: 0x30FC,
    0xFF71: 0x30A2, 0xFF72: 0x30A4, 0xFF73: 0x30A6, 0xFF74: 0x30A8,
    0xFF75: 0x30AA, 0xFF76: 0x30AB, 0xFF77: 0x30AD, 0xFF78: 0x30AF,
    0xFF79: 0x30B1, 0xFF7A: 0x30B3, 0xFF7B: 0x30B5, 0xFF7C: 0x30B7,
    0xFF7D: 0x30B9, 0xFF7E: 0x30BB, 0xFF7F: 0x30BD, 0xFF80: 0x30BF,
    0xFF81: 0x30C1, 0xFF82: 0x30C4, 0xFF83: 0x30C6, 0xFF84: 0x30C8,
    0xFF85: 0x30CA, 0xFF86: 0x30CB, 0xFF87: 0x30CC, 0xFF88: 0x30CD,
    0xFF89: 0x30CE, 0xFF8A: 0x30CF, 0xFF8B: 0x30D2, 0xFF8C: 0x30D5,
    0xFF8D: 0x30D8, 0xFF8E: 0x30DB, 0xFF8F: 0x30DE, 0xFF90: 0x30DF,
    0xFF91: 0x30E0, 0xFF92: 0x30E1, 0xFF93: 0x30E2, 0xFF94: 0x30E4,
    0xFF95: 0x30E6, 0xFF96: 0x30E8, 0xFF97: 0x30E9, 0xFF98: 0x30EA,
    0xFF99: 0x30EB, 0xFF9A: 0x30EC, 0xFF9B: 0x30ED, 0xFF9C: 0x30EF,
    0xFF9D: 0x30F3, 0xFF9E: 0x309B, 0xFF9F: 0x309C,
}


def fix_jp_chars(name):
    return name.translate(_jp_half_to_full)
