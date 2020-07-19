class Sentence(object):

    def __init__(self, url):
        self.url = url

    def getLTPAnalysis(self, sentence):
        data = bytes(json.dumps({'sentence': sentence}), encoding='utf8')
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(self.url, data, headers)
        resp = urllib.request.urlopen(req)
        respStr = resp.read()
        respJson = json.loads(respStr)
        return respJson

    def getHED(self, words):
        root = None
        for word in words:
            if word['gov'] == 'ROOT':
                root = word['dep']
        return root

    def getWord(self, words, HED, wType):
        sbv = None
        for word in words:
            if word['pos'] == wType and word['gov'] == HED:
                sbv = word['dep']
        return sbv

    def getFirstNotNone(self, array):
        for word in array:
            if word is not None:
                return word
        return None

    def getMain(self, sentence):
        re = ''
        result = self.getLTPAnalysis(sentence)
        if result['code'] == 200:
            array = result['result']
            if len(array) > 0:
                hed = self.getHED(array)
                if hed is not None:
                    sbv = self.getWord(array, hed, 'SBV')  # 主语
                    vob = self.getWord(array, hed, 'VOB')  # 宾语
                    fob = self.getWord(array, hed, 'FOB')  # 后置宾语

                    adv = self.getWord(array, hed, 'ADV')  # 定中
                    pob = self.getWord(array, adv, 'POB')  # 介宾如果没有主语可做主语

                    zhuWord = self.getFirstNotNone([sbv, pob])  # 最终主语
                    weiWord = hed  # 最终谓语
                    binWord = self.getFirstNotNone([vob, fob, pob])  # 最终宾语

                    re = '{}{}{}'.format(zhuWord, weiWord, binWord)
        return re.replace('None', '')