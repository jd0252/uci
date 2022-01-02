from flask import Flask, render_template
import pymongo
import pandas as pd
import statistics
import datetime
app = Flask(__name__,static_folder='static/assets/')#, static_url_path='', static_folder='templates')

client = pymongo.MongoClient("mongodb+srv://jd0252:0000@cluster0.nzlef.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.scaler_data
collections=db.origion
cursor=collections.find()

collections1=db.real
cursor1=collections1.find()

TA=['feature_0','feature_1','feature_2','feature_3','feature_4']
n=20
m=5
count=1
data=[]
temp=[]
stat=[]
time=[]
real=[]
predict=[]
status=[0 for i in range(n)]
ID=[]
for i in range(m):
    data.append([])



for i in cursor:
    if(count>n):
        break
    data[0].append(i[TA[0]])
    data[1].append(i[TA[1]])
    data[2].append(i[TA[2]])
    data[3].append(i[TA[3]])
    data[4].append(i[TA[4]])
    ID.append(str(i['_id']))
    t=str(i['year'])+"-"+str(i['month'])+"-"+str(i['date'])+" "+str(i['hour'])+":"+str(i['min'])
    t=datetime.datetime.strptime(t, "%Y-%m-%d %H:%M").strftime("%Y-%m-%dT%H:%M:%S.000Z")
    time.append(t)


for j in cursor1:
    if(count>n):
        break
    real.append(j['Pass_Fail'])
    predict.append(j['predict'])
    if(j['Pass_Fail']!=j['predict']):
        status[count-1]=1


    count+=1
stat.append([round(statistics.stdev(data[0]),2),round(statistics.mean(data[0]),2)])
stat.append([round(statistics.stdev(data[1]),2),round(statistics.mean(data[1]),2)])
stat.append([round(statistics.stdev(data[2]),2),round(statistics.mean(data[2]),2)])
stat.append([round(statistics.stdev(data[3]),2),round(statistics.mean(data[3]),2)])
stat.append([round(statistics.stdev(data[4]),2),round(statistics.mean(data[4]),2)])

@app.route("/")
def index():
    
    return render_template('index.html',
                            data=data,real=real,predict=predict,status=status,ID=ID,
                            stat=stat,time=time,TA=TA)



if __name__ == "__main__":
    app.run(debug=True)
