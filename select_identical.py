import bpy

# Epsilon is the tolerance threshold for percentage differences
epsilon = 0.05

# Get the active object
active_object = bpy.context.active_object

# Get the number of vertices of the active object
active_verts = len(active_object.data.vertices)

# Get the dimensions of the active object
dim_x, dim_y, dim_z = active_dimensions = active_object.dimensions

# Calculate the volume of the active object's bounding box
active_bbox_volume = dim_x * dim_y * dim_z

# Iterate over all objects in the scene
for obj in bpy.context.view_layer.objects:
    # Only check objects of type MESH
    if obj.type == 'MESH':
        # Get the number of vertices of the current object
        obj_verts = len(obj.data.vertices)
        
        # If the number of vertices matches the active object
        if obj_verts == active_verts:
            # If the dimensions of the current object are exactly the same as the active object
            if obj.dimensions == active_dimensions:
                obj.select_set(True)  # Select the object
            
            # Calculate the volume of the current object's bounding box
            current_bbox_volume = obj.dimensions[0] * obj.dimensions[1] * obj.dimensions[2]
            
            # If the percentage difference between the volumes is less than the threshold (epsilon)
            if abs((current_bbox_volume - active_bbox_volume) / active_bbox_volume) < epsilon:
                obj.select_set(True)  # Select the object
            
            # If each individual dimension of the current object differs by a percentage from the active object
            # within the threshold (epsilon)
            if all(
                abs((obj.dimensions[i] - active_object.dimensions[i]) / active_object.dimensions[i]) < epsilon
                for i in range(3)
            ):
                obj.select_set(True)  # Select the object
