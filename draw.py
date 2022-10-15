def draw_save_selected_edit_menu(self, context):
    # add operator to context menu
    layout = self.layout
    layout.separator()
    layout.operator("scene.save_selection_edit")
    layout.operator("scene.restore_selection_edit")

def draw_save_selected_menu(self, cotext):
    # add operator to context menu
    layout = self.layout
    layout.separator()
    layout.operator("scene.save_selection")
    layout.operator("scene.restore_selection")