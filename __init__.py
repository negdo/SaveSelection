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
    "version": (0, 7, 2),
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
else:
    from . import save_selection_edit
    from . import save_selection_object
    from . import draw
    from . import preferences


def register():
    bpy.utils.register_class(Preferences)
    bpy.utils.register_class(ApplyPreferences)

    preferences = bpy.context.preferences.addons[__name__].preferences

    if preferences.object_enable:
        bpy.utils.register_class(SaveSelection)
        bpy.utils.register_class(RestoreSelected)
        bpy.types.VIEW3D_MT_object_context_menu.append(draw_save_selected_menu)
    if preferences.edit_enable:
        bpy.utils.register_class(SaveSelectionEdit)
        bpy.utils.register_class(RestoreSelectedEdit)
        bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(draw_save_selected_edit_menu)
    
    print("SaveSelection registered")

def unregister():
    try:
        bpy.types.VIEW3D_MT_object_context_menu.remove(draw_save_selected_menu)
        bpy.utils.unregister_class(RestoreSelected)
        bpy.utils.unregister_class(SaveSelection)
    except: pass
    try:
        bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_save_selected_edit_menu)
        bpy.utils.unregister_class(SaveSelectionEdit)
        bpy.utils.unregister_class(RestoreSelectedEdit)
    except: pass

    bpy.utils.unregister_class(Preferences)
    bpy.utils.unregister_class(ApplyPreferences)