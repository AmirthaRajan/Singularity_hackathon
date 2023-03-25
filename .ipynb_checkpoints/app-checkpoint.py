import os
from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.densenet import preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
CORS(app)

model = load_model('customeModel.h5')

#Allow files with extension png, jpg and jpeg
ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXT
           
# Function to load and prepare the image in right shape
def read_image(filename):
    img = load_img(filename, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

@app.route('/', methods=['GET'])
def get_homepage():
    return render_template('index.html')   

@app.route('/predict',methods=['GET','POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename): #Checking file format
        filename = file.filename
        file_path = os.path.join('static/images', filename)
        file.save(file_path)
        img = read_image(file_path) #prepressing method
        class_prediction=model.predict(img)
        app.logger.info(class_prediction)
        classes_x=np.argmax(class_prediction,axis=1)
        app.logger.info(classes_x)
        class_names=['actinic keratosis', 'basal cell carcinoma', 'dermatofibroma', 'melanoma', 'nevus', 'pigmented benign keratosis', \
                     'seborrheic keratosis', 'squamous cell carcinoma', 'vascular lesion']
        return render_template('prediction.html', output = class_names[classes_x[0]], user_image = file_path)
    else:
        return "Unable to read the file. Please check file extension"

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p','--port',type=int,default=5000)
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port,debug=True)   
    
