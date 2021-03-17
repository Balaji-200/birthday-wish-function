import logging
import azure.functions as func
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import mimetypes
import base64
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    op_image = BytesIO()
    image = Image.open(r'birthday.jpg')
    width, height = image.size
    print(width, height)
    font_size = 62
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r"Great_Vibes/GreatVibes-Regular.ttf", size=font_size)
    w, h = draw.textsize(name, font=font)
    draw.text((int((width-w)/2), int(height)/4.3), name, fill=(105,22,30), font=font)
    image.save(op_image, 'JPEG')
    op_image.seek(0)
    headers  = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "Get, Post, Options"
    }
    if name:
        # return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
        return func.HttpResponse(base64.b64encode(op_image.getvalue()), headers=headers)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
