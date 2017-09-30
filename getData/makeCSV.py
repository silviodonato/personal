### Define the HTML parser class. We use it to simply transform the html in a string without tags (Myself.text)
import urllib.request
import datetime
from html.parser import HTMLParser

mesi = {
    'gen':1,    'feb':2,    'mar':3,    'apr':4,
    'mag':5,    'giu':6,    'lug':7,    'ago':8,
    'set':9,    'ott':10,    'nov':11,    'dic':12,
}

def fixData(data,anno):
    giorno = ''.join(ch for ch in data if ch.isnumeric())
    mese = ''.join(ch for ch in data if ch.isalpha())
    if mesi[mese]<=7: anno+=1
    data = "%s/%s/%d"%(giorno,mesi[mese],anno)
    return data

def dataToInt(data):
    g,m,a = data.split("/")
    a = int(a) - 1928
    t = datetime.datetime(a, int(m), int(g), 0, 0)
    return t.toordinal()

squadre = []
class Risultato():
    def __init__(self, risultato):
        ris = risultato.split("-")
        self.golCasa = int(ris[0])
        self.golOspiti = int(ris[1])

class Partita():
    def __init__(self):
        self.casa = None
        self.ospiti = None
        self.andata = None
        self.ritorno = None

class Giornata():
    def __init__(self,giornata,anno,serie):
        self.giornata = giornata
        self.anno = anno
        self.serie = serie
        self.giornataAndata = -1
        self.giornataRitorno = -1
        self.dataAndata = ""
        self.dataRitorno = ""
        self.partite = []

#andata (1ª)
class MyHTMLParser(HTMLParser):
    def __init__(self, anno,serie):
        HTMLParser.__init__(self)
        self.anno = anno
        self.serie = serie
        self.anno = anno
        self.serie = serie
        self.flag=False
        self.casa = None
        self.ospiti = None
        self.andata = None
        self.ritorno = None
        self.counter = 0
        self.giornata = Giornata(-1,self.anno,self.serie)
        self.partita = Partita()
        self.giornate = []
        self.text = ""
        self.currentTags = []
    
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
        data_clean = data_clean.replace("\\xc2","")
        data_clean = data_clean.replace("\\xaa","")
        data_clean = data_clean.replace("\\xba","")
        data_clean = data_clean.replace(" ","")
        
        if "h4" in self.currentTags or "h3" in self.currentTags or "h2" in self.currentTags:
            if 'Calendario' == data_clean:
                self.flag = True
            elif len(data_clean)>0 and data_clean[0].isalpha() and not "modifica" in data_clean:
                self.flag = False
                if len(self.giornata.partite)>0:
                    self.giornate.append(self.giornata)
                self.giornata = Giornata(-1,self.anno,self.serie)
        
        if self.flag and len(data_clean)>0 and data_clean[0].isalnum():
#            print(data_clean)
            if "ndata" in data_clean:
                if len(self.giornata.partite)>0:
                    self.giornate.append(self.giornata)
                giornata_andata = int(data_clean.split("(")[1].split(")")[0])
                self.giornata = Giornata(giornata_andata,self.anno,self.serie)
                self.giornata.giornataAndata = giornata_andata
            elif "itorno" in data_clean:
                giornata_ritorno = int(data_clean.split("(")[1].split(")")[0])
                self.giornata.giornataRitorno = giornata_ritorno
            elif "giornata" in data_clean or "alendario" in data_clean or "odifica" in data_clean:
                pass
            elif "-" in data_clean:
                if data_clean[0].isalpha():
                    self.partita.casa,self.partita.ospiti = data_clean.split("-")
                else:
                    if self.partita.casa==None:
                        self.partita.andata = Risultato(data_clean)
                    else:
                        self.partita.ritorno = Risultato(data_clean)
                        self.giornata.partite.append(self.partita)
                        self.partita = Partita()
            elif self.giornata.dataAndata=="":
                self.giornata.dataAndata = fixData(data_clean,anno)
            elif self.giornata.dataRitorno=="" and self.partita:
                self.giornata.dataRitorno = fixData(data_clean,anno)
            else:
                print("???? ",data_clean,self.currentTags)
        self.text +=data

giornate = []
for serie in ["A","B"]:
    for anno in range(1929,1930):
        fileName = "/home/sdonato/tensorflow/code/getData/web/%s_%s.html"%(str(anno),serie)
        print(fileName)
        response = urllib.request.urlopen("file://"+fileName)
        mfile = response.read()
        parser = MyHTMLParser(anno,serie)
        parser.feed(str(mfile))
        giornate += parser.giornate


csv = ""
debug = ""

mesi = set()

for giornata in giornate:
    giorn = int(giornata.giornataAndata)
    data = giornata.dataAndata
    dataInt = dataToInt(data)
    debug += "### Giornata %s - Campionato %s - Serie %s - %s ###\n"%(giorn,giornata.anno,giornata.serie, data)
    for partita in giornata.partite:
        debug += "# Partita %s - %s | %s-%s\n"%(partita.casa,partita.ospiti,partita.andata.golCasa,partita.andata.golOspiti)
        csv += "%s,%s,%s,%s\n"%(str(dataInt),partita.casa,partita.ospiti,partita.andata.golCasa-partita.andata.golOspiti)

npart = len(giornate)
for giornata in giornate:
    giorn = int(giornata.giornataRitorno)
    data = giornata.dataRitorno
    dataInt = dataToInt(data)
    debug += "### Giornata %s - Campionato %s - Serie %s - %s ###\n"%(giorn,giornata.anno,giornata.serie, data)
    for partita in giornata.partite:
        debug += "# Partita %s - %s | %s-%s\n"%(partita.ospiti,partita.casa,partita.ritorno.golOspiti,partita.ritorno.golCasa)
        csv += "%s,%s,%s,%s\n"%(str(dataInt),partita.ospiti,partita.casa,partita.ritorno.golOspiti-partita.ritorno.golCasa)

debug += "\n"+str(squadre)+"\n"

csvFile = open("data.csv",'w') 
csvFile.write("%d,3\n"%(len(csv.split("\n"))))
csvFile.write(csv)
csvFile.close()

debugFile = open("data.debug",'w') 
debugFile.write(debug)
debugFile.close()

