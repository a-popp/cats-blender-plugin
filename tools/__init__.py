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

if "bpy" not in locals():
    # print('STARTUP TOOLS!!')
    import bpy
    from . import register
    from . import armature_bones
    from . import armature_manual
    from . import armature_custom
    from . import bonemerge
    from . import common
    from . import decimation
    from . import export
    from . import material
    from . import rootbone
    from . import bake
    from . import settings
    from . import shapekey
    from . import translate
    from . import translations
    from . import viseme
else:
    # print('RELOAD TOOLS!!')
    import importlib
    importlib.reload(register)  # Has to be first
    importlib.reload(armature_bones)
    importlib.reload(armature_manual)
    importlib.reload(armature_custom)
    importlib.reload(bonemerge)
    importlib.reload(common)
    importlib.reload(decimation)
    importlib.reload(export)
    importlib.reload(material)
    importlib.reload(rootbone)
    importlib.reload(bake)
    importlib.reload(settings)
    importlib.reload(shapekey)
    importlib.reload(translate)
    importlib.reload(translations)
    importlib.reload(viseme)
