import bpy
import os
from bpy.types import Operator

class StaticMeshOperator(Operator):
    bl_idname = "object.staticmesh"
    bl_label = "Export Static Geometry"
    bl_description = "Exports selected objects as static geometry"

    def execute(self, context):
        # Get the current file directory
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Specify the script you want to run
        script_path = os.path.join(dir_path, 'static_mesh.py')
        
        try:
            # Execute the script
            exec(compile(open(script_path).read(), script_path, 'exec'))
            self.report({'INFO'}, "Static mesh exported successfully")
        except FileNotFoundError:
            self.report({'ERROR'}, f"Script not found: {script_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Error executing script: {str(e)}")
            
        return {'FINISHED'}

def register():
    bpy.utils.register_class(StaticMeshOperator)

def unregister():
    bpy.utils.unregister_class(StaticMeshOperator)