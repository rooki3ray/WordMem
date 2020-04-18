from decimal import Decimal

class Word:

    def __init__(self, id, enword, cntranslation, phonetic='', testedcount=0, correctcount=0, lasttime=0, finished=0):
        self.id = id
        self.enWord = enword
        self.cnTranslation = cntranslation
        self.phonetic = phonetic
        self.testedCount = testedcount
        self.correctCount = correctcount
        self.lastTime = lasttime
        self.finished = finished

    def change_explanation(self, newtranslation):
        self.cnTranslation = newtranslation

    def is_phrase(self):
        k = self.enWord.split(' ')
        return len(k)>1
