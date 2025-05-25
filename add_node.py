import bpy
from mathutils import Vector

def auto_rename_text_object(scene):
    """Handler function that renames text objects based on their content"""
    for obj in scene.objects:
        if obj.type == 'FONT':
            # Get the current text content (strip whitespace)
            text_content = obj.data.body.strip()
            
            # Only rename if text content is not empty and different from current name
            if text_content and text_content != obj.name:
                # Check if the new name would conflict with existing objects
                if text_content in bpy.data.objects:
                    # If conflict exists, Blender will automatically append .001, .002, etc.
                    pass
                
                # Rename the object to match text content
                old_name = obj.name
                obj.name = text_content
                print(f"Auto-renamed text object from '{old_name}' to '{obj.name}'")

# Register the handler if it's not already registered
handler_registered = False
for handler in bpy.app.handlers.depsgraph_update_post:
    if handler.__name__ == 'auto_rename_text_object':
        handler_registered = True
        break

if not handler_registered:
    bpy.app.handlers.depsgraph_update_post.append(auto_rename_text_object)
    print("Registered auto-rename handler for text objects")

# Get the selected objects
selected_objects = bpy.context.selected_objects

if not selected_objects:
    print("No objects selected. Please select at least one object.")
else:
    # Calculate the center point of the selected objects
    center = Vector((0, 0, 0))
    for obj in selected_objects:
        center += obj.location
    center /= len(selected_objects)

    # Create a new Text object
    bpy.ops.object.text_add(location=center)

    # Get the created Text object
    text_obj = bpy.context.object

    # Determine the desired name
    if len(selected_objects) > 1:
        desired_name = "Node"
    else:
        # If only one object is selected, use the same name as the mesh
        desired_name = selected_objects[0].name

    # Let Blender assign whatever name it wants (might be Node.001, etc.)
    # But we'll control the text content

    # Enter edit mode to set clean text content
    bpy.context.view_layer.objects.active = text_obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Clear all text and set clean name without any numeric suffix
    bpy.ops.font.select_all()
    bpy.ops.font.delete()
    bpy.ops.font.text_insert(text=desired_name)
    
    # Exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Now use the clean text content to rename the object
    text_obj.name = desired_name

    # Set the horizontal alignment of the text to 'CENTER'
    text_obj.data.align_x = 'CENTER'

    # Calculate the maximum Y dimension of the bounding boxes of the selected objects
    max_y_dim = max((obj.dimensions.y for obj in selected_objects if obj.dimensions.y > 0), default=1.0)

    # Adjust the Y offset of the text within the Text object to be outside the bounding box
    # Note: Blender uses meters as the unit for measurement, so we convert inches to meters
    text_obj.data.offset_y = -max_y_dim - 10 * 0.0254

    # Make the selected objects children of the Text object
    for obj in selected_objects:
        # Store the world space matrix
        matrix_world = obj.matrix_world.copy()
        
        # Set the parent
        obj.parent = text_obj
        
        # Restore the world space matrix
        obj.matrix_world = matrix_world

    # Create a new material with unique name to avoid conflicts
    mat_name = "RedMaterial"
    counter = 1
    while mat_name in bpy.data.materials:
        mat_name = f"RedMaterial.{counter:03d}"
        counter += 1
    
    mat = bpy.data.materials.new(name=mat_name)

    # Set the material's diffuse color (Updated for Blender 4.4)
    mat.diffuse_color = (1, 0, 0, 1)  # Red
    
    # For proper material setup in Blender 4.4
    if not mat.use_nodes:
        mat.use_nodes = True
    
    # Get the principled BSDF node
    nodes = mat.node_tree.nodes
    principled = nodes.get("Principled BSDF")
    if principled:
        principled.inputs[0].default_value = (1, 0, 0, 1)  # Base Color

    # Assign the material to the text object
    if text_obj.data.materials:
        # Assign to first material slot
        text_obj.data.materials[0] = mat
    else:
        # No slots
        text_obj.data.materials.append(mat)

    # Set the viewport display color to red
    text_obj.color = (1, 0, 0, 1)  # Red

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    print(f"Created node '{text_obj.name}' with {len(selected_objects)} child objects")
    print("Note: The object will automatically rename itself when you edit the text content")