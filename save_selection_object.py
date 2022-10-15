"""
Save and restore selection of objects in object mode
"""

import bpy

class SaveSelection(bpy.types.Operator):
    bl_idname = "scene.save_selection"
    bl_label = "Save Selection"
    bl_description = "Temporary save selected objects"

    def execute(self, context):
        bpy.ops.ed.undo_push()
        selection = context.selected_objects
        bpy.context.scene['SavedSelection'] = selection

        return {"FINISHED"}


class RestoreSelected(bpy.types.Operator):
    bl_idname = "scene.restore_selection"
    bl_label = "Restore Selection"
    bl_description = "Restore temporary saved object selection"


    def execute(self, context):
        bpy.ops.ed.undo_push()
        try:selection = context.scene.get('SavedSelection')
        except:selection = None

        if selection != None:
            names = []
            for i in selection:
                names.append(i.name)

            for obj in bpy.data.objects:
                # Check if object names match
                if obj.name in names:
                    obj.select_set(True)
                else:
                    obj.select_set(False)

        return {"FINISHED"}