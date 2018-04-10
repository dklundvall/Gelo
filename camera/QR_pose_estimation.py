from videostream import VideoStream
from PIL import Image
import sys
import numpy as np 
import cv2
import time
import zbar

if int(sys.argv[1]) == 1:
    isPiCamera = True
else:
    isPiCamera = False

if int(sys.argv[2]) == 640:
    resolution = (640,480)
elif int(sys.argv[2]) == 320:
    resolution = (320,240)
else:
    print "Not valid resolution"
    quit()

def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img


objp = np.float32([[0,0,0],[0,1,0],[1,1,0],[1,0,0]])
axis = np.float32([[1,0,0],[0,1,0],[0,0,1]])#.reshape(-1,3)
corners = np.zeros((4,1), np.float32)
#criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

vs = VideoStream(isPiCamera = isPiCamera, resolution = resolution).start()
time.sleep(2.0)

scanner = zbar.ImageScanner()
scanner.parse_config('enable')


while True:
	
	img = vs.readUndistorted()
	
	# raw detection code
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	pil = Image.fromarray(gray)
	width, height = pil.size
	raw = pil.tobytes()

    # create a reader
	image = zbar.Image(width, height, 'Y800', raw)
	scanner.scan(image)

	for symbol in image:
		print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
		corners = np.asarray(symbol.location, dtype = np.float32)
		#corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

		ret, rvecs, tvecs = cv2.solvePnP(objp, corners, vs.mtx, vs.dist)
		
		rmtx, jac = cv2.Rodrigues(rvecs)
		print rmtx
		print tvecs
		imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, vs.mtx, vs.dist)
		img = draw(img, corners, imgpts)
	#except:
	#	print "no code"
		
	cv2.imshow('Stream', img)
	keypress = cv2.waitKey(1) & 0xFF
	if keypress == ord('q'):
		break

vs.stop()
cv2.destroyAllWindows()