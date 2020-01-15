import time
import json
import requests

members=['keroru']
start_date,end_date="2018/1/1","2020/1/1"

def get_problem_info(): # Get proble information from AtCoder Problems API
    http="https://kenkoooo.com/atcoder/resources/merged-problems.json"
    get_problem_info = requests.get(http)
    return get_problem_info

def get_prob_dif_info(): # Get problem difficulty information from AtCoder Problems API
    http="https://kenkoooo.com/atcoder/resources/problem-models.json"
    get_prob_dif_info = requests.get(http)
    return get_prob_dif_info

def get_contest_info(): # Get contest information from AtCoder Problems API
    http="https://kenkoooo.com/atcoder/resources/contests.json"
    get_contest_info = requests.get(http)
    return get_contest_info

def get_acp_info(name): # Get time-based submission information from AtCoder Problems API, [name] = atcoder user name
    http="https://kenkoooo.com/atcoder/atcoder-api/results?user="+name
    get_url_info = requests.get(http)
    return get_url_info

def ac_in_period(submissions,begin,end,t_format="%Y/%m/%d"): # Get AC count during [begin, end)
    t_b=time.strptime(begin,t_format)
    t_e=time.strptime(end,t_format)

    results={}
    points={}
    difficulties={}
    dict_result={'WA':0,'AC':1,'TLE':2,'MLE':3,'RE':4,'CE':5,"OLE":6}

    for sbm in submissions:
        t=sbm['epoch_second']
        cid=['contest_id']
        #c_info[cid]
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
                if pid in dc_difficulty.keys():
                    difficulty=max(0, dc_difficulty[pid])
                    difficulties[pid]=difficulty
        else:
            points[pid]=point
            if dict_result[res]==1:
                results[pid]=1
                if pid in dc_difficulty.keys():
                    difficulty=max(0, dc_difficulty[pid])
                    difficulties[pid]=difficulty
            else:
                results[pid]=0
    
    total_ac,total_point,total_difficulty=0,0,0
    for pid,ac_cnt in results.items():
        total_ac+=ac_cnt
    for pid,earned_point in points.items():
        if earned_point<3000:
            total_point+=earned_point
    for pid,difficulty in difficulties.items():
        total_difficulty+=difficulty
    return total_ac,total_point,total_difficulty

c_info=json.loads(get_contest_info().text)
pd_info=json.loads(get_prob_dif_info().text)

dc_difficulty={}
for p in pd_info:
    if 'difficulty' in pd_info[p].keys():
        dc_difficulty[p]=pd_info[p]['difficulty']

txts=[]
for m in members:
    txts.append(get_acp_info(m).text)

for i in range(len(members)):
    submissions=json.loads(txts[i])
    ac,points,difs=ac_in_period(submissions,start_date,end_date)

    print(members[i],": Total",ac,"ACs, ",'{:,}'.format(int(points)),"points, ",'{:,}'.format(int(difs)),"difficulties","from ",start_date,"to",end_date)
    
