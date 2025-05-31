import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2 as cv
import camera
import os
import PIL.Image, PIL.ImageTk

class App:
    def __init__(self, window= tk.Tk(), window_title="Camera Classifier"):
        self.window = window
        self.window.title(window_title)
        self.camera = camera.Camera()
        self.counters = [1, 1]
        
        #self.model =
        
        self.auto_predict = False 
        
        #self.init_gui()
        self.delay = 15
        #self.update()
        
        self.window.attributes("topmost", True)
        self.window.mainloop()
        
    def init_gui(self):

        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()

        self.btn_toggleauto = tk.Button(self.window, text="Auto Predição", width=50, command=self.auto_predict_toggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

        self.classname_one = simpledialog.askstring("Classe Nº1", "Insira o nome da primeira classe:", parent=self.window)
        self.classname_two = simpledialog.askstring("Classe Nº2", "Insira o nome da segunda:", parent=self.window)

        self.btn_class_one = tk.Button(self.window, text=self.classname_one, width=50, command=lambda: self.save_for_class(1))
        self.btn_class_one.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_two = tk.Button(self.window, text=self.classname_two, width=50, command=lambda: self.save_for_class(2))
        self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

        self.btn_train = tk.Button(self.window, text="Treinar modelo", width=50, command=lambda: self.model.train_model(self.counters))
        self.btn_train.pack(anchor=tk.CENTER, expand=True)

        self.btn_predict = tk.Button(self.window, text="Predizer", width=50, command=self.predict)
        self.btn_predict.pack(anchor=tk.CENTER, expand=True)

        self.btn_reset = tk.Button(self.window, text="Reiniciar", width=50, command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER, expand=True)

        self.class_label = tk.Label(self.window, text="CLASS")
        self.class_label.config(font=("Arial", 20))
        self.class_label.pack(anchor=tk.CENTER, expand=True)

        
        
    def auto_predict_toggle(self):
        self.auto_predict = not self.auto_predict
        if self.auto_predict:
            self.update()
        else:
            self.window.after_cancel(self.update)