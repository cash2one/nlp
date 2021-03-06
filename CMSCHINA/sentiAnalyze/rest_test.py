# encoding=utf-8
from multiprocessing import Pool
import json
import requests

data = {'text': '我喜欢你'.decode('utf-8').encode('gbk')}
# data={'text':'创新能力是一支军队的核心竞争力，也是生成和提高战斗力的加速器。“军事力量的较量，深层次的是军事科技创新能力的较量。”全国人大代表、火箭军某研究所所长李贤玉说，实践证明，谁牵住了科技创新这个“牛鼻子”，谁就能走好科技创新这步棋，就能占领先机，赢得优势。'}
data2 = {
    'text': '周二早盘，两市高开后一度维持震荡，随后震荡下行双双翻绿.临近午间两市小幅跳水。午后，沪指弱势震荡，深成指表现相对较强。13：50过后，沪指震荡回升。截至收盘，沪指涨0.26%，报3651.77点，成交3608亿元；深成指涨0.85%，报13139.1点，成交5135亿元。 后市趋于乐观 红三兵布阵沪指稳步上扬 上证指数在站稳半年线上方后，沪指也水涨船高，过程中虽有震荡，但券商、地产、银行蓝筹股发力、题材股轮番接力，人气逐步回升；各大基金的排名战，各种“暴力”举牌战，轮番上演；年后一季度行情也在“拍摄中”，各种利好，你是不是在偷笑了！ 小编这么说你或许不信，王牌分析师的话你总不能不信吧！ 针对周一蓝筹股发力、创业板回调的走势，市场上关于二八风格转换终将成行的声音再度响起。其中的代表人国泰君安证券首席策略分析师乔永远等认为，中央经济工作会议打开“春季大切换”窗口期。被视为中央经济工作会议“定调会”的中央政治局会议指出“宏观政策要稳、微观政策要活、社会政策要托底”为2016年稳增长奠定基调;同时会议强调“抓住关键点、打好歼灭战”，供给侧改革“化解过剩产能、房地产去库存、降低企业成本”成为中长期发展共识。随着中央经济工作会议决议逐步落实，市场将提升对于中国经济增长目标的信心。而美国首次加息靴子落地有助于稳定市场偏好，美国下一次加息最可能发生在明年3月，这将为“春季大切换”提供了1~2个月的真空期。 与此同时，险资密集举牌提升市场对增量资金的预期。乔永远等认为，与增持股票不同，近期举牌案例发酵的实质在于产业资本谋求优质上市公司控制权，具有战略投资与财务投资双重意义。保险公司在资产荒背景下进一步提升权益投资配置比重，以金融地产为代表的产业资本对优质上市公司资产的战略布局加速。宝能系与安邦频频举牌万科的案例将提升市场对增量资金的预期，险资和产业资本正成为“春季大切换”的重要资金推手。 而安信证券首席策略分析师徐彪等认为，伴随量能的回升和年初增量资金的行动，未来可以更为乐观一些。 数据胜于雄辩 “钱”说话告诉你！  1 2 3 4 5 6 7 8 9 下一页'}
headers = {"Content-Type": "application/json"}


def process(data):
    print data['text']
    r = requests.post('http://172.18.1.146:9218/xinhuawang/senti/clf', data=json.dumps(data), headers=headers)
    print 'senti', r.text

    r = requests.post('http://172.18.1.146:9218/xinhuawang/senti/get_opinion_sentence', data=json.dumps(data),
                      headers=headers)
    print 'opinion_sentence', r.text
    return None


process(data)
# map(process, list([i for i in range(10000000)]))

# p=Pool(10)    
# p.map(process, list([i for i in range(10000000)]))
