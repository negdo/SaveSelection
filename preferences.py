import bpy
from bpy.props import BoolProperty
import importlib
import sys
from .save_selection_object import *
from .save_selection_edit import *
from .draw import *
from .preferences import *


class Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__
 
    object_enable: BoolProperty(
        name="Object Mode",
        default=True
    )

    edit_enable: BoolProperty(
        name="Edit Mode",
        default=True
    )
 
    def draw(self, context):
        layout = self.layout
        layout.label(text='Enable Save Selection:')
        split = layout.split(factor=0.3)
        col1,col2 = (split.column(),split.column())
        col2.prop(self, 'object_enable', expand=True)
        col2.prop(self, 'edit_enable', expand=True)
        col2.operator("scene.apply_preferences_save_selection")


class ApplyPreferences(bpy.types.Operator):
    bl_idname = "scene.apply_preferences_save_selection"
    bl_label = "Apply"
 
    def execute(self, context):
        preferences = bpy.context.preferences.addons[__package__].preferences
        try:
            bpy.types.VIEW3D_MT_object_context_menu.remove(draw_save_selected_menu)
            bpy.utils.unregister_class(RestoreSelected)
            bpy.utils.unregister_class(SaveSelection)
            if preferences.object_enable:
                bpy.utils.register_class(SaveSelection)
                bpy.utils.register_class(RestoreSelected)
        except:
            if preferences.object_enable:
                bpy.utils.register_class(SaveSelection)
                bpy.utils.register_class(RestoreSelected)
                bpy.types.VIEW3D_MT_object_context_menu.append(draw_save_selected_menu)
        try:
            bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_save_selected_edit_menu)
            bpy.utils.unregister_class(SaveSelectionEdit)
            bpy.utils.unregister_class(RestoreSelectedEdit)
            if preferences.edit_enable:
                bpy.utils.register_class(SaveSelectionEdit)
                bpy.utils.register_class(RestoreSelectedEdit)
        except:
            if preferences.edit_enable:
                bpy.utils.register_class(SaveSelectionEdit)
                bpy.utils.register_class(RestoreSelectedEdit)
                bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(draw_save_selected_edit_menu)

        return {'FINISHED'}