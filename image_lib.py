import cv2
import numpy as np
import random
# Import the effects from effects.py
from effects import ColorChange, BlurChange, LightChange

# Class to handle all the image math and cv2 stuff
# Person 2 worked on this file
class ImageHandler:
    def __init__(self):
        self.original = None
        self.modified = None
        self.diff_list = [] 

    def open_file(self, filename):
        # Read the image file using opencv
        temp = cv2.imread(filename)
        if temp is None:
            return False
        # Convert BGR (cv2 default) to RGB (Tkinter default)
        self.original = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
        return True

    def make_diffs(self, num=5):
        if self.original is None:
            return
        
        self.modified = self.original.copy()
        img_h, img_w, _ = self.original.shape
        self.diff_list = []
        
        # List of our change objects
        methods = [ColorChange(), BlurChange(), LightChange()]
        
        tries = 0
        while len(self.diff_list) < num and tries < 100:
            tries += 1
            # Random size for the box
            box_w = random.randint(45, 75)
            box_h = random.randint(45, 75)
            # Random spot
            pos_x = random.randint(0, img_w - box_w)
            pos_y = random.randint(0, img_h - box_h)
            
            # Check if this spot overlaps with another one we already made
            is_overlap = False
            for (old_x, old_y, old_w, old_h) in self.diff_list:
                if not (pos_x + box_w + 5 < old_x or pos_x > old_x + old_w + 5 or 
                        pos_y + box_h + 5 < old_y or pos_y > old_y + old_h + 5):
                    is_overlap = True
                    break
            
            if not is_overlap:
                # Pick a random change method and use it
                pick = random.choice(methods)
                pick.apply_change(self.modified, pos_x, pos_y, box_w, box_h)
                self.diff_list.append((pos_x, pos_y, box_w, box_h))
        
        return len(self.diff_list) == num
