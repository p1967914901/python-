import json
from sklearn.cluster import DBSCAN

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
    #print(data)
    final={}
    finals={}
    citys=[];
    for city in data[2013]:
        citys.append(city);
    for year in data:
        labels = []     # Record the ids by order
        matrix = []
        values = {}
        for city in data[year]:
            labels.append(city)
            matrix.append(data[year][city])
        clustering = DBSCAN(eps=1, min_samples=2).fit(normalize(matrix))
        #kmeans = KMeans(n_clusters=6, random_state=0).fit(normalize(matrix))
        value=clustering.labels_;
        print(value)
        for i in range(len(labels)):
            values[labels[i]]=value[i]*1.0
        final[year]=values
    
    for i in range(len(citys)):
        t=[]
        for year in final:
           for city in final[year]:
               if city==citys[i]:
                   t.append(final[year][city])
        finals[citys[i]]=t
    #print(finals)
    with open("kmeans.json", mode='w', encoding='utf8') as file:
        json.dump(finals,file,ensure_ascii=False)
    pass
#{2013:{"浙江省":0,"江苏省":1,"北京市":0，......},2012:{...},2011:{...},.....}
