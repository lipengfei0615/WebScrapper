import requests, re, traceback
from bs4 import BeautifulSoup
import time
import pymysql



conn=pymysql.connect(host='localhost', user='root', passwd='usbw', db='swimming', charset='utf8')
cur=conn.cursor()



def getHTMLText(url,code='utf8'):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        traceback.print_exc()


# functions for Athletes
#
#
def parsePageAthletes(alist,html):
    try:
        IdList = re.findall(r'athleteId=\d{7}',html)
        NameList = re.findall(r'\"nofollow\"[>][^<]+[<]',html)
        BirthDateList = re.findall(r'\"date\"[>][12-][0-9]*',html)
        NationList = re.findall(r'td class=\"code\"[>][A-Z]{3,3}',html)

        for i in range(len(IdList)):

            aid = eval(IdList[i].split('=')[1])
            name = NameList[i].split('>')[1]
            fname = name.split(',')[0]
            lname = name.split(',')[1][1:-1]
            bdate = BirthDateList[i].split('>')[1]
            if bdate != '-':
                bdate=eval(bdate)                                 #One athlete doesn't have birth year which is indicated by '-'.
            nation = NationList[i].split('>')[1]
            alist.append([aid,fname,lname,bdate,nation])
        return alist
    except:
        traceback.print_exc()

def ScrapeAthletes():
    types=['TOP100_MEN','TOP100_WOMEN','TOP100_MEN_ALL','TOP100_WOMEN_ALL']
    start_url = 'https://www.swimrankings.net/index.php?page=athleteSelect&nationId=0&selectPage='
    totalID=set()
    total=[]
    for t in types:
        time.sleep(0.1)
        url = start_url + t
        html = getHTMLText(url)
        t=[]
        t=parsePageAthletes(t, html)
        total.append(t)
        # printList(t)
        for i in t:
            totalID.add(i[0])
    totalID=list(totalID)
    return (total,totalID)

def addAthletes():
    result=ScrapeAthletes()[0]
    for middle in result:
        for b in middle:
            name=b[1]+', '+b[2]
            birth_year=str(b[3])
            nation=b[4]
            athletes_id=b[0]
            try:
                cur.execute("INSERT INTO athletes (athletes_id,name,birth_year,nation) VALUES (%s,%s,%s,%s)", (athletes_id,name,birth_year,nation))
                cur.connection.commit()
            except:
                continue
#functions for Calendar
#
#
def parsePageCalendar(carlist,html):
    try:

        href = re.findall(r'[1]\d{8}',html)
        href=list(set(href))
        for i in href:
            start_url='https://www.swimrankings.net/index.php?page=CalendarDetail&CalendarId='
            url=start_url+i
            t=getHTMLText(url).encode(errors="ignore").decode("utf8")
            time.sleep(0.5)
            soup = BeautifulSoup(html , 'html.parser')
            mn=re.findall(r'Meet Name</td><td class=["]valueTblValue["]>[^!]+?<',t)
            mc=re.findall(r'Meet City</td><td class=["]valueTblValue["]>[^!]+?<',t)
            mt=re.findall(r'Meet Type</td><td class=["]valueTblValue["]>[^!]+?<',t)
            dfe=re.findall(r'Deadline for Entries</td><td class=["]valueTblValue["]>[^!]+?<',t)
            ti=re.findall(r'Timing</td><td class=["]valueTblValue["]>[^!]+?<',t)
            org=re.findall(r'Organizer</td><td class=["]valueTblValue["]>[^!]+?<',t)
            hc=re.findall(r'Host Club</td><td class=["]valueTblValue["]>[^!]+?</a',t)
            ad=re.findall(r'Address</td><td class=["]valueTblValue["]>[^!]+?<',t)
            ph=re.findall(r'Phone</td><td class=["]valueTblValue["]>[^!]+?<',t)
            em=re.findall(r'Email</td><td class=["]valueTblValue["]>[^!]+?</a',t)

            if len(mn)== 0:
                mn =' '
            else:
                mn=mn[0].split("<")[-2].split('>')[-1]
            if len(mc)== 0 :
                mc =' '
            else:
                mc=mc[0].split("<")[-2].split('>')[-1]
            if len(mt)== 0 :
                mt =' '
            else:
                mt=mt[0].split("<")[-2].split('>')[-1]
            if len(dfe)== 0 :
                dfe =' '
            else:
                dfe=dfe[0].split("<")[-2].split('>')[-1]
            if len(ti)== 0 :
                ti =' '
            else:
                ti=ti[0].split("<")[-2].split('>')[-1]
            if len(org)== 0 :
                org =' '
            else:
                org=org[0].split("<")[-2].split('>')[-1]
            if len(hc)== 0 :
                hc =' '
            else:
                hc=hc[0].split("<")[-2].split('>')[-1]
            if len(ad)== 0:
                ad =' '
            else:
                ad=ad[0].split("<")[-2].split('>')[-1]
            if len(ph)== 0 :
                ph =' '
            else:
                ph=ph[0].split("<")[-2].split('>')[-1]
            if len(em)== 0 :
                em =' '
            else:
                em=em[0].split("<")[-2].split('>')[-1]
            print(hc)
            print(em)
            carlist.append([int(i),mn,mc.replace('&nbsp',' '),mt,dfe,ti,org,hc,ad,ph,em])
        return carlist

    except:
        traceback.print_exc()

def ScrapeCalendar():
    url="https://www.swimrankings.net/index.php?page=CalendarList&nationId=0&SubPage=LIST"
    html=getHTMLText(url)
    CalendarList=[]
    CalendarList=parsePageCalendar(CalendarList,html)
    return CalendarList

def addCalendar():
    result=ScrapeCalendar()
    for i in result:
        info_id=i[0]
        meet_name=i[1]
        meet_city=i[2]
        entries_deadline=i[4]
        timing=i[5]
        organizer=i[6]
        host_club=i[7]
        address=i[8]
        email=i[-1]

        try:
            cur.execute("INSERT INTO matchinfo (info_id,meet_name,meet_city,entries_deadline,timing,organizer,host_club,address,email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (info_id,meet_name,meet_city,entries_deadline,timing,organizer,host_club,address,email))
            cur.connection.commit()
        except:
            traceback.print_exc()


#functions for Meets
#
#
def parsePageMeets1(mlist,html):
    try:
        soup = BeautifulSoup(html , 'html.parser')
        date = soup.find_all('td',attrs={'class':'date'})
        city = soup.find_all('td',attrs={'class':'city'})
        name = soup.find_all('a',attrs={'rel':'nofollow'})


        for d in range(3):
            dt=date[d].text.encode(errors="ignore").decode("utf8")
            ct=city[d].text.encode(errors="ignore").decode("utf8")
            id=int(name[d].get('href').split("Id=")[1])
            if name[d].text.startswith('X'):
                meetname=ct[:-6]+' '+name[d].text.split(" ")[1]+" "+name[d].text.split(" ")[2]
            else:
                meetname=name[d].text
            mlist.append([id,meetname,dt,ct])
        return mlist
    except:
        traceback.print_exc()

def parsePageMeets2(mdict,mname,html,mnumber):
    try:
        soup = BeautifulSoup(html , 'html.parser')
        club = soup.find_all('a',attrs={'rel':'nofollow'},target=False)
        medal = soup.find_all('td',attrs={'class':'rankingPlace'})
        nation = soup.find_all('td',attrs={'class':'code'})

        meetdetail=[]

        for c in range(len(club)):
            gold=medal[4*c].text
            silver=medal[4*c+1].text
            bronze=medal[4*c+2].text
            total=medal[4*c+3].text
            meetdetail.append([club[c].text,nation[c].text,gold,silver,bronze,total,mnumber])
        mdict[mname]=meetdetail
        return mdict
    except:
        traceback.print_exc()

def addMeets1():  #meets info
    types=[1,2,3,7,8]

    for i in types:
        url = 'https://www.swimrankings.net/index.php?page=meetSelect&selectPage=BYTYPE&nationId=0&meetType='+str(i)
        html=getHTMLText(url)
        mlist=[]
        mlist=parsePageMeets1(mlist,html)
        for i in mlist:
            course='50m'
            date=i[2]
            city=i[3]
            meet_name=i[1]
            if i[1].split(' ')[1].endswith('th'):
                meet_type=i[1].split("th ")[1]
            elif i[1].endswith(r'\d'):
                meet_type=i[1].split(" ")[1]+" "+i[1].split(" ")[2]
            elif i[1].startswith('LEN'):
                meet_type=i[1][5:]
            elif i[1].startswith('European'):
                meet_type=i[1]
            else:
                meet_type=i[1].split(" ")[1]+" "+i[1].split(" ")[2]
            cur.execute("INSERT INTO meet (course,date,city,meet_name,meet_type) VALUES (%s,%s,%s,%s,%s)", (course,date,city,meet_name,meet_type))
            cur.connection.commit()

def addMeets2():  #participating nations
    MeetsList=ScrapeMeets()
    for l in MeetsList:
        for k,v in MeetsDict.items():
            count=0
            for i in v:
                count=count+1
                nation_id=count
                club=i[0]
                nation=i[1]
                cur.execute("SELECT meets_id FROM meet WHERE meet_name=%s",k)
                meet_id=int(cur.fetchone()[0])

                if i[2] == '-':
                    gold=0
                else:
                    gold=int(i[2])
                if i[3] == '-':
                    silver=0
                else:
                    silver=int(i[3])
                if i[4] == '-':
                    bronze=0
                else:
                    bronze=int(i[4])
                if i[5] == '-':
                    total=0
                else:
                    total=int(i[5])

                try:
                    cur.execute("INSERT INTO participating_nation (club,nation,gold,silver,bronze,total,meet_id) VALUES (%s,%s,%s,%s,%s,%s,%s)", (club,nation,gold,silver,bronze,total,meet_id))
                    cur.connection.commit()
                except:
                    traceback.print_exc()

def ScrapeMeets():
    types=[1,2,3,7,8]
    MeetsDict={}
    MeetsList=[]
    for i in types:
        url = 'https://www.swimrankings.net/index.php?page=meetSelect&selectPage=BYTYPE&nationId=0&meetType='+str(i)
        html=getHTMLText(url)
        mlist=[]
        mlist=parsePageMeets1(mlist,html)
        for m in mlist:
            meetname=m[1]
            meetnumber=m[0]
            start_url="https://www.swimrankings.net/index.php?page=meetDetail&meetId="
            url=start_url + str(meetnumber)
            html=getHTMLText(url)
            MeetsDict=parsePageMeets2(MeetsDict,meetname,html,meetnumber)
            MeetsList.append(MeetsDict)
            time.sleep(0.1)
    return MeetsList

def parsePagePersonalBests(id,alist,html):
    try:
        soup = BeautifulSoup(html , 'html.parser')
        event = soup.find_all('td',attrs={'class':'event'})
        course = soup.find_all('td',attrs={'class':'course'})
        time = soup.find_all('td',attrs={'class':'time'})
        pts = soup.find_all('td',attrs={'class':'code'})
        date = soup.find_all('td',attrs={'class':'date'})
        city = soup.find_all('td',attrs={'class':'city'})
        meet = soup.find_all('td',attrs={'class':'name'})
        for i in range(len(event)):
            ev=event[i].text
            cr=course[i].text
            tm=time[i].text
            pt=pts[i].text
            dt=date[i].text.encode(errors="ignore").decode("utf8")
            ct=city[i].text.encode(errors="ignore").decode("utf8")
            mt=meet[i].text.split(" ..")[0]
            alist.append([id,i+1,ev,tm,pt,dt,ct,mt,cr])
        print(alist)
        return alist
    except:
        traceback.print_exc()


def ScrapePersonalBests():
    #totalID is the result from Athletes.
    result=ScrapeAthletes()[1]
    PersonalBestsDict={}
    start_url = 'https://www.swimrankings.net/index.php?page=athleteDetail&athleteId='
    timer=5
    while timer<301:

        for i in range(timer-5,timer):
            time.sleep(0.5)
            t=result[i]
            url = start_url + str(t)
            html = getHTMLText(url)
            l=[]
            PersonalBestsDict[t]=parsePagePersonalBests(t,l,html)
        time.sleep(5)
        timer=timer+5
    return PersonalBestsDict


def addPersonalBests():
    result=ScrapePersonalBests()
    for key,value in result.items():
        for i in value:
            event=i[2]
            course=i[-1]
            time=i[3]
            points=i[4]
            date=i[5]
            city=i[6]
            meet=i[7]

            try:
                cur.execute("SELECT athletes_id FROM athletes WHERE athletes_id=%s",int(i[0]))
                athletes_id=cur.fetchone()[0]

                cur.execute("INSERT INTO personalbest (event,course,time,points,date,city,meet,athletes_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (event,course,time,points,date,city,meet,athletes_id))
                cur.connection.commit()
            except:
                pass

def parsePageRankings(rdict,gender,year,course,html):
    try:
        soup = BeautifulSoup(html , 'html.parser')
        style = soup.find_all('a',attrs={'title':'Full ranking'})
        name = soup.find_all('td',attrs={'class':'fullname'})
        rname = soup.find_all('a',attrs={'style':"color: gray;"})
        re1 = re.compile(r'\d{4}')
        yob = soup.find_all('td',attrs={'class':'rankingPlace'},text=re1)
        re2 = re.compile(r'[A-Z]{3}')
        nation = soup.find_all('td',attrs={'class':'rankingPlace'},text=re2)
        time = soup.find_all('td',attrs={'class':'time'})
        pts = soup.find_all('td',attrs={'class':'code'})
        date = soup.find_all('td',attrs={'class':'date'})
        city = soup.find_all('td',attrs={'class':'city'})

        rankings=[]
        relayname=[]
        for i in range(len(rname)):
            if i%4==0:
                r=rname[i].text+', '+rname[i+1].text+', '+rname[i+2].text+', '+rname[i+3].text
                r=r.encode(errors="ignore").decode("utf8")
                relayname.append(r)

        for i in range(len(style)):
           if i == len(style)-1:
              pass
           else:
              if style[i].text != style[i+1].text:
                 dt=date[i].text.encode(errors="ignore").decode("utf8")
                 ct=city[i].text.encode(errors="ignore").decode("utf8")
                 if style[i].text[2] != "x":
                    rankings.append([style[i].text,name[i].text,yob[i].text,nation[i].text,time[i].text,pts[i].text,dt,ct])
                 else:
                    rankings.append([style[i].text,relayname[i-len(name)],'-','-',time[i].text,pts[i].text,dt,ct])
        choice=gender+' '+str(year)+' '+course
        rdict[choice]=rankings
        return rdict
    except:
        traceback.print_exc()

def addRankings():
    result=ScrapeRankings()
    for i in result:
        for k,v in i.items():
            if k.split(' ')[0] == '1':
                gender='Men'
            else:
                gender='Women'

            ranking_year=k.split(' ')[1]

            if k.split(' ')[2] == 'LCM':
                course='Long Course(50m)'
            else:
                course='Short Course(25m)'
            for t in v:
                individuals=t[0]
                name=t[1]
                birth_year=t[2]
                nation=t[3]
                time=t[4]
                points=t[5]
                date=t[6]
                city=t[7]
                cur.execute("INSERT INTO ranking (course,gender,ranking_year,individuals,name,birth_year,nation,time,points,date,city) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (course,gender,ranking_year,individuals,name,birth_year,nation,time,points,date,city))
                cur.connection.commit()

def ScrapeRankings():
    gender=["1","2"]
    course=["LCM","SCM",]
    year=[ x+2005 for x in range(12)]
    start_url = 'https://www.swimrankings.net/index.php?page=rankingDetail&clubId=1&agegroup=X_X&stroke=0'
    RankingsList=[]
    for g in gender:
        for c in course:
            for y in year:
                url = start_url + '&gender=' + g + '&season=' + str(y) + '&course=' + c
                time.sleep(0.5)
                html=getHTMLText(url)
                rdict={}
                parsePageRankings(rdict,g,y,c,html)
                RankingsList.append(rdict)
    return RankingsList


def parseRecords1(rdict,html):
    try:
        soup = BeautifulSoup(html,'html.parser')
        content = soup.find('div',attrs={'id':'content'})
        # re1=re.compile(r'500[01]\d$')
        re1=re.compile(r'\d{5}$')
        record = content.find_all("a",attrs={'href':re1})

        for r in range(len(record)):
            # if int(record[r].attrs['href'].split('=')[2])<50017:
            #     rtext = record[r].text
            #     rnum = record[r].attrs['href'].split('=')[2]
            #     rdict[rnum] = rtext
            rtext = record[r].text
            rnum = record[r].attrs['href'].split('=')[2]
            rdict[rnum] = rtext
        return rdict
    except:
        traceback.print_exc()

def parseRecords2(rname,rdict2,html):
    try:
        content1 = re.findall(r'<th colspan=\"7\" class=\"name\">[^@]*?<tr height=\"10\"><td></td></tr><tr>',html)
        content2 = re.findall(r'<th colspan=\"7\" class=\"name\">Relays [-CN][^@]*?</script></td></tr></table></div>',html)
        if content2 != []:
            content1.append(content2[0])
        number = [ str(x) for x in range(10)]
        re1=re.compile(r"^[^R]")
        lt = []
        an = []
        yb = []
        cb = []
        tm = []
        dt = []
        ct = []
        count = 0
        records=[]
        for con in range(len(content1)):
            soup = BeautifulSoup(content1[con],'html.parser')
            content = soup.find('th',attrs={'colspan':'7',"class":"name"})
            rcontent = soup.find('th',attrs={'colspan':'7',"class":"name"},text=re1)
            if rcontent != None:
                count=count+len(rcontent)

            length = soup.find_all('a',attrs={'title':'Show record history'})
            aname = soup.find_all('td',attrs={'class':'fullname'})
            relayname = soup.find_all('td',attrs={'class':'relayNames'})
            yob = soup.find_all('td',attrs={'class':'rankingPlace'})
            club = soup.find_all('td',attrs={'class':'name'},colspan=False)
            time = soup.find_all('a',attrs={'class':'time'})
            date = re.findall(r'<td class=\"date\">[^@]*?</td><td class=\"city\">',content1[con])
            city = soup.find_all('td',attrs={'class':'city'})


            for i in range(len(date)):
                date[i]=date[i].split("class=\"date\">")[1]
                date[i]=date[i].split("</td>")[0]
                if date[i].startswith('<'):
                    date[i]=date[i].split('png\">')[1]
                dt.append((" ").join(date[i].split('&nbsp;')))


            for i in range(len(length)):

                lt.append(length[i].text)
                tm.append(time[i].text)
                ct.append(city[i].text.encode(errors="ignore").decode("utf8"))
                if con >= count:
                    cb.append(club[2*i].text.encode(errors="ignore").decode("utf8"))
                    yb.append('-')
                    an.append(relayname[con-count].text.encode(errors="ignore").decode("utf8"))
                else:
                    cb.append(club[i].text.encode(errors="ignore").decode("utf8"))
                    yb.append(yob[i].text)
                    an.append(aname[i].text)

            for i in range(len(cb)):
                records.append([content.text,lt[i],an[i],yb[i],cb[i],tm[i],ct[i],dt[i]])
            lt = []
            an = []
            yb = []
            cb = []
            tm = []
            dt = []
            ct = []
        print(records)
        rdict2[rname]=records
        return rdict2
    except:
        pass

def addRecords1():
    url = 'https://www.swimrankings.net/index.php?page=recordSelect'
    html = getHTMLText(url)
    rdict={}
    rdict=parseRecords1(rdict,html)
    for v in rdict.values():
        cur.execute("INSERT INTO recordlist (recordlist) VALUES (%s)", (v))
        cur.connection.commit()

def addRecords2():
    try:
        result=ScrapeRecords()
        for d in result:
            if d != None:
                for k,v in d.items():
                    for i in v:
                        stroke=i[0]
                        name=i[2]
                        birth_year=i[3]
                        club=i[4]
                        time=i[5]
                        date=i[7]
                        city=i[6]
                        cur.execute("SELECT id FROM recordlist WHERE recordlist =%s",k)
                        recordlist_id=int(cur.fetchone()[0])

                        cur.execute("INSERT INTO records (stroke,name,birth_year,club,time,date,city,recordlist_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (stroke,name,birth_year,club,time,date,city,recordlist_id))
                        cur.connection.commit()
    except:
        traceback.print_exc()

def ScrapeRecords():

    url = 'https://www.swimrankings.net/index.php?page=recordSelect'
    html = getHTMLText(url)
    rdict={}
    rdict=parseRecords1(rdict,html)
    RecordsList=[]
    print(rdict)
    for i in rdict.keys():
        time.sleep(0.5)
        new_url = 'https://www.swimrankings.net/index.php?page=recordDetail&recordListId='
        url = new_url + i
        html = getHTMLText(url)
        RecordsDict={}
        RecordsDict=(parseRecords2(rdict[i],RecordsDict,html))
        RecordsList.append(RecordsDict)
    return RecordsList


# addAthletes()
addCalendar()
# addMeets1()
# try:
#     addPersonalBests()
# except:
#     traceback.print_exc()
# addRankings()
# addRecords1()
# try:
#     addRecords2()
# except:
#     traceback.print_exc()

# ScrapeCalendar()



cur.close()
conn.close()


# print(ScrapeAthletes())
# print(ScrapeCalendar())
# print(ScrapeMeets())
# print(ScrapePersonalBests())
# print(ScrapeRankings())
# print(ScrapeRecords())
