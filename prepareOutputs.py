import pandas as pd
import glob as glob


filesToConvert = glob.glob('./outputs/**/average.fbz')
def writeToCSV(file):
    outFile = file.replace('fbz', 'csv')
    read_file = pd.read_csv(file, sep="   |    |  ")
    read_file.to_csv(outFile, index=None, sep=',')


for file in filesToConvert:
    writeToCSV(file)