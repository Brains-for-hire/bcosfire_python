#!/usr/bin/env python

""" 
This module provides basic functionalities for an image stack such as applying filters for each layer.

This program is free software: you can redistribute it and/or modify it under
the terms of the BSD General Public License as published by The COSFIRE Consolidation Project, version 0.0.1.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the BSD General Public License for more details.
You should have received a copy of the BSD General Public License along with
this program. If not, see https://github.com/Brains-for-hire/bcosfire_python/blob/main/LICENSE.
"""

import numpy as np

class ImageObject():

    def __init__(self, image, *args, **kwargs):
        self.image = image
        if kwargs is not None:
            for key, value in kwargs.items():
                setattr(self, key, value)


# Experimental class
class ImageStack():

    def __init__(self):
        self.stack = []
        self.threshold = 0

    def push(self, image):
        if type(image) is ImageObject:
            self.stack.append(image)
        else:
            self.stack.append(ImageObject(image))
        return self

    def pop(self):
        return self.stack.pop()

    # Reduce the stack to a single item: the result of a given
    # function after passing it the entire stack as a list
    def join(self, func, *args):
        self.stack = [func(self.stack, *args)]
        return self

    # Pass all current items in the stack to a given function
    # The function may push new items but these are not passed again later
    def applyAllCurrent(self, func, *args):
        stack2 = []
        while self.stack:
            func(stack2, self.stack.pop(), *args)
        self.stack = stack2
        return self

    # Pass all current items in the stack to a given function
    # The function may push new items and these are passed again later
    # This means this may run indefinitely/infinitely!
    def applyIndef(self, func, *args):
        while self.stack:
            func(self.stack, self.stack.pop(), *args)
        return self

    # Apply a filter to all items in the stack, popping them
    # and pushing the results
    def applyFilter(self, filt, filterArgs):
        # Compute all combinations of parameters
        argList = [(v,) for v in filterArgs[0]] if type(filterArgs[0])==list else [(filterArgs[0],)]
        for arg in filterArgs[1:]:
            if type(arg)==list:
                argList = [tupl + (v,) for tupl in argList for v in arg]
            else:
                argList = [tupl + (arg,) for tupl in argList]

        # Apply all possible filters
        def applyFilter(stack, item, filt, argList):
            responses = [ImageObject(filt(*tupl).transform(item.image), params=tupl) for tupl in argList]
            stack.extend(responses)

        def applyTreshold(stack, item, treshold):
            tresh = treshold*np.max(item.image)
            stack.append( ImageObject(np.where(item.image > tresh, item.image, 0), params=item.params) )

        self.applyAllCurrent(applyFilter, filt, argList)
        self.applyAllCurrent(applyTreshold, self.threshold)

        return self

    def valueAtPoint(self, x, y):
        val = 0
        params = None
        for img in self.stack:
            if img.image[y][x] > val:
                val = img.image[y][x]
                params = img.params
        if val > 0:
            return val,params
        else:
            return 0,None
