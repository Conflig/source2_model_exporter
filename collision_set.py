import bpy
import bmesh

# Get selected objects
selected_objects = bpy.context.selected_objects
active_object = bpy.context.active_object

# Check if we have exactly 2 objects selected
if len(selected_objects) != 2:
    print("Please select exactly 2 objects: first a mesh object, then a text object (with Shift)")
else:
    # The active object should be the text object (selected last with Shift)
    if active_object.type != 'FONT':
        print("The active object (last selected) must be a text object. Please select the mesh first, then Shift+select the text object.")
    else:
        # Find the mesh object (the one that's not active)
        mesh_object = None
        for obj in selected_objects:
            if obj != active_object and obj.type == 'MESH':
                mesh_object = obj
                break
        
        if mesh_object is None:
            print("Could not find a mesh object in selection. Please ensure you select a mesh object first.")
        else:
            # Get the text object's name for renaming
            text_name = active_object.name
            
            # Rename the mesh object to match the text object name + "_coll"
            mesh_object.name = text_name + "_coll"
            print(f"Renamed mesh object to: {mesh_object.name}")
            
            # Set the mesh object as active for the operations
            bpy.context.view_layer.objects.active = mesh_object
            
            # Apply auto smooth shading with 180 degree angle
            bpy.ops.object.shade_auto_smooth(angle=3.14159)  # 180 degrees in radians
            print("Applied auto smooth shading with 180° angle")
            
            # Make the mesh object a child of the text object
            # Store the world space matrix to maintain position
            matrix_world = mesh_object.matrix_world.copy()
            
            # Set the parent
            mesh_object.parent = active_object
            
            # Restore the world space matrix to maintain position
            mesh_object.matrix_world = matrix_world
            print(f"Made {mesh_object.name} a child of {active_object.name}")

            # Check if the collision material exists
            mat = bpy.data.materials.get("CollisionMat")

            # If it doesn't exist, create it
            if mat is None:
                mat = bpy.data.materials.new(name="CollisionMat")
                
                # Enable nodes for proper material setup in Blender 4.4
                mat.use_nodes = True
                
                # Get the principled BSDF node
                nodes = mat.node_tree.nodes
                principled = nodes.get("Principled BSDF")
                
                if principled:
                    # Set base color (RGB equivalent of HEX "A0E7B6")
                    principled.inputs['Base Color'].default_value = (0.627, 0.906, 0.714, 1)
                    principled.inputs['Metallic'].default_value = 1.0
                    principled.inputs['Roughness'].default_value = 0.9
                
                print("Created CollisionMat material")

            # Assign the material to the mesh object
            if mesh_object.data.materials:
                mesh_object.data.materials[0] = mat
            else:
                mesh_object.data.materials.append(mat)

            # Set the viewport display properties (for material preview)
            mat.diffuse_color = (0.627, 0.906, 0.714, 1)

            print(f"Collision setup completed for {mesh_object.name}")
            print("- Renamed based on text object")
            print("- Applied auto smooth shading (180°)")
            print("- Applied CollisionMat material")
            print("- Made child of text object")