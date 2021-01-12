#!/usr/bin/env python

""" 
This module defines the filters used by the BCOSFIRE algorithm. By following the paper (find the paper link in README.md), we only use the DoG filters.
Please check the Section 2 in the paper to see a detailed explanation of the DoG filter for the vessel segmentation in the retinal images.

Also, contrast limited adaptive histogram equalization (CLAHE) can be used to enhance the contrast of the vessels in the output of the B-COSFIRE filter. 
Please check Fig. 8 in the paper for a better understanding of the CLAHE filter.

Explanation of the filters and CLAHE:
DoG filter: https://en.wikipedia.org/wiki/Difference_of_Gaussians
Gabor filter: https://en.wikipedia.org/wiki/Gabor_filter
CLAHE: https://en.wikipedia.org/wiki/Adaptive_histogram_equalization#Contrast_Limited_AHE

This program is free software: you can redistribute it and/or modify it under
the terms of the BSD General Public License as published by The COSFIRE Consolidation Project, version 0.0.1.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the BSD General Public License for more details.
You should have received a copy of the BSD General Public License along with
this program. If not, see https://github.com/Brains-for-hire/bcosfire_python/blob/main/LICENSE.
"""

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
        super().__init__(_CLAHE, clahe)

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
