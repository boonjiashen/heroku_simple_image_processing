import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
import tempfile

import numpy as np
import werkzeug
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import matplotlib.pyplot
import Mosaicker
import uuid

# Initialize the Flask application
app = Flask(__name__)
max_dim = 500  # max dimension of both height and width of output image
               # overly large input images will be shrunk
mosaicker = Mosaicker.AppMosaicker(
        'static/data_batch_1',
        max_dim=max_dim,
        )

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


def generate_uuid() -> str:
    return str(uuid.uuid4())


def file_to_numpy_image(file: werkzeug.datastructures.FileStorage):
    with tempfile.NamedTemporaryFile() as fp:
        file.save(fp.name)
        im = matplotlib.pyplot.imread(fp.name)

        return im


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']

    # Check if the file is one of the allowed types/extensions
    if not file or not allowed_file(file.filename):
        return

    # Make the filename safe, remove unsupported chars
    filename = secure_filename(file.filename)

    # Convert to numpy image
    im = file_to_numpy_image(file)

    # Save output image in upload folder
    im = mosaicker.compute_mosaick(im)
    _, ext = os.path.splitext(filename)
    output_filename = generate_uuid() + ext
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    matplotlib.pyplot.imsave(output_path, im)

    # Redirect the user to the uploaded_file route, which
    # will basicaly show on the browser the uploaded file
    return redirect(url_for('uploaded_file',
                            filename=output_filename))


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
