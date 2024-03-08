# Databricks notebook source
#Get the last Saturday based on Load Date value
from datetime import datetime,timedelta
from dateutil.parser import parse
d=datetime.now()
day_name = 'saturday'
days_of_week = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
target_day = days_of_week.index(day_name.lower())
delta_day = target_day - d.isoweekday()
if delta_day >= 0:
  delta_day -= 7
endDt=(d + timedelta(days=delta_day)).replace(hour=23, minute=59).strftime('%Y-%m-%d')
print(endDt)

# COMMAND ----------

from pyspark.sql.functions import *;
from datetime import datetime,date,timedelta;
from pyspark.sql import SparkSession;
from dateutil.parser import parse;

spark=SparkSession.builder.appName("ForeSeeAPI").enableHiveSupport().getOrCreate();
dbutils.widgets.text("mnt","","");
mnt = dbutils.widgets.get("mnt");
currentdate = datetime.date(datetime.now()) 
print(datetime.now())
startDt = currentdate - timedelta(days=10)
loadDt=date.fromisoformat(endDt.replace("/","-"))
YYYY = loadDt.strftime('%Y')
mm = loadDt.strftime('%m')
dd = loadDt.strftime('%d')
all = "{*}"
spark.conf.set("spark.sql.sources.partitionOverwriteMode","dynamic");

# COMMAND ----------

startDt

# COMMAND ----------

# Define function to parse survey data
import csv

def parseJson(data_file):
  items = data.json()["items"]
  with open(data_file, "w") as file:
    csv_file = csv.writer(file)
    csv_file.writerow(["SurveyId","ExperienceDate","ResponseId","Name","Phrase","Type","Label","ResponseType","Answers"])
    for item in items:
      surveyId = item["id"]
      experienceDate = item["experienceDate"]
      for response in item["responses"]:
        for answer in response['answers']:
          csv_file.writerow([surveyId,experienceDate,response['id'],response['name'],response['phrase'],response['type'],response['label'],response['responseType'],'.'.join(answer.splitlines())])

# COMMAND ----------

# API authentication and connection to hannaford delivery endpoint
import requests
import base64
import json

url = "https://api.foresee.com/v1/token"

querystring = {"scope":"r_cx_basic","grant_type":"client_credentials"}
ClientID= "jQxJsXcPm7lw1tMewLTyULQBlfqB02jh"
Clientsecret= "boa3h9pOxHODTO9enSvO"

AccessCode = ClientID+":"+Clientsecret
# print(AccessCode)

# Standard Base64 Encoding
encodedBytes = base64.b64encode(AccessCode.encode("utf-8"))
encodedStr = str(encodedBytes, "utf-8")
# print(encodedStr)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Basic " + encodedStr
}

Token = requests.request("POST", url, headers=headers, params=querystring)

AccessToken = Token.json()['access_token']

#definition end point
def_url = "https://api.foresee.com/v1/measures/8873765/definition"

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + AccessToken
}

definition = requests.request("GET", def_url, headers=headers)

# # data endpoint
# data_url = "https://api.foresee.com/v1/measures/8873765/data?from={0}&to={0}".format(loadDt)

# headers = {
#     "Accept": "application/json",
#     "Authorization": "Bearer " + AccessToken
# }

# data = requests.request("GET", data_url, headers=headers)
# # print(data.text)

# COMMAND ----------

#Parse MQ questions with possible answers
import csv

filepath = "dbfs:{0}/RDS/Delhaize/FORESEE/Hannaford/Delivery/{1}/{2}".format(mnt,YYYY,endDt)
dbutils.fs.mkdirs(filepath)
def_file = "/dbfs{0}/RDS/Delhaize/FORESEE/Hannaford/Delivery/{1}/{2}/foreseeDeliveryQuestions-MQ-{2}.csv".format(mnt,YYYY,endDt)

items = definition.json()["MQ"]
channel = "Hannaford Delivery"

with open(def_file, "w") as file:
    csv_file = csv.writer(file)
    csv_file.writerow(["Channel","CategoryId","Category","QuestionId","Question","Label","ResponseType","Type","AnswerId","Text","Value"])
    for item in items:
        categoryId = item["id"]
        category = item["name"]
        for question in item["questions"]:
            questionid = question["id"]
            label = question["label"]
            responsetype = question["responseType"] 
            qestn = question["name"]
            qtype = question["type"]
            for answer in question["answers"]:
                answerid = answer["id"]
                text = answer["text"]
                value = answer["value"]
                csv_file.writerow([channel,categoryId,category,questionid,qestn,label,responsetype, qtype,answerid,text,value])
        
# df = spark.read.csv('/FileStore/tables/forsee.csv', header=True)
# df = spark.read.csv('dbfs:/mnt/rs06ue2dipadl01/FIONA/RDS/Delhaize/ForeSee/foresee-questions-withanswers.csv', header=True)
# display(df)

# dbutils.fs.rm('/FileStore/tables/forsee.csv')

# COMMAND ----------

#Parse CQ questions with possible answers
def_file = "/dbfs{0}/RDS/Delhaize/FORESEE/Hannaford/Delivery/{1}/{2}/foreseeDeliveryQuestions-CQ-{2}.csv".format(mnt,YYYY,endDt)

items = definition.json()["CQ"]
channel = "Hannaford Delivery"

with open(def_file, "w") as file:
    csv_file = csv.writer(file)
    csv_file.writerow(["Channel","QuestionId","Question","Label","ResponseType","Type","AnswerId","Text","Value"])
    for item in items:
        questionid = item["id"]
        label = item["label"]
        qestn = item["name"]
        responsetype = item["responseType"]
        qtype = item["type"]
        for answer in item["answers"]:
            answerid = answer["id"]
            text = answer["text"]
            value = answer["value"]
            csv_file.writerow([channel,questionid,qestn,label,responsetype,qtype,answerid,text,value])

# COMMAND ----------

# Exit if there are no responses
svy_url = "https://api.foresee.com/v1/measures/8873765/data?from={0}&to={1}".format(startDt,endDt)
svy = requests.request("GET", svy_url, headers=headers)

total_svy = svy.json()["total"] if "total" in svy.json() else 0

if (total_svy==0): dbutils.notebook.exit('stop')

# COMMAND ----------

#Parse response data to CSV
import math

limit = 50

a = math.ceil(total_svy/limit)
offset = 0 if total_svy==0 else a

for i in range(0,offset):
  data_url = "https://api.foresee.com/v1/measures/8873765/data?from={0}&to={1}&offset={2}&limit={3}".format(startDt,endDt,i,limit)
  data = requests.request("GET", data_url, headers=headers)
  dfile = "/dbfs{0}/RDS/Delhaize/FORESEE/Hannaford/Delivery/{1}/{3}/foreseeDeliverySurvey-p{2}-{3}.csv".format(mnt,YYYY,i,endDt)
  parseJson(dfile)

# COMMAND ----------

# Parse latentScores to CSV
file = "/dbfs{0}/RDS/Delhaize/FORESEE/Hannaford/Delivery/{1}/{2}/foreseeDelivery-latentScores-{2}.csv".format(mnt,YYYY,endDt)

items = svy.json()["items"]
count = 0

with open(file, "w") as file:
    csv_file = csv.writer(file)
    csv_file.writerow(["SurveyId","ExperienceDate","id","name","type","score"])
    for item in items:
        surveyId = item["id"]
        experienceDate = item["experienceDate"]
        for score in item["latentScores"]:
            csv_file.writerow([surveyId,experienceDate,score['id'],score['name'],score['type'],score['score']])
        
# df = spark.read.csv('/FileStore/tables/forsee.csv', header=True)
# df = spark.read.csv('dbfs:/mnt/rs06ue2dipadl01/FIONA/RDS/Ahold/ForeSee/foreseeDelivery-latentScores-{0}.csv'.format(loadDt), header=True)
# display(df)

# COMMAND ----------

# Merge the files
dfSurvey1 = spark.read.csv("{0}/RDS/Delhaize/FORESEE/Hannaford/Delivery/{1}/{2}/foreseeDeliverySurvey-*.csv".format(mnt,YYYY,endDt),header="true",sep=",");
dfSurvey = dfSurvey1.withColumn("WeekEndDate",lit(endDt))
dfSurvey.createOrReplaceTempView("tblSurvey")

dfDefMQ1 = spark.read.csv("{0}/RDS/Delhaize/FORESEE/Hannaford/Delivery/{1}/{2}/foreseeDeliveryQuestions-MQ-{2}.csv".format(mnt,YYYY,endDt),header="true",sep=",");
dfDefMQ = dfDefMQ1.select("Channel","QuestionId","Question","Label","ResponseType","Type","AnswerId","Text","Value")
dfDefCQ = spark.read.csv("{0}/RDS/Delhaize/FORESEE/Hannaford/Delivery/{1}/{2}/foreseeDeliveryQuestions-CQ-{2}.csv".format(mnt,YYYY,endDt),header="true",sep=",");

dfDef = dfDefMQ.union(dfDefCQ)
dfDef.createOrReplaceTempView("tblDefinitions")
# display(dfDef)

resultsDF = spark.sql("select D.Channel,SurveyId,ExperienceDate,ResponseId,Name,Phrase,S.Type,S.Label,S.ResponseType, ifnull(Text, Answers) as Answer, WeekEndDate from tblSurvey S left join tblDefinitions D on S.ResponseId=D.QuestionId and S.Answers=D.Value")
resultsDF.createOrReplaceTempView("tblResults")
# display(resultsDF)

flattenDF = spark.sql("select 'Hannaford Delivery' Channel,SurveyId,ExperienceDate,ResponseId,Name,Phrase,Type,Label,ResponseType,concat_ws('|',collect_list(Answer)) as Answer, WeekEndDate from tblResults group by Channel,SurveyId,ExperienceDate,ResponseId,Name,Phrase,Type,Label,ResponseType,WeekEndDate")
# display(flattenDF)


# COMMAND ----------

import pandas
filepath = "dbfs:{0}/SDM/Delhaize/FORESEE/Hannaford/DELIVERY/weekenddate={1}/".format(mnt,endDt)
dbutils.fs.mkdirs(filepath)

flattenDF.toPandas().to_parquet("/dbfs{0}/SDM/Delhaize/FORESEE/Hannaford/DELIVERY/weekenddate={1}/foreseeDeliverySurvey.parquet".format(mnt,endDt))

# COMMAND ----------

# survey = "/mnt/{0}/FIONA/SDM/Delhaize/Foresee/Hannaford/{1}/{2}/{3}/foreseeDeliverySurvey.parquet".format(mnt,YYYY,mm,dd,loadDt)
# flattenDF.repartition(1).write.format("parquet").mode("append").save(survey)
# flattenDF.repartition(1).write.format("parquet").mode("append").save(survey)
# flattenDF.write.option("header", "true").option("sep",",").mode("overwrite").parquet(survey)

# COMMAND ----------

# dfresult = spark.read.parquet("/mnt/{0}/FIONA/SDM/Delhaize/Foresee/Hannaford/weekenddate={1}/*.parquet".format(mnt,endDt));
# dfresult.createOrReplaceTempView("tblresults")

# data = spark.sql("select ExperienceDate, count(distinct SurveyId) as surveycount from tblresults where Channel='Hannaford Pickup' group by ExperienceDate limit 1000")
# display(data)

# dfresult.toPandas().to_csv("/dbfs/mnt/{0}/FIONA/Test/foresee/ForeseeSurvey_{1}.csv".format(mnt,loadDt),mode='w',header=True,sep=",",index=False)
