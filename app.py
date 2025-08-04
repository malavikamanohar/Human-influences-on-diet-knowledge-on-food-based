import os
import pandas as pd
import numpy as np
import tensorflow as tf
from flask import Flask, request, render_template, send_from_directory
from tensorflow.keras.preprocessing import image
from keras.models import load_model

app = Flask(__name__)

Food = ['apple_pie', 'cannoli', 'cheesecake', 'cheese_plate', 'chicken_wings', 'chocolate_cake', 'deviled_eggs', 'donuts', 'french_fries', 'frozen_yogurt', 'ice_cream', 'macarons']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/upload/<filename>")
def send_image(filename):
    return send_from_directory("images",filename)

@app.route("/upload",methods=["POST","GET"])
def upload():
    if request.method=='POST':
        print("hdgkj")
        m = int(request.form["alg"])


        myfile = request.files['file']
        fn = myfile.filename
        mypath = os.path.join("images/", fn)
        myfile.save(mypath)

        print("{} is the file name", fn)
        print("Accept incoming file:", fn)
        print("Save it to:", mypath)

        if m == 1:
            print("bv1")
            new_model = load_model(r'models/CNN.h5')
            test_image = image.load_img(mypath, target_size=(128, 128))
            test_image = image.img_to_array(test_image)


        elif m == 2:
            print("bv2")
            new_model = load_model(r'models/SqueezeNet.h5')
            test_image = image.load_img(mypath, target_size=(128, 128))
            test_image = image.img_to_array(test_image)

        elif m == 3:
            print("bv3")
            new_model = load_model(r'models/ResNet50.h5')
            test_image = image.load_img(mypath, target_size=(128, 128))
            test_image = image.img_to_array(test_image)

        else:
            print("bv4")
            new_model = load_model(r'models/VGG16.h5')
            test_image = image.load_img(mypath, target_size=(64, 64))
            test_image = image.img_to_array(test_image)


        test_image = np.expand_dims(test_image, axis=0)
        result = new_model.predict(test_image)
        preds = Food[np.argmax(result)]

        if preds == "apple_pie":
            msg = "345 calories,Fat 12.5g, Carbs 37.1g,Protein 2.4g," \
                  "Limit these to only special occasions and opt for whole foods and fresh fruit as your usual dessert option."

        elif preds == "cannoli":
            msg = "254 calories,Fat 11.04g, Carbs 28.84g,Protein 8.7g," \
                  "Cannoli is an indulgent sweet treat, but if you tweak the recipe, it's easy to make it diabetic-friendly."

        elif preds == "cheesecake":
            msg = "321  Calories/100g,Fat 22.5g, Carbs 25.5g,Protein 5.5g," \
                  "Cheesecake may sound like a diabetes-friendly option, but the traditional recipe can pack as much as 31.9 g of carbohydrates per slice."

        elif preds == "cheese_plate":
            msg = "380  Calories/100g,Fat 27.8g, Carbs 5.38g,Protein 26.93g," \
                  "Cheese is safe in moderation for people with diabetes. People with diabetes can safely eat cheese as part of a balanced, healthful diet. As with other foods, moderation is key, and so a diet that includes too much cheese would be harmful to people with or without diabetes."

        elif preds == "chicken_wings":
            msg = "288 calories/100g,Fat 19.3g, Carbs 0g,Protein 26.64g," \
                  "Chicken can be a great option for people with diabetes. All cuts of chicken are high in protein and many are low in fat. When prepared in a healthy way, chicken can be a great ingredient in a healthy diabetic eating plan."

        elif preds == "chocolate_cake":
            msg = "367 calories/100g,Fat 16.4g, Carbs 54.6g,Protein 4.1g," \
                  "Just because you have diabetes doesn't mean you can't enjoy chocolate cake as part of ahealthy, balanced diet.."
        elif preds == "deviled_eggs":
            msg = "201 Calories/100g,Fat 16.23g, Carbs 1.35g,Protein 11.57g," \
                  "Eggs are a versatile food and a great source of protein. The American Diabetes Association considers eggs an excellent choice for people with diabetes."
        elif preds == "donuts":
            msg = "452  Calories/100g, Fat 22.85g,Carbs 47g,Protein 5.7g," \
                  "Small amounts of sweets can be included in a healthy diet, even if you have diabetes"

        elif preds == "french_fires":
            msg = "312 Calories/100g, Fat 14.06g,Carbs 35.66g,Protein 3.48g," \
                  "French fries are a food you may want to steer clear of, especially if you have diabetes. Potatoes themselves are relatively high in carbs."
        elif preds == "frozen_yogurt":
            msg = "159 Calories/100g,Fat 1.47g,Carbs 19.62g,Protein 4.7g," \
                  "Frozen yogurt is a good alternative to ice cream. Diabetes-friendly desserts are available in most stores and are as easy to prepare at home as any other sweet treat.."
        elif preds == "ice_cream":
            msg = "207 Calories/100g,Fat 10.72g,Carbs 24.4g,Protein 3.52g," \
                  "Despite what many naysayers will tell you, people with diabetes CAN (and do) eat ice cream. Sure, ice cream can’t compete with, say, a salad when it comes to nutrition."
        else:
            msg = "404  Calories/100g,Fat 22.30g,Carbs 49.70,Protein 8.80g," \
                  "Just be sure to keep an eye on your portions. Go for whole wheat pasta, which will increase your fiber, vitamins, and minerals, and reduce any blood sugar spikes when compared to white pasta."


        arr = msg.split(',')
        print(arr)

        return render_template("template.html", text=preds, msg = arr, image_name=fn)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)