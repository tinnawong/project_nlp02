import re
import ast
import os
class prob:
    def readFile(self,fileName):
        data = []
        file = open(fileName, "r",encoding="utf8")
        dataset = file.read()
        dataset = re.split('\n', dataset)
        for sentence in dataset:
            if sentence !="" :
                get = sentence.split()
            # get.insert(0,"<s>")
            # get.insert(len(get),"</s>")
            # print(get)
            data.append(get)
        return data

    def createBigram(self,data):
        listOfBigrams = []
        bigramCounts = {}
        unigramCounts = {}
        nbyn = {}
        for data in data:
            for i in range(len(data)):
                if i < len(data) - 1:
                    listOfBigrams.append((data[i], data[i + 1]))
                    if (data[i], data[i + 1]) in bigramCounts:
                        bigramCounts[(data[i], data[i + 1])] += 1
                    else:
                        bigramCounts[(data[i], data[i + 1])] = 1

                if data[i] in unigramCounts:
                    unigramCounts[data[i]] += 1
                else:
                    unigramCounts[data[i]] = 1
        return listOfBigrams, unigramCounts, bigramCounts

    def createTrigram(self, data):
        listOfBigrams = []
        bigramCounts = {}
        unigramCounts = {}
        nbyn = {}
        for data in data:
            for i in range(len(data)):
                if i < len(data) - 1:
                    listOfBigrams.append((data[i], data[i + 1]))
                    if (data[i], data[i + 1]) in bigramCounts:
                        bigramCounts[(data[i], data[i + 1])] += 1
                    else:
                        bigramCounts[(data[i], data[i + 1])] = 1
                if data[i] in unigramCounts:
                    unigramCounts[data[i]] += 1
                else:
                    unigramCounts[data[i]] = 1
        # print(listOfBigrams)
        return listOfBigrams, unigramCounts, bigramCounts

    def calcBigramProb(self,listOfBigrams, unigramCounts, bigramCounts):

        listOfProb = {}
        for bigram in listOfBigrams:
            word1 = bigram[0]
            word2 = bigram[1]

            listOfProb[bigram] = (bigramCounts.get(bigram)) / (unigramCounts.get(word1))

        return listOfProb

    def addOneSmothing(self,listOfBigrams, unigramCounts, bigramCounts):
        listOfProb = {}
        cStar = {}
        for bigram in listOfBigrams:
            word1 = bigram[0]
            word2 = bigram[1]
            listOfProb[bigram] = (bigramCounts.get(bigram) + 1)/(unigramCounts.get(word1) + len(unigramCounts))
            cStar[bigram] = (bigramCounts[bigram] + 1) * unigramCounts[word1] / (unigramCounts[word1] + len(unigramCounts))
        return listOfProb, cStar

    def start(self):
        fileName = 'file/Dataset.txt'
        data = self.readFile(fileName)
        listOfBigrams, unigramCounts, bigramCounts = self.createBigram(data)
        print(listOfBigrams)
        print(unigramCounts)
        print(bigramCounts)
        # prob = self.calcBigramProb(listOfBigrams, unigramCounts, bigramCounts)
        # return  prob

    def start_add(self):
        fileName = 'file/Dataset.txt'
        data = self.readFile(fileName)
        listOfBigrams, unigramCounts, bigramCounts = self.createBigram(data)
        # print(listOfBigrams)
        # print(unigramCounts)
        # print(bigramCounts)
        prob = self.addOneSmothing(listOfBigrams, unigramCounts, bigramCounts)
        f = open("file/addOneSmoothing.txt", "w")
        f.write(str(prob[0]))
        f.close()
        return  prob[0]


    def propbigram(self,w1,w2):
        f = open("file/addOneSmoothing.txt", "r")
        prob = f.read()
        prob = ast.literal_eval(prob)
        readModel = True
        w1 = str(w1)
        w2 = str(w2)
        w1 = w1.lower()
        w2 = w2.lower()
        bigram = (w1, w2)
        # print(bigram in prob)
        # print(prob[bigram])
        f.close()
        try:
            return bigram in prob,prob[bigram]
        except Exception as e:
            print(e)
            return False,0

    def getnextWord(self,word):
        print("** ",word)
        try:
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, 'trigram.txt')
            b = self.readFile(filename)
            get = str(word)
            totalWord = []

            aa = [w for w in b if get in w[0] and get == w[0]]
            lenght = len(aa)
            if (lenght>=10):
                ll = 10
            else:
                ll =lenght
            for i in range(ll):
                # print(aa[i])
                word = ''
                for j in range(3):
                    if (aa[i][j] != "<s>" and aa[i][j] != "<p>" and aa[i][j] != "</p>"):
                        word += aa[i][j]
                # print("--", word)
                if (word != get):
                    totalWord.append(word)
            # print(totalWord)
            return totalWord
        except Exception as e:
            print("Error in prob : ",e)
            return []



if __name__ == '__main__':
    import time
    ss = time.time()
    filename = "trigram.txt"
    while(1):
        ww = input("คำ :")
        b = prob().getnextWord(ww)
        print(b)
