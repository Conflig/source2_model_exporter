import bpy
import os
from bpy.types import Operator

class SceneSetupOperator(Operator):
    bl_idname = "object.setup_scene"
    bl_label = "Setup Scene"
    bl_description = "Sets up the scene with proper units and grid"

    def execute(self, context):
        # Get the current file directory
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Specify the script you want to run
        script_path = os.path.join(dir_path, 'setup.py')
        
        try:
            # Execute the script
            exec(compile(open(script_path).read(), script_path, 'exec'))
            self.report({'INFO'}, "Scene setup completed successfully")
        except FileNotFoundError:
            self.report({'ERROR'}, f"Script not found: {script_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Error executing script: {str(e)}")
            
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SceneSetupOperator)

def unregister():
    bpy.utils.unregister_class(SceneSetupOperator)