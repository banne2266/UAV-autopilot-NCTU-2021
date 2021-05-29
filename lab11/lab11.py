import cv2
import numpy as np
import time

def main():
    print("OpenCV's version:", cv2.__version__)
    img1 = cv2.imread('./book.jpg', cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread('./table.jpg', cv2.IMREAD_GRAYSCALE)
    if img1 is None or img2 is None:
        print('Could not open or find the images!')
        exit(0)
    
### SURF
    start_time = time.time()
    detector = cv2.xfeatures2d.SURF_create()
    keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
    keypoints2, descriptors2 = detector.detectAndCompute(img2, None)
    matcher = cv2.BFMatcher(cv2.NORM_L1,crossCheck=False)
    matches = matcher.match(descriptors1, descriptors2)

    matches = sorted(matches, key = lambda x : x.distance)
    img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
    cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches[:10], img_matches)
    end_time = time.time()

    print("SURF take", (end_time - start_time), "sec to compute")
    cv2.imwrite("./SURF.jpg", img_matches)
    cv2.imshow('SURF', img_matches)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

### SIFT
    start_time = time.time()
    detector = cv2.xfeatures2d.SIFT_create()
    keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
    keypoints2, descriptors2 = detector.detectAndCompute(img2, None)
    matcher = cv2.BFMatcher(cv2.NORM_L1,crossCheck=False)
    matches = matcher.match(descriptors1, descriptors2)

    matches = sorted(matches, key = lambda x : x.distance)
    img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
    cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches[:10], img_matches)
    end_time = time.time()
    print("SIFT take", (end_time - start_time), "sec to compute")

    cv2.imwrite("./SIFT.jpg", img_matches)
    cv2.imshow('SIFT', img_matches)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


### ORB
    start_time = time.time()
    detector = cv2.ORB_create()
    keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
    keypoints2, descriptors2 = detector.detectAndCompute(img2, None)
    matcher = cv2.BFMatcher(cv2.NORM_L1,crossCheck=False)
    matches = matcher.match(descriptors1, descriptors2)

    matches = sorted(matches, key = lambda x : x.distance)
    img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
    cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches[:10], img_matches)
    end_time = time.time()
    print("ORB take", (end_time - start_time), "sec to compute")

    cv2.imwrite("./ORB.jpg", img_matches)
    cv2.imshow('ORB', img_matches)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main()