import bpy

def get_selection_name(context):
    bpy.context.scene.save_selection_index_max += 1
    return "Selection " + str(bpy.context.scene.save_selection_index_max), bpy.context.scene.save_selection_index_max

def save_new_selection(context):
    tag, index = get_selection_name(context)
    selection = bpy.context.scene.saved_selections.add()
    selection.name = tag
    selection.selection_index = index
    selection.selection_type = bpy.context.mode
    selection.active_object = bpy.context.active_object
    for obj in bpy.context.selected_objects:
        selection.selected_objects.add().obj = obj

    bpy.context.scene.save_selection_index = index

    return index

    
class SelectedObjects(bpy.types.PropertyGroup):
    obj: bpy.props.PointerProperty(type=bpy.types.Object)


class SavedSelection(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    selection_index: bpy.props.IntProperty()
    selection_type: bpy.props.StringProperty()
    selected_objects: bpy.props.CollectionProperty(type=SelectedObjects)
    active_object: bpy.props.PointerProperty(type=bpy.types.Object)