import bpy
import os

# Ensure an object is selected
if bpy.context.selected_objects:
    # Get the selected object
    selected_object = bpy.context.selected_objects[0]

    # If the selected object has any material other than "graygrid", delete all materials
    if selected_object.data.materials:
        materials_to_remove = []
        for slot in selected_object.material_slots:
            if slot.material and slot.material.name != "graygrid":
                materials_to_remove.append(slot.material)

        # Remove materials (but keep references to avoid issues)
        for mat in materials_to_remove:
            if mat.users == 1:  # Only remove if this is the only user
                bpy.data.materials.remove(mat)

        # Clear all material slots of the object
        selected_object.data.materials.clear()

    # Check if the material already exists
    mat = bpy.data.materials.get("graygrid")

    # If the material does not exist, create a new one
    if mat is None:
        mat = bpy.data.materials.new(name="graygrid")

    # Assign the material to the selected object
    selected_object.data.materials.append(mat)

    # Add a custom property named "FBX_vmatPath" to the material
    mat["FBX_vmatPath"] = "materials/dev/graygrid.vmat"

    # Enable use nodes
    mat.use_nodes = True

    # Get the material node tree
    nodes = mat.node_tree.nodes

    # Clear all nodes except the output
    nodes_to_remove = [node for node in nodes if node.type != 'OUTPUT_MATERIAL']
    for node in nodes_to_remove:
        nodes.remove(node)

    # Create a new texture node
    texture_node = nodes.new(type='ShaderNodeTexImage')
    texture_node.location = (-300, 0)

    # Try to load the texture
    try:
        dirname = os.path.dirname(__file__)
        texture_path = os.path.join(dirname, "greygrid.png")
        
        # Check if image already exists in Blender
        img = bpy.data.images.get("greygrid.png")
        if img is None:
            if os.path.exists(texture_path):
                img = bpy.data.images.load(texture_path)
            else:
                print(f"Warning: Texture file not found at {texture_path}")
                # Create a simple procedural texture as fallback
                img = None
        
        # Assign the image to the texture node
        if img:
            texture_node.image = img
    except Exception as e:
        print(f"Error loading texture: {e}")

    # Create a new BSDF node
    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf_node.location = (0, 0)

    # Get or create output node
    output_node = None
    for node in nodes:
        if node.type == 'OUTPUT_MATERIAL':
            output_node = node
            break
    
    if output_node is None:
        output_node = nodes.new('ShaderNodeOutputMaterial')
    
    output_node.location = (300, 0)

    # Link the nodes
    links = mat.node_tree.links
    
    # Link texture to BSDF base color
    if texture_node.image:
        links.new(bsdf_node.inputs['Base Color'], texture_node.outputs['Color'])
    else:
        # Set a gray color if no texture
        bsdf_node.inputs['Base Color'].default_value = (0.5, 0.5, 0.5, 1.0)

    # Link BSDF to output
    links.new(output_node.inputs['Surface'], bsdf_node.outputs['BSDF'])
    
    print(f"Applied graygrid material to {selected_object.name}")
    
else:
    print("No object selected. Please select an object.")