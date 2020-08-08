import cv2
import numpy as np

def click_event(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(base_image_copy, (x,y), 4, (0,0,255), -1)
        points.append([x, y])
        if len(points) <= 4:
            cv2.imshow('image', base_image_copy)

points = []

base_image = cv2.imread('base_img.jpg')
base_image_copy = base_image.copy()
subject_image = cv2.imread('subject.jpg')

cv2.imshow('image', base_image_copy)
cv2.setMouseCallback('image', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Let's sort the points in the following order
# Top-Left, Top-Right, Bottom-Right, Bottom-Left

sorted_pts = np.zeros((4, 2), dtype="float32")
s = np.sum(points, axis=1)
sorted_pts[0] = points[np.argmin(s)]
sorted_pts[2] = points[np.argmax(s)]

diff = np.diff(points, axis=1)
sorted_pts[1] = points[np.argmin(diff)]
sorted_pts[3] = points[np.argmax(diff)]


h_base, w_base, c_base = base_image.shape
h_subject, w_subject = subject_image.shape[:2]

pts1 = np.float32([[0, 0], [w_subject, 0], [w_subject, h_subject], [0, h_subject]])
pts2 = np.float32(sorted_pts)

# Get the transformation matrix and use it to get the warped image of the subject
transformation_matrix = cv2.getPerspectiveTransform(pts1, pts2)
warped_img = cv2.warpPerspective(subject_image, transformation_matrix, (w_base, h_base))

# Create a mask
mask = np.zeros(base_image.shape, dtype=np.uint8)
roi_corners = np.int32(sorted_pts)
# Fill in the region selected with white color
cv2.fillConvexPoly(mask, roi_corners, (255,255,255))

# Invert the mask color
mask = cv2.bitwise_not(mask)

# Bitwise AND the mask with the base image
masked_image = cv2.bitwise_and(base_image, mask)


#Using Bitwise OR to merge the two images
output = cv2.bitwise_or(warped_img, masked_image)
cv2.imshow('Fused Image', output)
cv2.imwrite('Final_Output.png', output)
cv2.waitKey(0)
cv2.destroyAllWindows()



