import bpy

def draw_save_selected_menu(self, cotext):
    # add operator to context menu
    layout = self.layout
    layout.separator()
    layout.operator("scene.save_selection")
    layout.operator("scene.restore_selection")


class SaveSelectionPanel(bpy.types.Panel):
    bl_label = "Save Selection"
    bl_idname = "SCENE_PT_save_selection"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        # Draw the list of objects in the scene
        row = layout.row()

        col = row.column()
        #list
        col.template_list("SCENE_UL_save_selection_list", "", context.scene, "saved_selections", context.scene, "save_selection_list_index")

        # add and delete button
        col = row.column()
        col.operator("scene.save_selection", icon="ADD", text="")
        col.operator("scene.delete_selection", icon="REMOVE", text="")
        
        # restore and edit buttons
        if len(context.scene.saved_selections) > context.scene.save_selection_list_index and len(context.scene.saved_selections) > 0:

            selection = context.scene.saved_selections[context.scene.save_selection_list_index]

            if selection is not None:
                # restore and edit buttons
                row2 = layout.row()
                row2.operator("scene.restore_selection", icon="FILE_TICK", text="Restore")
                row2.operator("scene.edit_selection", icon="GREASEPENCIL", text="Edit")


class SCENE_UL_save_selection_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # if selection mode is object
        if item.selection_type == "OBJECT":
            layout.label(text="", icon="MESH_CUBE")
            layout.prop(item, "name", text="", emboss=False, icon_value=icon)

        elif item.selection_type == "FACE":
            layout.label(text="", icon="FACESEL")
            layout.prop(item, "name", text="", emboss=False, icon_value=icon)

        elif item.selection_type == "EDGE":
            layout.label(text="", icon="EDGESEL")
            layout.prop(item, "name", text="", emboss=False, icon_value=icon)

        elif item.selection_type == "VERTEX":
            layout.label(text="", icon="VERTEXSEL")
            layout.prop(item, "name", text="", emboss=False, icon_value=icon)

        else:
            layout.label(text="", icon="ERROR")
            layout.prop(item, "name", text="", emboss=False, icon_value=icon)