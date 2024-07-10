from flask import Blueprint, Flask, request, jsonify, send_file , make_response, render_template
from flask_cors import CORS
import base64
import os

#Model imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
from tensorflow import keras

from imblearn.over_sampling import SMOTENC

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier


app = Blueprint('cancer', __name__)

#Global variables
global min_age
global max_age 
global max_bmi
global min_bmi
global final_df_columns
global model

#global seed
seed=11

#global DATA_PATH
DATA_PATH = "/home/muhuthu/Documents/medic_kit_hackathon.group20/workspace/dataset/breast_mammogram_dataset.csv"

#global max_age
max_age=0

#global min_age
min_age=0 

#global max_bmi
max_bmi=0

#global min_bmi
min_bmi=0

#global final_df_columns
final_df_columns = ['age_c', 
                    'bmi_c', 
                    'density_c_1.0', 
                    'density_c_2.0', 
                    'density_c_3.0',
                    'density_c_4.0', 
                    'famhx_c_0.0', 
                    'famhx_c_1.0', 
                    'famhx_c_9.0',
                    'hrt_c_0.0', 
                    'hrt_c_1.0', 
                    'hrt_c_9.0',
                    'prvmam_c_0.0', 
                    'prvmam_c_1.0',
                    'prvmam_c_9.0',
                    'biophx_c_0.0', 
                    'biophx_c_1.0', 
                    'biophx_c_9.0',
                    'mammtype_1.0',
                    'mammtype_2.0'
                    ]

model = None

@app.route('/biopsy', methods=['POST'])
def predict_biopsy():
    try:
        # Save the uploaded file
        f = request.files['file']
        save_path = 'to_predict.png'
        f.save(save_path)

        imgs = []
        shape = 256

        # Load sample images (adjust the path as necessary)
        for i in range(15):
            img_path = f'dataset/Dataset_BUSI_with_GT/f{i+1}.png'
            if os.path.exists(img_path):
                img = plt.imread(img_path)
                img = cv2.resize(img, (shape, shape))
                imgs.append(img)
            else:
                print(f"Warning: Image {img_path} not found.")

        # Load the image to predict
        img = plt.imread(save_path)
        h, w, _ = img.shape
        img = cv2.resize(img, (shape, shape))
        imgs.append(img)

        # Load the model
        model_path = 'model/keras_biopsy.h5'
        if os.path.exists(model_path):
            model = keras.models.load_model(model_path)
        else:
            return jsonify({"error": "Model file not found."}), 404

        # Predict
        preds = model.predict(np.array(imgs))
        output = cv2.resize(preds[15][:, :, 0], (w, h))
        plt.imsave('predicted.png', output)

        # Encode and send the image
        with open("predicted.png", "rb") as f:
            image_binary = f.read()

        response = make_response(base64.b64encode(image_binary))
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment; filename=mask.png')
        return response

    except Exception as e:
        # Log the exception
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/mammogram', methods=['POST'])
def predict_mammogram():
    global min_age, max_age, min_bmi, max_bmi, final_df_columns, model

    data = request.get_json()

    # Update min and max age
    if data['age'] > max_age:
        max_age = data['age']
    elif data['age'] < min_age:
        min_age = data['age']

    # Update min and max BMI
    if data['bmi'] > max_bmi:
        max_bmi = data['bmi']
    elif data['bmi'] < min_bmi:
        min_bmi = data['bmi']

    # Normalize age and BMI
    data['age'] = data['age'] / 100.0
    data['bmi'] = data['bmi'] / 100.0

    # Create a NumPy array for the input data
    ar = np.array([[data['age'], data['bmi'],
                    1 if data['density'] == 1 else 0,
                    1 if data['density'] == 2 else 0,
                    1 if data['density'] == 3 else 0,
                    1 if data['density'] == 4 else 0,
                    1 if data['famhx'] == 0 else 0,
                    1 if data['famhx'] == 1 else 0,
                    1 if data['famhx'] == 9 else 0,
                    1 if data['hrt'] == 0 else 0,
                    1 if data['hrt'] == 1 else 0,
                    1 if data['hrt'] == 9 else 0,
                    1 if data['prvmam'] == 0 else 0,
                    1 if data['prvmam'] == 1 else 0,
                    1 if data['prvmam'] == 9 else 0,
                    1 if data['biophx'] == 0 else 0,
                    1 if data['biophx'] == 1 else 0,
                    1 if data['biophx'] == 9 else 0,
                    1 if data['mammtype'] == 1 else 0,
                    1 if data['mammtype'] == 2 else 0
                    ]])

    # Ensure consistency in feature names
    # Mapping to remove `.0` from feature names
    feature_names = [col.replace('.0', '') for col in final_df_columns]
    
    df2 = pd.DataFrame(ar, columns=feature_names)

    # Ensure columns match the model's feature names
    df2 = df2.reindex(columns=model.feature_names_in_, fill_value=0)

    try:
        val = model.predict_proba(df2)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "assess_1": val[0][0],
        "assess_2": val[0][1],
        "assess_3": val[0][2],
        "assess_4": val[0][3],
        "assess_5": val[0][4],
        "assess_6": val[0][5],
    })
    

# A welcome message to test our server
@app.route('/cancer-detection')
def index():
    return render_template('main/cancer.html')

