import cv2.cv2 as cv


# 读取图片
# img = cv.imread('face2.jpg')
# resize_img = cv.resize(img, dsize=(1280, 800))
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi',fourcc,50,(1920,1080))
# 检测函数
def face_detect_demo(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    face_detect = cv.CascadeClassifier('E:/opencv/opencv/sources/data/haarcascades_cuda/haarcascade_frontalface_alt.xml')
    body_detect = cv.CascadeClassifier('E:/opencv/opencv/sources/data/haarcascades_cuda/haarcascade_fullbody.xml')
    face = face_detect.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5 , minSize=(60, 60), maxSize=(500, 500), flags = 1)
    for x, y, w, h in face:
        cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2)
    body = body_detect.detectMultiScale(gray, scaleFactor=1.07, minNeighbors=2, minSize=(150, 150), maxSize=(1000, 1000), flags = 1)
    for x, y, w, h in body:
        cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)

    out.write(img)
    cv.imshow('img', img)


# 读取摄像头
# cap = cv.VideoCapture(0)
cap = cv.VideoCapture('测试3.mp4')
# face_detect_demo()
# cv.imshow('123', img)
# 等待
while True:
    flag, frame = cap.read()
    if not flag:
        break
    face_detect_demo(frame)
    if ord('q') == cv.waitKey(1):
        break


cap.release()
out.release()
cv.destroyAllWindows()
