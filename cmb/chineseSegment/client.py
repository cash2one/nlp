# encoding=utf-8
import json
from gen.segment.SegmentService import Client
from bfd.harpc.common import config
from bfd.harpc import client
import sys
import time

if __name__ == '__main__':
    branch = sys.argv[1]
    conf_path = 'etc/client.conf.' + branch
    conf = config.Config(conf_path)
    manager = client.Client(Client, conf)
    client_ = manager.create_proxy()

    word = """
    　近日，一则名为《河南农村68岁老大爷迎娶22岁非洲新娘 村里炸开了锅》的新闻被多家媒体转发，并配有多张“现场图”，但真是这样的吗?真相是什么样子的?

    　　听说过很多的老夫少妻、少夫老妻，但毕竟血统都是一样的啊!今天这对，真是惊到了，非洲的22岁小姑娘，跨越种族肤色，只身来到中国，嫁给68岁的农村老大爷，这感情还是很深啊!虽说在生活中，性是很重要的一部分，但是只要感情深，一切都不是问题啊!要爱就应该这样，轰轰烈烈啊!

    　　河南农村一名68岁的老大爷迎娶22岁非洲姑娘让父老乡亲羡慕不已，他们还在老家举办了一场别具一格的中国元素婚礼。穿上这身红嫁衣，“黑美人”当得起啊!

    　　非洲妻子穿着中国传统的红色嫁衣，头顶一块红盖头，不仅让人想起那首：掀起了你的盖头来，让我来看看你的脸，你的脸儿。。。。“不过说实话，这非洲姑娘也是把我们中国嫁衣之美，展现的淋漓尽致的啊! 
    　　婚礼的主人公登场，老大爷气色相当不错啊。

    　　22岁的非洲姑娘，虽然没有中国血统，但是举止礼仪做得十足，俨然一个满清大家闺秀啊。

    　　最令人感动又惊讶的则是，婚礼上非洲新娘竟然用中文唱了一首《月亮代表我的心》，征服了现场的父老乡亲。虽是老夫少妻，但双方配合的相当默契，真是宝刀未老!
    　　一名35岁的美甲师周倩在一次培训课程中认识了自称教授微整型培训课程的老师，于是交了学费，仅仅只花了2天就结业。事后，她的闺蜜想尝鲜，请周倩施打玻尿酸隆鼻试试，没想到最后竟导致这名闺蜜右眼失明。

    　　35岁的周倩嫁到龙游县后经营起美甲店，同时兼做半永久绣眉服务，去年3月，她在参加美甲培训中认识了一位老师，对方介绍了微整型手术，并称一针玻尿酸的利润丰厚、且操作简单。

    　　听了很心动的周倩交了1万元学费，花了2天向老师学习理论知识，其中一天下午老师还进行现场示范，垫下巴、隆鼻、打嘟嘟唇，施打对象有外面找的客人，也有班上的学员当模特儿。

    　　现在回头想想，当时我真是疯了!现场观摩的周倩也拍了影片传上网，她回忆整个过程后悔地说，只看了老师的示范操作，自己连针头都没碰过，也不懂什么穴位，而且老师还和她们说，不就一针嘛，脸部都会吸收的。 
    　周倩的闺蜜王丹(化名)是个很爱的女生，经常给她做美甲，先前也曾在其他美容机构打了下巴玻尿酸，看到好友也学习了这项技术，便决定尝试一下。于是周倩透过朋友，花了500元买了1支玻尿酸和1根钝针。

    　　不料，王丹在周倩的美甲店裡打完玻尿酸隆鼻后，仅1分鐘就出现不适症状，左手发麻、眼睑下垂，右眼视力模煳…，赶紧就医，最后医生确诊，王丹右眼动脉栓塞导致失明，跑了好几家医院治疗都是一样的结果。

    　　报导指出，当初教周倩玻尿酸和贩售的人同时人间蒸发，目前她被依非法行医被拘，和周丹的闺蜜情谊也回不去了，还得面临巨额赔偿。
    　　广州市住房保障办公室征收储备处原副处长黄华辉，因受贿8931万元，被广州市中级人民法院判处无期徒刑。

    　　这是一宗典型的“小官巨贪”案，随着案情的披露，征地拆迁中的“暗箱操作”也随之浮出水面。

    　　广州市住房保障办公室征收储备处原副处长黄华辉，因受贿8931万元，被广州市中级人民法院判处无期徒刑。广参记者了解到，涉案行为主要发生在其担任科级干部，负责征地拆迁、安置补偿工作期间。黄华辉用赃款购买了11套房产、8个车位、2辆车及办理投资移民、购买红木家具、理财产品等。这些资产要么被查封，要么其亲属变卖用于退缴赃款。

    　　小土地官：负责征地拆迁近20年

    　　黄华辉自1996年8月在广州市土地开发中心(以下简称土发中心)、广州市人民政府征用土地办公室(以下简称市征用办)工作，此后近20年的时间内，一直负责征地拆迁项目。

    　　敛财之术：

    　　1.拆迁消息公布前提前囤房

    　　早在1993年，广州市已确定金沙洲纳入土地开发中心征收储备用地范围。2004年，土地开发中心才成立金沙洲开发建设项目办。当年，黄华辉被抽调至项目办，因此认识了横沙村委会工作人员骆某、沙凤村村民谭某。

    　　尽管金沙洲的征地红线范围已公布，但土发中心根据建设、道路的需要分步、分期推进征收、拆迁工作，收储时间跨度长，因而村民无法确定房产、地块的具体拆迁时间。

    　　在横沙某路征收工作开始前，黄华辉向骆某、倪某提议并商定：在该消息公布前，骆某、倪某出资低价收购房产，黄华辉负责提供征地信息、提高补偿标准及加快征收、补偿款支付进度，利润共同分配。

    　　之后，骆某、倪某疯狂“囤房”。2005年初，他们出资购买了横沙村黄丽路44号房产。下半年征地拆迁开始，黄华辉配合他们加快征收、补偿款支付进度，黄甚至为此专门跟进测量、财政评审等手续。

    　　法院查明，黄华辉与骆某、倪某按此方式赚取拆迁补偿款，黄华辉共分得1080万元。 
    2.保证行贿人获最好补偿

    　　黄华辉的受贿款项主要来自行贿人谭某，2010年至2014年间，黄华辉共收取谭某7380万元。

    　　2006年，黄华辉与谭某商定：由黄华辉负责协调、拆迁进度、控制拆迁时间、补偿标准，保证谭某在沙凤村购置的房产能获得最好、最适当的拆迁补偿，谭某送给黄华辉部分利润。此后，黄华辉按约定帮助谭某顺利取得了85套房产的拆迁补偿款，近9000万元，黄让谭某代管其分得的2030万元。

    　　2008年起，为建设金沙洲武广客运专线项目，土发中心需征收沙某村大量住宅基地及拆除上盖的住宅、构筑物。

    　　黄华辉与谭某商定：由沙某村集中收取村民的拆迁补偿款自行建设安置房的方式向土发中心承接征地、拆迁项目，通过控制安置房的建设成本获利。谭某承接工程后以5100万元转包，黄让谭某代管其分得的1700万元。

    　　2011年5月起，黄华辉负责跟进白云区征地项目，其中钟落潭镇广某路储备用地项目红线涉及的约2400亩地块。谭某称有五间厂房在红线范围内，要求黄华辉协助拆迁并按高标准确定补偿额、及时支付。此后，谭某获得首期补偿款(合同总金额的60%)共1.34亿元，谭某告知黄华辉可分得1500万元。

    　　赃款去向：买11套豪宅 办理投资移民

    　　法院查明，2006年至2014年，黄华辉用上述贿赂款购买了11套房产、8个车位、2辆车(均登记在女友梅某及梅某亲属名下)及办理投资移民、购买红木家具、理财产品等。

    　　黄华辉在供述中说，梅某原来在酒店工作，2005年8月其认识梅某后，约2005年底成为男女朋友并于2006年初起同居，因其所收的钱大部分放她银行账户，为了避免被查，2008年二人在香港登记结婚。

    　　2008年3月，黄华辉还委托一家移民顾问公司办理美国绿卡，对方审核材料后，让黄向香港汇丰银行的一个账户存入50万美元。2008年底，他将该账户交给倪某办理。2009年9月，黄华辉和妻子梅某取得美国投资移民绿卡。除了豪宅、名车，黄华辉购买家具时也出手不凡。他购买红木家具花费高达764万元，其中已支付564万元。至案发，还有部分家具还未收取。其他还包括办理美国投资移民共400万元，购买理财产品共200万元。

    　　涉案金额巨大 纪委提级调查

    　　2014年1月，广东省纪律检查委员会向广州市监察局移交了黄华辉涉嫌收受电力工程承包商巨额款项的线索，黄华辉进入纪检监察机关的“视野”。

    　　2014年12月22日下午，广州市纪委通报，黄华辉涉嫌严重经济违纪，市纪委已对其立案调查。鉴于黄华辉涉嫌构成犯罪，已将其移交司法机关处理。

    　　黄华辉并非市管干部，一般不由市纪委立案。对此，广州市纪委相关负责人专门解释，黄华辉涉案金额巨大、情节恶劣、案情触目惊心，因此由市纪委立案调查并通报。

    　　2014年12月10日，广州市番禺区人民检察院查封了7套涉案房产和一个车位，截至2015年7月，被告人黄华辉的妹妹协助黄华辉出售了5套房产和6个车位，以及车辆、理财产品和红木家具等。

    　　2016年2月6日，广州市检察院提起公诉。检方指控黄华辉在2005年至2014年间，涉嫌受贿犯罪11起，多次非法收受贿共计8891万元。

    　　自首、退赃、立功 酌情从轻判处无期徒刑

    　　法院查明，2005年至2014年，黄华辉利用担任前述职务、负责征地拆迁、安置、补偿工作的职务便利，为骆某、倪某、谭某等人谋取利益，多次收受骆某、倪某、谭某贿送的财物共计人民币8931万元，均由黄华辉自行支配、使用。

    　　广州中院认为，黄华辉没有自动投案，在办案机关采取调查措施期间，如实交代办案机关未掌握的罪行，与办案机关所掌握线索针对的犯罪事实不成立，在此范围外犯罪分子交代同种罪行，是自首，且黄华辉检举揭发的他人犯罪行为，经查证属实，有立功表现，依法可以从轻、减轻处罚。黄华辉的家属代其退缴了8891万元，可酌情从轻处罚。

    　　广州中院一审判决黄华辉犯受贿罪，判处无期徒刑，剥夺政治权利终身，并处没收财产1000万元;退缴的人民币8891万元，予以没收，上缴国库。

    　　自述：出身清贫，以“出人头地 改善家人生活”为奋斗理想

    　　在法院开庭审理时，黄华辉多次表示，所有贪腐都是自己一人所为，家人并不知情。

    　　他诉说，自己出身清贫，父母努力供他读大学，他曾以“出人头地、改善家人生活”作为奋斗理想。上班后，他就从事征地拆迁工作，这项工作困难不小，甚至常被拆迁户围在中间，要靠派出所去解围，工作压力很大。后来，他逐渐和村里一些有影响的人走到一起，希望借助他们的力量，去完成工作。
    开着宝马车去接孩子放学，却因为停车费的问题和收费员起争执。这位家长居然从车里拿出了“枪”指着收费员进行威胁。记者了解到，南京秦淮警方介入调查后，从该家长的公司内查获三把仿真枪。目前，该家长因非法持有枪支被秦淮警方依法刑事拘留。

    　　3月18日，秦淮警方接到某学校门外停车收费员报警称，有人不愿交停车费，还拿“枪”威胁自己。接到报警后，民警火速赶到报警人所在地。此时收费员张师傅显得非常气愤，他告诉民警，前一天，他看到一辆宝马车停在车位上，便正常给车贴了单子计费。没想到车主第二天找到他，称自己是临时停车，要求取消收费。

    　　现代快报记者了解到，据张师傅反映，他告知车主，如果停车时间在15分钟以内是不收费的，但如果超过了则要正常收费。而且张师傅注意到，当时对方停车时也没有打双跳，不像是临时停车。没想到，男子见张师傅不愿意取消车费单后，竟从车里找出一把锯子，对着张师傅比划。张师傅也不示弱，一把就抢了过去。紧接着，男子再次折回汽车里，居然从副驾驶座那边掏出了一把“枪”。
    　当时张师傅心里就咯噔一下，虽然有些害怕，但脾气上来了指着对方就喊，“有本事你就开枪!”学校保安听到了，赶紧从保安室跑出来拉住争吵的两人。而男子见到有人拉架后，回到车上驾车离去。

    　　民警了解情况后，立即调取了现场监控，果然看到了张师傅所说的一幕。同时，警方也通过学校工作人员确认了男子身份，是一名学生的家长吴某。现代快报记者了解到，当天下午南京秦虹派出所民警找到了男子吴某。根据吴某交代，他的“枪”藏在其公司的办公室里。民警当即赶到其公司搜查，结果发现了3把仿真枪。吴某交代，自己是仿真枪爱好者，这些枪是用来收藏的。

    　　目前，吴某因非法持有枪支的行为被秦淮警方刑事拘留，相关情况正在进一步调查之中。
    　在各类侵财类案件中，飞车抢夺一直是成都郫都警方高压打击的类型之一。近日，成都郫都警方侦破了一起飞车抢夺案。女士们提在手里的包，就是抢夺嫌疑人的目标。

    　　监控画面显示，一名女子右手提着的包，随着走动的幅度，正在有节奏的来回晃着。一名飞夺嫌疑人骑着摩托车迎面而来，将这一切看在了眼里。没过多久，嫌疑人骑摩托从女子身后一把抢过她的包并立即离去。

    　　在另一个地方，嫌疑人也用同样的飞夺手法，抢走了一名女子的包。 
    　民警通过视频侦查发现，嫌疑人基本上是两人或者一人作案，经常骑着摩托在街上遛弯。每次抢夺成功，他们都是往一个方向逃跑。很快民警便顺藤摸瓜找到了他们的落脚地，成功将两名飞车抢夺的嫌疑人抓捕归案。而就在其中一个嫌疑人抬起头时，负责侦破此案的民警发现这名嫌疑人有些眼熟。

    　　原来，民警发现其中一名犯罪嫌疑人此前也因飞车抢夺被打击过，之后他刑满释放。这次民警核实身份时，嫌疑人还主动和民警打招呼。

    　　目前，案件仍在进一步的审理中。
    　3月20日，住在东莞道滘镇的李女士向记者报料称，她的老公服用了家附近一间凉茶店售卖的凉茶和西药后反应剧烈，最后因抢救无效去世。她怀疑这间凉茶店涉嫌非法卖药。

    　　李女士夫妻俩是高州人，来东莞已经 20 多年了，六、七年前，他们一家搬到了道滘南城村住，她老公廖先生一直在附近的市场卖猪肉。3 月 18 日晚，廖先生因为咳嗽，儿媳妇就在附近的凉茶店为他买了一杯凉茶，还附带了 5 粒西药。儿媳妇表示，凉茶店的人向她询问了廖先生的病症后，直接开了凉茶和药。当时她看到店里的人还往凉茶里面加了些药粉。

    　　" 我老公就这样把药放进口里，喝了半杯凉茶之后，我就拿了一点陈皮给他解解苦，没想到不到 3 分钟，我老公就出事了。" 李女士回忆道，服药后的李先生表情变得非常痛苦，她赶紧跑过去拍他的胸口，" 我问他是不是胸口很辛苦，他一句话都说不出。"

    　　看到这种情形，李女士除了叫儿媳妇打 120 外，自己也马上跑到附近卫生站请人回来急救。在此期间，她看到老公的嘴巴里吐了一些东西，鼻子也流了血 
    　最终，廖先生因抢救无效死亡。李女士说，她老公身体一直都不错，在吃完药喝完凉茶后，才出现这种情况，她怀疑是凉茶店的药有问题。

    　　随后，记者来到这家凉茶店走访，店主李某承认，他们并没有售卖药物的资格。李某示，他们的凉茶都是中药熬制的，加入的粉也是中药制成的，开的药是正规厂商拿的西药，之前也开过给其他人，都没有问题。

    　　事发后，道滘镇卫生监督所、食药监站对该店进行现场检查时发现，店内有一批含有处方药的药品及凉茶原料，已依法进行查封。经查实，凉茶店店主李某并无从医资格。 目前，死者家属已经报警，警方已经介入调查，死因还有待确定。
    　　3月9号上午9点过，重庆沙坪坝小龙坎街边的一家小面馆开门还不久，店里都是早晨上班来吃早饭的顾客。这时，走进来一个二三十岁的年轻男子，打扮比较时髦，看着也挺帅，他点了一碗面后，就到靠近大门的一个座位坐下了。

    　　小伙子似乎有心事，面端上来后也没动筷子，他就在座位上坐着。上午10点过，小伙子从兜里拿出一瓶二锅头，拧开酒瓶盖，开始喝了起来。当时面馆老板刘先生就感觉不对劲：“怎么有大清早就来喝酒的。"

    　　这碗面，从上午9点吃到了下午2点过。一瓶二锅头喝完了，碗里的面基本上还没动，老板刘先生最后无奈只好报警了。
    　　沙区110民警赶来时，喝醉酒的小伙子正和店里的伙计争论着，他满口酒气。

    　　老板刘先生说，遇上这样的顾客真是有些倒霉。“一碗面吃了几个小时不走也就算了，他还骚扰其他的顾客，我们生意都没法做了!"原来，这位年轻人喝了一瓶二锅头后，就自动去找店里的顾客聊天，进来一个顾客，他就凑上去找人谈话，面馆被他闹成了“聊天室"。老板说，大家都知道这个小伙子是喝醉了，有的人害怕，不敢进店来吃饭，严重影响了店里的生意，因此他才报的警。

    　　民警发现，这个喝醉酒的小伙子并没有暴力倾向，似乎就是醉酒后想找人倾诉。于是民警也和他聊了起来。 
    　醉酒男子叫小谢(化名)，今年30岁出头，是四川遂宁来重庆打工的。小谢说，如今工作不容易，他生活压力比较大。三八妇女节本想问候下女友，想买点礼物的，可最后和女朋友吵了起来。

    　　和女友吵架后，小谢郁闷了一晚上，第二天一大早就买了一瓶白酒，来到这家面馆里喝闷酒。喝醉后，又特别想找人聊天倾诉。

    　　民警劝说小谢，年轻人不要酗酒，更不能借酒消愁。年轻人要靠勤劳致富，大白天一人在这儿喝酒，耽误自己出去找工作，并且店家和其他客人也非常反感。

    　　民警劝说了半个小时后，小谢点了点头，此时酒劲也醒了，最后他才拿起酒瓶离开。

    　　小伙子，与其借酒消愁，不如把这时间拿来积极地寻找出路!同感点赞!
    因为没带作业本上课时被老师体罚，学生被老师推倒后造成锁骨骨折。兴城小学的刘贺(化名)一个月前因为这样的一次经历，造成他现在仍然在家养伤无法 正常上学。事发后，涉事老师去医院看过刘贺，之后就再联系不上了。而对于此事，校方韩姓校长称事实确如家长所言，但拒绝了记者的采访。

    　　忘带作业本，孩子被体罚致锁骨骨折

    　　学生家长告诉记者，孩子就读于高新区兴城办事处的兴城小学，“事情发生在今年二月份，孩子性格挺老实，在学校表现一直还不错，就因为那天没带作业 本，老师就让班级里四个同样没有带作业本的孩子，站成一排。先是拿小竹竿打手，然后又拿竹竿对着刘贺推了一把，直接把孩子推倒了，当时孩子就摔倒在桌子附 近，当时刘贺站起来就哭了，班主任戴老师拽着刘贺的胳膊把他拉到了门口，并告诉刘贺，你要是哭就在外面哭够了再进教室。

    　　当时刘贺告诉戴老师他胸口疼，但是戴老师却说是因为刘贺哭得太厉害所以才会疼。”刘贺妈妈告诉记者，当时戴老师应该是没当回事，上完第二节课也没再 管刘贺，到了第四节课的体育课，体育老师发现刘贺没有跟其他同学一起玩，反而是耷拉着肩膀哭，上去询问情况刘贺告诉体育老师他胸口疼，体育老师赶紧拨打了 刘贺妈妈的电话，这才带刘贺去了医院。 
    　班上学生反映，老师不止一次打学生

    　　20日上午，记者来到了位于小吕巷村的刘贺家，刘贺目前还需要带着固定骨头的绑带，记者在与刘贺的交流中发现，刘贺是一个内向的男孩，当记者问道，戴老师好不好时，刘贺冲着记者摇了摇头，并告诉记者戴老师平时很凶，也经常发脾气，戴老师也不止一次打过学生。

    　　刘贺的父亲告诉记者，老师严厉一点是好事，但是这样的后果也太严重了。“从孩子受伤到我们听说隔了那么长时间，这也太不负责任了，孩子在医院住了二 十多天，除了入院第一天给孩子拍X光时见过戴老师，之后再也没见过，学校这边也没有什么说法，不管怎么样，学校总得处理这个事吧。”

    　　随后，刘贺父亲告诉记者，刘贺骨折当天下午，他就来到了孩子所在的班级，班里的同学们告诉他，当时戴老师拿竹竿打了班里面四个孩子，并且把刘贺用竹 竿推倒。还有一些跟刘贺关系不错的同学告诉他，平时戴老师也会处罚学生，有时下雨时会让学生在室外站着，甚至还会让班里面的班长帮忙监督被处罚的学生。

    　　校方：家长所言如实，但拒绝采访

    　　家长反映的情况确实如此吗?涉事班主任老师为什么联系不上?

    　　20日中午，记者来到了刘贺就读的兴城小学，当联系到一名具体负责的韩姓校长时，他本人称不在学校。对于家长所说的情况，这名校长称，“学生家长说的都是事实，没有必要再采访了。”那么体罚学生的班主任哪去了?当天，记者试图多次联系这名校长，都没有接通对方电话。

    　　而家长称，之前学校跟他们讲老师请孕假了，一直也没去学校上课，后来他们干脆联系了薛城区教育局，教育局的工作人员说尽快给他们一个满意的答复，而后来答复是经公处理。

    　　“孩子伤成这样，到现在连个说法都没有，我们上哪说理去!”刘贺的父亲无奈地说。

    　　这件事对学生身体、心里造成的伤害谁该来弥补，打人的老师就这样一直避而不见，此事就这样不了了之吗?对此，齐鲁晚报记者将继续追踪报道。
    记者接到了一位杨先生的电话。跟别人不同的是，他打来电话不是为自己，也不为家人，而是为了和自己没啥关系的一对老夫妻，这是咋回事呢?

    　　原来杨先生是外省来沈的务工人员，由于手头拮据住在了一家每天 7 块钱的旅馆里，从去年开始，旅馆内忽然来了对七十多岁无家可归的老两口，眼看着老两口每天捡垃圾勉强度日，再一问，感情他俩还有女儿在沈阳呢，为啥要过这样的日子呢?经过了一段时间，杨先生实在看不下去了，这才给我们拨打了热线电话。

    　　来到老两口所在的旅馆之后，朱霞看了眼门口的情况，感觉这里更像是集体宿舍，随后朱霞找到了这对七十多岁的老两口，刘大爷和他的老伴儿 ……

    　　原来老人家是吉林的，去年因身体原因不能再劳动了，老伴儿也得了白内障，眼睛失明。于是把家里的几亩地给亲戚种，老两口来沈阳投奔打工的姑娘姑爷。

    　　老人已经在这里住了一年多，平常靠卖废品赚得的十块八块钱维持生活。老人无奈的说："(杨先生)看我俩太可怜了，人家帮打的电话，我们这么大岁数了没经历过这种事。"

    　　话音未落，二位老人已经抑制不住哽咽了起来。对于 70 多岁的人来说，人生的风风雨雨看得多了，得多无助，心里得多不是滋味，两位老人才能委屈得落泪啊 …… 刘大爷说，女儿和姑爷把他们送到这里之后虽然负担了房租，但由于老伴得了白内障需要照顾，他们还是希望能和女儿生活在一起。而老两口的大女儿远在黑龙江，也无法照顾老人。

    　　大娘的眼病得治，有女儿，老两口的赡养也不能就这么飘着，这个忙，朱霞决定，得帮!于是，她拨通了刘大爷姑爷的电话。几分钟后，刘大爷的姑爷先生来到了现场。 
    姑爷来后，开口就是一句 " 我不想养了 "，让我们有点不知所措，接着姑爷也有点无奈的表示，老人现在不能自理，希望老人的两个女儿也能出一份力，同时希望政府也能负责老人的生活。

    　　记者：你老了之后谁管，是自己儿女养，没有儿女的孤寡老人政府管啊，首先老人得有保险，一年 100 多的新农合交上老人很多病就会能用，有这个保险国家就管，我帮你问问。但是老人家该养你得养啊，由于你是外地的，你就需要回吉林跑一趟，再看病就能省很多钱。

    　　姑爷：你们给我讲这些到底我就明白了，心里舒坦了。

    　　记者：我看你现在也乐出来了，太不容易了，跟你刚来时候表情不一样，那你也表个态以后怎么对大爷大娘。

    　　姑爷：对他们好点，我希望他们多活几年，没有父母没有我们今天。

    　　你看，也不是真那么混，这是心里的疙瘩没解开!这心结打开了，哪有过不去的砍呢!

    　　记者：" 今天在这解了希先生的一个心结我也挺开心的，大爷大娘今天就能和希先生回家了，在希先生的照料下希望二老安度晚年，也希望希先生回吉林办新农合能顺利。"

    　　下午 3 点，我们接到了杨先生的电话，刘大爷老两口已经被姑爷接回家了，这个结果让我们心里轻松了许多，大团圆结局啊!无论怎样百善孝为先，希先生把老两口接回家，好好尽尽孝，这一家人的日子才能更红红火火。
    发生在去年10月17日通州京塘路上的一起大货车砸扁等候红灯出租车的事件，还让很多市民记忆犹新。今天，肇事司机王成龙因被控交通肇事罪，在通州法院出庭受审。

    　　当时的监控画面中，在出事的红绿灯周期里一共出现了四辆车。受害人、出租车司机李某和一辆大货车同时抵达京塘路姚辛庄村东口的路口，遇到红灯，李某的出租车减速停车，而大货车直闯了过去。接着，一辆跟在出租车后面的小轿车为了更靠近路口，突然轧过实线，并线到了出租车左侧车道上。

    　　之前在这条车道上行驶的一辆满载石块的大货车高速冲过来，突然发现并线过来的小轿车，司机紧急向右侧打轮，车辆先是在路面上横了过来，紧接着侧翻，恰好躲过了违法并线的轿车，砸到了正等候红灯的出租车，出租车瞬间被大量石块掩埋。

    　　公诉机关指控说，王成龙当时驾驶河北牌照的重型自卸货车，为了躲避突然从右侧车道并入的河北牌照的小轿车，向右急打方向造成货车侧翻，货车及车上所载石块将出租车掩埋，司机李某当场死亡。经通州交通支队认定，王成龙负事故主要责任，并道小轿车司机丁某负次要责任，死者李某无责任。
    　并线小客车司机丁某当时离开了现场，但是由于事件很快发酵，网上对他的斥责声响成一片，他于次日前往交通队说明了情况。按照交通肇事罪的构成要件，在此类事故中，只有承担事故主要责任的肇事方才会涉嫌刑事犯罪，次要责任一方虽应承担相应的民事赔偿责任，但并不涉及刑事犯罪。

    　　“我挺对不起死者的。”庭上，王成龙说，在回答法庭和公诉人问题时，他承认，事发之后他本人没赔偿过死者家属，也不知道家里人赔过没有。“我那天是从顺义运石头去漷县，车子应该装12吨，但是那天装了46吨。”他说，如果不超载，老板挣不到钱。王成龙自称，他是第一次走这条路，一直跟着前边的货车。结果那辆车在变灯时闯过去了。“我当时减速了，如果没有小轿车并线，我能停下。”王成龙在庭上说。但是这个说法立即被公诉人指出“你在交通队不是这么说的，你说的是‘这个速度在路口停不住’。”

    　　犹豫了几秒钟，王成龙嗫嚅道：“我觉得应该能停……”按他的说法，当时的货车时速“差不多26、27公里”，但是经过交管部门的鉴定，真实车速应在36到48公里之间。无论车速多少，王成龙都没停住。“我突然发现有个小轿车并到我前边，我赶紧猛踩刹车，又打轮。结果翻了。”

    　　事发之后，王成龙没有离开现场，后来向警方自首。在王成龙肇事的那段时间中，北京接连发生了多起货车夺命的交通事故，也引发了公众对于货车肇事的高度关注。今天，王成龙在审理中表示认罪。公诉机关建议量刑为有期徒刑1年到1年半。法院没有当庭宣判。
    　决议公布后，印度媒体的注意力集中在安理会决议对“一带一路”的支持上，称“对印度领土主权的主张有害”。“一带一路”是中国的“国家倡议”，不需要印度或其他国家的认可，决议“有害”印度领土主权。

    　　那么，究竟中国的“一带一路”是怎样有损印度领土主权呢?主要原因就在于“中巴经济走廊”穿越巴控克什米尔地区，印度人对此耿耿于怀。另外，我们注意到，在这次联合国安理会的表决中，美国面对中国的巨大影响力也罕见服软，投了赞成票，最终这次决议以15票全部赞成的方式通过。
    　实际上，中国早就针对“一带一路”做出了极为详尽的说明，去年4月起，联合国亚太经社会、联合国开发计划署、联合国工业发展组织等机构先后以多种形式认可并促进“一带一路”的开展与实施。

    　　今年1月，我国元首在联合国日内瓦总部发表重要演讲，深刻阐释了共建人类命运共同体的理念，为推动世界发展和人类文明进步提出了中国方案。此次安理会决议首次载入“构建人类命运共同体”的重要理念，体现了国际社会的共识，彰显了中国理念和中国方案对全球治理的重要贡献。

    　　在今年两会记者会上，中国外长王毅表示，“一带一路”是“迄今最受欢迎的国际公共产品，也是目前前景最好的国际合作平台”，据目前统计，20多个国家的元首或政府首脑、50多位国际组织负责人、100多位部长级官员以及总共1200多名来自世界各国、各地区的代表将出席今年5月“一带一路”国际合作高峰论坛。
    　长期以来，美国对中国一直保持着武器和技术禁运的态度，在高端技术领域，尤其是高端军事技术领域，美国恨不得彻底掐死中国的军工研发产业!因为只有这样，才能保住自己的霸主地位!

    　　于是，中国奋发图强，自起炉灶，誓要打破美国的技术封锁!当然，一开始我们遭受到了一波又一波嘲笑，无论国内外……可是现在，小编可以跟大家说，中国军工再也不会受到嘲笑与漠视了!

    　　众所周知，航母作为当代海军的图腾，其战略意义远大于它自身的实战能力!曾经有人说道，当世界上任何一个地方发生热点事件时，美国总统总是第一时间询问：我们的航母战斗群在哪里?

    　　也许这是一句调侃的话，但是也足以显示航母在当代海军作战体系中不可动摇的地位!
    　美国作为现今世界上拥有航母最多的国家，无论是航母研制技术还是使用经验，都可以说达到了一个难以逾越的高度!

    　　然而，中国作为一个拥有1.8万公里海岸线，以及拥有72800平方公里海岛面积的国家，拥有一支强大海军势在必行!而一个国家的海军是否强大，标准之一就是要看这个国家能否自行建造航母!

    　　1918年，时值一战，受北洋政府海军部指派的陈绍宽和郑礼庆正在欧洲观战，学习现代战争经验。
    　当时英国正将“恩加丹”、“暴怒”号等大型舰艇改装成水上飞机母舰，其中“暴怒”号加装了飞行甲板，使其成为世界上第一艘真正意义上的航空母舰。

    　　是年7月，从“暴怒”号起飞的7架舰载机，轰炸了德国的空军基地，显示了航母的巨大作战能力。

    　　从此，陈绍宽等人意识到了航母对于现代海战的重要性，中国航母梦由此起航!
    　但是，由于当时国内经济凋敝，战乱连连，这个梦，直到2002年3月，才开始慢慢发芽!

    　　而承载这个梦想的，就是曾经的“瓦良格”，如今的“辽宁舰”!

    　　在耗历经4个月的艰难远航后，“瓦良格号”在2002年3月抵达大连港，但此时的她只有一个锈迹斑斑的空壳：所有武器、电子系统均已拆除或者破坏!动力系统甚至被传闻已经被炸毁!
    　为了阻止中国得到这艘前苏联遗留的航空母舰，美国等国家设下重重关卡!先是在土耳其博斯普鲁斯海峡，土耳其政府受美国旨意，强行命令其退回黑海!这一拦，便是28个月!

    　　后来，在我国政府的斡旋之下，土方同意放行，但条件是中国做到每年200万旅游人次，为土耳其创造20亿美元外汇!

    　　这还没完，当“瓦良格”一行即将驶入苏伊士运河时，美国再次从中作梗，指使埃及政府不要放行!如此，“瓦良格”一行就必须沿非洲西海岸航行回国，航程硬生生被增加至1.5万海里(约2.82万公里)!
    　美国为了阻止中国拥有航母，可谓是煞费苦心!在中国拿到“瓦良格”之后，它又是一阵冷嘲热讽，说中国根本掌握不了航母技术!

    　　但是现在，中国海军用实际行动给了美国狠狠一耳光!

    　　在今年两会期间，“中国电磁弹射之父”、中国工程院院士马伟明在接受采访时表示：中国不仅研制成功了航母电磁弹射技术，而且还搞定了更高难的电磁拦阻技术!
    上述两样技术，目前在研的只有中美两个国家，一旦研制成功，那就意味着未来中国舰载机可以携带更多燃料弹药，作战半径和能力将得到质的飞跃!

    　　电磁弹射技术相比于蒸汽弹射技术，结构更简单，更方便维护;电磁阻拦系统相比于传统的拦阻索系统，控制起来更灵活，特别是不同重量的飞机轮流降落时，只需按下按钮，一切由自动调节装置搞定!

    　　这样一来，航母的整体作战效率将大副提升!

    　　另外，关于中国的舰船综合电力技术，马院士还表示中国的全电推进系统目前处于世界第一的位置!


    """
    # word = """美国格林大学乔治?克林顿决定出访中国， 习近平将迎接他。他们将在1991年2月3日下午五点左右会面。我的电话号码是13807025737，QQ号是3356701943，email是sgyjkl_34@126.com，备用邮箱是30807033@qq.com，身份证号是370401198912150427，银行账号是6214342578651989，车牌号是冀J33455，我在瑞斯康达上班，股票代码为X15068"""
    # print client_.get_pos_tag(word, [])
    '''
    start=time.time()
    for i in range(50):
        client_.get_pos_tag(word*100, ["/opt/Jinhuang/xinhua_net/chineseSegment/user_dicts/颜色.txt"])
    end=time.time()
    print end-start
    '''
    '''
    start=time.time()
    for i in range(100):
        client_.get_pos_tag(word*5, ["/opt/Jinhuang/xinhua_net/chineseSegment/user_dicts/颜色.txt"])
    end=time.time()
    print end-start
    '''
    word = '''常规是conventional, common的意思'''
    word = '''
    百度，全球最大的中文搜索引擎、最大的中文网站。2000年1月创立于北京中关村。河南农村一名68岁的老大爷迎娶22岁非洲姑娘让父老乡亲羡慕不已，他们还在老家举办了一场别具一格的中国元素婚礼。我爱学习，学习使我快乐55555QQWER。
    '''
    print client_.get_pos_tag(word, [])
    print client_.get_pos_tag(word, ['user_dicts/会计.txt'])
    print client_.get_ner(word)
