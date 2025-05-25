import bpy
import os
from bpy.types import Operator

class AddDevMatOperator(Operator):
    bl_idname = "object.adddevmat"
    bl_label = "Add Dev Mat"
    bl_description = "Adds development material to selected object"

    def execute(self, context):
        # Get the current file directory
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Specify the script you want to run
        script_path = os.path.join(dir_path, 'dev_material.py')
        
        try:
            # Execute the script
            exec(compile(open(script_path).read(), script_path, 'exec'))
            self.report({'INFO'}, "Dev material added successfully")
        except FileNotFoundError:
            self.report({'ERROR'}, f"Script not found: {script_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Error executing script: {str(e)}")
            
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AddDevMatOperator)

def unregister():
    bpy.utils.unregister_class(AddDevMatOperator)