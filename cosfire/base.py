#!/usr/bin/env python

""" 
This module provides a parent class for the filters.

This program is free software: you can redistribute it and/or modify it under
the terms of the BSD General Public License as published by The COSFIRE Consolidation Project, version 0.0.1.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the BSD General Public License for more details.
You should have received a copy of the BSD General Public License along with
this program. If not, see https://github.com/Brains-for-hire/bcosfire_python/blob/main/LICENSE.
"""

from sklearn.base import BaseEstimator, TransformerMixin

class FunctionFilter(BaseEstimator, TransformerMixin):
    
    def __init__(self, filter_function, *pargs, **kwargs):
        self.filter_function = filter_function
        self.pargs = pargs
        self.kwargs = kwargs

    def fit(self):
        return self

    def transform(self, image):
        return self.filter_function(image, *self.pargs, **self.kwargs)
