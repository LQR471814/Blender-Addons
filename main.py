bl_info = {
    "name": "Add Modifier",
    "description": "Adds an add menu for Modifiers. Shortcut: Ctrl + Shift + A",
    "author": "LQR471814",
    "blender": (2, 80, 0),
    "category": "User Interface",
}

import bpy

addon_keymaps = []
modifier_operators = []

class ADDMOD_MT_Menu(bpy.types.Menu):
    bl_idname = "ADDMOD_MT_Menu"
    bl_label = "Add Modifier Menu"

    @classmethod
    def poll(self, context):
        if len(context.selected_objects) > 0:
            return {"CANCELLED"}

    def draw(self, context):
        layout = self.layout

        for operator in modifier_operators:
            try:
                layout.operator(operator.bl_idname, text=operator.modName, icon=f"MOD_{operator.modType}")
            except:
                try:
                    layout.operator(operator.bl_idname, text=operator.modName, icon=f"MOD_{operator.modType.replace('_', '')}")
                except:
                    if "MESH" in operator.modType:
                        layout.operator(operator.bl_idname, text=operator.modName, icon="MOD_MESHDEFORM")
                    elif "WEIGHT" in operator.modType:
                        layout.operator(operator.bl_idname, text=operator.modName, icon="MOD_VERTEX_WEIGHT")
                    elif "SMOOTH" in operator.modType:
                        layout.operator(operator.bl_idname, text=operator.modName, icon="MOD_SMOOTH")
                    elif "UV" in operator.modType:
                        layout.operator(operator.bl_idname, text=operator.modName, icon="MOD_UVPROJECT")
                    elif "DEFORM" in operator.modType:
                        layout.operator(operator.bl_idname, text=operator.modName, icon="MOD_SIMPLEDEFORM")
                    elif "WELD" in operator.modType:
                        layout.operator(operator.bl_idname, text=operator.modName, icon="AUTOMERGE_OFF")
                    elif "DECIMATE" in operator.modType:
                        layout.operator(operator.bl_idname, text=operator.modName, icon="MOD_DECIM")
                    elif "HOOK" in operator.modType:
                        layout.operator(operator.bl_idname, text=operator.modName, icon="HOOK")
                    elif "PARTICLE" in operator.modType:
                        layout.operator(operator.bl_idname, text=operator.modName, icon="MOD_PARTICLES")
                    elif "SOFT" in operator.modType and "BODY" in operator.modType:
                        layout.operator(operator.bl_idname, text=operator.modName, icon="MOD_SOFT")
                    elif "COLLISION" in operator.modType:
                        layout.operator(operator.bl_idname, text=operator.modName, icon="MOD_PHYSICS")
                    else:
                        layout.operator(operator.bl_idname, text=operator.modName)

        layout.operator(ClearModifiers.bl_idname, icon="REMOVE")

def onExecute(self, context):
    selected = bpy.context.selected_objects
    if len(selected) > 0:
        for obj in selected:
            obj.modifiers.new("", self.modType)

        return {'FINISHED'}

class ClearModifiers(bpy.types.Operator):
    bl_idname = "object.clear_modifiers"
    bl_label = "Clear Modifiers"
    bl_description = "Clears Modifiers of selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        selected = bpy.context.selected_objects
        for obj in selected:
            obj.modifiers.clear()

        return {'FINISHED'}

def register():
    modifiers = [modifier for modifier in bpy.types.Modifier.bl_rna.properties['type'].enum_items]
    print(modifiers)
    for mod in modifiers:
        modifier_operators.append(type("", (bpy.types.Operator, object), {
            "execute": (onExecute),
            "bl_idname": f"object.add_{mod.identifier.lower()}",
            "bl_label": f"Add {mod.name}",
            "bl_description": f"Adds {mod.name} to selected objects",
            "bl_options": {'REGISTER', 'UNDO'},
            "modType": mod.identifier,
            "modName": mod.name,
        } ))

    for operator in modifier_operators:
        bpy.utils.register_class(operator)

    bpy.utils.register_class(ClearModifiers)
    bpy.utils.register_class(ADDMOD_MT_Menu)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')

        kmi = km.keymap_items.new("wm.call_menu", 'A', 'PRESS', ctrl=True, shift=True)
        kmi.properties.name = ADDMOD_MT_Menu.bl_idname

        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    for operator in modifier_operators:
        bpy.utils.unregister_class(operator)
    bpy.utils.unregister_class(ADDMOD_MT_Menu)

if __name__ == "__main__":
    register()