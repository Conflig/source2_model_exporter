import bpy
import os

def add_vmat_properties_to_objects(objects):
    """Add FBX_vmatPath custom property to objects based on their material names"""
    for obj in objects:
        if obj.type == 'MESH' and obj.data.materials:
            # Get the first material (primary material)
            material = obj.data.materials[0]
            if material:
                # Add the custom property with the material name
                obj["FBX_vmatPath"] = material.name
                print(f"Added FBX_vmatPath='{material.name}' to object '{obj.name}'")

# Get the addon preferences
addon_prefs = bpy.context.preferences.addons[__name__.split('.')[0]].preferences

# Get export path from user preferences
export_path = addon_prefs.static_mesh_export_path

# Exit if no export path is defined
if not export_path:
    print("Error: No export path defined. Please set the path in addon preferences.")
    print(f"Go to Edit > Preferences > Add-ons > Source 2 Model Exporter > Preferences")
    # Exit the script without doing anything
    exit()

temp_folder_name = "TEMPEXPORT"

print(f"Using export path: {export_path}")

# Ensure the export path exists
try:
    if not os.path.exists(export_path):
        os.makedirs(export_path)
        print(f"Created export directory: {export_path}")
except Exception as e:
    print(f"Error: Could not create export directory: {e}")
    # Exit if we can't create the directory
    exit()

# Check if any objects are selected
if not bpy.context.selected_objects:
    print("No objects selected. Please select objects to export.")
else:
    # Ensure the TEMPEXPORT collection exists
    if temp_folder_name not in bpy.data.collections:
        temp_collection = bpy.data.collections.new(temp_folder_name)
        bpy.context.scene.collection.children.link(temp_collection)
    else:
        temp_collection = bpy.data.collections[temp_folder_name]

    # Store original selection
    original_selection = bpy.context.selected_objects.copy()

    try:
        # Duplicate selected objects and move duplicates to TEMPEXPORT collection
        bpy.ops.object.duplicate()
        duplicated_objects = bpy.context.selected_objects.copy()
        
        for obj in duplicated_objects:
            # Remove from all current collections
            for collection in obj.users_collection:
                collection.objects.unlink(obj)
            # Add to temp collection
            temp_collection.objects.link(obj)

        # Add FBX_vmatPath custom properties to all duplicated objects
        add_vmat_properties_to_objects(temp_collection.objects)

        # Add Edge Split modifier to each duplicated object
        for obj in temp_collection.objects:
            if obj.type == 'MESH':
                # Check if edge split modifier already exists
                edge_split_exists = any(mod.type == 'EDGE_SPLIT' for mod in obj.modifiers)
                
                if not edge_split_exists:
                    edge_split_modifier = obj.modifiers.new(name="EdgeSplit", type='EDGE_SPLIT')
                    edge_split_modifier.use_edge_angle = False
                    edge_split_modifier.use_edge_sharp = True

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # Select all objects in TEMPEXPORT collection
        for obj in temp_collection.objects:
            obj.select_set(True)

        # Set an active object for export
        if temp_collection.objects:
            bpy.context.view_layer.objects.active = temp_collection.objects[0]

        # Define the file path for the combined export
        file_path = os.path.join(export_path, "combined_export.fbx")

        # Export all selected objects as one file with specified parameters
        try:
            bpy.ops.export_scene.fbx(
                filepath=file_path,
                use_selection=True,
                object_types={'MESH'},
                bake_space_transform=False,
                axis_forward='-Z',
                axis_up='Y',
                global_scale=0.393701,
                use_custom_props=True,
                # Updated for Blender 4.4 - mesh_smooth_type might have changed
                mesh_smooth_type='FACE'
            )
            print(f"Successfully exported all objects to {file_path} with VMAT properties")
            
        except Exception as e:
            print(f"Export failed: {e}")
            # Try alternative export settings
            try:
                bpy.ops.export_scene.fbx(
                    filepath=file_path,
                    use_selection=True,
                    object_types={'MESH'},
                    global_scale=0.393701,
                    use_custom_props=True
                )
                print(f"Exported with fallback settings to {file_path} with VMAT properties")
            except Exception as e2:
                print(f"Fallback export also failed: {e2}")

    except Exception as e:
        print(f"Error during export process: {e}")

    finally:
        # Clean up: delete all objects in TEMPEXPORT collection
        try:
            bpy.ops.object.select_all(action='DESELECT')
            objects_to_delete = list(temp_collection.objects)
            
            for obj in objects_to_delete:
                obj.select_set(True)
                
            if objects_to_delete:
                bpy.ops.object.delete()

            # Delete the TEMPEXPORT collection
            bpy.data.collections.remove(temp_collection)
            print("Cleanup completed: TEMPEXPORT collection deleted.")
            
        except Exception as cleanup_error:
            print(f"Cleanup warning: {cleanup_error}")

        # Restore original selection
        try:
            bpy.ops.object.select_all(action='DESELECT')
            for obj in original_selection:
                if obj.name in bpy.data.objects:  # Check if object still exists
                    obj.select_set(True)
        except Exception as selection_error:
            print(f"Could not restore original selection: {selection_error}")

    print("Static mesh export process completed.")