import pdb
import json
import re
import jieba
import jieba.analyse
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 设置jieba分词时所用的停用词表
jieba.analyse.set_stop_words("stopwords.txt")

# 读入原始数据文件，json格式，存入列表中
def read_file():
    file_name = "chinese_only.json"
    rawdata = []
    with open(file_name, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            rawdata.append(json.loads(line))
    # print(len(rawdata))
    # 输出为：28219
    return rawdata

# 从原始数据文件中挑出需要用到的变量，存入列表中
def select_data():
    rawdata = read_file()
    movie_data = []
    for rdt in rawdata:
        # 仅分析电影数据
        if rdt["subtype"] == "movie":
            # 为了避免出现不必要的异常，使用try-catch语句
            try:
                title = rdt["title"]
                score = float(rdt["rating"]["average"])
                ratings_count = rdt["ratings_count"]
                wish_count = rdt["wish_count"]
                collect_count = rdt["collect_count"]
                # 年份有可能只是四位数，也有可能带"年"字，此处仅取数字串
                year = rdt["year"]
                if re.match(r"\d{4}", year) != None:
                    year = re.match(r"\d{4}", year).group(0)
                else:
                    year = ""
                genres = rdt["genres"]
                # 导演与主演的名字信息均需从dict中再次一步提取
                directors = [director["name"] for director in rdt["directors"]]
                casts = [cast["name"] for cast in rdt["casts"]]
                summary = rdt["summary"]
            except KeyError:
                print("KeyError in rawdata: ", rdt)
            else:
                dataitem = {
                    "title": title, "score": score, "year": year,
                    "ratings_count": ratings_count, "wish_count": wish_count, "collect_count": collect_count,
                    "genres": genres, "directors": directors, "casts": casts, "summary": summary,
                }
                movie_data.append(dataitem)
    # print(len(data))
    # 输出为：17192
    return rawdata, movie_data

rawdata, data = select_data()

# 画出不同类别电影的数目 柱状图
def draw_allgenres(sorted_genres):
    # 指定默认字体，解决plt显示中文的问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.bar(range(len(sorted_genres)), [sg[1] for sg in sorted_genres], tick_label=[sg[0] for sg in sorted_genres])
    plt.show()
    # plt.savefig("allgenres.png")

# 统计电影的类别数，以及不同类别的电影数目
def get_allgenres():
    genres = {}
    for dt in data:
        for genre in dt["genres"]:
            if genre in genres:
                genres[genre] += 1
            else:
                genres[genre] = 1
    # print(genres)
    sorted_genres = sorted(genres.items(), key=lambda d:d[1], reverse=True)
    # print(sorted_genres)
    # draw_allgenres()
    return sorted_genres

sorted_genres = get_allgenres()

# 画出不同类别电影的关键词/特征词的词云
def keywords_genres(genre):
    # 获取所有该类电影的summary，拼接起来
    text = "".join([dt["summary"] for dt in data if genre in dt["genres"]])
    # 抽取出该类电影的summary中的关键词/特征词
    keywords_list = jieba.analyse.extract_tags(text, topK=30, withWeight=True)
    print(keywords_list)
    wd = WordCloud(background_color="white", font_path=r"msty.ttf", width=1400, height=1400, margin=5).generate(
        " ".join(list(jieba.cut(text))))
    plt.imshow(wd)
    plt.axis("off")
    plt.show()
    wd.to_file(genre + "_keywords.png")

keywords_genres("科幻")

def topdirectors_genres(genre, topk=15):
    directors = {}
    for dt in data:
        if genre in dt["genres"]:
            for director in dt["directors"]:
                if director in directors:
                    directors[director]["count"] += 1
                    directors[director]["sum_rating"] += dt["score"]
                else:
                    directors[director] = {
                        "count": 1, "sum_rating": dt["score"]
                    }
    # pdb.set_trace()
    ranked_directors = {d: directors[d]["sum_rating"] / directors[d]["count"] for d in directors}
    sorted_directors = sorted(ranked_directors.items(), key=lambda d:d[1], reverse=True)[:topk]
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.bar(range(len(sorted_directors)), [sd[1] for sd in sorted_directors], tick_label=[sd[0] for sd in sorted_directors])
    plt.show()
    plt.savefig(genre + str(topk) + "directors.png")

topdirectors_genres("科幻", 20)

pdb.set_trace()