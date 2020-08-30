import cv2
import os
from firebase import firebase 

firebase = firebase.FirebaseApplication("https://python-firebase-ebenti.firebaseio.com/",None)

metodo = 'LBPH'
emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()
emotion_recognizer.read('reconocimiento_reacciones/modelo'+metodo+'.xml')
emociones = ['enojo','felicidad','neutral','sorpresa','tristeza']
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
resultados = []

class VideoCamara(object):
    
    pelicula = ''

    def __init__(self):
       self.video = cv2.VideoCapture(1)

    def set_pelicula(self, valor):
        self.pelicula = valor
    
    def __del__(self):
        self.video.release()
        
        sentimientos = [["enojo",0.0,0],["felicidad",0.0,0],["neutral",0.0,0],["sorpresa",0.0,0],["tristeza",0.0,0]]
        for dato in resultados:
            for n in range(0, 4):
                if(dato[0] == n):
                    sentimientos[n][2] += 1
                    sentimientos[n][1] += dato[1]
        
        for n in range(0, 4):
            if(sentimientos[n][2] != 0):
                sentimientos[n][1] = sentimientos[n][1]/sentimientos[n][2]

        datos = {
            "usuario":"Daniel Pérez Flores",
            "reacciones": sentimientos
        }

        url = '/reacciones/'+self.pelicula
        if(self.pelicula != ''):
            resultado = firebase.post(url,datos)

    def get_frame(self):
        ret,frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()
        faces = faceClassif.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
            result = emotion_recognizer.predict(rostro)
            cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
            if metodo == 'LBPH':
                if result[1] < 60:
                    cv2.putText(frame,'{}'.format(emociones[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                    resultados.append(result)
                else:
                    cv2.putText(frame,'No identificado',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
