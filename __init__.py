# __init__.py
"""
Source 2 Model Exporter for Blender 4.4+
A comprehensive addon for exporting models and collision meshes for Source 2 engine
"""

bl_info = {
    "name": "Source 2 Model Exporter",
    "author": "Jakub Vaja",
    "version": (1, 0, 1),
    "blender": (4, 5, 0),
    "location": "View3D > Sidebar > Source 2 Model Exporter",
    "description": "Exports models and collision meshes for Source 2 engine with proper setup tools",
    "category": "Import-Export",
    "doc_url": "",
    "tracker_url": "",
}

import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty

# Import all modules
from . import (
    GameModelExporter,
    add_node_operator,
    dev_material_operator,
    static_mesh_operator,
    scene_setup_operator,
    collision_operators,
    fbx_export_operator
)

def auto_rename_text_object(scene):
    """Handler function that renames text objects based on their content"""
    for obj in scene.objects:
        if obj.type == 'FONT':
            # Get the current text content (strip whitespace)
            text_content = obj.data.body.strip()
            
            # Only rename if text content is not empty and different from current name
            if text_content and text_content != obj.name:
                # Rename the object to match text content
                old_name = obj.name
                obj.name = text_content

# Addon preferences
class Source2ExporterPreferences(AddonPreferences):
    bl_idname = __name__

    addons_path: StringProperty(
        name="Addons Path",
        description="Base path for all exports - all export paths will be relative to this location",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
    )
    
    static_mesh_export_path: StringProperty(
        name="Static Mesh Export Path",
        description="Path for static mesh exports (e.g., C:\\User\\CS2_Maps\\MapName\\Edit\\static)",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    def draw(self, context):
        layout = self.layout
        
        # Addons path
        layout.prop(self, "addons_path")
        if not self.addons_path:
            box = layout.box()
            box.label(text="⚠ Please set the Addons Path", icon='ERROR')
            box.label(text="This will be the base directory for all exports")
        
        # Static mesh export path
        layout.separator()
        layout.label(text="Static Mesh Export Settings:")
        layout.prop(self, "static_mesh_export_path")
        
        if not self.static_mesh_export_path:
            box = layout.box()
            box.label(text="⚠ Please set the static mesh export path", icon='ERROR')
            box.label(text="This should point to your CS2 static mesh folder")

# List of modules to register
modules = [
    GameModelExporter,
    add_node_operator,
    dev_material_operator,
    static_mesh_operator,
    scene_setup_operator,
    collision_operators,
    fbx_export_operator
]

def register():
    """Register all addon components"""
    # Register preferences first
    bpy.utils.register_class(Source2ExporterPreferences)
    
    # Register the auto-rename handler
    if auto_rename_text_object not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(auto_rename_text_object)
    
    # Register all modules
    for module in modules:
        try:
            module.register()
        except Exception as e:
            print(f"Failed to register module {module.__name__}: {e}")

def unregister():
    """Unregister all addon components"""
    # Unregister the auto-rename handler
    if auto_rename_text_object in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(auto_rename_text_object)
    
    # Unregister modules in reverse order
    for module in reversed(modules):
        try:
            module.unregister()
        except Exception as e:
            print(f"Failed to unregister module {module.__name__}: {e}")
    
    # Unregister preferences last
    bpy.utils.unregister_class(Source2ExporterPreferences)

# This allows running the script directly for testing
if __name__ == "__main__":
    register()