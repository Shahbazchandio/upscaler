import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from gfpgan import GFPGANer
from PIL import Image
import numpy as np
import io

def process_image(image_data, model_type):
    img = Image.open(io.BytesIO(image_data))
    img_np = np.array(img)

    if model_type == 'upscale':
        return upscale_image(img_np)
    elif model_type == 'enhance':
        return enhance_image(img_np)
    else:
        raise ValueError("Invalid model type")

def upscale_image(img_np):
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    upsampler = RealESRGANer(scale=4, model_path='/app/models/ESRGAN_x4.pth', model=model, tile=0, tile_pad=10, pre_pad=0, half=True)
    output, _ = upsampler.enhance(img_np, outscale=4)
    
    output_img = Image.fromarray(output)
    img_byte_arr = io.BytesIO()
    output_img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def enhance_image(img_np):
    restorer = GFPGANer(model_path='/app/models/GFPGANv1.3.pth', upscale=2, arch='clean', channel_multiplier=2, bg_upsampler=None)
    _, _, output = restorer.enhance(img_np, has_aligned=False, only_center_face=False, paste_back=True)
    
    output_img = Image.fromarray(output)
    img_byte_arr = io.BytesIO()
    output_img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()