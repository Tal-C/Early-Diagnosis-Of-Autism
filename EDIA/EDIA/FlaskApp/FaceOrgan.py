#import cv2

class FaceOrgan(object):
    """ This class represents an organ location in an image."""
    def __init__(self, organ, name):
        self.x = organ[0]
        self.y = organ[1]
        self.w = organ[2]
        self.h = organ[3]
        self.name = name
        self.center = (self.x + int(self.w/2), self.y + int(self.h/2))
    
    def get_rect(self):
        return (self.x, self.y, self.w, self.h)

    def mark_organ(self, frame, color):
        point = (self.x, self.y)
        size = (self.x+self.w, self.y+self.h)
        cv2.rectangle(frame, point, size, color, 1)

    def get_center(self):
        return self.center