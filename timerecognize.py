import re
from datetime import timedelta
import datetime
from dateutil.parser import parse
import jieba.posseg as psg

UTIL_CN_NUM = {
    '零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
}

UTIL_CN_UNIT = {'十': 10, '百': 100, '千': 1000, '万': 10000}

def cn2dig(src):
    if src == "":
        return None
    m = re.match("\d+", src)
    if m:
        return int(m.group(0))
    rsl = 0
    unit = 1
    for item in src[::-1]:
        if item in UTIL_CN_UNIT.keys():
            unit = UTIL_CN_UNIT[item]
        elif item in UTIL_CN_NUM.keys():
            num = UTIL_CN_NUM[item]
            rsl += num * unit
        else:
            return None
    if rsl < unit:
        rsl += unit
    return rsl

def year2dig(year):
    res = ''
    for item in year:
        if item in UTIL_CN_NUM.keys():
            res = res + str(UTIL_CN_NUM[item])
        else:
            res = res + item
    m = re.match("\d+", res)
    if m:
        if len(m.group(0)) == 2:
            return int(datetime.datetime.today().year/100)*100 + int(m.group(0))
        else:
            return int(m.group(0))
    else:
        return None

def parse_datetime(msg):
    #print('msg:',msg)
    if msg is None or len(msg) == 0:
        return None


    m = re.match(
        r"([0-9零一二两三四五六七八九十]+年)?([0-9一二两三四五六七八九十]+月)?([0-9一二两三四五六七八九十]+[号日])?([上中下午晚早]+)?([0-9零一二两三四五六七八九十百]+[点:\.时])?([0-9零一二三四五六七八九十百]+分?)?([0-9零一二三四五六七八九十百]+秒)?",
             msg)
    #print('m.group:',m.group(0),m.group(1),m.group(2),m.group(3),m.group(4),m.group(5))
    if m.group(0) is not None:
        res = {
            "year": m.group(1),
            "month": m.group(2),
            "day": m.group(3),
            "noon":m.group(4),  # 上中下午晚早
            "hour": m.group(5) if m.group(5) is not None else '00',
            "minute": m.group(6) if m.group(6) is not None else '00',
            "second": m.group(7) if m.group(7) is not None else '00',
        }
        params = {}
        for name in res:
            if res[name] is not None and len(res[name]) != 0:
                tmp = None
                if name == 'year':
                    tmp = year2dig(res[name][:-1])
                else:
                    tmp = cn2dig(res[name][:-1])
                if tmp is not None:
                    params[name] = int(tmp)
        target_date = datetime.datetime.today().replace(**params)
        #print('target_date:',target_date)
        is_pm = m.group(4)
        if is_pm is not None:
            if is_pm == u'下午' or is_pm == u'晚上' or is_pm =='中午':
                hour = target_date.time().hour
                if hour < 12:
                    target_date = target_date.replace(hour=hour + 12)
        return target_date.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return None


# 对提取出的拼接日期串进行进一步的处理，进行有效性判断
def check_time_valid(word):
    #print('check:',word)
    m = re.match("\d+$", word)
    if m:
        if len(word) <= 6:
            return None
    word1 = re.sub('[号|日]\d+$', '日', word)
    #print('word1:',word1)
    if word1 != word:
        return check_time_valid(word1)
    else:
        return word1

#时间提取
def time_extract(text,time):
    time_res = []
    date=datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    word = ''
    keyDate = {'今天': 0, '明天':1, '后天': 2}
    for k, v in psg.cut(text):
        #print(k,v)
        if k in keyDate:
            if word != '':
                time_res.append(word)
            # 日期的转换，timedelta提取任意延迟天数的信息
            word = (date+timedelta(days=keyDate.get(k, 0))).\
                      strftime('%Y{y}%m{m}%d{d}').format(y='年',m='月',d='日')

        elif word != '':
            if v in ['m', 't']:
                word = word + k
            else:
                time_res.append(word)
                word = ''
        elif v in ['m', 't']:  # m:数字 t:时间
            word = k
    #print('word:',word)
    if word != '':
        time_res.append(word)
    #print('time_res:',time_res)
    # filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表
    result = list(filter(lambda x: x is not None, [check_time_valid(w) for w in time_res]))
    #print('result:',result)
    final_res = [parse_datetime(w) for w in result]
    #print('final_res:',final_res)
    return [x for x in final_res if x is not None]


#text1 = '我要住到明天下午四点'
#print(text1, time_extract(text1,'2020-07-23 13:08:00'))

