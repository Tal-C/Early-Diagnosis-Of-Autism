from FaceOrgan import FaceOrgan

class Mouth(FaceOrgan):
    """ This class represents a mouth location in an image.
        if its a smile is_smile = True  """
    def __init__(self, mouth, is_smile):
        FaceOrgan.__init__(self, mouth, "mouth")
        self.is_smile = is_smile
