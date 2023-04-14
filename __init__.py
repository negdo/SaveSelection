'''
Copyright (C) 2022 Miha Marinko
miha.marinko20@gmail.com

Created by Miha Marinko

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Save Selection",
    "description": "Save and restore selection of objects/vertices/edges/faces",
    "author": "Miha Marinko",
    "version": (0, 9, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    "bl_options": {"REGISTER", "UNDO"} }

import importlib
import sys
from .save_selection_object import *
from .save_selection_edit import *
from .draw import *
from .preferences import *
from .properties import *
import bpy


if "bpy" in locals():
    try: importlib.reload(save_selection_edit)
    except: from . import save_selection_edit
    try: importlib.reload(save_selection_object)
    except: from . import save_selection_object
    try: importlib.reload(draw)
    except: from . import draw
    try: importlib.reload(preferences)
    except: from . import preferences
    try: importlib.reload(properties)
    except: from . import properties
else:
    from . import save_selection_edit
    from . import save_selection_object
    from . import draw
    from . import preferences
    from . import properties


def register():
    bpy.utils.register_class(Preferences)
    bpy.utils.register_class(ApplyPreferences)

    preferences = bpy.context.preferences.addons[__name__].preferences

    # properties for storing selections
    bpy.utils.register_class(SelectedObjects)
    bpy.utils.register_class(SavedSelection)
    bpy.types.Scene.saved_selections = bpy.props.CollectionProperty(type=SavedSelection)
    bpy.types.Scene.save_selection_index = bpy.props.IntProperty(default=-1)
    bpy.types.Scene.save_selection_index_max = bpy.props.IntProperty(default=-1)

    # operators
    bpy.utils.register_class(SaveSelection)
    bpy.utils.register_class(RestoreSelected)
    bpy.utils.register_class(SaveSelectionEdit)
    bpy.utils.register_class(SaveSelectionPanel)
    bpy.utils.register_class(WORLD_UL_my_list)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_save_selected_menu)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(draw_save_selected_edit_menu)


def unregister():
    try:
        bpy.types.VIEW3D_MT_object_context_menu.remove(draw_save_selected_menu)
        bpy.utils.unregister_class(RestoreSelected)
        bpy.utils.unregister_class(SaveSelection)
    except: pass
    try:
        bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_save_selected_edit_menu)
        bpy.utils.unregister_class(SaveSelectionEdit)
        bpy.utils.unregister_class(RestoreSelected)
    except: pass

    bpy.utils.unregister_class(Preferences)
    bpy.utils.unregister_class(ApplyPreferences)
    bpy.utils.unregister_class(SaveSelectionPanel)
    bpy.utils.unregister_class(WORLD_UL_my_list)