### Define the HTML parser class. We use it to simply transform the html in a string without tags (MyHTMLParser.text)
import urllib.request
from html.parser import HTMLParser

squadre = []
class Risultato():
    def __init__(self, risultato):
        ris = risultato.split("-")
        self.golCasa = int(ris[0])
        self.golOspiti = int(ris[1])

class Partita():
    def __init__(self):
        self.casa = -1
        self.ospiti = -1
        self.andata = None
        self.ritorno = None

class Giornata():
    def __init__(self,giornata):
        self.giornata = giornata
        self.partite = []

class MyHTMLParser(HTMLParser):
    HTMLParser.flag=False
    HTMLParser.casa = None
    HTMLParser.ospiti = None
    HTMLParser.andata = None
    HTMLParser.ritorno = None
    HTMLParser.counter = 0
    HTMLParser.giornata = None
    HTMLParser.partita = Partita()
    HTMLParser.giornate = []
    HTMLParser.text = ""
    HTMLParser.currentTags = []
    def handle_starttag(self, tag, attrs):
        self.currentTags.append(tag)
#        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        try:
            el = self.currentTags.pop()
        except:
            pass
#        if el!=tag:
#            Exception("parsing error. El = %s, Tag = %s"%(el,tag))
#        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        data_clean = data.replace("\\n","")
        data_clean = data_clean.replace("\\t","")
        data_clean = data_clean.replace(" ","")
        if "Giornata" in data_clean:
            HTMLParser.flag = True
            if HTMLParser.giornata:
                HTMLParser.giornate.append(HTMLParser.giornata)
#                print("### Giornata ###",HTMLParser.giornata.giornata)
            HTMLParser.giornata = Giornata(int(data_clean.split('ˆ')[0].replace(" ","")))
            HTMLParser.counter = 1
        if "\\r" in data_clean:
            HTMLParser.flag = False
            HTMLParser.counter = 0
        data_clean = data_clean.replace(" ","")
#        if len(data_clean)>0 and HTMLParser.flag:
#            HTMLParser.giornate[len(HTMLParser.giornate)-1] += "\n"+data_clean
        if HTMLParser.counter>0 and not data_clean:
            HTMLParser.counter+=1
        print("data_clean",data_clean,".",HTMLParser.counter)
        if HTMLParser.counter>=7 and data_clean:
            if HTMLParser.partita.casa<0:
                if not data_clean in squadre:
                    squadre.append(data_clean)
                HTMLParser.partita.casa = squadre.index(data_clean)
            elif HTMLParser.partita.ospiti<0:
                if not data_clean in squadre:
                    squadre.append(data_clean)
                HTMLParser.partita.ospiti = squadre.index(data_clean)
            elif not HTMLParser.partita.andata:
                HTMLParser.partita.andata = Risultato(data_clean)
            elif not HTMLParser.partita.ritorno:
                HTMLParser.partita.ritorno = Risultato(data_clean)
                HTMLParser.giornata.partite.append(HTMLParser.partita)
                print("### Partita %s - %s | %s | %s"%(HTMLParser.partita.casa,HTMLParser.partita.ospiti,HTMLParser.partita.andata,HTMLParser.partita.ritorno))
                HTMLParser.partita = Partita()
            
        if HTMLParser.casa:
            HTMLParser.ospiti = data_clean

        
        self.text +=data
#        print data,
#        print("Encountered some data  :", data,self.currentTags)

#response = urllib.request.urlopen('http://www.gazzetta.it/speciali/risultati_classifiche/2010/calcio/seriea/calendario.shtml')

files = [
    "/home/sdonato/tensorflow/code/getData/web/2010.html",
#    "/home/sdonato/tensorflow/code/getData/web/b_2010.html",
]

parser = MyHTMLParser()

for fileName in files:
    response = urllib.request.urlopen("file://"+fileName)
    mfile = response.read()
    
    parser.feed(str(mfile))


csv = ""
giornate = parser.giornate

for giornata in giornate:
    giorn = int(giornata.giornata)
    print("### Giornata ###",giorn)
    for partita in giornata.partite:
        print("# Partita %s - %s | %s"%(partita.casa,partita.ospiti,partita.andata.golCasa-partita.andata.golOspiti))
        csv += "%s,%s,%s,%s\n"%(giorn,partita.casa,partita.ospiti,partita.andata.golCasa-partita.andata.golOspiti)

npart = len(giornate)
for giornata in giornate:
    giorn = int(giornata.giornata+npart)
    print("### Giornata ###",giorn)
    for partita in giornata.partite:
        print("# Partita %s - %s | %s"%(partita.ospiti,partita.casa,partita.ritorno.golOspiti-partita.ritorno.golCasa))
        csv += "%s,%s,%s,%s\n"%(giorn,partita.ospiti,partita.casa,partita.ritorno.golOspiti-partita.ritorno.golCasa)

csvFile = open("data.csv",'w') 
csvFile.write("%d,3\n"%(len(csv.split("\n"))))
csvFile.write(csv)
csvFile.close()

#print(parser.giornate)
#giornate = str(mfile).split('<th colspan="2">')
#giorn = giornate[4].split("\tbody")[0]
#parser = MyHTMLParser()
#parser.feed(giorn)
#giorn = parser.text
#for i in range(10):
#    giorn = giorn.replace("\\n","")
#    giorn = giorn.replace("\\t","")

#print(giorn)

#print(parser.text)
