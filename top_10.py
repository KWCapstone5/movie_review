from collections import Counter
import make_csv_wordcloud
# 언급된 수 konply로 하거나 SOYNLP
new=make_csv_wordcloud.positive_reviews
print(Counter(new).most_common(10))






# import os
# os.environ["JAVA_HOME"] = "C:\Program Files\Java\jdk-17"
# from pyspark.sql import *
# from pyspark.sql.functions import *
# from pyspark import SparkContext
# import os
# os.environ["JAVA_HOME"] = "C:\Program Files\Java\jdk-17"
# # create the Spark Session
# spark = SparkSession.builder.getOrCreate()
#
# # create the Spark Context
# sc = spark.sparkContext
# RDDs = sc.textFile('test.txt')
# RDDs = RDDs.flatMap(lambda line: line.split(" "))
# RDDs = RDDs.filter(lambda word: len(word) > 1) #delete blank
#
# # #소문자로 변환
# # RDDs = RDDs.map(lambda word: word.lower())
#
# # # s로 시작하는 단어만 찾기
# # RDDs = RDDs.filter(lambda word: (word[0]) =='s') #is s?
#
#
# # # 리듀스해서 가장많이
# RDDs = RDDs.map(lambda word: (word, 1))
# RDDs = RDDs.reduceByKey(lambda a, b:a+b )#identical key :value+value
#
# #정렬
#
# RDDs = RDDs.sortBy(lambda x : x[1], False)# default is asc Fasle=desc
#
# print(RDDs.take(10))