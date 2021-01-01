bl_info = {
    "name": "Swap Vertex Group Data",
    "description": "Swaps vertex group data between two vertex groups.",
    "author": "LQR471814",
    "blender": (2, 90, 0),
    "category": "Mesh",
}

import bpy

class OPERATOR_OT_SwapVertexGroups(bpy.types.Operator):
    bl_idname = "object.swap_vertex_groups"
    bl_label = "Swap Vertex Groups"
    bl_description = "Swaps vertex group data between two vertex groups."
    bl_options = {'REGISTER', 'UNDO'}

    g1 : bpy.props.StringProperty(name = "First Vertex Group", default = "")
    g2 : bpy.props.StringProperty(name = "Second Vertex Group", default = "")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selected = bpy.context.selected_objects

        for obj in selected:
            vg1 = obj.vertex_groups.get(self.g1)
            vg2 = obj.vertex_groups.get(self.g2)

            vg_idx1 = vg1.index
            vs1 = getVertexAndWeights(obj, vg_idx1)

            vg_idx2 = vg2.index
            vs2 = getVertexAndWeights(obj, vg_idx2)

            vg1.remove(list(vs1.keys()))
            vg2.remove(list(vs2.keys()))

            for key in list(vs1.keys()):
                vg2.add([key], vs1[key], 'REPLACE')

            for key in list(vs2.keys()):
                vg1.add([key], vs2[key], 'REPLACE')

        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

def getVertexAndWeights(obj, grp_idx):
    vs = {}
    for v in obj.data.vertices:
        try:
            if grp_idx in [vg.group for vg in v.groups]:
                vs[v.index] = v.groups[0].weight
        except RuntimeError:
            vs[v.index] = 0
        except IndexError:
            vs[v.index] = 0
    return vs

def menu_func(self, context):
    self.layout.operator(OPERATOR_OT_SwapVertexGroups.bl_idname)

def register():
    bpy.utils.register_class(OPERATOR_OT_SwapVertexGroups)
    bpy.types.TOPBAR_MT_app_system.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OPERATOR_OT_SwapVertexGroups)
    bpy.types.TOPBAR_MT_app_system.remove(menu_func)

if __name__ == "__main__":
    register()