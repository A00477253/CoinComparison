import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image

class ImageApp:
    def __init__(self):
        self.model = self.load_model()

    @staticmethod
    @st.cache(allow_output_mutation=True)
    def load_model():
        model_path = "digit_classifier_model.h5"
        model = tf.keras.models.load_model(model_path)
        return model

    @staticmethod
    def preprocess_image(image):
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        resized_image = image.resize((28, 28))
        grayscale_image = resized_image.convert('L')
        image_array = np.array(grayscale_image) / 255.0
        image_array = image_array.reshape((1, 28, 28, 1))
        return image_array

    def classify_digit(self, image_array):
        prediction = self.model.predict(image_array)
        predicted_digit = np.argmax(prediction)
        return predicted_digit

    def main(self):
        st.title('Digit Classifier')
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            processed_image = self.preprocess_image(image)
            predicted_digit = self.classify_digit(processed_image)
            st.write(f"Predicted Digit: {predicted_digit}")

def main():
    image_app = ImageApp()
    image_app.main()

if __name__ == "__main__":
    main()
