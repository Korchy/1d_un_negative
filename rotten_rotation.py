# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/1d_rotten_rotation

from math import isclose
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class

bl_info = {
    "name": "Rotten Rotation",
    "description": "Detects objects which have rotation equal to -180 about X, Y or Z axis",
    "author": "Nikita Akimov, Paul Kotelevets",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool panel > 1D > Rotten Rotation",
    "doc_url": "https://github.com/Korchy/1d_rotten_rotation",
    "tracker_url": "https://github.com/Korchy/1d_rotten_rotation",
    "category": "All"
}


# MAIN CLASS

class RottenRotation:

    @classmethod
    def detect_rotten(cls, context):
        # detect objects which have rotation equal to -180 about X, Y or Z axis
        for obj in context.selected_objects:
            if all((not isclose(channel, -3.14, rel_tol=0.01) for channel in obj.rotation_euler)):
                obj.select = False

    @staticmethod
    def ui(layout, context):
        # ui panel
        layout.operator(
            operator='rotten_rotation.detect_rotten',
            icon='MOD_MIRROR'
        )

# OPERATORS

class RottenRotation_OT_detect_rotten(Operator):
    bl_idname = 'rotten_rotation.detect_rotten'
    bl_label = 'Detect Rotation'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        RottenRotation.detect_rotten(
            context=context
        )
        return {'FINISHED'}


# PANELS

class RottenRotation_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Rotten Rotation'
    bl_category = '1D'

    def draw(self, context):
        RottenRotation.ui(
            layout=self.layout,
            context=context
        )


# REGISTER

def register(ui=True):
    register_class(RottenRotation_OT_detect_rotten)
    if ui:
        register_class(RottenRotation_PT_panel)


def unregister(ui=True):
    if ui:
        unregister_class(RottenRotation_PT_panel)
    unregister_class(RottenRotation_OT_detect_rotten)


if __name__ == '__main__':
    register()
