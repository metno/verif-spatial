import cv2

from .analyse import Analyse


class MeanGradientMagnitude(Analyse):
    """Compute sharpness"""
    def __init__(self,
        field_2d,
        ksize=3,
    ) -> None:
        # super
        self.ksize = ksize

    def __call__(self):
        gradient_x = cv2.Sobel(self.field_2d, cv2.CV_64F, 1, 0, ksize=self.ksize)
        gradient_y = cv2.Sobel(self.field_2d, cv2.CV_64F, 0, 1, ksize=self.ksize)
        gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)

        mgm = np.mean(gradient_magnitude)
        return mgm
