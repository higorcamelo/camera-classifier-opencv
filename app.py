import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2 as cv
import model
import camera
import os
from PIL import Image, ImageTk


class App:
    def __init__(self, window=tk.Tk(), window_title="Camera Classifier"):
        self.window = window
        self.window.title(window_title)
        self.camera = camera.Camera()

        self.is_capturing = [False, False]
        self.capture_interval = 500  # ms
        self.counters = [1, 1]

        # Nomes das classes
        self.classname_one = simpledialog.askstring("Classe Nº1", "Insira o nome da primeira classe:", parent=self.window)
        self.classname_two = simpledialog.askstring("Classe Nº2", "Insira o nome da segunda classe:", parent=self.window)
        self.class_names = [self.classname_one, self.classname_two]

        # Modelo
        self.model = model.Model(self.class_names)

        self.init_gui()

        self.delay = 15
        self.update()
        self.window.mainloop()

    def init_gui(self):
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()

        # Linha da classe 1
        frame1 = tk.Frame(self.window)
        frame1.pack(pady=5)

        tk.Label(frame1, text=self.classname_one, font=("Arial", 14)).pack(side=tk.LEFT)
        tk.Button(frame1, text="Iniciar Coleta", command=lambda: self.start_capture(0)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame1, text="Parar", command=lambda: self.stop_capture(0)).pack(side=tk.LEFT, padx=5)
        self.counter_label1 = tk.Label(frame1, text="0 imagens")
        self.counter_label1.pack(side=tk.LEFT, padx=5)

        # Linha da classe 2
        frame2 = tk.Frame(self.window)
        frame2.pack(pady=5)

        tk.Label(frame2, text=self.classname_two, font=("Arial", 14)).pack(side=tk.LEFT)
        tk.Button(frame2, text="Iniciar Coleta", command=lambda: self.start_capture(1)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame2, text="Parar", command=lambda: self.stop_capture(1)).pack(side=tk.LEFT, padx=5)
        self.counter_label2 = tk.Label(frame2, text="0 imagens")
        self.counter_label2.pack(side=tk.LEFT, padx=5)

        # Controles gerais
        frame_controls = tk.Frame(self.window)
        frame_controls.pack(pady=10)

        tk.Button(frame_controls, text="Treinar Modelo", command=lambda: self.model.train_model(self.counters), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_controls, text="Predizer", command=self.predict, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_controls, text="Resetar", command=self.reset, width=10).pack(side=tk.LEFT, padx=5)

        self.class_label = tk.Label(self.window, text="Classificação Atual: ---", font=("Arial", 16))
        self.class_label.pack(pady=10)

    def start_capture(self, class_num):
        self.is_capturing[class_num] = True
        self.capture_loop(class_num)

    def capture_loop(self, class_num):
        if self.is_capturing[class_num]:
            self.save_for_class(class_num)
            self.window.after(self.capture_interval, lambda: self.capture_loop(class_num))

    def stop_capture(self, class_num):
        self.is_capturing[class_num] = False
        messagebox.showinfo("Parado", f"Coleta da classe {self.class_names[class_num]} interrompida.")

    def save_for_class(self, class_num):
        frame = self.camera.get_frame()[1]
        dir_path = f'dataset/{self.class_names[class_num]}'
        os.makedirs(dir_path, exist_ok=True)

        img_path = f'{dir_path}/frame{self.counters[class_num]}.jpg'
        gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
        resized = cv.resize(gray, (150, 150))

        cv.imwrite(img_path, resized)

        self.counters[class_num] += 1
        self.update_counter_labels()

    def update_counter_labels(self):
        self.counter_label1.config(text=f"{self.counters[0] - 1} imagens")
        self.counter_label2.config(text=f"{self.counters[1] - 1} imagens")

    def reset(self):
        self.is_capturing = [False, False]
        self.counters = [1, 1]
        self.model.reset_model()

        for class_name in self.class_names:
            dir_path = f"dataset/{class_name}"
            if os.path.exists(dir_path):
                for file in os.listdir(dir_path):
                    os.remove(os.path.join(dir_path, file))

        self.class_label.config(text="Classificação Atual: ---")
        self.update_counter_labels()
        messagebox.showinfo("Resetado", "Tudo foi resetado.")

    def update(self):
        ret, frame = self.camera.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)

    def predict(self):
        ret, frame = self.camera.get_frame()
        if ret:
            try:
                prediction = self.model.predict(frame)
                class_name = self.class_names[prediction - 1]
                self.class_label.config(text=f"Classificação Atual: {class_name}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao predizer: {e}\nTreine o modelo antes.")
