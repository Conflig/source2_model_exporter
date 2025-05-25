import bpy

# Find all collision objects
collision_objects = []
for obj in bpy.context.scene.objects:
    if '_coll' in obj.name.lower():
        collision_objects.append(obj)

if not collision_objects:
    print("No collision objects found (objects containing '_coll')")
else:
    # Count visible and hidden objects
    visible_count = 0
    hidden_count = 0
    
    for obj in collision_objects:
        if obj.hide_viewport:
            hidden_count += 1
        else:
            visible_count += 1
    
    total_count = len(collision_objects)
    
    print(f"Found {total_count} collision objects:")
    print(f"  - Visible: {visible_count}")
    print(f"  - Hidden: {hidden_count}")
    
    # Determine action based on majority
    if visible_count >= hidden_count:
        # More objects are visible (or equal), so HIDE ALL
        target_state = True  # True means hidden
        action = "HIDING"
    else:
        # More objects are hidden, so SHOW ALL
        target_state = False  # False means visible
        action = "SHOWING"
    
    print(f"\n{action} all collision objects...")
    
    # Apply the target state to all collision objects
    changes_made = 0
    for obj in collision_objects:
        if obj.hide_viewport != target_state:
            obj.hide_viewport = target_state
            changes_made += 1
    
    if target_state:
        print(f"SUCCESS: All {total_count} collision objects are now HIDDEN")
    else:
        print(f"SUCCESS: All {total_count} collision objects are now VISIBLE")
    
    print(f"Made changes to {changes_made} objects")