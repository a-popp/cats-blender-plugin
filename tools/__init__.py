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
