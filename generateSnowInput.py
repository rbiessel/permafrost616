import os
import numpy as np

def getNewData(fp, expression):
    newData = []
    data = False
    for line in fp:
        if data:
            line = line.replace('\n', '').split()
            line[1] = float(line[1]) * expression
            line = '	'.join(map(str, line)) + '\n'
        if 'Time    Snow Depth' in line:
            data = True
        newData.append(line)
    return newData


def writeToFile(fileName, data):
    with open(fileName, 'w') as f:
        for line in data:
            f.writelines(line)

def main():
    filename = 'SNOW.fbz'
    with open(filename) as file:
        data=file.readlines()

    multiples = np.arange(0,4.2,.2)
    

    for multiple in multiples:
        newData = getNewData(data, multiple)
        newFileName = f'output/SNOW-{int(multiple * 100)}%.fbz'
        writeToFile(newFileName, newData)




if __name__ == '__main__':
    main()