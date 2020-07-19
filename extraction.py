import os
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
from pyltp import NamedEntityRecognizer
def simlify(text):
    LTP_DATA_DIR = r'E:\anaconda\ltpmoxin\ltp_data'  # ltp模型目录的路径
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')# 分词模型路径，模型名称为`cws.model`

    lexicon_path = os.path.join(LTP_DATA_DIR, 'lexicon')# 分词词典lexicon



    segmentor = Segmentor()# 初始化实例

    # segmentor.load(cws_model_path)  # 加载模型，如果不想自定义词典，就用这一句load模型即可

    segmentor.load_with_lexicon(cws_model_path,lexicon_path)# 加载模型，参数lexicon是自定义词典的文件路径


    words = segmentor.segment(text)# 分词

    #print('|'.join(words))#打印分词结果

    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')# 词性标注模型路径，模型名称为`pos.model`


    postagger = Postagger()# 初始化实例

    postagger.load(pos_model_path)# 加载模型

    postags = postagger.postag(words)# 词性标注,这里words是分词后的list

    #print(' | '.join(postags))

    postagger.release()# 释放模型

    par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')# 依存句法分析模型路径，模型名称为`parser.model`



    parser = Parser()# 初始化实例

    parser.load(par_model_path)# 加载模型

    arcs = parser.parse(words, postags)# 句法分析
    parser.release()  # 释放模型
    #信息提取，结果展示

    rely_id = [arc.head for arc in arcs]# 提取依存父节点id

    relation = [arc.relation for arc in arcs]# 提取依存关系

    heads = ['Root' if id ==0 else words[id-1] for id in rely_id]# 匹配依存父节点词语

    #for i in range(len(words)):

        #print(relation[i] +'(' + words[i] +', ' + heads[i] +')')


    array=[]
    for i in range(len(words)):
        dict={}
        dict["dep"]=words[i]
        dict["gov"] = heads[i]
        dict["pos"] = relation[i]
        array.append(dict)
    return array



    ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')
    recognizer = NamedEntityRecognizer()  # 初始化实例
    recognizer.load(ner_model_path)  # 加载模型
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    #for word, ntag in zip(words, netags):
    #   print(word + '/' + ntag)
    recognizer.release()  # 释放模型

    # for word, ntag in zip(words, netags):
    #     if(ntag != 'O'):#过滤非命名实体
    #        print(word + '/' + ntag)



def getHED(words):
    root = None
    for word in words:
        if word['gov'] == 'Root':
             root = word['dep']
    return root

def getWord(words, HED, wType):
    sbv = None
    for word in words:
        if word['pos'] == wType and word['gov'] == HED:
            sbv = word['dep']
    return sbv

def getFirstNotNone(array):
    for word in array:
        if word is not None:
            return word
    return None

def getMain(array):
    re = ''
    if len(array) > 0:
        hed = getHED(array)
        if hed is not None:
            sbv = getWord(array, hed, 'SBV')  # 主语
            vob = getWord(array, hed, 'VOB')  # 宾语
            fob = getWord(array, hed, 'FOB')  # 后置宾语

            adv =getWord(array, hed, 'ADV')  # 定中
            pob = getWord(array, adv, 'POB')  # 介宾如果没有主语可做主语

            zhuWord = getFirstNotNone([sbv, pob])  # 最终主语
            weiWord = hed  # 最终谓语
            binWord = getFirstNotNone([vob, fob, pob])  # 最终宾语

            re = '{}{}{}'.format(zhuWord,weiWord,binWord)
    return re.replace('None', '')

#print(getMain(simlify("因为考的不错今天晚上去西餐厅吃大餐好好犒劳一下自己！")))


