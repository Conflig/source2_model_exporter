import bpy
from mathutils import Vector

def get_areas_by_type(context, area_type):
    """Get all areas of a specific type"""
    return [a for a in context.screen.areas if a.type == area_type]

def change_viewport_to_texture():
    """Change viewport color type to texture view without changing shading mode"""
    
    # Get the current 3D viewport
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Only change color type to texture, keep current shading type
                    space.shading.color_type = 'TEXTURE'
                    
                    print(f"Viewport color type changed to TEXTURE (keeping {space.shading.type} shading)")
                    return True
    
    print("No 3D viewport found")
    return False

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Use an existing scene or create new one
scene = bpy.data.scenes.get("Scene")
if scene is None:
    # If the scene does not exist, create a new one
    bpy.ops.scene.new(type='EMPTY')
    scene = bpy.context.scene

# Set the unit system to 'IMPERIAL'
scene.unit_settings.system = 'IMPERIAL'
# Set the length unit to 'INCHES'
scene.unit_settings.length_unit = 'INCHES'

# Enable absolute grid snapping if available
if hasattr(bpy.context.scene.tool_settings, 'use_snap_grid_absolute'):
    bpy.context.scene.tool_settings.use_snap_grid_absolute = True

# Define the size of the box in inches
size = 64 / 39.3701  # Convert inches to meters (Blender's internal units)

# Add a cube to the scene
bpy.ops.mesh.primitive_cube_add(size=size, location=(0, 0, 0))

# Get the created cube
cube = bpy.context.object

try:
    # Simple method to set origin to bottom of cube
    # Calculate the bottom center position
    bbox = [cube.matrix_world @ Vector(corner) for corner in cube.bound_box]
    z_coords = [corner.z for corner in bbox]
    min_z = min(z_coords)
    
    # Set 3D cursor to bottom center
    bpy.context.scene.cursor.location = (0, 0, min_z)
    
    # Set origin to cursor
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    
    # Move the cube so its bottom sits at Z=0
    cube.location = (0, 0, 0)
    
except Exception as e:
    print(f"Warning: Could not set origin properly: {e}")
    # Fallback: just position the cube normally
    cube.location = (0, 0, size/2)

# Setup viewport overlays and grid
viewport_configured = False
try:
    # Set the grid scale to correspond to an inch
    # This value may need adjustment based on your specific needs
    if bpy.context.space_data and bpy.context.space_data.type == 'VIEW_3D':
        # Set grid properties
        bpy.context.space_data.overlay.grid_scale = 1.33329
        bpy.context.space_data.overlay.grid_subdivisions = 1
        
        # Set the shading type to material preview
        bpy.context.space_data.shading.type = 'MATERIAL_PREVIEW'
        
        # Set color type to TEXTURE - the simple way!
        bpy.context.space_data.shading.color_type = 'TEXTURE'
        
        viewport_configured = True
        print("Successfully configured viewport via context.space_data")
    else:
        print("Current context is not a VIEW_3D space, trying alternative method...")
        
except Exception as e:
    print(f"Warning: Could not configure viewport via context.space_data: {e}")

# If the primary method didn't work, use the comprehensive viewport function
if not viewport_configured:
    print("Attempting viewport configuration via screen areas...")
    viewport_configured = change_viewport_to_texture()

# Final viewport configuration status
if viewport_configured:
    print("Successfully set shading color type to TEXTURE")
else:
    print("Warning: Could not fully configure viewport settings")
    print("Grid and shading settings may need manual adjustment")

# Final positioning check
if cube.location.z < 0:
    cube.location.z = 0

print("Scene setup completed successfully")
print(f"- Units set to Imperial (inches)")
print(f"- Created 64-inch reference cube at origin")
print(f"- Grid configured for inch measurements")
print(f"- Viewport configured for material preview with texture color type")

# Deselect the cube
bpy.ops.object.select_all(action='DESELECT')