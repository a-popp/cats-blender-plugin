import bpy

# for bone root parenting
root_bones = {}
root_bones_choices = {}

# Keeps track of operations done for unit testing
testing = []

dev_branch = False
dict_found = False
version = None
version_str = ''

# other
time_format = "%Y-%m-%d %H:%M:%S"
time_format_github = "%Y-%m-%dT%H:%M:%SZ"

# Icons for UI
ICON_ADD, ICON_REMOVE = 'ADD', 'REMOVE'
ICON_SETTINGS = 'SETTINGS'
ICON_ALL = 'PROP_ON'
ICON_MOD_ARMATURE = 'MOD_ARMATURE'
ICON_POSE_MODE = 'POSE_HLT'
ICON_EXPORT = 'EXPORT'