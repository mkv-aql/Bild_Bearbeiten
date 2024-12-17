import cv2

img_name = ''
count = 0
# Open camera
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #if space is pressed
    if cv2.waitKey(1) & 0xFF == ord(' '):
        img_name = "opencv_frame_{}.png".format(count)
        cv2.imwrite(img_name, frame)
        count += 1
        continue

cap.release()
cv2.destroyAllWindows()

#open image
img = cv2.imread(img_name, cv2.IMREAD_UNCHANGED)
#show image
cv2.imshow('Image', img)
#wait for key press
cv2.waitKey(0)