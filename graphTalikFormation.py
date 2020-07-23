#!/usr/bin/env python3

import os
import glob
import argparse
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
import numpy as np
from matplotlib import pyplot as plt
from osgeo.gdalconst import *
import osr
import datetime
from matplotlib import *
from dateutil.parser import parse
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1 import make_axes_locatable
from lib import lib as corlib
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from numpy import genfromtxt
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd


def parse():
    parser = argparse.ArgumentParser(description='Computes a Coherence Matrix given a directory of files')
    
    parser.add_argument('-i', '--infile', dest='infile', type=str, required=True,
            help='Coherence input path glob pattern.')

    parser.add_argument('-t', '--title', dest='title', type=str, required=True,
            help='Figure Title')

    return parser

def cmdLineParse():
    parser = parse()
    inps = parser.parse_args()
    inps.filePath = os.path.abspath(inps.infile)

    return inps


def computeMaxAnnualSnowHeight(dates=None, snowLevel=None):


    tuples = [[dates[i], snowLevel[i]] for i in range(len(dates))]

    df = pd.DataFrame(tuples) # convert to dataframe                                
    df[0] = pd.to_datetime(df[0], format='%m/%d/%Y') # create a datetime series    

    df = df.groupby(df[0].map(lambda x: x.year)).max() # groupby year and mean from g roups

    return df.to_numpy()


def daysToDates(dates, startDate):
    date = datetime.datetime.strptime(startDate, '%m/%d/%Y')
    dates = dates - dates[0]
    return [(date + datetime.timedelta(days=day)).strftime("%m/%d/%Y") for day in dates]


def graph(filename=None, snowHeights=None, talikFormation=None, startDate=None, talikDepths=None, permafrostDepth=None):

    font = {'family': 'serif',
            'fontname': 'arial',
            'color': 'black',
            'weight': 'heavy',
            'size': 12,
    }

    snowHeights = np.array(snowHeights) * 100

    fig, (ax1) = plt.subplots(figsize=(12, 6), ncols=1)
    # ax1.plot(snowHeights, talikFormation, 'ro', c='b')
    # ax1.plot(snowHeights, talikFormation)

    permafrostDepth = permafrostDepth - permafrostDepth[5]

    ax1.plot(snowHeights, permafrostDepth, 'ro', c='b')
    ax1.plot(snowHeights, permafrostDepth)

    # talikFormation = np.array(talikFormation)
    # talikFormation = talikFormation[~numpy.isnan(talikFormation)]

    # snowHeights = snowHeights[-len(talikFormation)]
    # print(len(snowHeights), len(talikFormation))

    ax1.tick_params(axis='x', which='major', labelsize=10, rotation=30)
    ax1.tick_params(axis='y', which='major', labelsize=10)

    ax1.set_ylabel('Permafrost Height Difference Relative to 100% (m)')
    ax1.set_xlabel('Snow Height (%)')

    # ax1.scatter(baseline, coherence, s=0.3, c='b', marker=".", label='Individual Interferograms')
    # ax1.scatter(baselineMean, coherenceMean, s=10, c='r', marker="o", label='Average')

    ax1.legend(loc='upper right')
    ax1.set_title("Permafrost Depth Difference by end of the Century", fontdict=font, pad=16)
    ax1.grid(color='black', linewidth=0.5)

    plt.tight_layout()
    
    if False:
        plt.savefig(filename, bbox_inches='tight', dpi=800)
        print(f'Wrote matrix to {filename}')
    else:
        plt.show()


def loadDataSet():
    
    permafrostExtent = 72.5
    snowHeights = [0, .2, .4, .6, .8, 1, 2, 3, 4]
    talikFormation= [float("NAN"), float("NAN"), float("NAN"), 2089, 2079, 2069, 2040, 2030, 2027]
    talikDepths = [0, 0, 0, 3.9, 6, 7.6, 10.7, 12.3, 13.4]
    permafrostDepth = [.6, .7, 2.6, 4.6, 6, 8, 11, 12.5, 13.6]
    permafrostDepth = 72.5 - np.array(permafrostDepth)
    filename = None

    graph(snowHeights=snowHeights, talikFormation=talikFormation, filename=filename, talikDepths=talikDepths, permafrostDepth=permafrostDepth)


def main():
    inputs = cmdLineParse()
    loadDataSet()


if __name__ == '__main__':
    main()
    # secondMain() 