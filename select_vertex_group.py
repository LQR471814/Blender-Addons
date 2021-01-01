bl_info = {
    "name": "Select Vertex Group by Name",
    "description": "Select Vertex Group by name.",
    "author": "LQR471814",
    "blender": (2, 90, 0),
    "category": "Mesh",
}

import bpy

class OPERATOR_OT_SelectVertexGroup(bpy.types.Operator):
    bl_idname = "object.select_vertex_group"
    bl_label = "Select Vertex Group by Name"
    bl_description = "Select Vertex Group by name."
    bl_options = {'REGISTER', 'UNDO'}

    name : bpy.props.StringProperty(name = "Vertex Group Name", default = "")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selected = context.selected_objects

        for obj in selected:
            grp = obj.vertex_groups.get(self.name)
            if grp == None:
                self.report({'ERROR'}, "Vertex group does not exist in object!")
                return {"CANCELLED"}

            obj.vertex_groups.active_index = grp.index

        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

def menu_func(self, context):
    self.layout.operator(OPERATOR_OT_SelectVertexGroup.bl_idname)

def register():
    bpy.utils.register_class(OPERATOR_OT_SelectVertexGroup)
    bpy.types.TOPBAR_MT_app_system.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OPERATOR_OT_SelectVertexGroup)
    bpy.types.TOPBAR_MT_app_system.remove(menu_func)

if __name__ == "__main__":
    register()