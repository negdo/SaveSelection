"""
Save and restore selection of objects in object mode
"""

import bpy, bmesh
from .properties import get_selection_name


class SaveSelection(bpy.types.Operator):
    bl_idname = "scene.save_selection"
    bl_label = "Save Selection"
    bl_description = "Temporary save selected objects"

    def execute(self, context):
        bpy.ops.ed.undo_push()

        tag, index = get_selection_name(context)
        selection = bpy.context.scene.saved_selections.add()
        selection.name = tag
        selection.selection_index = index
        selection.selection_type = bpy.context.mode
        selection.active_object = bpy.context.active_object
        for obj in bpy.context.selected_objects:
            selection.selected_objects.add().obj = obj

        bpy.context.scene.save_selection_index = index

        return {"FINISHED"}


class RestoreSelected(bpy.types.Operator):
    bl_idname = "scene.restore_selection"
    bl_label = "Restore Selection"
    bl_description = "Restore temporary saved object selection"


    def execute(self, context):
        bpy.ops.ed.undo_push()
        if bpy.context.scene.save_selection_index == -1:
            return {"FINISHED"}

        selection = bpy.context.scene.saved_selections[bpy.context.scene.save_selection_index]

        bpy.ops.object.mode_set(mode="OBJECT")

        # deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # select objects
        for obj in selection.selected_objects:
            obj.obj.select_set(True)

        if selection.selection_type == "OBJECT":
            pass
        else:
            bpy.ops.object.editmode_toggle()
            # deselect geometry
            bpy.ops.mesh.select_all(action='DESELECT')
            
            if selection.selection_type == "FACE":
                bpy.ops.mesh.select_mode(type="FACE")
                self.select_faces(bpy.context.scene.save_selection_index, selection.selected_objects)
            
            elif selection.selection_type == "EDGE":
                bpy.ops.mesh.select_mode(type="EDGE")
                self.select_edges(bpy.context.scene.save_selection_index, selection.selected_objects)

            elif selection.selection_type == "VERTEX":
                bpy.ops.mesh.select_mode(type="VERT")
                self.select_vertices(bpy.context.scene.save_selection_index, selection.selected_objects)

            bpy.ops.object.mode_set(mode="EDIT")
            
     
        return {"FINISHED"}
    
    def select_faces(self, n, selection):
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

    def select_edges(self, n, selection):
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

    def select_vertices(self, n, selection):
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
            

    

    
