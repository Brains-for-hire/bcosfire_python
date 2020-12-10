from sklearn.base import BaseEstimator, TransformerMixin
import cv2
import scipy.signal as signal
from .base import FunctionFilter
import numpy as np

class GaussianFilter(FunctionFilter):
    def __init__(self, sigma, sz=0):
        sz = sigma2sz(sigma) if sz <= 0 else sz
        kernel = cv2.getGaussianKernel(sz, sigma)
        super().__init__(_sepFilter2D, kernel)

class DoGFilter(FunctionFilter):
    def __init__(self, sigma, onoff, sigmaRatio=0.5):
        sz = sigma2sz(sigma)
        kernel1 = np.outer(cv2.getGaussianKernel(sz, sigma),cv2.getGaussianKernel(sz, sigma))
        kernel2 = np.outer(cv2.getGaussianKernel(sz, sigma*sigmaRatio),cv2.getGaussianKernel(sz, sigma*sigmaRatio))
        if (onoff):
            kernel = kernel2 - kernel1
        else:
            kernel = kernel1 - kernel2
        super().__init__(_Filter2D, kernel)

class GaborFilter(FunctionFilter):
    def __init__(self, sigma, theta, lambd, gamma, psi):
        sz = sigma2sz(sigma)
        kernel = cv2.getGaborKernel((sz, sz), sigma, theta, lambd, gamma, psi);
        super().__init__(_Filter2D, kernel);

class CLAHE(FunctionFilter):
    def __init__(self):
        clahe = cv2.createCLAHE(tileGridSize=(8, 8), clipLimit=0.01, distribution='uniform', alpha=0.4)
        super().__init__(_CLAHE, clahe);

# Executes a 2D convolution by using a 1D kernel twice
def _sepFilter2D(image, kernel):
    return cv2.sepFilter2D(image, -1, kernel, kernel)

# Executes a 2D convolution by using a 2D kernel
def _Filter2D(image, kernel):
    result = signal.convolve(image, kernel, mode='same')
    return result

# Executes Contrast Limited Adaptive Histogram Equalization
def _CLAHE(image, clahe):
    return clahe.apply(image)

def sigma2sz(sigma):
    return int(np.ceil(sigma*3))*2 + 1; # Guaranteed to be odd
