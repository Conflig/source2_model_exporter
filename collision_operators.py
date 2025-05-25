import bpy
import os
from bpy.types import Operator

class HideCollOperator(Operator):
    bl_idname = "object.hide_coll"
    bl_label = "Hide/Show Coll"
    bl_description = "Toggle visibility of collision objects"

    def execute(self, context):
        # Get the current file directory
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Specify the script you want to run
        script_path = os.path.join(dir_path, 'collision.py')
        
        try:
            # Execute the script
            exec(compile(open(script_path).read(), script_path, 'exec'))
            self.report({'INFO'}, "Collision visibility toggled")
        except FileNotFoundError:
            self.report({'ERROR'}, f"Script not found: {script_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Error executing script: {str(e)}")
            
        return {'FINISHED'}

class SetupCollOperator(Operator):
    bl_idname = "object.setup_coll"
    bl_label = "Setup Coll"
    bl_description = "Select the collision object and with shift select then Node of prop this coolisions belongs to"

    def execute(self, context):
        # Get the current file directory
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Specify the script you want to run
        script_path = os.path.join(dir_path, 'collision_set.py')
        
        try:
            # Execute the script
            exec(compile(open(script_path).read(), script_path, 'exec'))
            self.report({'INFO'}, "Collision setup completed")
        except FileNotFoundError:
            self.report({'ERROR'}, f"Script not found: {script_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Error executing script: {str(e)}")
            
        return {'FINISHED'}

def register():
    bpy.utils.register_class(HideCollOperator)
    bpy.utils.register_class(SetupCollOperator)

def unregister():
    bpy.utils.unregister_class(SetupCollOperator)
    bpy.utils.unregister_class(HideCollOperator)