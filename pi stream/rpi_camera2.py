# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

PAGE="""\
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
        
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
        <link rel="stylesheet" href="/styles.css">
    
</head>
<style>
    body {
        background-color: #001C30;
    }
    
    h1 {
        color: white;
    }
    
    .group_name {
        margin-left: 180px;
    }
    
    .header {
        display: flex;
    }
    
    .triangle-topleft {
        width: 0;
        height: 0;
        border-top: 200px solid #DAFFFB;
        border-right: 400px solid transparent;
    }
    
    .screen {
        position: relative;
        background-color: white;
        /* width : 75%;  */
        height: 400px;
        display: inline-block;
        border-radius: 7px;
        box-shadow: 0px 7px 7px 7px #878788;
        top: -120px;
        margin: auto;
        grid-column-start: 1;
        grid-column-end: 4;
    }
    
    .middle_content {
        display: grid;
        grid-template-columns: repeat(3, 400px);
        grid-template-rows: repeat(3, 125px);
    }
    
    .cancel {
        grid-row-start: 3;
        margin-left: 150px;
    }
    
    .drop {
        grid-row-start: 3;
        grid-column-start: 2;
        margin-left: 100px;
    }
    
    .revert {
        grid-row-start: 3;
        grid-column-start: 3;
        margin-left: 60px;
    }
    
    .buttons {
        height: 40px;
        width: 200px;
        margin-top: 80px;
        background-color: #DAFFFB;
        border-radius: 20px;
    }
    
    .popup {
        display: none;
        margin-right: 200%;
        /* left: 0; */
        height: 100%;
        background-color: rgba(0, 0, 0, 0.7);
    }
    
    .popup-content {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        padding: 20px;
        border: 1px solid #ccc;
        box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.2);
    }
    
    .close-button {
        position: absolute;
        top: 10px;
        right: 10px;
        cursor: pointer;
    }
</style>




<body>
    <div class="header">
        <div class="triangle-topleft"> </div>
        <h1 class="group_name"> XCEED </h1>
    </div>

    <div class="middle_content">
        <div class="screen">
            <img src="http://192.168.174.15:8000/stream.mjpg" controls autoplay height="400" style="border-radius:7px;">
            </img>
        </div>
        <!-- Popup container -->

        <button type="button" class="buttons cancel" onclick="openPopup()">Cancel Drop</button>
        <button type=" button " class="buttons drop ">Return To Station</button>
        <button type="button " class="buttons revert ">Wait</button>

    </div>

    <div id="popup" class="popup">
        <!-- Popup content -->
        <div class="popup-content">
            <span class="close-button" onclick="closePopup()">&times;</span>
            <p>This is a popup!</p>
        </div>
    </div>
    <script>
        function openPopup() {
            document.getElementById('popup').style.display = 'block';
        }
        
        function closePopup() {
            document.getElementById('popup').style.display = 'none';
        }
    </script>

</body>


</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='1020x720', framerate=30) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
