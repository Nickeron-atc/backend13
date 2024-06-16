import webuiapi
from PIL import Image, PngImagePlugin

def init_stable_diffusion() -> webuiapi.WebUIApi:
    api = webuiapi.WebUIApi(host="194.113.34.212", port="7860", sampler="DPM++ 2M", scheduler="karras")
    api.util_set_model("revAnimated_v2Rebirth.safetensors")
    return api

def request_image(api: webuiapi.WebUIApi, request: str, output_path, image_count = 1):
    const_prompt = "masterpiece,best quality,cute,3dzujian,3d rendering,Cartoon material,clean background,white background,blank background,<lora:3dzujianV3:1>,"
    result: webuiapi.WebUIApiResult = api.txt2img(
        prompt=const_prompt + request,
        negative_prompt="bad quality,low quality,jpeg artifact,cropped,flank,reverse side,no reflexes,human",
        cfg_scale=7,
        steps=20,
        width=256,
        height=256,
        
        batch_size=image_count,
    )

    img: PngImagePlugin.PngImageFile = result.image
    print("PATH" + output_path)
    img.save(output_path)
