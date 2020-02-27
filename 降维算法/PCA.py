import json
from sklearn.decomposition import PCA

def loadDataFromFile(path):
    with open(path, mode='r', encoding='utf8') as file:
        stream = file.read()
        data = json.loads(stream)
    return data

def normalize(matrix):
    normalizedMatrix = []
    for line in matrix:
        newLine = []
        for _ in line:
            newLine.append(0)
        normalizedMatrix.append(newLine)
    for columnIndex in range(len(matrix[0])):
        minimum = 0
        maximum = 1         # prevent from ending up 0, occurring ZeroDivisionError
        for line in matrix:
            each = line[columnIndex]
            minimum = min(minimum,each)
            maximum = max(maximum,each)
        for lineIndex in range(len(matrix)):
            each = matrix[lineIndex][columnIndex]
            normalizedMatrix[lineIndex][columnIndex] = (each - minimum) / (maximum - minimum)
    return normalizedMatrix

def convertData(origin):
    data={}
    for year in range(1952,2014):
        temp={}
        for member in origin:
            if year==member['Sgnyea'] and member['Prvcnm']!='中国':
                values=list(member.values())
                values=values[3:]
                for i in range(0,20):
                    if values[i]=="":
                        del values[i]
                        values.insert(i,0)
                    if isinstance(values[i],str):
                        del values[i]
                        values.insert(i,0)
                temp[member['Prvcnm']]=values
        data[year]=temp
    return data

    
if __name__ == '__main__':
    path = "gdp.json"
    origin = loadDataFromFile(path)
    data = convertData(origin)
    pca = PCA(n_components=2)
    outputAll = {}                  # Use a dict to store the output data
    for year in data:
        labels = []     # Record the ids by order
        matrix = []
        for city in data[year]:
            labels.append(city)
            matrix.append(data[year][city])
        #print(normalize(matrix))
        coordinates = pca.fit_transform(normalize(matrix))        # Get 2-d matrix
        output = {}
        for i in range(len(labels)):
            output[labels[i]] = list(coordinates[i])    # IMPORTANT: output of MDS is not a common list object \
        for city in output:
            for k in range(0,2):
                if output[city][k]<=-1:
                    output[city][k]=-0.9
                if output[city][k]>=1:
                    output[city][k]=0.9
            
        outputAll[year] = output
        print(outputAll)
    with open("MDS.json", mode='w', encoding='utf8') as file:
        json.dump(outputAll,file,ensure_ascii=False)

    pass
