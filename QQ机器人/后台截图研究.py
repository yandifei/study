import dxcam
camera = dxcam.create()  # returns a DXCamera instance on primary monitor
frame = camera.grab()
from PIL import Image
Image.fromarray(frame).show()