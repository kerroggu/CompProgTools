import time
import json
import requests

members=['keroru']
start_date,end_date="2019/1/1","2020/1/1"

def get_acp_info(name): # Get time-based submission information from AtCoder Problems API, [name] = atcoder user name
    http="https://kenkoooo.com/atcoder/atcoder-api/results?user="+name
    get_url_info = requests.get(http)
    return get_url_info

def ac_in_period(submissions,begin,end,t_format="%Y/%m/%d"): # Get AC count during [begin, end)
    t_b=time.strptime(begin,t_format)
    t_e=time.strptime(end,t_format)

    results={}
    points={}
    dict_result={'WA':0,'AC':1,'TLE':2,'MLE':3,'RE':4,'CE':5,"OLE":6}

    for sbm in submissions:
        t=sbm['epoch_second']
        cid=['contest_id']
        pid=sbm['problem_id']
        point=sbm['point']
        res=sbm['result']
        lang=sbm['language']
        yymmdd,str_t=time.gmtime(t)[0:3],time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime(t))
        year,month,date=yymmdd

        if not time.mktime(t_b) <= t < time.mktime(t_e):
            continue

        if pid in results:
            points[pid]=max(points[pid],point)
            if dict_result[res]==1:
                results[pid]=1
        else:
            points[pid]=point
            if dict_result[res]==1:
                results[pid]=1
            else:
                results[pid]=0
    
    total_ac,total_point=0,0
    for pid,ac_cnt in results.items():
        total_ac+=ac_cnt
    for pid,earned_point in points.items():
        total_point+=earned_point
    return total_ac,total_point


txts=[]
for m in members:
    txts.append(get_acp_info(m).text)

for i in range(len(members)):
    submissions=json.loads(txts[i])
    ac,points=ac_in_period(submissions,start_date,end_date)

    print(members[i],":",ac,"ACs, ",'{:,}'.format(int(points)),"points","from ",start_date,"to",end_date)
