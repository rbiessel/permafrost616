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


def daysToDates(dates, startDate):
    date = datetime.datetime.strptime(startDate, '%m/%d/%Y')
    dates = dates - dates[0]
    return [(date + datetime.timedelta(days=day)).strftime("%m/%d/%Y") for day in dates]


def displayArray(array, data=None, filename=None, days=None, snowLevel=None, depths=None, startDate=None):

    font = {'family': 'serif',
            'fontname': 'arial',
            'color': 'black',
            'weight': 'heavy',
            'size': 12,
    }
    
    dates = daysToDates(days, startDate)

    days = days - days[0]
    days = days / 365
   
    cmap = cm.get_cmap('seismic', 131)

    fig, (ax1) = plt.subplots(figsize=(12, 6), ncols=1)
    pos = ax1.contour(array, colors='k', aspect='auto', vmax=0, vmin=0, levels=0, linewidths=0.5)
    pos = ax1.imshow(array, cmap=cmap, aspect='auto', interpolation='spline36', vmax=13, vmin=-13)


    xtickInterval = (365 * 2)
    ytickInterval = 5

    x = np.arange(0, len(days), xtickInterval)
    y = np.arange(0, len(depths), ytickInterval) - 0.5

    plt.xticks(x, dates[0::xtickInterval], rotation=45)
    plt.yticks(y, depths[0::ytickInterval], rotation=45)

    ax1.tick_params(axis='x', which='major', labelsize=7)
    ax1.tick_params(axis='y', which='major', labelsize=10)

    ax1.xaxis.set_minor_locator(MultipleLocator(365))


    ax1.set_ylabel('Depth (m)')
    ax1.set_xlabel('Date')
    # plt.ylim(30, 0)



    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="5%", pad=0.05)


    title = os.path.dirname(filename).split('/')[-1]
    title = f'Bonanza Creek Black Spruce Temperature Timeseries - {title}% Snow Height'

    ax1.set_title(title, fontdict=font, pad=16)
    ax1.grid(color='gray', linewidth=0.25)
    plt.subplots_adjust(left=0.25)
    cbar = plt.colorbar(pos, cax=cax)
    cbar.set_label('Temperature (°C)', rotation=270)

    plt.tight_layout()
    
    if filename is not None:
        plt.savefig(filename, bbox_inches='tight', dpi=800)
        print(f'Wrote matrix to {filename}')
    else:
        plt.show()


def loadDataSet(file):
    csvData = genfromtxt(file, delimiter=',')
    days = csvData[1:,[0]].transpose()[0]
    snowLevel = csvData[1:,[3]]
    depths = csvData[[0], 5:]
    depths = depths[~numpy.isnan(depths)]

    tempData = csvData[1:, 3:].transpose()   
    tempData = tempData[:-27, :]

    print('Snow Level: ', snowLevel)
    print('Depths:', depths)
    print('TempData: ', tempData)
    startDate = '8/15/2010'
    print('Start Date:', startDate)

    filename = file.replace('.csv', '.png')
    print(tempData)
    displayArray(tempData, days=days, depths=depths, snowLevel=snowLevel, startDate=startDate, filename=filename)


def main():
    inputs = cmdLineParse()
    # workbook = xlrd.open_workbook(inputs.filePath)
    
    data = glob.glob('./outputs/**/result.csv')
    print(data)

    for file in data:
        loadDataSet(file)


if __name__ == '__main__':
    main()
    # secondMain() 