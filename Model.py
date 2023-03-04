from __future__ import division, print_function
import os
import numpy as np
from keras.models import load_model
from keras.utils import load_img, img_to_array


from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)

model = load_model('Kathakali.h5')

def model_predict(img_path, model):
    print(img_path)
    img = load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = img_to_array(img)

    x=x/255
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds == 0:
            preds = 'kartharee mugham'
    elif preds == 1:
            preds = 'katakam'
    elif preds ==2:
            preds = 'mudraakhyam'
    elif preds ==3:
             preds = 'mushti'
    elif preds ==3:
             preds = 'pathaka'
      
    return preds


@app.route('/', methods=['GET'])
def index():
    return render_template('/home/lionex/bin/Python/Project-Kathakali/index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        preds = model_predict(file_path, model)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(port=5001,debug=True)