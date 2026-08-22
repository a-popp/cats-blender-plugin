if "bpy" not in locals():
    # print('STARTUP UI!!')
    import bpy
    from . import main
    from . import armature
    from . import manual
    from . import custom
    from . import decimation
    from . import visemes
    from . import optimization
    from . import bake
else:
    # print('RELOAD UI!!')
    import importlib
    importlib.reload(main)
    importlib.reload(armature)
    importlib.reload(manual)
    importlib.reload(custom)
    importlib.reload(decimation)
    importlib.reload(visemes)
    importlib.reload(optimization)
    importlib.reload(bake)
