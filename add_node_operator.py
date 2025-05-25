import bpy
import os
from bpy.types import Operator

class AddNodeOperator(Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Create Node"
    bl_description = "Creates a text node at the center of selected objects"

    def execute(self, context):
        # Get the current file directory
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Specify the script you want to run
        script_path = os.path.join(dir_path, 'add_node.py')
        
        try:
            # Execute the script
            exec(compile(open(script_path).read(), script_path, 'exec'))
            self.report({'INFO'}, "Node created successfully")
        except FileNotFoundError:
            self.report({'ERROR'}, f"Script not found: {script_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Error executing script: {str(e)}")
            
        return {'FINISHED'}

def register():
    bpy.utils.register_class(AddNodeOperator)

def unregister():
    bpy.utils.unregister_class(AddNodeOperator)