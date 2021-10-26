### Instance object segmentation ###
"""
    Description :
                    Apply object detection and instance segmentation using Mask R-CNN model
"""

# Importing modules
import cv2
import numpy as np

# 1 | Load the image
img = cv2.imread("Images/img2.jpg")
img = cv2.resize(img, (650,550))
height, width, _ = img.shape
img_black = np.zeros((height, width, 3), np.uint8)
img_black[:] = (0, 0, 0)

# 2 | Load classes and generate rundom colors
classes = open("classes.txt").read().strip().split("\n")
colors = np.random.randint(125, 255, (80, 3))

# 3 | Load the model
net = cv2.dnn.readNetFromTensorflow("Model/frozen_inference_graph.pb", "Model/mask_rcnn_inception_v2.pbtxt")
blob = cv2.dnn.blobFromImage(img, swapRB=True)
net.setInput(blob)
boxes, masks = net.forward(["detection_out_final", "detection_masks"])
detection_count = boxes.shape[2]

# 4 | Loop overt detections
for i in range(detection_count):
    
     # Get box, class id and score
     box = boxes[0, 0, i]
     class_id = box[1]
     score = box[2]
     if score < 0.5:
         continue
     
     # Get coordinates and region of interest
     x = int(box[3] * width)
     y = int(box[4] * height)
     x2 = int(box[5] * width)
     y2 = int(box[6] * height)
     roi = img_black[y: y2, x: x2]
     roi_height, roi_width, _ = roi.shape
     
     # Get mask
     mask = masks[i, int(class_id)]
     mask = cv2.resize(mask, (roi_width, roi_height))
     _, mask = cv2.threshold(mask, 0.5, 255, cv2.THRESH_BINARY)
     
     # Draw bounding box
     color = colors[int(class_id)]
     cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 3)
     cv2.putText(img, classes[int(class_id)], (x+20, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
     contours, _ = cv2.findContours(np.array(mask, np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
     for cnt in contours:
         cv2.fillPoly(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))
         
# Show final images
cv2.imshow("Objects detection", img)
cv2.imshow("Segmentation masks", img_black)
cv2.imshow("Objects detection and segmentation", ((0.6*img_black)+(0.4*img)).astype("uint8"))
cv2.waitKey(0)

