from FaceOrgan import FaceOrgan

class Nose(FaceOrgan):
    """ This class represents an eye location in an image."""
    def __init__(self, nose):
        FaceOrgan.__init__(self, nose, "nose")