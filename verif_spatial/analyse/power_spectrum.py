import numpy as np

from .analyse import Analyse


class PowerSpectrum(Analyse):
    """Compute the power spectrum"""
    def __init__(
        self,
        field_2d,
    ) -> None:
        # super

    def __call__(
        self,
    ) -> None:
        N = np.prod(field_2d.shape)
        coeff = np.fft.rfft2(field_2d)
        
        spectrum = np.sum(np.abs(coeff), axis=0) / N

        return spectrum
