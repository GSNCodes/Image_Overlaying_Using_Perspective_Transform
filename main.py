import cv2
import numpy as np
import argparse


def click_event(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(base_image_copy, (x,y), 4, (0,0,255), -1)
        points.append([x, y])
        if len(points) <= 4:
            cv2.imshow('image', base_image_copy)



# Let's sort the points in the following order
# Top-Left, Top-Right, Bottom-Right, Bottom-Left
def sort_pts(points):
    sorted_pts = np.zeros((4, 2), dtype="float32")
    s = np.sum(points, axis=1)
    sorted_pts[0] = points[np.argmin(s)]
    sorted_pts[2] = points[np.argmax(s)]

    diff = np.diff(points, axis=1)
    sorted_pts[1] = points[np.argmin(diff)]
    sorted_pts[3] = points[np.argmax(diff)]

    return sorted_pts



if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_img',    type=str, help='Path to the base image', required=True)
    parser.add_argument('--subject_img', type=str, help='Path to the subject image', required=True)
    parser.add_argument('--debug', type=bool, help='Enable debug', default=False)
    args = vars(parser.parse_args())


    points = []

    base_image = cv2.imread(args['base_img'])
    base_image_copy = base_image.copy()
    subject_image = cv2.imread(args['subject_img'])

    cv2.imshow('image', base_image_copy)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    sorted_pts = sort_pts(points)
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
    filled_mask = mask.copy()
    cv2.fillConvexPoly(filled_mask, roi_corners, (255, 255, 255))

    # Invert the mask color
    inverted_mask = cv2.bitwise_not(filled_mask)

    # Bitwise AND the mask with the base image
    masked_image = cv2.bitwise_and(base_image, inverted_mask)


    if args['debug']:
        cv2.imshow('Warped Image', warped_img)
        cv2.imshow('Mask Created', mask)
        cv2.imshow('Mask after filling', filled_mask)
        cv2.imshow('Inverting Mask colors', inverted_mask)
        cv2.imshow('Masked Image', masked_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Using Bitwise OR to merge the two images
    output = cv2.bitwise_or(warped_img, masked_image)
    cv2.imshow('Fused Image', output)
    cv2.imwrite('Final_Output.png', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

