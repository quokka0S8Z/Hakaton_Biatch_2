import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

webcam = cv2.VideoCapture(0)

smile_counter = 0
SMILE_THRESHOLD = 10

def detect_smile():
    global smile_counter
    success, frame = webcam.read()
    if not success:
        return False
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        face_gray = gray[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(face_gray, 1.7, 20)
        if len(smiles) > 0:
            smile_counter += 1
            if smile_counter >= SMILE_THRESHOLD:
                return True
        else:
            smile_counter = 0
    return False

def release_camera():
    webcam.release()
    cv2.destroyAllWindows()
