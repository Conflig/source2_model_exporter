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

# Define the update function for the relative path
def update_relative_path(self, context):
    """Update function for relative export path"""
    # Store the relative path in the object's custom properties
    self["custom_relative_path"] = self.relative_export_path
    
    # Get addon preferences
    preferences = context.preferences.addons[__name__.split('.')[0]].preferences
    base_path = preferences.addons_path
    
    if base_path and self.relative_export_path:
        # Calculate full path
        full_path = os.path.join(base_path, self.relative_export_path)
        self["custom_file_path"] = full_path
        print(f"Updated export path: {full_path}")
        
        # Update material color to grey when path is set
        if self.relative_export_path != "":
            # Create a new material
            mat = bpy.data.materials.new(name="GreyMaterial")
            # Set the material's diffuse color
            mat.diffuse_color = (0.5, 0.5, 0.5, 1)  # Grey
            # Assign the material to the text object
            if self.data.materials:
                self.data.materials[0] = mat
            else:
                self.data.materials.append(mat)

# Add the relative path property to the Object class
bpy.types.Object.relative_export_path = bpy.props.StringProperty(
    name="Relative Export Path",
    description="Path relative to the Addons Path",
    default="",
    maxlen=1024,
    update=update_relative_path
)

# File browser operator for selecting relative path
class OBJECT_OT_BrowseRelativePath(Operator):
    bl_idname = "object.browse_relative_path"
    bl_label = "Browse Export Folder"
    bl_description = "Browse and select export folder relative to Addons Path"
    
    directory: bpy.props.StringProperty(subtype="DIR_PATH")
    
    def invoke(self, context, event):
        # Get addon preferences
        preferences = context.preferences.addons[__name__.split('.')[0]].preferences
        base_path = preferences.addons_path
        
        if not base_path or not os.path.exists(base_path):
            self.report({'ERROR'}, "Addons Path is not set or doesn't exist. Please set it in addon preferences.")
            return {'CANCELLED'}
        
        # Set the directory to start browsing from the base path
        self.directory = base_path
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        # Get addon preferences
        preferences = context.preferences.addons[__name__.split('.')[0]].preferences
        base_path = preferences.addons_path
        
        if not base_path:
            self.report({'ERROR'}, "Addons Path is not set")
            return {'CANCELLED'}
        
        # Calculate relative path
        selected_path = self.directory
        
        # Make sure the selected path is within the base path
        if not selected_path.startswith(base_path):
            self.report({'ERROR'}, "Selected path must be within the Addons Path")
            return {'CANCELLED'}
        
        # Calculate relative path
        relative_path = os.path.relpath(selected_path, base_path)
        
        # Handle case where user selected the base directory itself
        if relative_path == ".":
            relative_path = ""
        
        # Update the active object's relative path
        obj = context.object
        if obj and obj.type == 'FONT':
            obj.relative_export_path = relative_path
            self.report({'INFO'}, f"Export path set to: {relative_path or 'Base directory'}")
        else:
            self.report({'ERROR'}, "Please select a text object (node)")
        
        return {'FINISHED'}

# Custom panel for file path (keeping for potential compatibility)
class OBJECT_PT_CustomPanel(Panel):
    bl_idname = "OBJECT_PT_custom_panel"
    bl_label = "Model Export Path (Must be inside of the CS2's Content folder)"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
        # Get addon preferences
        preferences = context.preferences.addons[__name__.split('.')[0]].preferences
        base_path = preferences.addons_path
        
        if not base_path:
            box = layout.box()
            box.label(text="⚠ Set Addons Path in preferences first", icon='ERROR')
            return
        
        if obj and obj.type == 'FONT':
            # Show browse button
            row = layout.row()
            row.operator("object.browse_relative_path", icon='FILEBROWSER')
            
            # Show current relative path
            if hasattr(obj, 'relative_export_path') and obj.relative_export_path:
                box = layout.box()
                box.label(text=f"Export to: {obj.relative_export_path}")
            else:
                box = layout.box()
                box.label(text="No export path set", icon='INFO')

# Export FBX Properties (keeping for potential future use)
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

        # Get addon preferences
        preferences = context.preferences.addons[__name__.split('.')[0]].preferences
        base_path = preferences.addons_path

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

        # Show export settings for selected text objects (nodes)
        if obj and obj.type == 'FONT':
            box = layout.box()
            box.label(text="Node Export Settings:", icon='TEXT')
            
            if not base_path:
                # Warning if base path not set
                warning_box = box.box()
                warning_box.label(text="⚠ Set Addons Path in preferences", icon='ERROR')
            else:
                # Browse button
                row = box.row()
                row.operator("object.browse_relative_path", icon='FILEBROWSER', text="Select Export Folder")
                
                # Show current path info
                if hasattr(obj, 'relative_export_path') and obj.relative_export_path:
                    info_box = box.box()
                    info_box.label(text="Export Path:", icon='CHECKMARK')
                    info_box.label(text=f"  {obj.relative_export_path}")
                    info_box.label(text=f"Full Path: {os.path.join(base_path, obj.relative_export_path)}")
                else:
                    info_box = box.box()
                    info_box.label(text="⚠ No export path set", icon='ERROR')
        
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
    # Register property groups and operators first
    bpy.utils.register_class(ExportFBXProperties)
    bpy.utils.register_class(OBJECT_OT_BrowseRelativePath)
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
    bpy.utils.unregister_class(OBJECT_OT_BrowseRelativePath)
    bpy.utils.unregister_class(ExportFBXProperties)
    
    # Remove scene properties
    del bpy.types.Scene.export_fbx

if __name__ == "__main__":
    register()