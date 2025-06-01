import cv2 as cv

class Camera:
    def __init__(self):
        self.camera = cv.VideoCapture(0) # Abre a câmera padrão
        if not self.camera.isOpened():
            raise Exception("Não foi possível abrir a câmera")
        
        self.width = int(self.camera.get(cv.CAP_PROP_FRAME_WIDTH))  # Largura do frame
        self.height = int(self.camera.get(cv.CAP_PROP_FRAME_HEIGHT)) # Altura do frame
        
    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()
            
    def get_frame(self):
        if self.camera.isOpened():
            ret, frame = self.camera.read() # ret indica se a captura foi bem-sucedida, frame contém o frame capturado
            if ret:
                return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB)) # Converte o frame de BGR para RGB
            return (ret, None)
        else:
            raise Exception("Câmera não está aberta")
        
