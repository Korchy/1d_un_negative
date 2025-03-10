# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/1d_un_negative

from bpy.props import FloatProperty
from bpy.types import Operator, Panel, Scene
from bpy.utils import register_class, unregister_class
from math import isclose

bl_info = {
    "name": "Filter Uniformly Scaled",
    "description": "Select objects which have |scale_x|=|scale_y|=|scale_z| != 1.0",
    "author": "Nikita Akimov, Paul Kotelevets",
    "version": (1, 3, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool panel > 1D > Filter Uniformly Scaled",
    "doc_url": "https://github.com/Korchy/1d_un_negative",
    "tracker_url": "https://github.com/Korchy/1d_un_negative",
    "category": "All"
}


# MAIN CLASS

class FilterUniformlyScaled:

    @classmethod
    def detect_uniformly_scaled(cls, context, threshold=0.0001):
        for obj in context.selected_objects:
            if isclose(abs(obj.scale.x), abs(obj.scale.y), rel_tol=threshold) \
                    and isclose(abs(obj.scale.x), abs(obj.scale.z), rel_tol=threshold) \
                    and not isclose(abs(obj.scale.x), 1.0, rel_tol=threshold):
                obj.select = True
            else:
                obj.select = False

    @staticmethod
    def ui(layout, context):
        # ui panel
        op = layout.operator(
            operator='filteruniformlyscaled.detect_uniformly_scaled',
            icon='MAN_SCALE'
        )
        op.threshold = context.scene.filter_uniformly_scaled_prop_threshold
        layout.prop(
            data=context.scene,
            property='filter_uniformly_scaled_prop_threshold',
            text='Threshold'
        )

# OPERATORS

class FilterUniformlyScaled_OT_detect_uniformly_scaled(Operator):
    bl_idname = 'filteruniformlyscaled.detect_uniformly_scaled'
    bl_label = 'Filter Uniformly Scaled'
    bl_options = {'REGISTER', 'UNDO'}

    threshold = FloatProperty(
        name='Threshold',
        subtype='FACTOR',
        min=0.0,
        default=0.0001
    )

    def execute(self, context):
        FilterUniformlyScaled.detect_uniformly_scaled(
            context=context,
            threshold=self.threshold
        )
        return {'FINISHED'}


# PANELS

class FilterUniformlyScaled_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Filter Uniformly Scaled'
    bl_category = '1D'

    def draw(self, context):
        FilterUniformlyScaled.ui(
            layout=self.layout,
            context=context
        )


# REGISTER

def register(ui=True):
    Scene.filter_uniformly_scaled_prop_threshold = FloatProperty(
        name='Filter Uniformly Scaled Selection Threshold',
        subtype='FACTOR',
        min=0.0,
        default=0.0001
    )
    register_class(FilterUniformlyScaled_OT_detect_uniformly_scaled)
    if ui:
        register_class(FilterUniformlyScaled_PT_panel)


def unregister(ui=True):
    if ui:
        unregister_class(FilterUniformlyScaled_PT_panel)
    unregister_class(FilterUniformlyScaled_OT_detect_uniformly_scaled)
    del Scene.filter_uniformly_scaled_prop_threshold


if __name__ == '__main__':
    register()
