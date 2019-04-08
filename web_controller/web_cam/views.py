from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from django.http import HttpResponse
import numpy
import cv2
import threading
from django.views.decorators import gzip
import pprint

class VideoCamera():
    def __init__(self,cam_num):
        self.video = cv2.VideoCapture(cam_num)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        image = self.frame
        image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

cam = VideoCamera()

#def gen(camera):
def gen():
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
##
## Create your views here.
@gzip.gzip_page
def Cam_data(request):
    try:
        print("cam_data")
        return StreamingHttpResponse(gen(0), 
            content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

@gzip.gzip_page
def Cam_data2(request):
    try:
        print("cam_data2")
        return StreamingHttpResponse(gen(1), 
            content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

@csrf_exempt
def CamHome(request):
    print("request data")
    print(request.POST)
    #return HttpResponse("ok", content_type="text/plain")
    return render(request, 'web_cam/index.html')
