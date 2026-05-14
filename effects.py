import cv2
import numpy as np
import random

# Base class for the different types of changes we can make to the image
# Person 3 worked on this file
class ChangeBase:
    def apply_change(self, img, x, y, w, h):
        pass

# This one shifts the colors in a box area
class ColorChange(ChangeBase):
    def apply_change(self, img, x, y, w, h):
        area = img[y:y+h, x:x+w].astype(np.int16)
        # Randomly change BGR channels
        diffs = [random.randint(40, 80) * random.choice([-1, 1]) for _ in range(3)]
        for i in range(3):
            area[:, :, i] += diffs[i]
        img[y:y+h, x:x+w] = np.clip(area, 0, 255).astype(np.uint8)

# This one makes a box area blurry
class BlurChange(ChangeBase):
    def apply_change(self, img, x, y, w, h):
        area = img[y:y+h, x:x+w]
        # Use cv2 gaussian blur
        blurred_area = cv2.GaussianBlur(area, (25, 25), 0)
        img[y:y+h, x:x+w] = blurred_area

# This one changes how bright a box is
class LightChange(ChangeBase):
    def apply_change(self, img, x, y, w, h):
        area = img[y:y+h, x:x+w].astype(np.int16)
        val = random.choice([-60, 60])
        area += val
        img[y:y+h, x:x+w] = np.clip(area, 0, 255).astype(np.uint8)
