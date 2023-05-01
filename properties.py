import bpy

def get_selection_name(context):
    bpy.context.scene.save_selection_index_max += 1
    return "Selection " + str(bpy.context.scene.save_selection_index_max), bpy.context.scene.save_selection_index_max
   
    
class SelectedObjects(bpy.types.PropertyGroup):
    obj: bpy.props.PointerProperty(type=bpy.types.Object)


class SavedSelection(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    selection_index: bpy.props.IntProperty()
    selection_type: bpy.props.StringProperty()
    selected_objects: bpy.props.CollectionProperty(type=SelectedObjects)