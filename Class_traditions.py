import json

from nltk.tokenize import word_tokenize

from optparse import OptionParser

from cltk.tag.pos import POSTag

import pickle

from cltk.stem.lemma import LemmaReplacer
from cltk.tag.pos import POSTag
from cltk.stop.greek.stops import STOPS_LIST

class Traditions:

  # Lists to be filled with their corresponding passages.
  Mt_TT = []
  Mk_TT = []
  Lk_TT = []

  Mt_DT = []
  Lk_DT = []

  Lk_S = []
  Mt_S = []

  Mt_MM = []
  Mk_MM = []
  Mk_S = []

  # Q passages from Luke and Matthew hand written :D
  Lk_Q = [[6,27], [6,28], [6,31], [6,35], [6,39], [6,40], [6,45],
       [9,57], [9,58], [9,59], [9,60], 
       [10,2], [10,3], [10,4], [10,5], [10,6], [10,7], [10,8], [10,9], [10,10], [10,11], [10,12], [10,16], [10,23], [10,24],
       [11,2], [11,3], [11,4], [11,9], [11,10], [11,11], [11,14], [11,15], [11,16], [11,24], [11,25], [11,26], [11,33], [11,34], [11,35], 
       [11,39], [11,40], [11,41], [11,42], [11,43], [11,44], [11,46], [11,47], [11,49], [11,50], [11,51], [11,52],
       [12,2], [12,3], [12,4], [12,5], [12,6], [12,7], [12,8], [12,9], [12,10], [12,11], [12,22], [12,23], [12,24], [12,25], [12,26], [12,27], 
       [12,28], [12,29], [12,30], [12,31], [12,32], [12,33], [12,34], [12,39], [12,40], [12,42], [12,43], [12,44], [12,45], [12,46], [12,51], [12,52],
       [12,53], [12,54], [12,55], [12,56], [12,58], [12,59],
       [13,24], [13,26], [13,27], [13,28], [13,29], [13,30], [13,34], [13,35], 
       [14,5], [14,11], [14,16], [14,17], [14,18], [14,19], [14,20], [14,21], [14,22], [14,23], [14,24], [14,26], [14,27], [14,34], [14,35],
       [16,13], [16,16], [16,17], [16,18], 
       [17,1], [17,2], [17,6], [17,33], [17,37], 
       [22,28], [22,29], [22,30],
       ]

  Mt_Q = [[5,13], [5,15], [5,18], [5,26], [5,32], [5,44], [5,45],
        [6,7], [6,9], [6,10], [6,11], [6,12], [6,13], [6,19], [6,20], [6,21], [6,22], [6,23], [6,24], [6,25], [6,26], [6,27], [6,28], [6,29], [6,30],
        [6,31], [6,32], [6,33], [6,34],
        [7,7], [7,8], [7,9], [7,10], [7,11], [7,12], [7,13], [7,14], [7,22], [7,23],
        [8,11], [8,12], [8,18], [8,19], [8,20], [8,21], [8,22],
        [9,32], [9,33], [9,34], [9,37], [9,38],
        [10,7], [10,8], [10,9], [10,10], [10,11], [10,12], [10,13], [10,14], [10,16], [10,17], [10,18], [10,19], [10,24], [10,25], [10,26], [10,27], 
        [10,28], [10,29], [10,30], [10,31], [10,32], [10,33], [10,34], [10,36], [10,35], [10,37], [10,38], [10,39], [10,40],
        [11,13], [11,12], [11,24], 
        [12,11], [12,12], [12,32], [12,34], [12,35], [12,38], [12,43], [12,44], [12,45],
        [13,16], [13,17], 
        [15,14], 
        [16,2], [16,3], 
        [17,20], 
        [18,7], [18,6],
        [19,28], 
        [20,16], 
        [22,2], [22,3], [22,5], [22,8], [22,9], [22,10], 
        [23,4], [23,7], [23,6], [23,12], [23,13], [23,23], [23,25], [23,26], [23,27], [23,28], [23,29], [23,31], [23,34], [23,35], [23,36], 
        [23,37], [23,38], [23,39],
        [24,28], [24,43], [24,44], [24,45], [24,46], [24,47], [24,48], [24,49], [24,50], [24,51],
      ] 



  # Function to process the given row with gospel entries by the three authors.
  # Puts every single verse per tradition in the right list as created above.
  def processRow(self, field):
    import re

    newList = []

    field = re.sub("[a-zA-Z]+", '', field)

    print(field)

    verseList = field.split(',')
    for element in verseList:
      if '-' in element:
        # There is a range, lets split this.
        chapter = element.split(':')[0]
        rangeWhole = element.split(':')[1]
        rangeStart = int(rangeWhole.split('-')[0])
        rangeEnd = int(rangeWhole.split('-')[1])
        rangeList = list(range(rangeStart, rangeEnd+1))

        for verse in rangeList:
          toAppend = [int(chapter), int(verse)]
          newList.append(toAppend)

      # print(element)
      else:
        element = element.strip()
        chapter = element.split(':')[0]
        verse = element.split(':')[1]
        toAppend = [int(chapter), int(verse)]
        newList.append(toAppend)

    return newList  

  # Retrieves the different traditions from the given csv file. Uses global variables to store lists!
  def retrieveTraditions(self):
    import csv  # Open CSV file and allow identification using Columns

    with open('4Gospels_v2.csv') as csvfile:
      readCSV = csv.DictReader(csvfile, delimiter=';')
      for row in readCSV:
        # print(row)
        
        # If all are not empty, triple tradition!
        if row['Matthew'] and row['Mark'] and row['Luke']:
          print('Triple Tradition!', row['Pericope'], row['Matthew'], row['Mark'], row['Luke'])
          self.Mt_TT.extend(self.processRow(row['Matthew']))
          self.Mk_TT.extend(self.processRow(row['Mark']))
          self.Lk_TT.extend(self.processRow(row['Luke']))

        # If Mark is empty, but Luke and Matthew are not, double tradition!
        elif row['Matthew'] and not row['Mark'] and row['Luke']:
          print('Double Tradition!', row['Pericope'], row['Matthew'], row['Luke'])
          self.Mt_DT.extend(self.processRow(row['Matthew']))
          self.Lk_DT.extend(self.processRow(row['Luke']))   

        # Text only in Luke is Luke Sondergut
        elif not row['Matthew'] and not row['Mark'] and row['Luke']:
          print('Luke Sondergut!', row['Pericope'], row['Luke'])
          self.Lk_S.extend(self.processRow(row['Luke']))
        # Text only in Matthew is Matthew Sondergut 
        elif row['Matthew'] and not row['Mark'] and not row['Luke']:
          print('Matthew Sondergut!', row['Pericope'], row['Matthew'])                
          self.Mt_S.extend(self.processRow(row['Matthew']))

        # Mark and Matthew tradition
        elif row['Matthew'] and row['Mark'] and not row['Luke']:
          print('MM Tradition!', row['Pericope'], row['Matthew'], row['Mark'])
          self.Mt_MM.extend(self.processRow(row['Matthew']))
          self.Mk_MM.extend(self.processRow(row['Mark']))
        # Mark tradition
        elif not row['Matthew'] and row['Mark'] and not row['Luke']:
          print('Mark Sondergut!', row['Pericope'], row['Matthew'], row['Mark'])
          self.Mk_S.extend(self.processRow(row['Mark']))

  # Removes carriage return from Perseus JSON
  def removeCarriage(self, s):
    return ' '.join(s.split())

  # Gets file name + path and retrieves author name.
  def retrieveName(self, filepath):
      items = filepath.split('/')
      items = items[len(items)-1]
      
      items = items.split('.')[0]
      
      return items

  # Lemmatizes a given list. Returns a string with lemmatized words.
  def lemmatizeList(self, lines):
    from cltk.corpus.utils.formatter import cltk_normalize

    tagger = POSTag('greek')

    lemmatizer = LemmaReplacer('greek')

    # can help when using certain texts (doc says it, so i does it)
    lines = cltk_normalize(lines) 
    
    # print(lines)
    # exit(0)
    lines = lemmatizer.lemmatize(lines)

    # Remove Stopwords and numbers and lowercases all words.
    lines = [w.lower() for w in lines if not w in STOPS_LIST]
    # lemmWords = removeNumbers(lemmWords)

    return ' '.join(lines)

  def createLemmatizedVersions(self):
    import os

    path = "./TXT/Output/"

    entries = []
    for file in os.listdir(path):
      if file.endswith(".txt"):
        entries.append(file)    

    for entry in entries:
      file = path + entry
      print('lemmatizing ', file)
      with open(file) as f:
        lines = f.read()
        # print(lines)
        # exit(0)
        newOutput = self.lemmatizeList(lines)        
        # print(newOutput)
        
        writeTo = path + '/Pickle/' + entry + '_lemmWords.pickle'

        with open(writeTo, 'wb') as f:
          pickle.dump(newOutput, f)

        writeTo = path + '/Lemmatized/' + entry + '_lemm.txt'
        f = open(writeTo, "w")
        # sentence = sentence + " "
        f.write(newOutput)
        f.close()          

        # exit(0)
  # Puts the verses in their corresponding tradition list
  def processText(self, file, author):
    with open(file) as json_file:
      data = json.load(json_file)
      gospel = data['text'] # The field we want in the Perseus JSON.

      for chapter in gospel:
        for verse in gospel[chapter]:
          sentence = gospel[chapter][verse]

          sentence = self.removeCarriage(sentence)
          
          
          item = [int(chapter)+1, int(verse)+1]

          print(author, item)


          if author == 'luke':
            self.writeFile(sentence, 'Lk_Book')

            if item in self.Lk_Q:
              self.writeFile(sentence, 'Lk_Q')

            if item in self.Lk_S:
              self.writeFile(sentence, 'Lk_S')
            elif item in self.Lk_DT:
              self.writeFile(sentence, 'Lk_DT')
            elif item in self.Lk_TT:  
              self.writeFile(sentence, 'Lk_TT')

          elif author == 'matthew':
            self.writeFile(sentence, 'Mt_Book')

            if item in self.Mt_Q:
              self.writeFile(sentence, 'Mt_Q')

            if item in self.Mt_S:
              self.writeFile(sentence, 'Mt_S')
            elif item in self.Mt_DT:
              self.writeFile(sentence, 'Mt_DT')
            elif item in self.Mt_TT:  
              self.writeFile(sentence, 'Mt_TT')
            elif item in self.Mt_MM:  
              self.writeFile(sentence, 'Mt_MM')            
          
          elif author == 'mark':
            self.writeFile(sentence, 'Mk_Book')

            if item in self.Mk_S:
              self.writeFile(sentence, 'Mk_S')
            elif item in self.Mk_MM:
              self.writeFile(sentence, 'Mk_MM')
            elif item in self.Mk_TT:  
              self.writeFile(sentence, 'Mk_TT')            

          elif author == 'john':
            self.writeFile(sentence, 'Jn_Book')

          else: 
            print('Not a gospel author! Check your input folder.')
            print(author, int(chapter)+1, int(verse)+1)
            exit(1)

  # Writes the line to the corresponding tradition file.
  def writeFile(self, sentence, output):
    bookFile = './TXT/Output/' + output + '.txt'

    f = open(bookFile, "a")
    sentence = sentence + " "
    f.write(sentence)
    f.close()


  # # Lemmatizes every sentence from the given book. 
  # def lemmatizeText(self, file, entry):
  #   with open(file) as json_file:
  #     data = json.load(json_file)
  #     gospel = data['text'] # The field we want in the Perseus JSON.

  #     for chapter in gospel:
  #       for verse in gospel[chapter]:
  #         sentence = gospel[chapter][verse]

  #         sentence = self.removeCarriage(sentence)

  #         sentence = lemmatizeList(sentence)

  #         writeFile(sentence, 'Lk_Lemm')    