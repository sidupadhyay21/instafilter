import cv2
from mtcnn import MTCNN
import pgzrun
from pygame import surfarray
from numpy import transpose

cam = cv2.VideoCapture(0)
ret_val, img = cam.read()
print(ret_val)

detector = MTCNN()
bounding_boxes = detector.detect_faces(img)
star = cv2.imread("star2.jpg")
mustache = cv2.imread("mustache2.jpg")

left_eye_x, left_eye_y = bounding_boxes[0]['keypoints']['left_eye']
right_eye_x, right_eye_y = bounding_boxes[0]['keypoints']['right_eye']
nose_x, nose_y = bounding_boxes[0]['keypoints']['nose']

print(bounding_boxes[0]['keypoints'])

def img_replace(overlay, o_x, o_y):
        for y in range(len(overlay)):
                
                for x in range(len(overlay[y])):
                        img_x = o_x - int((len(overlay[y]))/2) + x
                        img_y = o_y - int((len(overlay))/2) + y
                        
                        if img_y >= len(img) or img_x>= len(img[img_y]):
                                continue
                                
                        img[img_y][img_x][0] = overlay[y][x][0]

                        img[img_y][img_x][1] = overlay[y][x][1]

                        img[img_y][img_x][2] = overlay[y][x][2]

def update():
        global img, left_eye_x, left_eye_y, right_eye_x, right_eye_y, nose_x, nose_y
        ret_val, img = cam.read()
        if ret_val == True:
                
                bounding_boxes = detector.detect_faces(img)

                if len(bounding_boxes) > 0:
                        left_eye_x, left_eye_y = bounding_boxes[0]['keypoints']['left_eye']
                        right_eye_x, right_eye_y = bounding_boxes[0]['keypoints']['right_eye']
                        nose_x, nose_y = bounding_boxes[0]['keypoints']['nose']

                img_replace(star, left_eye_x, left_eye_y)
                img_replace(star, right_eye_x, right_eye_y)
                img_replace(mustache, nose_x, nose_y + 20)

def draw():
        frame = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        frame = transpose(frame, (1,0,2))
        surf = surfarray.make_surface(frame)
        screen.blit(surf, (0,0))

pgzrun.go()
