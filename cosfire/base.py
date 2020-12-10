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
