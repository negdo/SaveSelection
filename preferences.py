import bpy
from bpy.props import BoolProperty

class addCubeSamplePreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    print("Preferences loaded 3")
 
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