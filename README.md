** In latest update you DO NOT NEED to manually setup custom property. It will be automatically added on export for both static and props. Just make sure the materials name always match the Hammers asset name**


Source2 Model Exporter

It is a simple-to-use plugin for Blender that I created during the development of my map for Counter-Strike 2.

Quick disclaimer! AI was used to help me create this plugin. I have limited knowledge of programming, and this tool was made to assist me. However, since I found it really useful, I decided to make it available to everyone. If you don’t like that AI was involved, I fully understand.

![image](https://github.com/user-attachments/assets/ff6b0c82-2650-48fc-ab83-fb12c15f584a)



![image](https://github.com/user-attachments/assets/0a244812-b5e2-4a58-b151-d6be895a94f3)

Setup Scene will create an empty scene, change the units to inches, and create a cube with dimensions of 64 inches.
Additionally, the scene grid will be split into 16-inch sections.



![image](https://github.com/user-attachments/assets/d32c794a-c98e-4a8a-b05a-e468f411b79f)

This was the main reason this plugin was created. When you create a custom prop for your level, select it and click 'Create Node.' (If you have selected multiple objects, they will be part of one prop.)
This will create a new text object with the name of the selected object in red. 

this will be the name of the exported mesh (If you want to rename your prop just enter edit mode and type the new name). All the objects will now be children of this object, allowing you to move them anywhere in your scene.
The pivot of the Node will be the pivot of the exported object. The pivot is taken from the pivot of the mesh at the time the Node was created. If you want to adjust the pivot position, modify the placement of the child objects.

![image](https://github.com/user-attachments/assets/6ab519b2-b083-403f-ba5d-dc0553a7ebae)

Now you will need to define export path of the Prop. Keep in mind this path need to be INSIDE of the CS2's content folder!

example: F:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\content\csgo_addons\test\models\test_model

Now when the export path is setup the node will turn white and you can now hit EXPORT (see below how to setup new prop inside the Source 2)

You dont need to care about scale or export parameters 




![image](https://github.com/user-attachments/assets/6b86fdb6-7822-4fc9-a9b5-933a72392338)

Add Material' will create a new material with a basic grid texture. At the same time, it also adds a custom property with the relative path to the material inside the Hammer editor. This means that if you export your prop with this material, it will use the same material inside the Hammer editor.

You can use all materials available in the Hammer editor. However, note that they will not be visible in Blender, as Blender cannot read the file format of the textures.
To change the material you just need to copy path of the material inside the hammer Asset browser 

![image](https://github.com/user-attachments/assets/e4f668b9-992b-423d-9df8-0197d72a7f9a)






![image](https://github.com/user-attachments/assets/be6372d7-16f3-451a-acb1-3aab25b369e1)
![image](https://github.com/user-attachments/assets/700c3c6c-5313-4573-8690-4cbc6d9a1310)

Since Counter-Strike 2, you can now use modeling tools directly inside the Hammer editor.
However, if you feel more efficient in Blender, you can model all your non-prop geometry there and simply import it into Hammer. Material linking will still work, even with vertex colors for blended materials.


Just select the objects you want to export and click the button. (Export path is defined Add-ons Preferences)


Unfortunately, there is no way to replace static geometry in the Hammer editor—you will always need to manually delete and then import it. It would be great if we could find a way to automate this process.



![image](https://github.com/user-attachments/assets/6f177207-e45b-494b-b595-6f22feb3f86f)

Props need collisions! Model a simple collision out of boxes (can be multiple objects but all need to be boxes) Merge all boxes in to one object (CTRL + J)
Select the collision and then with Shift select the Node of the object we want to have the collison 

![image](https://github.com/user-attachments/assets/b6eff793-f94e-4ccd-9167-405b4aad5dfa)


All is now ready and you can hit the export 
This will create 2 files in the directory 

![image](https://github.com/user-attachments/assets/1b179aa8-85d5-4b57-907c-7c10e728ffc4)


How to setup the prop in Hammer?

In the hammer editor acces the ModelDoc

![image](https://github.com/user-attachments/assets/2df7c08c-4837-4000-860f-eb1ca0f70143)

Create a new model by double clicking the "Model"

![image](https://github.com/user-attachments/assets/4587f26f-4a29-47d3-b084-0cbdad1c8a68)

Click the Add button and find "RenderMeshList"

![image](https://github.com/user-attachments/assets/3c7f9b83-3ba8-401c-9f87-3d97cbc567fd)

To add the collisions also click ADD and then look for "PhysicsShapeList"

![image](https://github.com/user-attachments/assets/80d56185-36ff-44e6-99c8-e8742788cbd8)

After just click compile and save the new model 
You need to do this just to set up the model. Now when you hit "Export model in blender it will automatically update the prop in Hammer






![image](https://github.com/user-attachments/assets/c3ecdc10-b4f6-4749-a406-5f68c965f579)
![image](https://github.com/user-attachments/assets/67d4da6c-c6d0-41b4-be8e-1b5e7e81b8e7)
![image](https://github.com/user-attachments/assets/cd25cd4e-d774-4a15-817f-5a08c8d0e920)












