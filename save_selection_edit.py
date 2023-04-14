"""
Save and restore selection of vertices/edges/faces in edit mode
"""

import bpy
import bmesh
from .properties import get_selection_name

class SaveSelectionEdit(bpy.types.Operator):
    bl_idname = "scene.save_selection_edit"
    bl_label = "Save Selection"
    bl_description = "Temporary save selected vertices/edges/faces"

    def execute(self, context):
        bpy.ops.ed.undo_push()
        bpy.ops.object.editmode_toggle()

        tag, index = get_selection_name(context)
        selection = bpy.context.scene.saved_selections.add()
        selection.name = tag
        selection.selection_index = index
        selection.active_object = bpy.context.active_object
        for obj in bpy.context.selected_objects:
            selection.selected_objects.add().obj = obj

        bpy.context.scene.save_selection_index = index
        
        select_mode = bpy.context.tool_settings.mesh_select_mode[:]
        if select_mode[0]:
            selection.selection_type = "VERTEX"
            self.mark_vertices(index)
        elif select_mode[1]:
            selection.selection_type = "EDGE"
            self.mark_edges(index)
        elif select_mode[2]:
            selection.selection_type = "FACE"
            self.mark_faces(index)

        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}

    def mark_faces(self, n):
        layer_name = "savedSelectionCounter" + str(n)

        # For each selected object
        selection = bpy.context.selected_objects
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
                if obj.data.polygons[i].select:
                    bm.faces[i][layer] = 1
            
            # write the bmesh back to the mesh
            bm.to_mesh(obj.data)
            bm.free()

    def mark_edges(self, n):
        layer_name = "savedSelectionCounter" + str(n)

        # For each selected object
        selection = bpy.context.selected_objects
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
                if obj.data.edges[i].select:
                    bm.edges[i][layer] = 1
            
            # write the bmesh back to the mesh
            bm.to_mesh(obj.data)
            bm.free()


    def mark_vertices(self, n):
        layer_name = "savedSelectionCounter" + str(n)

        # For each selected object
        selection = bpy.context.selected_objects
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
                if obj.data.vertices[i].select:
                    bm.verts[i][layer] = 1
            
            # write the bmesh back to the mesh
            bm.to_mesh(obj.data)
            bm.free()