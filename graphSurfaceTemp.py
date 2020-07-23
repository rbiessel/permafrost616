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


def computeMeanAnnualTemp(dates=None, surfaceTemp=None):


    tuples = [[dates[i], surfaceTemp[i]] for i in range(len(dates))]

    df = pd.DataFrame(tuples) # convert to dataframe                                
    df[0] = pd.to_datetime(df[0], format='%m/%d/%Y') # create a datetime series    

    df = df.groupby(df[0].map(lambda x: x.year)).mean() # groupby year and mean from g roups

    return df.to_numpy()


def daysToDates(dates, startDate):
    date = datetime.datetime.strptime(startDate, '%m/%d/%Y')
    dates = dates - dates[0]
    return [(date + datetime.timedelta(days=day)).strftime("%m/%d/%Y") for day in dates]


def graph(filename=None, days=None, surfaceTemp=None, startDate=None):

    font = {'family': 'serif',
            'fontname': 'arial',
            'color': 'black',
            'weight': 'heavy',
            'size': 12,
    }




    dates = daysToDates(days, startDate)
    meanAnnual = computeMeanAnnualTemp(dates=dates, surfaceTemp=surfaceTemp)


    print(meanAnnual)

    days = days - days[0]
   
    fig, (ax1) = plt.subplots(figsize=(12, 6), ncols=1)
    ax1.plot(dates, surfaceTemp, label='Mean Monthly Temperatures')
    ax1.plot(dates[::12], meanAnnual, c="r", label='Mean Annual Temperature')

    ax1.tick_params(axis='x', which='major', labelsize=10, rotation=30)
    ax1.tick_params(axis='y', which='major', labelsize=10)

    ax1.xaxis.set_major_locator(MultipleLocator(40))

    ax1.set_ylabel('Temperature (°C)')
    ax1.set_xlabel('Date')
    plt.xlim(0, len(dates))
    plt.ylim(-30, 30)

    # ax1.scatter(baseline, coherence, s=0.3, c='b', marker=".", label='Individual Interferograms')
    # ax1.scatter(baselineMean, coherenceMean, s=10, c='r', marker="o", label='Average')

    ax1.legend(loc='upper right')


    # divider = make_axes_locatable(ax1)
    # cax = divider.append_axes("right", size="5%", pad=0.05)


    # # title = os.path.dirname(filename).split('/')[-1]
    # title = f'Predicted Temperature, Fairbanks, next 90 years'

    ax1.set_title("Permafrost Model Temperature Inputs", fontdict=font, pad=16)
    ax1.grid(color='black', linewidth=0.5)

    plt.tight_layout()
    
    if filename is not None:
        plt.savefig(filename, bbox_inches='tight', dpi=800)
        print(f'Wrote matrix to {filename}')
    else:
        plt.show()


def loadDataSet(file):
    csvData = genfromtxt(file, delimiter='	')
    
    # print(csvData)

    days = csvData[0:,[0]].transpose()[0]
    surfaceTemp = csvData[0:,[1]].transpose()[0]
    # print('DAYS', days)
    # print('TEMP', surfaceTemp)
    startDate = '8/15/2010'
    filename = None

    print('Surface Temp', surfaceTemp)
    print(len(days))


    graph(days=days, surfaceTemp=surfaceTemp, startDate=startDate, filename=filename)


def main():
    inputs = cmdLineParse()
    
    loadDataSet('surfaceTemp.csv')


if __name__ == '__main__':
    main()
    # secondMain() 