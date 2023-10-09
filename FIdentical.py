import bpy

bl_info = {
    "name": "Find Identical",
    "author": "Marco Capelli",
    "version": (0, 4, 0),
    "blender": (3, 5, 0),
    "location": "3D Viewport > Sidebar > FIdentical",
    "description": "Find Identical",
    "category": "Mesh",
}


# Epsilon is the tolerance threshold for percentage differences
epsilon = 0.05


def find_identical_objects():
    # Get the active object
    active_object = bpy.context.active_object

    if active_object and active_object.type == 'MESH':
        # Get the number of vertices of the active object
        active_verts = len(active_object.data.vertices)
    else:
        # Handle the case if there is no active object or it is not a mesh
        # You can choose an appropriate action here, like displaying an error message or providing a default value
        return

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


class VIEW3D_PT_FindAllIdentical(bpy.types.Panel):
    bl_label = "Find Identical v0.4"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Find Identical'

    def draw(self, context):
        layout = self.layout

        # Display description text
        row = layout.row()
        row.label(text="© 2023 by Marco Capelli")

        # Add button to run the script
        row = layout.row()
        row.operator("script.find", text="FIND IDENTICAL")


class SCRIPT_OT_Find(bpy.types.Operator):
    bl_idname = "script.find"
    bl_label = "Find Identical"
    bl_description = "Find identical objects based on vertex count, dimensions, and volume"

    def execute(self, context):
        find_identical_objects()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(VIEW3D_PT_FindAllIdentical)
    bpy.utils.register_class(SCRIPT_OT_Find)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_FindAllIdentical)
    bpy.utils.unregister_class(SCRIPT_OT_Find)


if __name__ == "__main__":
    register()
