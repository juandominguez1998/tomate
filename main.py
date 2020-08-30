from flask import Flask, render_template, Response
from camara import VideoCamara

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camara):
    while True:
        #get camara frame
        frame = camara.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed/<pelicula>')
def video_feed(pelicula):
    VideoCamara().set_pelicula(pelicula)
    return Response(gen(VideoCamara()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stand')
def stand():
    return render_template('stand.html')

@app.route('/capitan')
def capitan():
    return render_template('capitan.html')

@app.route('/batman')
def batman():
    return render_template('batman.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000', debug=True)