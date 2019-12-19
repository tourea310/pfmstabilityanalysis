import pandas as pd
import numpy as np

def loadResponseCurve(filename, dx):
    '''Loads a pfm response curve from a text file.
        Args:
            filename (string): path to response curve file
            dx (float): spacing between adjacent data points in nanometers
        Returns:
            responseCurve (pandasDataFrame): the response curve
    '''
    response = np.loadtxt(filename)[::2] # to do: fix in lab view
    position = np.arange(len(response)) * 2 * dx
    responseCurve = pd.DataFrame({"position": position, "response": response})

    return responseCurve

def derivativeOfResponseCurve(responseCurve):
    '''Take the derivative of the response curve and attach a new column to input data frame.
        Args:
            responseCurve (pandasDataFrame): the response curve
    '''
    dx = responseCurve['position'].values[1]
    ddx = np.diff(responseCurve['response'])/dx
    responseCurve['derivative'] = list(ddx) + [0]

def findLinearRegionOfResponseCurve(responseCurve):
    '''Find linear region of response curve defined as +/- 10% of max slope.
    Append linear region column to input data frame.
        Args:
            responseCurve (pandasDataFrame): the response curve
        Returns:
            avgSlope (float): average slope of linear region
    '''
    if 'derivative' not in responseCurve:
        derivativeOfResponseCurve(responseCurve)
        
    ddx = responseCurve['derivative'].values
    linRange = (ddx > 0.9*(max(ddx))) & (ddx <= 1.1*(max(ddx)))
    peak_range = ddx[linRange]
    responseCurve['linearRange'] = linRange

    return np.mean(peak_range)

