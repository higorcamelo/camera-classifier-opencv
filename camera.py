import cv2 as cv

class Camera:
    def __init__(self):
        self.camera = cv.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception("Não foi possível abrir a câmera")

        self.width = int(self.camera.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.camera.get(cv.CAP_PROP_FRAME_HEIGHT))

    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()

    def get_frame(self):
        if self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                # Converte BGR → RGB antes de retornar
                return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            return (ret, None)
        else:
            raise Exception("Câmera não está aberta")
