from sklearn.svm import LinearSVC
import numpy as np
import cv2 as cv
import os
from PIL import Image


class Model:
    def __init__(self, class_names):
        self.model = LinearSVC(max_iter=10000)  # Adicionado max_iter para evitar warning
        self.class_names = class_names

    def preprocess(self, frame):
        # Recebe imagem RGB ou grayscale, converte, redimensiona e flatten
        if len(frame.shape) == 3:
            gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
        else:
            gray = frame

        img = Image.fromarray(gray)
        img = img.resize((150, 150), Image.Resampling.LANCZOS)
        img_array = np.array(img).reshape(-1)

        return img_array

    def train_model(self, counters):
        img_list = []
        class_list = []

        for idx, class_name in enumerate(self.class_names):
            dir_path = os.path.join('dataset', class_name)
            for i in range(1, counters[idx]):
                img_path = os.path.join(dir_path, f'frame{i}.jpg')
                img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)

                if img is None:
                    continue

                img = cv.resize(img, (150, 150))
                img = img.reshape(-1)

                img_list.append(img)
                class_list.append(idx + 1)

        img_list = np.array(img_list)
        class_list = np.array(class_list)

        if img_list.shape[0] == 0:
            raise ValueError("Nenhuma imagem de treinamento encontrada.")

        self.model.fit(img_list, class_list)
        print("Modelo treinado com sucesso!")

    def predict(self, frame):
        img_array = self.preprocess(frame)
        prediction = self.model.predict([img_array])
        return prediction[0]

    def reset_model(self):
        self.model = LinearSVC(max_iter=10000)
