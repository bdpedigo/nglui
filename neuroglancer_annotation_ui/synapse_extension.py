from neuroglancer_annotation_ui.extension_core import check_layer, AnnotationExtensionBase, PointHolder
from neuroglancer_annotation_ui.ngl_rendering import SchemaRenderer
from neuroglancer_annotation_ui.annotation import point_annotation, \
                                                  line_annotation
from emannotationschemas.synapse import SynapseSchema

class SynapseSchemaWithRule(SynapseSchema):
    @staticmethod
    def render_rule():
        return {'line': {'pre': [('pre_pt', 'ctr_pt')],
                         'post': [('post_pt', 'ctr_pt')]},
                'point': {'syn': ['ctr_pt']}
                }


class SynapseExtension(AnnotationExtensionBase):
    def __init__(self, easy_viewer, annotation_client=None):
        super(SynapseExtension, self).__init__(easy_viewer, annotation_client)
        self.ngl_renderer = {'synapse':SchemaRenderer(SynapseSchemaWithRule)}
        self.allowed_layers = ['synapses']

        self.color_map = {'synapses': '#cccccc',
                          'synapses_pre': '#ff0000',
                          'synapses_post': '#00ffff',
                          }
        self.message_dict = {'pre_pt': 'presynaptic point',
                             'post_pt': 'postsynaptic point',
                             'ctr_pt': 'synapse'}
        self.point_layer_dict = {'pre_pt': 'synapses_pre',
                                 'post_pt': 'synapses_post',
                                 'ctr_pt': 'synapses'}
        self.anno_layer_dict = {'pre':'synapses_pre',
                                'post':'synapses_post',
                                'syn':'synapses'}

        self.create_synapse_layers(None)
        self.points = PointHolder(viewer=self.viewer,
                                  pt_types=['pre_pt','post_pt', 'ctr_pt'],
                                  trigger='ctr_pt',
                                  layer_dict=self.point_layer_dict)

    @staticmethod
    def _default_key_bindings():
        bindings = {
            'update_presynaptic_point': 'keyd',
            'update_center_synapse_point': 'keyf',
            'update_postsynaptic_point': 'keyg',
            }
        return bindings

    @staticmethod
    def _defined_layers():
        return ['synapses_pre', 'synapses_post', 'synapses']

    def create_synapse_layers(self, s):
        for layer in self._defined_layers():
            self.viewer.add_annotation_layer(layer,
                                             color=self.color_map[layer])

    @check_layer()
    def update_presynaptic_point(self, s):
        self.update_synapse_points('pre_pt', s)

    @check_layer()
    def update_postsynaptic_point(self, s):
        self.update_synapse_points('post_pt', s)

    @check_layer()
    def update_center_synapse_point(self, s):
        self.update_synapse_points('ctr_pt', s)

    def update_synapse_points(self, point_type, s):
        pos = self.viewer.get_mouse_coordinates(s)
        anno_done = self.points.update_point(pos,
                                             point_type,
                                             message_type=self.message_dict[point_type])

        if anno_done:
            self.render_and_post_annotation(self.format_synapse_data,
                                            'synapse',
                                            self.anno_layer_dict,
                                            'synapse')
            self.points.reset_points()

    def format_synapse_data(self, points):
        return {'type':'synapse',
                'pre_pt':{'position':[int(x) for x in points['pre_pt'].point]},
                'ctr_pt':{'position':[int(x) for x in points['ctr_pt'].point]},
                'post_pt':{'position':[int(x) for x in points['post_pt'].point]}}

    def _update_annotation(self, ngl_id):
        anno_id = self.get_anno_id(ngl_id)
        d_syn = self.annotation_df[self.annotation_df.anno_id==anno_id]
        ngl_id_ctr = d_syn[d_syn.layer=='synapses'].ngl_id.values[0]
        ngl_id_pre = d_syn[d_syn.layer=='synapses_pre'].ngl_id.values[0]
        ngl_id_post = d_syn[d_syn.layer=='synapses_post'].ngl_id.values[0]
        print(ngl_id_pre)
        print(ngl_id_ctr)
        print(ngl_id_post)

        self.points.reset_points()
        self.points.update_point(self._get_pt_pos('synapses_pre', ngl_id_pre), 'pre_pt')
        self.points.update_point(self._get_pt_pos('synapses_post', ngl_id_post), 'post_pt')
        self.points.update_point(self._get_pt_pos('synapses', ngl_id_ctr), 'ctr_pt')
        print(self.points())
        new_datum = self.format_synapse_data( self.points() )
        self.points.reset_points()

        ae_type, ae_id = self.parse_anno_id(anno_id)
        self.annotation_client.update_annotation(ae_type, ae_id, new_datum)
        self.viewer.update_message('Updated synapse annotation!')

    def _get_pt_pos(self, ln, ngl_id):
        for anno in self.viewer.state.layers[ln].annotations:
            if anno.id == ngl_id:
                if anno.type == 'point':
                    return anno.point
                elif anno.type == 'line':
                    return anno.pointA
        else:
            return None