import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from PIL import Image
import numpy as np
import io

def process_image(image_data):
    img = Image.open(io.BytesIO(image_data))
    img_np = np.array(img)
    return upscale_image(img_np)

def upscale_image(img_np):
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    upsampler = RealESRGANer(scale=4, model_path='/app/models/ESRGAN_x4.pth', model=model, tile=0, tile_pad=10, pre_pad=0, half=True)
    output, _ = upsampler.enhance(img_np, outscale=4)
    
    output_img = Image.fromarray(output)
    img_byte_arr = io.BytesIO()
    output_img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()