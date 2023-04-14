import bpy

def draw_save_selected_edit_menu(self, context):
    # add operator to context menu
    layout = self.layout
    layout.separator()
    layout.operator("scene.save_selection_edit")
    layout.operator("scene.restore_selection")

def draw_save_selected_menu(self, cotext):
    # add operator to context menu
    layout = self.layout
    layout.separator()
    layout.operator("scene.save_selection")
    layout.operator("scene.restore_selection")


class SaveSelectionPanel(bpy.types.Panel):
    bl_label = "Save Selection"
    bl_idname = "WORD_PT_save_selection"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "world"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        # Draw the list of objects in the scene
        row = layout.row()
        row.template_list("WORLD_UL_my_list", "", context.scene, "saved_selections", context.scene, "save_selection_index")



class WORLD_UL_my_list(bpy.types.UIList):
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
