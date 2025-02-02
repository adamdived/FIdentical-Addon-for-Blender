import bpy

bl_info = {
    "name": "Find Identical",
    "author": "Marco Capelli",
    "version": (0, 9, 5),
    "blender": (4, 3, 0),
    "location": "3D Viewport > Sidebar > FIdentical",
    "description": "Find identical or nearly identical objects based on vertex count, dimensions, and volume.",
    "category": "Mesh",
}

# Default tolerance threshold for percentage differences
DEFAULT_EPSILON = 0.05

def find_identical_objects(epsilon):
    # Get the active object
    active_object = bpy.context.active_object

    if not active_object or active_object.type != 'MESH':
        # Show error message if no valid active object is selected
        bpy.ops.wm.message_box('INVOKE_DEFAULT', message="No active mesh object selected!")
        return

    # Get properties of the active object
    active_verts = len(active_object.data.vertices)
    active_dimensions = active_object.dimensions
    active_bbox_volume = active_dimensions[0] * active_dimensions[1] * active_dimensions[2]

    # Store matching objects in a set
    matching_objects = set()

    # Iterate over all objects in the scene
    for obj in bpy.context.view_layer.objects:
        if obj.type == 'MESH' and obj != active_object:
            # Get properties of the current object
            obj_verts = len(obj.data.vertices)
            obj_dimensions = obj.dimensions
            obj_bbox_volume = obj_dimensions[0] * obj_dimensions[1] * obj_dimensions[2]

            # Check if the object matches the criteria
            if (obj_verts == active_verts and
                abs((obj_bbox_volume - active_bbox_volume) / active_bbox_volume) < epsilon and
                all(abs((obj_dimensions[i] - active_dimensions[i]) / active_dimensions[i]) < epsilon
                    for i in range(3))):
                matching_objects.add(obj)

    # Select matching objects
    for obj in matching_objects:
        obj.select_set(True)

    # Report results
    if matching_objects:
        print(f"Found {len(matching_objects)} identical or nearly identical objects.")
    else:
        print("No matching objects found.")

class VIEW3D_PT_FindAllIdentical(bpy.types.Panel):
    bl_label = "Find Identical v0.9.5"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Find Identical'

    def draw(self, context):
        layout = self.layout

        # Display description text
        row = layout.row()
        row.label(text="2023/2025 by Marco Capelli")

        # Add slider for epsilon (tolerance)
        row = layout.row()
        row.prop(context.scene, "find_identical_epsilon", text="Tolerance")

        # Add button to run the script
        row = layout.row()
        row.operator("script.find", text="FIND IDENTICAL")

class SCRIPT_OT_Find(bpy.types.Operator):
    bl_idname = "script.find"
    bl_label = "Find Identical"
    bl_description = "Find identical objects based on vertex count, dimensions, and volume"

    def execute(self, context):
        epsilon = context.scene.find_identical_epsilon
        find_identical_objects(epsilon)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VIEW3D_PT_FindAllIdentical)
    bpy.utils.register_class(SCRIPT_OT_Find)
    # Add a property for epsilon in the scene
    bpy.types.Scene.find_identical_epsilon = bpy.props.FloatProperty(
        name="Tolerance",
        description="Tolerance threshold for identifying identical objects",
        default=DEFAULT_EPSILON,
        min=0.0,
        max=1.0,
    )

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_FindAllIdentical)
    bpy.utils.unregister_class(SCRIPT_OT_Find)
    del bpy.types.Scene.find_identical_epsilon

if __name__ == "__main__":
    register()
