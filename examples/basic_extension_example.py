import sys
from neuroglancer_annotation_ui.base import AnnotationManager, stop_ngl_server
from annotationframeworkclient.infoservice import InfoServiceClient
from example_extensions import PointDropperExtension
import click

info_url = 'https://www.dynamicannotationframework.com'
dataset = 'pinky100dev'

infoclient = InfoServiceClient(server_address=info_url,
                               dataset_name=dataset)
img_src = infoclient.image_source(format_for='neuroglancer')
seg_src = infoclient.flat_segmentation_source(format_for='neuroglancer')

if __name__ == '__main__':

    manager = AnnotationManager()
    manager.add_image_layer(layer_name='img', image_source=img_src)
    manager.add_segmentation_layer(layer_name='seg', segmentation_source=seg_src)
    manager.add_extension(extension_name='basic_extension',
                          ExtensionClass=PointDropperExtension) 

    click.echo(manager.viewer.url)
    click.echo('\tNeuroglancer server running. Press q to quit')
    while True:
        c = click.getchar()
        if c == 'q':
            break
        else:
            pass
    
    stop_ngl_server()