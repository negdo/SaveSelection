"""
Save and restore selection of vertices/edges/faces in edit mode
"""

import bpy
import bmesh

class SaveSelectionEdit(bpy.types.Operator):
    bl_idname = "scene.save_selection_edit"
    bl_label = "Save Selection"
    bl_description = "Temporary save selected vertices/edges/faces"

    def execute(self, context):
        bpy.ops.ed.undo_push()
        bpy.ops.object.editmode_toggle()

        # get next number
        if bpy.context.scene.get('saveCounter') == None:
            bpy.context.scene['saveCounter'] = 1
            n = 1
        else:
            bpy.context.scene['saveCounter'] += 1
            n = bpy.context.scene['saveCounter']
        

        # check select mode (faces/edges/vertices)
        select_mode = bpy.context.tool_settings.mesh_select_mode[:]
        if select_mode[0]:
            bpy.context.scene['saveSelectionMode'] = 0
            self.vertices(context, n)
        elif select_mode[1]:
            bpy.context.scene['saveSelectionMode'] = 1
            self.edges(context, n)
        elif select_mode[2]:
            bpy.context.scene['saveSelectionMode'] = 2
            self.faces(context, n)

        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}

    def vertices(self, context, n):
        # For each selected object
        selection = bpy.context.selected_objects
        for obj in selection:    

            #BMESH of active object
            bm = bmesh.new() 
            bm.from_mesh(obj.data)
            bm.verts.ensure_lookup_table()

            # add new layer on vertices if not exist
            layer = bm.verts.layers.int.get("savedSelectionCounter")
            if layer == None:
                layer = bm.verts.layers.int.new("savedSelectionCounter")
                bm.verts.ensure_lookup_table()

            # set selected vertex layer to n
            for i in range(len(obj.data.vertices)):
                if obj.data.vertices[i].select:
                    bm.verts[i][layer] = n
            
            # Finish up, write the bmesh back to the mesh
            bm.to_mesh(obj.data)
            bm.free()  # free and prevent further access

    def edges(self, context, n):
        # For each selected object
        selection = bpy.context.selected_objects
        for obj in selection:    

            #BMESH of active object
            bm = bmesh.new() 
            bm.from_mesh(obj.data)
            bm.edges.ensure_lookup_table()

            # add new layer on edges if not exist
            layer = bm.edges.layers.int.get("savedSelectionCounter")
            if layer == None:
                layer = bm.edges.layers.int.new("savedSelectionCounter")
                bm.edges.ensure_lookup_table()

            # set selected edges layer to n
            for i in range(len(obj.data.edges)):
                if obj.data.edges[i].select:
                    bm.edges[i][layer] = n
            
            # Finish up, write the bmesh back to the mesh
            bm.to_mesh(obj.data)
            bm.free()  # free and prevent further access

    def faces(self, context, n):
        # For each selected object
        selection = bpy.context.selected_objects
        for obj in selection:    

            #BMESH of active object
            bm = bmesh.new() 
            bm.from_mesh(obj.data)
            bm.faces.ensure_lookup_table()

            # add new layer on faces if not exist
            layer = bm.faces.layers.int.get("savedSelectionCounter")
            if layer == None:
                layer = bm.faces.layers.int.new("savedSelectionCounter")
                bm.faces.ensure_lookup_table()

            # set selected faces layer to n
            for i in range(len(obj.data.polygons)):
                if obj.data.polygons[i].select:
                    bm.faces[i][layer] = n
            
            # Finish up, write the bmesh back to the mesh
            bm.to_mesh(obj.data)
            bm.free()  # free and prevent further access    


class RestoreSelectedEdit(bpy.types.Operator):
    bl_idname = "scene.restore_selection_edit"
    bl_label = "Restore Selection"
    bl_description = "Restore temporary saved vertex/edge/face selection"

    def execute(self, context):
        bpy.ops.ed.undo_push()
        try: n = bpy.context.scene['saveCounter'] # number of last saved selection
        except: n = None
        try: select_mode = bpy.context.scene['saveSelectionMode'] # select mode (faces/edges/vertices) = (2/1/0)
        except: select_mode = None

        if n != None and select_mode != None:
            bpy.ops.mesh.select_all(action='DESELECT')

            if select_mode == 0:
                found_selection = self.vertices(context, n)
            elif select_mode == 1:
                found_selection = self.edges(context, n)
            elif select_mode == 2:
                found_selection = self.faces(context, n)
            
            bpy.ops.object.editmode_toggle()

            if not found_selection:
                if select_mode == 0:
                    n = self.find_biggest_vertex_layer()
                    self.vertices(context, n)
                elif select_mode == 1:
                    n = self.find_biggest_edge_layer()
                    self.edges(context, n)
                elif select_mode == 2:
                    n = self.find_biggest_face_layer()
                    self.faces(context, n)

                bpy.ops.object.editmode_toggle()

        return {"FINISHED"}

    def vertices(self, context, n):
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.object.editmode_toggle()

        found_selection = False

        # For each selected object
        selection = bpy.context.selected_objects
        for obj in selection:    

            #BMESH of active object
            bm = bmesh.new() 
            bm.from_mesh(obj.data)
            bm.verts.ensure_lookup_table()

            # Get data from layer
            layer = bm.verts.layers.int.get("savedSelectionCounter")
            if layer != None:
                for i in range(len(obj.data.vertices)):
                    # if number in vertex is equal to saveCounter
                    value = (bm.verts[i][layer] == n)
                    obj.data.vertices[i].select = value
                    found_selection = found_selection or value

            bm.free()  # free and prevent further access
        return found_selection

    def edges(self, context, n):
        bpy.ops.mesh.select_mode(type="EDGE")
        bpy.ops.object.editmode_toggle()

        found_selection = False

        # For each selected object
        selection = bpy.context.selected_objects
        for obj in selection:    

            #BMESH of active object
            bm = bmesh.new() 
            bm.from_mesh(obj.data)
            bm.edges.ensure_lookup_table()

            # Get data from layer
            layer = bm.edges.layers.int.get("savedSelectionCounter")
            if layer != None:
                for i in range(len(obj.data.edges)):
                    # if number in edges is equal to saveCounter
                    value = (bm.edges[i][layer] == n)
                    obj.data.edges[i].select = value
                    found_selection = found_selection or value

            bm.free()  # free and prevent further access
        return found_selection

    def faces(self, context, n):
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.object.editmode_toggle()

        found_selection = False

        # For each selected object
        selection = bpy.context.selected_objects
        for obj in selection:    

            #BMESH of active object
            bm = bmesh.new() 
            bm.from_mesh(obj.data)
            bm.faces.ensure_lookup_table()

            # Get data from layer
            layer = bm.faces.layers.int.get("savedSelectionCounter")
            if layer != None:
                for i in range(len(obj.data.polygons)):
                    # if number in edges is equal to saveCounter
                    value = (bm.faces[i][layer] == n)
                    obj.data.polygons[i].select = value
                    found_selection = found_selection or value

            bm.free()  # free and prevent further access
        return found_selection


    def find_biggest_vertex_layer(self):
        biggest_layer = -1

        # For each selected object
        selection = bpy.context.selected_objects
        for obj in selection:    

            #BMESH of active object
            bm = bmesh.new() 
            bm.from_mesh(obj.data)
            bm.verts.ensure_lookup_table()

            # Get data from layer
            layer = bm.verts.layers.int.get("savedSelectionCounter")
            if layer != None:
                for i in range(len(obj.data.vertices)):
                    biggest_layer = max(bm.verts[i][layer], biggest_layer)

            bm.free()  # free and prevent further access
        return biggest_layer

    def find_biggest_edge_layer(self):
        biggest_layer = -1

        # For each selected object
        selection = bpy.context.selected_objects
        for obj in selection:    

            #BMESH of active object
            bm = bmesh.new() 
            bm.from_mesh(obj.data)
            bm.edges.ensure_lookup_table()

            # Get data from layer
            layer = bm.edges.layers.int.get("savedSelectionCounter")
            if layer != None:
                for i in range(len(obj.data.edges)):
                    biggest_layer = max(bm.edges[i][layer], biggest_layer)

            bm.free()  # free and prevent further access
        return biggest_layer

    def find_biggest_face_layer(self):
        biggest_layer = -1

        # For each selected object
        selection = bpy.context.selected_objects
        for obj in selection:    

            #BMESH of active object
            bm = bmesh.new() 
            bm.from_mesh(obj.data)
            bm.faces.ensure_lookup_table()

            # Get data from layer
            layer = bm.faces.layers.int.get("savedSelectionCounter")
            if layer != None:
                for i in range(len(obj.data.polygons)):
                    biggest_layer = max(bm.faces[i][layer], biggest_layer)

            bm.free()  # free and prevent further access
        return biggest_layer