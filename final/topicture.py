import cv2

'''video1 = cv2.VideoCapture('database/train1.mp4')
video2 = cv2.VideoCapture('database/train2.mp4')'''

video1 = cv2.VideoCapture('final_video.mp4')

idx = 0

while video1.isOpened():
    ret, frame = video1.read()
    if not ret:
        break

    #print("database/test/test-" + str(idx).zfill(4) + ".jpg")
    cv2.imwrite("train/train-" + str(idx).zfill(4) + ".jpg", frame)

    idx += 1

video1.release()