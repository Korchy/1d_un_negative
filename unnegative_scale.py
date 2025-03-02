# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/1d_un_negative

from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class

bl_info = {
    "name": "Unnegative scale",
    "description": "Detects objects which have scale < 0.0 about X, Y or Z axis and restore it",
    "author": "Nikita Akimov, Paul Kotelevets",
    "version": (1, 2, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool panel > 1D > Unnegative scale",
    "doc_url": "https://github.com/Korchy/1d_un_negative",
    "tracker_url": "https://github.com/Korchy/1d_un_negative",
    "category": "All"
}


# MAIN CLASS

class UnnegativeScale:

    @classmethod
    def unnegative_scale(cls, objs):
        # make all scale channels positive for selected objects
        for obj in objs:
            if obj.scale.x < 0.0:
                obj.scale.x = abs(obj.scale.x)
            if obj.scale.y < 0.0:
                obj.scale.y = abs(obj.scale.y)
            if obj.scale.z < 0.0:
                obj.scale.z = abs(obj.scale.z)

    @classmethod
    def detect_negative_scale(cls, context):
        # detect objects which have negative scale (< 0.0) about X, Y or Z axis
        for obj in context.selected_objects:
            if all((channel >= 0.0 for channel in obj.scale)):
                obj.select = False

    @staticmethod
    def ui(layout, context):
        # ui panel
        layout.operator(
            operator='unnegative_scale.unnegative_scale',
            icon='MOD_MIRROR'
        )
        layout.operator(
            operator='unnegative_scale.detect_negative_scale',
            icon='IMPORT'
        )

# OPERATORS

class UnnegativeScale_OT_unnegative_scale(Operator):
    bl_idname = 'unnegative_scale.unnegative_scale'
    bl_label = 'Unnegative Scale'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        UnnegativeScale.unnegative_scale(
            objs=context.selected_objects
        )
        return {'FINISHED'}


class UnnegativeScale_OT_detect_negative_scale(Operator):
    bl_idname = 'unnegative_scale.detect_negative_scale'
    bl_label = 'Negative Scale Selection'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        UnnegativeScale.detect_negative_scale(
            context=context
        )
        return {'FINISHED'}


# PANELS

class UnnegativeScale_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Unnegative Scale'
    bl_category = '1D'

    def draw(self, context):
        UnnegativeScale.ui(
            layout=self.layout,
            context=context
        )


# REGISTER

def register(ui=True):
    register_class(UnnegativeScale_OT_unnegative_scale)
    register_class(UnnegativeScale_OT_detect_negative_scale)
    if ui:
        register_class(UnnegativeScale_PT_panel)


def unregister(ui=True):
    if ui:
        unregister_class(UnnegativeScale_PT_panel)
    unregister_class(UnnegativeScale_OT_detect_negative_scale)
    unregister_class(UnnegativeScale_OT_unnegative_scale)


if __name__ == '__main__':
    register()
