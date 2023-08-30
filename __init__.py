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
    "version": (2, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    "bl_options": {"REGISTER", "UNDO"} }

import importlib
import sys
from .save_selection import *
from .draw import *
from .properties import *
import bpy


if "bpy" in locals():
    try: importlib.reload(save_selection)
    except: from . import save_selection
    try: importlib.reload(draw)
    except: from . import draw
    try: importlib.reload(properties)
    except: from . import properties
else:
    from . import save_selection
    from . import draw
    from . import preferences
    from . import properties


def register():
    # properties for storing selections
    bpy.utils.register_class(SelectedObjects)
    bpy.utils.register_class(SavedSelection)
    bpy.types.Scene.saved_selections = bpy.props.CollectionProperty(type=SavedSelection)
    bpy.types.Scene.save_selection_list_index = bpy.props.IntProperty(default=-1)
    bpy.types.Scene.save_selection_index_max = bpy.props.IntProperty(default=-1)

    # operators
    bpy.utils.register_class(SaveSelection)
    bpy.utils.register_class(RestoreSelected)
    bpy.utils.register_class(DeleteSelection)
    bpy.utils.register_class(EditSelection)
    bpy.utils.register_class(SaveSelectionPanel)
    bpy.utils.register_class(SCENE_UL_save_selection_list)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_save_selected_menu)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(draw_save_selected_menu)


def unregister():
    try:
        bpy.types.VIEW3D_MT_object_context_menu.remove(draw_save_selected_menu)
        bpy.utils.unregister_class(RestoreSelected)
        bpy.utils.unregister_class(SaveSelection)
    except: pass
    try:
        bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_save_selected_menu)
        bpy.utils.unregister_class(RestoreSelected)
    except: pass

    bpy.utils.unregister_class(SaveSelectionPanel)
    bpy.utils.unregister_class(DeleteSelection)
    bpy.utils.unregister_class(EditSelection)
    bpy.utils.unregister_class(SCENE_UL_save_selection_list)
    