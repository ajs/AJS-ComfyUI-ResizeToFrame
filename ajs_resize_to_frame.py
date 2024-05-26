#import random
#import io
#import re
#from PIL import Image
#from PIL import ImageOps
#import numpy as np
#import torch
#from torchvision.ops import masks_to_boxes
import comfy.utils
#import os


TEXT_TYPE = "STRING"
INT_TYPE = "INT"
IMAGE_TYPE = "IMAGE"
UND='undefined'


class AjsResizeToFrame:
    """
    Resize a `source_image` into the frame of a `frame_image`.
    the source and frame images' aspect ratios will be preserved.
    The source image will be as large as possible within the frame
    image without cropping.
    The frame image will only be visible where empty space is
    left around the source.

    The `alignment` parameter controls where the source image is placed
    within the frame image if there is additional space left over.
    This is directly passed to the `crop` parameter of
    `comfy.utils.common_upscale`, which you can see for more detail.
    """
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "source_image": (IMAGE_TYPE,),
                "frame_image": (IMAGE_TYPE,),
                "alignment": {["center", "disabled"]},
            }
        }

    RETURN_TYPES = (IMAGE_TYPE,)
    RETURN_NAMES = ("image",)
    FUNCTION = "calculate"

    CATEGORY = "AJS"

    @staticmethod
    def _calculate_largest_dimensions(source_size, frame_size):
        source_width, source_height = source_size
        frame_width, frame_height = frame_size

        # Calculate the scaling factors for width and height
        width_scale = frame_width / source_width
        height_scale = frame_height / source_height

        # Choose the smaller scaling factor to ensure the source image fits within the frame
        scale_factor = min(width_scale, height_scale)

        # Calculate the largest dimensions to scale the source image to
        scaled_width = int(source_width * scale_factor)
        scaled_height = int(source_height * scale_factor)

        return scaled_width, scaled_height


    def calculate(self, source_image, frame_image, alignment):
        source_size = source_image.size()
        frame_size = frame_image.size()
        new_source_size = self._calculate_largest_dimensions(source_size, frame_size)
        samples = source_image.movedim(-1,1)
        new_source_image = comfy.utils.common_upscale(
            samples, new_source_size[0], new_source_size[1],
            upscale_method='lanczos',
            crop=alignment,
        )
        return frame_image + new_source_image


NODE_CLASS_MAPPINGS = {
    "AJS Resize to Frame": AjsResizeToFrame,
}
