"""
Save and restore selection of objects in object mode
"""

import bpy, bmesh
from .properties import get_selection_name

def mark_faces(context, n):
    layer_name = "savedSelectionCounter" + str(n)

    # For each selected object
    selection = context.selected_objects
    for obj in selection:    

        # get bmesh of current object
        bm = bmesh.new() 
        bm.from_mesh(obj.data)
        bm.faces.ensure_lookup_table()

        # add new layer
        layer = bm.faces.layers.int.new(layer_name)
        bm.faces.ensure_lookup_table()

        # set selected faces layer to True
        for i in range(len(obj.data.polygons)):
            bm.faces[i][layer] = obj.data.polygons[i].select
        
        # write the bmesh back to the mesh
        bm.to_mesh(obj.data)
        bm.free()

def mark_edges(context, n):
    layer_name = "savedSelectionCounter" + str(n)

    # For each selected object
    selection = context.selected_objects
    for obj in selection:    

        # get bmesh of current object
        bm = bmesh.new() 
        bm.from_mesh(obj.data)
        bm.edges.ensure_lookup_table()

        # add new layer
        layer = bm.edges.layers.int.new(layer_name)
        bm.edges.ensure_lookup_table()

        # set selected edges layer to True
        for i in range(len(obj.data.edges)):
            bm.edges[i][layer] = obj.data.edges[i].select
        
        # write the bmesh back to the mesh
        bm.to_mesh(obj.data)
        bm.free()

def mark_vertices(context, n):
    layer_name = "savedSelectionCounter" + str(n)

    # For each selected object
    selection = context.selected_objects
    for obj in selection:    

        # get bmesh of current object
        bm = bmesh.new() 
        bm.from_mesh(obj.data)
        bm.verts.ensure_lookup_table()

        # add new layer
        layer = bm.verts.layers.int.new(layer_name)
        bm.verts.ensure_lookup_table()

        # set selected vertices layer to True
        for i in range(len(obj.data.vertices)):
            bm.verts[i][layer] = obj.data.vertices[i].select

        # write the bmesh back to the mesh
        bm.to_mesh(obj.data)
        bm.free()

def select_faces(n, selection):
    bpy.ops.object.mode_set(mode="OBJECT")
    layer_name = "savedSelectionCounter" + str(n)

    for obj in selection:    
        # get bmesh of current object
        bm = bmesh.new() 
        bm.from_mesh(obj.obj.data)
        bm.faces.ensure_lookup_table()

        # get layer
        layer = bm.faces.layers.int.get(layer_name)
        if layer == None:
            bm.free()
            continue
        bm.faces.ensure_lookup_table()

        # set selected faces layer to n
        for face in bm.faces:
            if face[layer] == 1:
                face.select = True

        # write the bmesh back to the mesh
        bm.to_mesh(obj.obj.data)
        bm.free()

def select_edges(n, selection):
    bpy.ops.object.mode_set(mode="OBJECT")
    layer_name = "savedSelectionCounter" + str(n)

    for obj in selection:    
        # get bmesh of current object
        bm = bmesh.new() 
        bm.from_mesh(obj.obj.data)
        bm.edges.ensure_lookup_table()

        # get layer
        layer = bm.edges.layers.int.get(layer_name)
        if layer == None:
            bm.free()
            continue
        bm.edges.ensure_lookup_table()

        # set selected faces layer to n
        for edge in bm.edges:
            if edge[layer] == 1:
                edge.select = True

        # write the bmesh back to the mesh
        bm.to_mesh(obj.obj.data)
        bm.free()

def select_vertices(n, selection):
    bpy.ops.object.mode_set(mode="OBJECT")
    layer_name = "savedSelectionCounter" + str(n)

    for obj in selection:    
        # get bmesh of current object
        bm = bmesh.new() 
        bm.from_mesh(obj.obj.data)
        bm.verts.ensure_lookup_table()

        # get layer
        layer = bm.verts.layers.int.get(layer_name)
        if layer == None:
            bm.free()
            continue

        bm.verts.ensure_lookup_table()

        # set selected faces layer to n
        for vertex in bm.verts:
            if vertex[layer] == 1:
                vertex.select = True

        # write the bmesh back to the mesh
        bm.to_mesh(obj.obj.data)
        bm.free()   


class RestoreSelected(bpy.types.Operator):
    bl_idname = "scene.restore_selection"
    bl_label = "Restore Selection"
    bl_description = "Restore temporary saved object selection"

    def execute(self, context):
        bpy.ops.ed.undo_push()
        if context.scene.save_selection_index == -1:
            return {"FINISHED"}

        selection = context.scene.saved_selections[context.scene.save_selection_index]

        try:
            bpy.ops.object.mode_set(mode="OBJECT")
        except:
            return {"FINISHED"}

        # deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # select objects
        obj_count = 0
        for obj in selection.selected_objects:
            try:
                obj.obj.select_set(True)
                obj_count += 1
            except:
                pass

        if selection.selection_type == "OBJECT" or obj_count == 0:
            pass
        else:
            bpy.ops.object.editmode_toggle()
            # deselect geometry
            bpy.ops.mesh.select_all(action='DESELECT')
            
            if selection.selection_type == "FACE":
                bpy.ops.mesh.select_mode(type="FACE")
                select_faces(context.scene.save_selection_index, selection.selected_objects)
            
            elif selection.selection_type == "EDGE":
                bpy.ops.mesh.select_mode(type="EDGE")
                select_edges(context.scene.save_selection_index, selection.selected_objects)

            elif selection.selection_type == "VERTEX":
                bpy.ops.mesh.select_mode(type="VERT")
                select_vertices(context.scene.save_selection_index, selection.selected_objects)

            bpy.ops.object.mode_set(mode="EDIT")
     
        return {"FINISHED"}
               

class SaveSelection(bpy.types.Operator):
    bl_idname = "scene.save_selection"
    bl_label = "Save Selection"
    bl_description = "Temporary save selected vertices/edges/faces"

    def execute(self, context):
        bpy.ops.ed.undo_push()

        tag, index = get_selection_name(context)
        selection = context.scene.saved_selections.add()
        selection.name = tag
        selection.selection_index = index
        for obj in context.selected_objects:
            selection.selected_objects.add().obj = obj

        context.scene.save_selection_index = index

        if context.mode == "OBJECT":
            # object mode
            selection.selection_type = "OBJECT"

        elif context.mode == "EDIT_MESH":
            # edit mode
            bpy.ops.object.editmode_toggle()
            select_mode = context.tool_settings.mesh_select_mode[:]

            if select_mode[0]:
                selection.selection_type = "VERTEX"
                mark_vertices(context, index)
            elif select_mode[1]:
                selection.selection_type = "EDGE"
                mark_edges(context, index)
            elif select_mode[2]:
                selection.selection_type = "FACE"
                mark_faces(context, index)

            bpy.ops.object.editmode_toggle()
        return {"FINISHED"}

    
class DeleteSelection(bpy.types.Operator):
    bl_idname = "scene.delete_selection"
    bl_label = "Delete Selection"
    bl_description = "Remove saved selection"

    def execute(self, context):
        bpy.ops.ed.undo_push()
        
        index = context.scene.save_selection_index
        context.scene.saved_selections.remove(index)

        return {"FINISHED"}
    
    @classmethod
    def poll(self, context):
        if context.scene.save_selection_index == -1:
            return False
        if context.scene.saved_selections[context.scene.save_selection_index] is None:
            return False
        return True
    

class EditSelection(bpy.types.Operator):
    bl_idname = "scene.edit_selection"
    bl_label = "Edit Selection"
    bl_description = "Edit saved selection"

    def execute(self, context):
        bpy.ops.ed.undo_push()

        index = context.scene.save_selection_index
        selection = context.scene.saved_selections[index]
        selection.selected_objects.clear()
        for obj in context.selected_objects:
            selection.selected_objects.add().obj = obj

        context.scene.save_selection_index = index

        if selection.selection_type == "OBJECT":
            # object mode
            bpy.ops.object.mode_set(mode="OBJECT")

        else:
            # edit mode
            bpy.ops.object.mode_set(mode="OBJECT")

            if selection.selection_type == "VERTEX":
                mark_vertices(context, index)
            elif selection.selection_type == "EDGE":
                mark_edges(context, index)
            elif selection.selection_type == "FACE":
                mark_faces(context, index)

            bpy.ops.object.editmode_toggle()

        return {"FINISHED"}
    
    @classmethod
    def poll(self, context):
        selection = context.scene.saved_selections[context.scene.save_selection_index]
        if selection.selection_type == "OBJECT":
            if context.mode != "OBJECT":
                return False
        else:
            if context.mode != "EDIT_MESH":
                return False
            elif selection.selection_type == "VERTEX" and not context.tool_settings.mesh_select_mode[0]:
                return False
            elif selection.selection_type == "EDGE" and not context.tool_settings.mesh_select_mode[1]:
                return False
            elif selection.selection_type == "FACE" and not context.tool_settings.mesh_select_mode[2]:
                return False

        return True