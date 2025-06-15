import bpy
import os
from bpy.types import PropertyGroup, Panel, Operator

# Import individual operators
from . import (
    add_node_operator,
    dev_material_operator,
    static_mesh_operator,
    scene_setup_operator,
    collision_operators,
    fbx_export_operator
)

# Define the update function for the file path
def update_file_path(self, context):
    print("The chosen file path is", self.my_file_path)
    # Store the file path in the object's custom properties
    self["custom_file_path"] = self.my_file_path

    # Check if the file path has been set
    if self.my_file_path != "":
        # Create a new material
        mat = bpy.data.materials.new(name="GreyMaterial")

        # Set the material's diffuse color
        mat.diffuse_color = (0.5, 0.5, 0.5, 1)  # Grey

        # Assign the material to the text object
        if self.data.materials:
            # Assign to first material slot
            self.data.materials[0] = mat
        else:
            # No slots
            self.data.materials.append(mat)

# Add the file path property to the Object class
bpy.types.Object.my_file_path = bpy.props.StringProperty(
    name="File Path",
    description="Path to the file",
    default="",
    maxlen=1024,
    subtype='FILE_PATH',
    update=update_file_path
)

# Custom panel for file path
class OBJECT_PT_CustomPanel(Panel):
    bl_idname = "OBJECT_PT_custom_panel"
    bl_label = "Model Export Path (Must be inside of the CS2's Content folder)"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()
        row.prop(obj, "my_file_path")

# Export FBX Properties (keeping for potential future use, but removing export_scale)
class ExportFBXProperties(PropertyGroup):
    pass  # Empty for now, but keeping the structure

# Main panel
class ExportFBXPanel(Panel):
    bl_label = "Source 2 Model Exporter"
    bl_idname = "OBJECT_PT_export_fbx"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Source 2 Model Exporter'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object

        # Create Node and Scene Setup buttons
        row = layout.row()
        row.operator("object.simple_operator", icon='ADD')
        row.scale_y = 2
        row.operator("object.setup_scene", icon='WINDOW')
        row.scale_y = 2
        
        layout.separator()

        # Dev Material button
        row = layout.row()
        row.operator("object.adddevmat", icon='MATERIAL')
        
        layout.separator()

        # Show file path for selected text objects (nodes)
        if obj and obj.type == 'FONT':
            box = layout.box()
            box.label(text="Node Export Settings:", icon='TEXT')
            
            # File path property directly in the panel
            row = box.row()
            row.prop(obj, "my_file_path", text="Export Path")
            
            # Show current status
            if obj.my_file_path:
                box.label(text="✓ Path set", icon='CHECKMARK')
            else:
                box.label(text="⚠ No path set", icon='ERROR')
        
        elif obj and obj.type != 'FONT':
            # Show info when non-text object is selected
            box = layout.box()
            box.label(text="Select a Node (text object) to set export path", icon='INFO')

        layout.separator()

        # Main export button
        row = layout.row()
        row.scale_y = 3
        row.operator("object.export_fbx", icon='PLAY')
        
        layout.separator()
        
        # Static mesh export button
        row = layout.row()
        row.scale_y = 3
        row.operator("object.staticmesh", icon='PLAY')
        
        layout.separator()

        # Collision buttons
        row = layout.row()
        row.operator("object.setup_coll", icon='MESH_CUBE')
        row.scale_y = 2
        row.operator("object.hide_coll", icon='GHOST_ENABLED')
        row.scale_y = 2

def register():
    # Register property groups first
    bpy.utils.register_class(ExportFBXProperties)
    bpy.utils.register_class(OBJECT_PT_CustomPanel)
    bpy.utils.register_class(ExportFBXPanel)
    
    # Register operators from separate modules
    add_node_operator.register()
    dev_material_operator.register()
    static_mesh_operator.register()
    scene_setup_operator.register()
    collision_operators.register()
    fbx_export_operator.register()
    
    # Add scene property
    bpy.types.Scene.export_fbx = bpy.props.PointerProperty(type=ExportFBXProperties)

def unregister():
    # Unregister in reverse order
    fbx_export_operator.unregister()
    collision_operators.unregister()
    scene_setup_operator.unregister()
    static_mesh_operator.unregister()
    dev_material_operator.unregister()
    add_node_operator.unregister()
    
    bpy.utils.unregister_class(ExportFBXPanel)
    bpy.utils.unregister_class(OBJECT_PT_CustomPanel)
    bpy.utils.unregister_class(ExportFBXProperties)
    
    # Remove scene properties
    del bpy.types.Scene.export_fbx

if __name__ == "__main__":
    register()