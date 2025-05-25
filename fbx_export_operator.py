import bpy
import os
import math
from bpy.types import Operator

class ExportFBXOperator(Operator):
    bl_idname = "object.export_fbx"
    bl_label = "Export model + Coll"
    bl_description = "Export selected models and collision meshes as separate FBX files"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the export scale from the properties
        export_scale = context.scene.export_fbx.export_scale

        # Check if the 'temp' collection exists, if not create it
        if 'temp' not in bpy.data.collections:
            temp_collection = bpy.data.collections.new('temp')
            bpy.context.scene.collection.children.link(temp_collection)
        else:
            temp_collection = bpy.data.collections['temp']

        # Get all selected objects
        selected_objects = bpy.context.selected_objects

        if not selected_objects:
            self.report({'WARNING'}, "No objects selected for export")
            return {'CANCELLED'}

        try:
            # Store original selection
            original_selection = selected_objects.copy()
            
            # Duplicate selected objects and their children and move them to 'temp' collection
            duplicated_objects = []
            
            for obj in original_selection:
                # Deselect all first
                bpy.ops.object.select_all(action='DESELECT')
                
                # Select the object and its children
                obj.select_set(True)
                if obj.children:
                    for child in obj.children:
                        child.select_set(True)
                
                # Duplicate the selection
                bpy.ops.object.duplicate()
                
                # Get the duplicated objects and move them to temp collection
                for duplicated_obj in bpy.context.selected_objects:
                    # Remove from current collections
                    for collection in duplicated_obj.users_collection:
                        collection.objects.unlink(duplicated_obj)
                    # Add to temp collection
                    temp_collection.objects.link(duplicated_obj)
                    duplicated_objects.append(duplicated_obj)
                        
            # Convert all objects in 'temp' collection to mesh
            for obj in temp_collection.objects:
                if obj.type != 'MESH':
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.convert(target='MESH')

            # Deselect everything
            bpy.ops.object.select_all(action='DESELECT')

            # Find parent objects in the 'temp' collection (objects with children)
            parent_objects = []
            for obj in temp_collection.objects:
                if obj.children:
                    parent_objects.append(obj)

            # Process each parent object
            exported_count = 0
            for obj in parent_objects:
                # Get the export path from the custom property of the original object
                # We need to find the corresponding original object
                original_obj = None
                for orig in original_selection:
                    if orig.name.split('.')[0] == obj.name.split('.')[0]:
                        original_obj = orig
                        break
                
                if original_obj is None or "custom_file_path" not in original_obj:
                    self.report({'WARNING'}, f"No export path set for {obj.name}")
                    continue
                    
                output_dir = original_obj["custom_file_path"]
                
                if not output_dir or not os.path.exists(output_dir):
                    self.report({'WARNING'}, f"Invalid export path for {obj.name}: {output_dir}")
                    continue

                # Get the filename from the original text object's content
                # This is the key fix - use the text content, not the object name
                if original_obj.type == 'FONT':
                    base_filename = original_obj.data.body.strip()
                    if not base_filename:
                        # Fallback to object name if text is empty
                        base_filename = original_obj.name.split(".")[0]
                else:
                    # Fallback for non-text objects
                    base_filename = original_obj.name.split(".")[0]

                # Store the current location of the parent
                old_location = obj.location.copy()

                # Move the parent to the center of the scene
                obj.location = (0, 0, 0)

                # Rotate the object 90 degrees on the Z axis (if needed)
                obj.rotation_euler[2] = math.radians(0)

                # Separate collision and regular children
                coll_child = None
                other_children = []
                for child in obj.children:
                    if '_coll' in child.name:
                        coll_child = child
                    else:
                        other_children.append(child)

                # Export collision child as separate FBX
                if coll_child is not None:
                    bpy.ops.object.select_all(action='DESELECT')                    
                    coll_child.select_set(True)
                    bpy.context.view_layer.objects.active = coll_child
                    filename = base_filename + "_coll.fbx"  # Use base_filename instead of obj.name
                    file_path = os.path.join(output_dir, filename)
                    
                    bpy.ops.export_scene.fbx(
                        filepath=file_path, 
                        use_selection=True, 
                        object_types={'MESH'}, 
                        global_scale=export_scale, 
                        mesh_smooth_type='FACE', 
                        use_custom_props=True, 
                        axis_forward='X', 
                        axis_up='Y'
                    )

                # Merge and export other children
                if other_children:
                    bpy.ops.object.select_all(action='DESELECT')
                    for child in other_children:
                        child.select_set(True)
                    
                    if len(other_children) > 1:
                        bpy.context.view_layer.objects.active = other_children[0]
                        bpy.ops.object.join()

                    # Export the merged children as one FBX
                    bpy.ops.object.select_all(action='DESELECT')
                    other_children[0].select_set(True)
                    bpy.context.view_layer.objects.active = other_children[0]
                    filename = base_filename + ".fbx"  # Use base_filename instead of obj.name
                    file_path = os.path.join(output_dir, filename)
                    
                    bpy.ops.export_scene.fbx(
                        filepath=file_path, 
                        use_selection=True, 
                        object_types={'MESH'}, 
                        global_scale=export_scale, 
                        mesh_smooth_type='FACE', 
                        use_custom_props=True, 
                        axis_forward='X', 
                        axis_up='Y'
                    )
                    
                exported_count += 1

            self.report({'INFO'}, f"Successfully exported {exported_count} objects")

        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            return {'CANCELLED'}

        finally:
            # Clean up: select all objects in 'temp' collection and delete them
            try:
                bpy.ops.object.select_all(action='DESELECT')
                objects_to_delete = list(temp_collection.objects)
                for obj in objects_to_delete:
                    obj.select_set(True)
                if objects_to_delete:
                    bpy.ops.object.delete()
            except Exception as cleanup_error:
                self.report({'WARNING'}, f"Cleanup warning: {str(cleanup_error)}")

        return {'FINISHED'}

def register():
    bpy.utils.register_class(ExportFBXOperator)

def unregister():
    bpy.utils.unregister_class(ExportFBXOperator)