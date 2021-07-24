from flask import Flask, request, json, Response
from PIL import Image
from io import BytesIO

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return ''


@app.route('/image', methods=['POST'])
def process():
    file = request.files.get('file')

    if file is None:
        return json_response('No file found', 400)

    image = Image.open(file)

    new_width = request.args.get('width')
    new_height = request.args.get('height')
    quality = request.args.get('quality')

    if quality is None:
        quality = 80

    if new_width is not None and new_height is not None:
        new_width = int(new_width)
        new_height = int(new_height)

        if new_width > 0 and new_height > 0:
            image = image.resize((new_width, new_height))

    with BytesIO() as output:
        image.save(output, format="WEBP", quality=quality, method=4)

        image_contents = output.getvalue()

        return Response(image_contents, 200, mimetype='image/webp')


def json_response(message: str or None, status_code: int = 200, data=None):
    if data is None:
        data = {}

    data['message'] = message

    return Response(json.dumps(data), status=status_code, mimetype='application/json')


if __name__ == '__main__':
    app.run()
