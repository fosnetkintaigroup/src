from django.http import HttpResponse
from django.template import RequestContext
from app_folder.models import syain_info
from app_folder.models import project_work
from app_folder.models import torihikisaki_list
from app_folder.models import trans_info
from app_folder.models import kintai_touroku_info
from app_folder.models import project_uchiwake
from django.db.models import Avg, Max, Min, Sum
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .forms import CustomUserCreateForm
from django.views import generic
#from xoxzo.cloudpy import XoxzoClient
import datetime
import calendar
import locale
import os
import secrets

# Create your views here.
import webbrowser



def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render( None, request))
    

    
def kintai(request):
    template = loader.get_template('registration/kintai.html')
    
    return HttpResponse(template.render( None, request))
    
def login(request):
    template = loader.get_template('registration/login.html')
    
    
    return HttpResponse(template.render( None, request))
    
def password(request):
    template = loader.get_template('registration/password_change.html')
    print('pass')
    return HttpResponse(template.render( None, request))
    
def passwordchange(request):
    template = loader.get_template('registration/password_change.html')
    
    id = request.POST.get('UserId','')
    passw =request.POST.get('Password','')
    passn =request.POST.get('APassword','')
    passk =request.POST.get('KPassword','')
    list =  syain_info.objects.all()
    context = {}
    if(len(passn) < 8):
       context.update({
              'shorterror': '新パスワードは8文字以上で入力してください',
       })
       
    if (passn != passk):
       context.update({
             'kakuninerror': '新パスワード,確認パスワードが一致しません',
         })
    if (passn == passw):
       context.update({
             'sameerror': '新パスワードと旧パスワードが同じです',
         })
    sameflg = False
    for i in range(len(list)):
      syaincd1=list[i].syaincd
      password1=list[i].password
      if (id != syaincd1 or passw != password1):
        continue
        
      sameflg = True
      
      if(passn == passk and passn != passw and len(passn) >= 8):
           p =  syain_info.objects.filter(syaincd = syaincd1)
           print(p)
           p.update(password = passn)
           return render(request, 'registration/login.html')
           
    if not sameflg:
       context.update({
              'matcherror': 'ユーザーidまたはパスワードが違います',
       })
    return render(request, 'registration/password_change.html', context)
    
def koutuhilist(request):
    template = loader.get_template('registration/koutuhi_itiran.html')
    id = request.session.get('User','')
    data = trans_info.objects.filter(syaincd = id)
    print(data)
    my_dict2 = {
        'data':  data
    }
    return render(request, 'registration/koutuhi_itiran.html', my_dict2)
    
def koutuhi(request):
    template = loader.get_template('registration/koutuhi.html')
    listtori =  torihikisaki_list.objects.all()
    request.session['User'] = request.POST['User']
    request.session['Pass'] = request.POST['Pass']
    id = request.POST['User']
    passw = request.POST['Pass']
    
    list =  syain_info.objects.all()
    secret_key = secrets.randbelow(10000)
    message = "こちらはXOXZOです。あなたの暗証番号は %04d です" % secret_key

    # APIを呼び出すための秘密鍵は、環境変数に保存されているものとします
    # SIDとTOKENは https://www.xoxzo.com/ からサインアップして入手してください
    sid = os.getenv('XOXZO_API_SID')
    auth_token = os.getenv('XOXZO_API_AUTH_TOKEN')

    # SMSの送信
    #xc = XoxzoClient(sid=sid, auth_token=auth_token)
    #result = xc.send_sms(message=message, recipient="+818050213916", sender="XOXZO")

    for i in range(len(list)):
      syaincd=list[i].syaincd
      password=list[i].password
      print(list[i].syaincd)
      print(list[i].password)
      if (id == syaincd and passw == password):
         context = {
                   'cus': listtori,
                   'syaincd':id,
              }
         url = 'http://127.0.0.1:8000/accounts/kintai/'
         webbrowser.open(url,2)
         return render(request, 'registration/koutuhi.html', context)
    context = {
              'error': 'ユーザーIDまたはパスワードが違います',
        }
    return render(request, 'registration/login.html', context)
    
def koutuhisubmit(request):
    template = loader.get_template('registration/koutuhi.html')
    list =  torihikisaki_list.objects.all()
    ida = request.session.get('User','')
    name = syain_info.objects.get(syaincd=ida).syainname
    torihiki = request.POST.get('torihiki', '')
    print(name)
    print(torihiki)
    if request.method == 'POST':
      tourokuno = request.POST.get('tourokuno', '')
      kbn = request.POST['tourokukbn']
      date = datetime.date.today()
      
      
      startdatelist = []
      enddatelist = []
      homonlist = []
      kamokulist = []
      syudanlist = []
      transportlist = []
      seikyulist = []
      count = 0
      seisan = request.POST['seisan']
      
      
      for i in range(len(request.POST.getlist('homonlist', None))):
         start = request.POST.getlist('startdatelist', None)[i]
         end = request.POST.getlist('enddatelist', None)[i]
         startstr = start[:4] + '-' + start[4:6] + '-' + start[6:]
         endstr = end[:4] + '-' + end[4:6] + '-' + end[6:]
         homon = request.POST.getlist('homonlist', None)[i]
         kamoku = request.POST.getlist('kamokulist', None)[i]
         syudan = request.POST.getlist('syudanlist', None)[i]
         transport = request.POST.getlist('transportlist', None)[i]
         seikyu = request.POST.getlist('seikyulist', None)[i]
         print(range(len(request.POST.getlist('homonlist', None))))
         print(i)
         startdatelist.append(startstr)
         enddatelist.append(endstr)
         homonlist.append(homon)
         kamokulist.append(kamoku)
         syudanlist.append(syudan)
         transportlist.append(transport)
         seikyulist.append(seikyu)
         print(name)
         print(startdatelist)
         print(enddatelist)
         print(homonlist)
         print(kamokulist)
         print(syudanlist)
         print(transportlist)
         print(seikyulist)
         tourokuid = '10' + str(trans_info.objects.count())

         
         if (kbn == '削除'):
            print('delete')
            b = trans_info.objects.filter(tourokuno = str(tourokuno))
            b.delete()
         if (kbn == '修正'):
            print('update')
            b = trans_info.objects.filter(tourokuno = str(tourokuno))
            b.update(tourokukbn = kbn,tourokudate = date,homon = homonlist[i],tourokuno = tourokuid, startdate = startdatelist[i], enddate = startdatelist[i],kamoku = kamokulist[i], syudan = syudanlist[i],transport = transportlist[i], k_seikyu = seikyulist[0], seisan_kbn = seisan)
         if (kbn == '登録'):
            print('set')
            b = trans_info(syaincd = ida,syainname = name,tourokukbn = kbn,customname = torihiki, tourokudate = date,homon = homonlist[i],tourokuno = tourokuid, startdate = startdatelist[i], enddate = startdatelist[i],kamoku = kamokulist[i], syudan = syudanlist[i],transport = transportlist[i], k_seikyu = seikyulist[0], seisan_kbn = seisan)
            b.save()
    cus = {
               'cus': list,
               'message': '処理が完了しました',
          }
    return render(request, 'registration/koutuhi.html', cus)
def appearrance(request):
    template = loader.get_template('registration/syukketsusentaku.html')
    return HttpResponse(template.render( None, request))


# 一覧出力画面(年月選択前)
def output(request):
    template = loader.get_template('registration/output_ichiran.html')
    
    return HttpResponse(template.render( None, request))

# 一覧出力画面(年月選択後)
def output2(request):
    
    datelist = []
    weeklist = []
    monthyear =request.POST['monthselect']
    year = monthyear[:4]
    month = monthyear[5:7]
    monthz = monthyear[5:6]
    ida = request.session.get('User','')

    # 選択月の0埋めを無効化
    month_range = calendar.monthrange(int(year), int(month))
 
    listf = kintai_touroku_info.objects.filter(ymd__month = month,syaincd = ida).order_by('ymd')
    listmmm = []
    listweek = []
    
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    # 日数分ループ
    for i in range(1,month_range[1] + 1):
       listmmm.append(i)
       date = datetime.date(int(year), int(month),i)
       print(date.strftime('%a'))
       listweek.append(i)
    
    
    # DB格納日数分ループ
    for i in range(len(listf)):
       mmmm = listf[i].ymd.day
       listmmm[mmmm - 1] = listf[i] # DBのデータ格納
       

    # DB未格納箇所を日付型に変換
    for i in range(1,month_range[1] + 1):
       if  i in listmmm:
            listmmm[i - 1] = str(year) + str(month) + str(format(i, '02'))
            listmmm[i - 1] = datetime.datetime.strptime(listmmm[i - 1], '%Y%m%d')

    # 休暇理由、届出種類を数値から日本語に変換
    for i in range(len(listf)):
           kanmaflg = False
           if (listf[i].holidayriyu  == "0"):
              listf[i].holidayriyu = str(listf[i].holidayriyu)
              listf[i].holidayriyu = ""
              
              
           if (listf[i].todoke_tikoku  == 0):
              listf[i].todoke_tikoku = str(listf[i].todoke_tikoku)
              listf[i].todoke_tikoku = ""
              
           if (listf[i].todoke_soutai  == 0):
              listf[i].todoke_soutai = str(listf[i].todoke_soutai)
              listf[i].todoke_soutai = ""
              
           if (listf[i].todoke_midnight  == 0):
              listf[i].todoke_midnight = str(listf[i].todoke_midnight)
              listf[i].todoke_midnight = ""
              
           if (listf[i].todoke_hayade  == 0):
              listf[i].todoke_hayade = str(listf[i].todoke_hayade)
              listf[i].todoke_hayade = ""
              
           if (listf[i].todoke_irregular  == 0):
              listf[i].todoke_irregular = str(listf[i].todoke_irregular)
              listf[i].todoke_irregular = ""
              
           if (listf[i].todoke_holiwork  == 0):
              listf[i].todoke_holiwork = str(listf[i].todoke_holiwork)
              listf[i].todoke_holiwork = ""
              
           if (listf[i].todoke_tikoku  == 1):
              listf[i].todoke_tikoku = str(listf[i].todoke_tikoku)
              listf[i].todoke_tikoku = "遅刻"
              kanmaflg = True
           print(kanmaflg)
           if (listf[i].todoke_soutai  == 1):
              listf[i].todoke_soutai = str(listf[i].todoke_soutai)
              if kanmaflg:
                listf[i].todoke_soutai = ",早退"
              else:
                listf[i].todoke_soutai = "早退"
              kanmaflg = True
              
           if (listf[i].todoke_midnight  == 1):
              listf[i].todoke_midnight = str(listf[i].todoke_midnight)
              if kanmaflg:
                listf[i].todoke_midnight = ",深夜"
              else:
                listf[i].todoke_midnight = "深夜"
              kanmaflg = True
              
           if (listf[i].todoke_hayade  == 1):
              listf[i].todoke_hayade = str(listf[i].todoke_hayade)
              if kanmaflg:
                listf[i].todoke_hayade = ",早出"
              else:
                listf[i].todoke_hayade = "早出"
              kanmaflg = True
              
           if (listf[i].todoke_irregular  == 1):
              listf[i].todoke_irregular = str(listf[i].todoke_irregular)
              if kanmaflg:
                listf[i].todoke_irregular = ",変則出勤"
              else:
                listf[i].todoke_irregular = "変則出勤"
              kanmaflg = True
              
           if (listf[i].todoke_holiwork  == 1):
              listf[i].todoke_holiwork = str(listf[i].todoke_holiwork)
              if kanmaflg:
                listf[i].todoke_holiwork = ",休日出勤"
              else:
                listf[i].todoke_holiwork = "休日出勤"

    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    sumwork = float(0.0);
    overwork = float(0.0);
    resttime = float(0.0);
    
    for l in listf:
        sumwork = sumwork + float(l.worktime)
        overwork = overwork + float(l.overtime)
        resttime = resttime + float(l.resttime)
    
    sumwork = round(sumwork,2)
    overwork = round(overwork,2)
    resttime = round(resttime,2)
    context = {
         'monthselect' : monthyear,
         'listaaaa': listmmm,
         'sumwork': sumwork,
         'overwork': overwork,
         'resttime': resttime,
    }
    return render(request, 'registration/output_ichiran.html', context)
    
    
#ログイン画面→勤怠入力画面
def kintailogin(request):
    template = loader.get_template('registration/kintai.html')
    id = request.session.get('User','')
    passw =request.session.get('Pass','')
   
    list =  syain_info.objects.all()
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    print(passw)
    print(id)
    for i in range(len(list)):
      syaincd=list[i].syaincd
      password=list[i].password
      print(list[i].syaincd)
      print(list[i].password)
      if (id == syaincd and passw == password):
         context = {
                   'syaincd':id,
              }
         return render(request, 'registration/kintai.html', context)
    context = {
              'error': 'ユーザーIDまたはパスワードが違います',
        }
    return render(request, 'registration/login.html', context)



def project(request):
    template = loader.get_template('registration/projecttouroku.html')
    list =  project_work.objects.all().distinct('projectname')
    
    print("absproject "   + request.POST.get('absproject', ''))
    request.session['abs'] = request.POST.get('absproject', '')
    request.session['chikoku'] = request.POST.get('chikokuproject', '')
    request.session['hayade'] = request.POST.get('hayadeproject', '')
    request.session['soutai'] = request.POST.get('soutaiproject', '')
    request.session['hensoku'] = request.POST.get('hensokuproject', '')
    request.session['midnight'] = request.POST.get('midnightproject', '')
    request.session['holiday'] = request.POST.get('holidayproject', '')
    request.session['holidaykbn'] = request.POST.get('holidaykbnproject', '')
    request.session['riyu'] = request.POST.get('riyuproject', '')
    print(request.session.get('chikoku',''))
    request.session['starttime'] = request.POST.get('starttime', '')
    request.session['endtime'] = request.POST.get('endtime', '')
    request.session['overtime'] = request.POST.get('overtime', '')
    cont = {
        'pro': list,
    }
    return render(request, 'registration/projecttouroku.html', context=cont)
    
# 出欠選択画面
def kintaiabs(request):
    template = loader.get_template('registration/kintai.html')
    request.session['Absentkbn'] = request.POST['Absentkbn']
    abskbn = ""
        
    kbn = request.POST.get('holidaykbn', '')
    abs = request.POST.get('Absentkbn', '')
    if (abs == '0'):
        abskbn = "出勤"
    if (abs == '1'):
        abskbn = "欠勤"
        
    context = {}
    if(abs == ''):
        context.update({
                  'riyuerror': '出欠区分を選択してください',
           })
        return render(request, 'registration/syukketsusentaku.html', context)
        

    riyu = request.POST.get('riyu', '')
    
    chikoku = request.POST['Todokede0']
    hayade  = request.POST['Todokede1']
    soutai  = request.POST['Todokede2']
    hensoku = request.POST['Todokede3']
    midnight = request.POST['Todokede4']
    holiday = request.POST['Todokede5']
    

    value1 = project_work.objects.filter(projectname=request.session.get('touroku1', '')).distinct('kouteiname')
    value2 = project_work.objects.filter(projectname=request.session.get('touroku2', '')).distinct('kouteiname')
    value3 = project_work.objects.filter(projectname=request.session.get('touroku3', '')).distinct('kouteiname')
    if(abs == '1'  and (kbn == '' or riyu == '')):
       if(kbn == ''):
           context.update({
                  'holierror': '休暇区分を選択してください',
           })
       if(riyu == ''):
           context.update({
                  'riyuerror': '休暇理由を選択してください',
           })
       return render(request, 'registration/syukketsusentaku.html', context)
    kanmaflg = False
    
    if(chikoku != ''):
        kanmaflg = True
    if(hayade != ''):
        if kanmaflg:
            hayade = ',早出有'
        else:
            hayade = '早出有'        
    kanmaflg = True
    
    if(soutai != ''):
        if kanmaflg:
            soutai = ',早退'
        else:
            soutai = '早退'        
    kanmaflg = True
    
    if(hensoku != ''):
        if kanmaflg:
            hensoku = ',変則勤務'
        else:
            hensoku = '変則勤務'        
    kanmaflg = True
    
    if(midnight!= ''):
        if kanmaflg:
            midnight= ',深夜有'
        else:
            midnight= '深夜有'        
    kanmaflg = True
    
    if(holiday!= ''):
        if kanmaflg:
            holiday= ',休日出勤'
        else:
            holiday= '休日出勤'        
    kanmaflg = True

    context = {
                'ymd': request.session.get('dateselect', ''),
                'starttime': request.session.get('starttime', ''),
                'endtime': request.session.get('endtime', ''),
                'overtime': request.session.get('overtime', ''),
                'projectname1': request.session.get('touroku1', ''),
                'projectname2': request.session.get('touroku2', ''),
                'projectname3': request.session.get('touroku3', ''),
                'koutei1': value1,
                'koutei2': value2,
                'koutei3': value3,
                'abs'    : abskbn,
                'chikoku' : chikoku,
                'hayade'  : hayade,
                'soutai'  : soutai,
                'hensoku' : hensoku,
                'midnight': midnight,
                'holiday' : holiday,
          }
    return render(request, 'registration/kintai.html', context)

      
def kintaiproject(request):
    template = loader.get_template('registration/kintai.html')
    dateselect = request.session.get('dateselect', '')
    abs = request.session.get('abs', '')
    hol = request.session.get('holidaykbn','')
    riyu = request.session.get('riyu','')
    todo0 = request.session.get('chikoku','')
    todo1 = request.session.get('hayade','')
    todo2 = request.session.get('soutai','')
    todo3 = request.session.get('hensoku','')
    todo4 = request.session.get('midnight','')
    todo5 = request.session.get('holiday','')
     
    print("abs" + abs)
    value = project_work.objects.all().distinct('workname')
    value1 = project_work.objects.filter(projectname=request.POST['touroku1']).distinct('kouteiname')
    value2 = project_work.objects.filter(projectname=request.POST['touroku2']).distinct('kouteiname')
    value3 = project_work.objects.filter(projectname=request.POST['touroku3']).distinct('kouteiname')
    value4 = project_work.objects.filter(projectname=request.POST['touroku4']).distinct('kouteiname')  
    
    touroku1 = request.POST['touroku1']
    touroku2 = request.POST['touroku2']
    touroku3 = request.POST['touroku3']
    touroku4 = request.POST['touroku4']

    request.session['touroku1'] = request.POST['touroku1']
    request.session['touroku2'] = request.POST['touroku2']
    request.session['touroku3'] = request.POST['touroku3']
    request.session['touroku4'] = request.POST['touroku4']
    if request.method == 'POST':
      context = {
                'ymd': dateselect,
                'starttime': request.session.get('starttime', ''),
                'endtime': request.session.get('endtime', ''),
                'overtime': request.session.get('overtime', ''),
                'projectname1': touroku1,
                'projectname2': touroku2,
                'projectname3': touroku3,
                'projectname4': touroku4,
                'koutei1': value1,
                'koutei2': value2,
                'koutei3': value3,
                'koutei4': value4,
                'abs': abs,
                'chikoku' : todo0,
                'hayade'  : todo1,
                'soutai'  : todo2,
                'hensoku' : todo3,
                'midnight': todo4,
                'holiday' : todo5,
                'holidaykbn': hol,
                'riyu' : riyu,  
          }
      return render(request, 'registration/kintai.html', context)
    return HttpResponse(template.render( None, request))



def kintaiwork(request):
    template = loader.get_template('registration/kintai.html')
    t1 = request.session.get('touroku1','')
    #t1 = request.POST['touroku1']
    #t2 = request.session.get('touroku2','')
    t222 = request.session.get('touroku13','')
    k1 = request.session.get('kouteiname1','')
    koutei = request.POST.get('kouteiname1', '')
    print("t1"+  request.POST['kouteiname1']  + " aa " + t1)
    #value = ('kouteiname','workname')
    value1 = project_work.objects.filter(projectname=t1).distinct('kouteiname')
    value22 = project_work.objects.filter(projectname=t1,kouteiname=koutei)
    #value = project_work.objects.all()
    #value1 = project_work.objects.filter(projectname=t1).distinct('kouteiname')
    #value2 = project_work.objects.filter(projectname=t2).distinct('kouteiname')
    context = {
                'projectname1': t1,
    #            'projectname2': t2,
                'koutei1': value1,
    #            'koutei2': value2,
                'gyomu1': value22,
                #'gyomu2': value,
         }
    #return render(request, 'registration/kintai.html', context)
    
#勤怠登録押下、工程選択時    
def kintaitouroku(request):
    template = loader.get_template('registration/kintai.html')
    btt = request.POST.get('btnExecH','')
    start = request.POST.get('starttime','00:00')
    end = request.POST.get('endtime','00:00')
   
    abs  = request.POST.get('abs','')
    timestr = request.session.get('dateselect','2021-01-01')
    print(start)
    print(end)
    ida = request.session.get('User','')
    listf = kintai_touroku_info.objects.filter(ymd = timestr,syaincd = ida)
    errflg = False
    context = {}
    
    syainname =  syain_info.objects.all()
    
    start = request.POST.get('starttime', '00:00')
    end = request.POST.get('endtime', '00:00')
    over = request.POST.get('overtime', '')

    tourokuope = request.POST.get('tourokuope','')
    if(tourokuope != ''):
        t1 = request.POST.get('project1','')
        t2 = request.POST.get('project2','')
        t3 = request.POST.get('project3','')
        t4 = request.POST.get('project4','')    
    else:
        t1 = request.POST.get('projectname1','')
        t2 = request.POST.get('projectname2','')
        t3 = request.POST.get('projectname3','')
        t4 = request.POST.get('projectname4','')
    
    pcd1 = project_work.objects.filter(projectname = t1)
    pcd2 = project_work.objects.filter(projectname = t2)
    pcd3 = project_work.objects.filter(projectname = t3)
    pcd4 = project_work.objects.filter(projectname = t4)
    
    if (len(pcd1) != 0):
        projectcd1 = pcd1[0].projectcd
    else:
        projectcd1 = ""
    print("projectcd1" + projectcd1)
    
    if (len(pcd2) != 0):
        projectcd2 = pcd2[0].projectcd
    else:
        projectcd2 = ""
    print("projectcd2" + projectcd2)
    
    if (len(pcd3) != 0):
        projectcd3 = pcd3[0].projectcd
    else:
        projectcd3 = ""
    print("projectcd3" + projectcd3)
    
    if (len(pcd4) != 0):
        projectcd4 = pcd4[0].projectcd
    else:
        projectcd4 = ""
    print("projectcd4" + projectcd4)

    koutei1 = request.POST.get('kouteiname1','')
    koutei2 = request.POST.get('kouteiname2','')
    koutei3 = request.POST.get('kouteiname3','')
    koutei4 = request.POST.get('kouteiname4','')
    kcd1 = project_work.objects.filter(kouteiname = koutei1)
    kcd2 = project_work.objects.filter(kouteiname = koutei2)
    kcd3 = project_work.objects.filter(kouteiname = koutei3)
    kcd4 = project_work.objects.filter(kouteiname = koutei4)
    if (len(kcd1) != 0):
        kouteicd1 = kcd1[0].kouteicd
    else:
        kouteicd1 = ""
    print("kouteicd1" + kouteicd1)
    
    if (len(kcd2) != 0):
        kouteicd2 = kcd2[0].kouteicd
    else:
        kouteicd2 = ""
    print("kouteicd2" + kouteicd2)
    
    if (len(kcd3) != 0):
        kouteicd3 = kcd3[0].kouteicd
    else:
        kouteicd3 = ""
    print("kouteicd3" + kouteicd3)
    
    if (len(kcd4) != 0):
        kouteicd4 = kcd4[0].kouteicd
    else:
        kouteicd4 = ""
    print("kouteicd4" + kouteicd4)
    
    gyomuselect1 = request.POST.get('workname1','')
    gyomuselect2 = request.POST.get('workname2','')
    gyomuselect3 = request.POST.get('workname3','')
    gyomuselect4 = request.POST.get('workname4','')
    gcd1 = project_work.objects.filter(workname = gyomuselect1)
    gcd2 = project_work.objects.filter(workname = gyomuselect2)
    gcd3 = project_work.objects.filter(workname = gyomuselect3)
    gcd4 = project_work.objects.filter(workname = gyomuselect4)
    
    if (len(gcd1) != 0):
        workcd1 = gcd1[0].workcd
    else:
        workcd1 = ""
    print("workcd1" + workcd1)
    
    if (len(gcd2) != 0):
        workcd2 = gcd2[0].workcd
    else:
        workcd2 = ""
    print("workcd2" + workcd2)
    
    if (len(gcd3) != 0):
        workcd3 = gcd3[0].workcd
    else:
        workcd3 = ""
    print("workcd3" + workcd3)
    
    if (len(gcd4) != 0):
        workcd4 = gcd4[0].workcd
    else:
        workcd4 = ""
    print("workcd4" + workcd4)
    
    value1 = project_work.objects.filter(projectname=t1).distinct('kouteiname')
    value2 = project_work.objects.filter(projectname=t2).distinct('kouteiname')
    value3 = project_work.objects.filter(projectname=t3).distinct('kouteiname')
    value4 = project_work.objects.filter(projectname=t4).distinct('kouteiname')
    gyomu1 = project_work.objects.filter(projectname=t1,kouteiname=koutei1)
    gyomu2 = project_work.objects.filter(projectname=t2,kouteiname=koutei2)
    gyomu3 = project_work.objects.filter(projectname=t3,kouteiname=koutei3)
    gyomu4 = project_work.objects.filter(projectname=t4,kouteiname=koutei4)
    
    starttime1 = request.POST.get('starttime1','00:00')
    starttime2 = request.POST.get('starttime2','00:00')
    starttime3 = request.POST.get('starttime3','00:00')
    starttime4 = request.POST.get('starttime4','00:00')
    endtime1 = request.POST.get('endtime1','00:00')
    endtime2 = request.POST.get('endtime2','00:00')
    endtime3 = request.POST.get('endtime3','00:00')
    endtime4 = request.POST.get('endtime4','00:00')
    resttime1 = request.POST.get('resttime1','0')
    resttime2 = request.POST.get('resttime2','0')
    resttime3 = request.POST.get('resttime3','0')
    resttime4 = request.POST.get('resttime4','0')

    hol = request.POST.get('holidaykbn','')
    riyu = request.POST.get('riyu','')
    todo0 = request.POST.get('chikoku','')
    todo1 = request.POST.get('hayade','')
    todo2 = request.POST.get('soutai','')
    todo3 = request.POST.get('hensoku','')
    todo4 = request.POST.get('midnight','')
    todo5 = request.POST.get('holiday','')

    if(btt != '勤怠登録'):

        if (abs == '欠勤'):
            context = {
                        'ymd': timestr,
                        'abs': abs,
                        'chikoku' : todo0,
                        'hayade'  : todo1,
                        'soutai'  : todo2,
                        'hensoku' : todo3,
                        'midnight': todo4,
                        'holiday' : todo5,
                        'holidaykbn': hol,
                        'riyu' : riyu,  
                      }
            return render(request, 'registration/kintai.html', context)

        request.session['kouteiname1'] = request.POST.get('kouteiname1','')
        request.session['kouteiname2'] = request.POST.get('kouteiname2','')
        request.session['kouteiname3'] = request.POST.get('kouteiname3','')
        request.session['kouteiname4'] = request.POST.get('kouteiname4','')
        context = {
                    'starttime': start,
                    'endtime': end,
                    'overtime': over,
                    'projectname1': t1,
                    'projectname2': t2,
                    'projectname3': t3,
                    'projectname4': t4,
                    'starttime1': request.POST.get('starttime1',''),
                    'starttime2': request.POST.get('starttime2',''),
                    'starttime3': request.POST.get('starttime3',''),
                    'starttime4': request.POST.get('starttime4',''),
                    'endtime1': request.POST.get('endtime1',''),
                    'endtime2': request.POST.get('endtime2',''),
                    'endtime3': request.POST.get('endtime3',''),
                    'endtime4': request.POST.get('endtime4',''),
                    'resttime1': request.POST.get('resttime1',''),
                    'resttime2': request.POST.get('resttime2',''),
                    'resttime3': request.POST.get('resttime3',''),
                    'resttime4': request.POST.get('resttime4',''),
                    'koutei1': value1,
                    'koutei2': value2,
                    'koutei3': value3,
                    'koutei4': value4,
                    'kouteiselect1': koutei1,
                    'kouteiselect2': koutei2,
                    'kouteiselect3': koutei3,
                    'kouteiselect4': koutei4,
                    'gyomu1': gyomu1,
                    'gyomu2': gyomu2,
                    'gyomu3': gyomu3,
                    'gyomu4': gyomu4,
                    'gyomuselect1': gyomuselect1,
                    'gyomuselect2': gyomuselect2,
                    'gyomuselect3': gyomuselect3,
                    'gyomuselect4': gyomuselect4,
                    'ymd':      timestr,
                    'abs': abs,
                    'chikoku' : todo0,
                    'hayade'  : todo1,
                    'soutai'  : todo2,
                    'hensoku' : todo3,
                    'midnight': todo4,
                    'holiday' : todo5,
                    'holidaykbn': hol,
                    'riyu' : riyu,  
             }
        return render(request, 'registration/kintai.html', context)

    name = syain_info.objects.get(syaincd=ida).syainname
    print(name)
    worktime = 0.0
    rest = 0.0
    holdb = 0
    todok = 0
    if(hol == "取得なし"):
        holdb = 0
        
    if(hol == "有給休暇"):
        holdb = 1

    if(hol == "特休・その他休暇"):
        holdb = 2

    if(hol == "代休"):
        holdb = 3
        
    if(hol == "その他"):
        holdb = 4
        
    if(hol == "半休等"):
        holdb = 5
        
    if(abs == '出勤'):
        absdb = 0
    if(abs == '欠勤'):
        absdb = 1

    if(abs == '出勤' or abs == ''):
        
        if(t1 == '' and t2 == '' and t3 == '' and t4 == ''):
            context.update({
                  'projecterror': 'プロジェクト登録をしてください',
                  'ymd': timestr,
                  'abs': abs,
                  'holidaykbn': hol,
                  'riyu' : riyu,
                  'chikoku' : todo0,
                  'hayade'  : todo1,
                  'soutai'  : todo2,
                  'hensoku' : todo3,
                  'midnight': todo4,
                  'holiday' : todo5,
            })
            errflg = True
        
        if( abs == '' ):
            context.update({
                  'absnerror': '出欠選択されていません',
                  'starttime': start,
                  'endtime': end,
                  'overtime': over,
                  'projectname1': t1,
                  'projectname2': t2,
                  'projectname3': t3,
                  'projectname4': t4,
                  'starttime1': request.POST.get('starttime1',''),
                  'starttime2': request.POST.get('starttime2',''),
                  'starttime3': request.POST.get('starttime3',''),
                  'starttime4': request.POST.get('starttime4',''),
                  'endtime1': request.POST.get('endtime1',''),
                  'endtime2': request.POST.get('endtime2',''),
                  'endtime3': request.POST.get('endtime3',''),
                  'endtime4': request.POST.get('endtime4',''),
                  'resttime1': request.POST.get('resttime1',''),
                  'resttime2': request.POST.get('resttime2',''),
                  'resttime3': request.POST.get('resttime3',''),
                  'resttime4': request.POST.get('resttime4',''),
                  'koutei1': value1,
                  'koutei2': value2,
                  'koutei3': value3,
                  'koutei4': value4,
                  'kouteiselect1': koutei1,
                  'kouteiselect2': koutei2,
                  'kouteiselect3': koutei3,
                  'kouteiselect4': koutei4,
                  'gyomu1': gyomu1,
                  'gyomu2': gyomu2,
                  'gyomu3': gyomu3,
                  'gyomu4': gyomu4,
                  'gyomuselect1': gyomuselect1,
                  'gyomuselect2': gyomuselect2,
                  'gyomuselect3': gyomuselect3,
                  'gyomuselect4': gyomuselect4,
                  'abs': abs,
                  'holidaykbn': hol,
                  'riyu' : riyu,
                  'chikoku' : todo0,
                  'hayade'  : todo1,
                  'soutai'  : todo2,
                  'hensoku' : todo3,
                  'midnight': todo4,
                  'holiday' : todo5,
                  'ymd': timestr,

            })
            errflg = True
        if( (t1 != '' and starttime1 == '')  or (t2 != '' and starttime2 == '') or (t3 != '' and starttime3 == '') or (t4 != '' and starttime4 == '') ):
            context.update({
                  'starterror': '開始時刻が入力されていません',
                  'starttime': start,
                  'endtime': end,
                  'overtime': over,
                  'projectname1': t1,
                  'projectname2': t2,
                  'projectname3': t3,
                  'projectname4': t4,
                  'starttime1': request.POST.get('starttime1',''),
                  'starttime2': request.POST.get('starttime2',''),
                  'starttime3': request.POST.get('starttime3',''),
                  'starttime4': request.POST.get('starttime4',''),
                  'endtime1': request.POST.get('endtime1',''),
                  'endtime2': request.POST.get('endtime2',''),
                  'endtime3': request.POST.get('endtime3',''),
                  'endtime4': request.POST.get('endtime4',''),
                  'resttime1': request.POST.get('resttime1',''),
                  'resttime2': request.POST.get('resttime2',''),
                  'resttime3': request.POST.get('resttime3',''),
                  'resttime4': request.POST.get('resttime4',''),
                  'koutei1': value1,
                  'koutei2': value2,
                  'koutei3': value3,
                  'koutei4': value4,
                  'kouteiselect1': koutei1,
                  'kouteiselect2': koutei2,
                  'kouteiselect3': koutei3,
                  'kouteiselect4': koutei4,
                  'gyomu1': gyomu1,
                  'gyomu2': gyomu2,
                  'gyomu3': gyomu3,
                  'gyomu4': gyomu4,
                  'gyomuselect1': gyomuselect1,
                  'gyomuselect2': gyomuselect2,
                  'gyomuselect3': gyomuselect3,
                  'gyomuselect4': gyomuselect4,
                  'abs': abs,
                  'holidaykbn': hol,
                  'riyu' : riyu,
                  'chikoku' : todo0,
                  'hayade'  : todo1,
                  'soutai'  : todo2,
                  'hensoku' : todo3,
                  'midnight': todo4,
                  'holiday' : todo5,
                  'ymd': timestr,
            })
            errflg = True
        if( (t1 != '' and endtime1 == '')  or (t2 != '' and endtime2 == '') or (t3 != '' and endtime3 == '') or (t4 != '' and endtime4 == '')  ):
            context.update({
                  'enderror': '終了時刻が入力されていません',
                  'starttime': start,
                  'endtime': end,
                  'overtime': over,
                  'projectname1': t1,
                  'projectname2': t2,
                  'projectname3': t3,
                  'projectname4': t4,
                  'starttime1': request.POST.get('starttime1',''),
                  'starttime2': request.POST.get('starttime2',''),
                  'starttime3': request.POST.get('starttime3',''),
                  'starttime4': request.POST.get('starttime4',''),
                  'endtime1': request.POST.get('endtime1',''),
                  'endtime2': request.POST.get('endtime2',''),
                  'endtime3': request.POST.get('endtime3',''),
                  'endtime4': request.POST.get('endtime4',''),
                  'resttime1': request.POST.get('resttime1',''),
                  'resttime2': request.POST.get('resttime2',''),
                  'resttime3': request.POST.get('resttime3',''),
                  'resttime4': request.POST.get('resttime4',''),
                  'koutei1': value1,
                  'koutei2': value2,
                  'koutei3': value3,
                  'koutei4': value4,
                  'kouteiselect1': koutei1,
                  'kouteiselect2': koutei2,
                  'kouteiselect3': koutei3,
                  'kouteiselect4': koutei4,
                  'gyomu1': gyomu1,
                  'gyomu2': gyomu2,
                  'gyomu3': gyomu3,
                  'gyomu4': gyomu4,
                  'gyomuselect1': gyomuselect1,
                  'gyomuselect2': gyomuselect2,
                  'gyomuselect3': gyomuselect3,
                  'gyomuselect4': gyomuselect4,
                  'abs': abs,
                  'holidaykbn': hol,
                  'riyu' : riyu,
                  'chikoku' : todo0,
                  'hayade'  : todo1,
                  'soutai'  : todo2,
                  'hensoku' : todo3,
                  'midnight': todo4,
                  'holiday' : todo5,
                  'ymd': timestr,
            })
            errflg = True
        if( (t1 != '' and resttime1 == '')  or (t2 != '' and resttime2 == '') or (t3 != '' and resttime3 == '') or (t4 != '' and resttime4 == '')  ):
            context.update({
                  'resterror': '休憩時間が入力されていません',
                  'starttime': start,
                  'endtime': end,
                  'overtime': over,
                  'projectname1': t1,
                  'projectname2': t2,
                  'projectname3': t3,
                  'projectname4': t4,
                  'starttime1': request.POST.get('starttime1',''),
                  'starttime2': request.POST.get('starttime2',''),
                  'starttime3': request.POST.get('starttime3',''),
                  'starttime4': request.POST.get('starttime4',''),
                  'endtime1': request.POST.get('endtime1',''),
                  'endtime2': request.POST.get('endtime2',''),
                  'endtime3': request.POST.get('endtime3',''),
                  'endtime4': request.POST.get('endtime4',''),
                  'resttime1': request.POST.get('resttime1',''),
                  'resttime2': request.POST.get('resttime2',''),
                  'resttime3': request.POST.get('resttime3',''),
                  'resttime4': request.POST.get('resttime4',''),
                  'koutei1': value1,
                  'koutei2': value2,
                  'koutei3': value3,
                  'koutei4': value4,
                  'kouteiselect1': koutei1,
                  'kouteiselect2': koutei2,
                  'kouteiselect3': koutei3,
                  'kouteiselect4': koutei4,
                  'gyomu1': gyomu1,
                  'gyomu2': gyomu2,
                  'gyomu3': gyomu3,
                  'gyomu4': gyomu4,
                  'gyomuselect1': gyomuselect1,
                  'gyomuselect2': gyomuselect2,
                  'gyomuselect3': gyomuselect3,
                  'gyomuselect4': gyomuselect4,
                  'abs': abs,
                  'holidaykbn': hol,
                  'riyu' : riyu,
                  'chikoku' : todo0,
                  'hayade'  : todo1,
                  'soutai'  : todo2,
                  'hensoku' : todo3,
                  'midnight': todo4,
                  'holiday' : todo5,
                  'ymd': timestr,
            })
            errflg = True
            

        if( (t1 != '' and koutei1 == '')  or (t2 != '' and koutei2 == '') or (t3 != '' and koutei3 == '') or (t4 != '' and koutei4 == '')):
            context.update({
                  'kouteierror': '工程が入力されていません',
                  'starttime': start,
                  'endtime': end,
                  'overtime': over,
                  'projectname1': t1,
                  'projectname2': t2,
                  'projectname3': t3,
                  'projectname4': t4,
                  'starttime1': request.POST.get('starttime1',''),
                  'starttime2': request.POST.get('starttime2',''),
                  'starttime3': request.POST.get('starttime3',''),
                  'starttime4': request.POST.get('starttime4',''),
                  'endtime1': request.POST.get('endtime1',''),
                  'endtime2': request.POST.get('endtime2',''),
                  'endtime3': request.POST.get('endtime3',''),
                  'endtime4': request.POST.get('endtime4',''),
                  'resttime1': request.POST.get('resttime1',''),
                  'resttime2': request.POST.get('resttime2',''),
                  'resttime3': request.POST.get('resttime3',''),
                  'resttime4': request.POST.get('resttime4',''),
                  'koutei1': value1,
                  'koutei2': value2,
                  'koutei3': value3,
                  'koutei4': value4,
                  'kouteiselect1': koutei1,
                  'kouteiselect2': koutei2,
                  'kouteiselect3': koutei3,
                  'kouteiselect4': koutei4,
                  'gyomu1': gyomu1,
                  'gyomu2': gyomu2,
                  'gyomu3': gyomu3,
                  'gyomu4': gyomu4,
                  'gyomuselect1': gyomuselect1,
                  'gyomuselect2': gyomuselect2,
                  'gyomuselect3': gyomuselect3,
                  'gyomuselect4': gyomuselect4,
                  'abs': abs,
                  'holidaykbn': hol,
                  'riyu' : riyu,  
                  'chikoku' : todo0,
                  'hayade'  : todo1,
                  'soutai'  : todo2,
                  'hensoku' : todo3,
                  'midnight': todo4,
                  'holiday' : todo5,
                  'ymd': timestr,

            })
            errflg = True
        if( (t1 != '' and gyomuselect1 == '')  or (t2 != '' and gyomuselect2 == '') or (t3 != '' and gyomuselect3 == '') or (t4 != '' and gyomuselect4 == '')):
            context.update({
                  'workerror': '業務が入力されていません',
                  'starttime': start,
                  'endtime': end,
                  'overtime': over,
                  'projectname1': t1,
                  'projectname2': t2,
                  'projectname3': t3,
                  'projectname4': t4,
                  'starttime1': request.POST.get('starttime1',''),
                  'starttime2': request.POST.get('starttime2',''),
                  'starttime3': request.POST.get('starttime3',''),
                  'starttime4': request.POST.get('starttime4',''),
                  'endtime1': request.POST.get('endtime1',''),
                  'endtime2': request.POST.get('endtime2',''),
                  'endtime3': request.POST.get('endtime3',''),
                  'endtime4': request.POST.get('endtime4',''),
                  'resttime1': request.POST.get('resttime1',''),
                  'resttime2': request.POST.get('resttime2',''),
                  'resttime3': request.POST.get('resttime3',''),
                  'resttime4': request.POST.get('resttime4',''),
                  'koutei1': value1,
                  'koutei2': value2,
                  'koutei3': value3,
                  'koutei4': value4,
                  'kouteiselect1': koutei1,
                  'kouteiselect2': koutei2,
                  'kouteiselect3': koutei3,
                  'kouteiselect4': koutei4,
                  'gyomu1': gyomu1,
                  'gyomu2': gyomu2,
                  'gyomu3': gyomu3,
                  'gyomu4': gyomu4,
                  'gyomuselect1': gyomuselect1,
                  'gyomuselect2': gyomuselect2,
                  'gyomuselect3': gyomuselect3,
                  'gyomuselect4': gyomuselect4,
                  'abs': abs,
                  'holidaykbn': hol,
                  'riyu' : riyu,
                  'chikoku' : todo0,
                  'hayade'  : todo1,
                  'soutai'  : todo2,
                  'hensoku' : todo3,
                  'midnight': todo4,
                  'holiday' : todo5,
                  'ymd': timestr,

            })
            errflg = True
        if( timestr == ''):
            context.update({
                  'timeerror': '日付が入力されていません',
                  'projectname1': t1,
                  'projectname2': t2,
                  'projectname3': t3,
                  'projectname4': t4,
                  'starttime': start,
                  'endtime': end,
                  'overtime': over,
                  'starttime1': request.POST.get('starttime1',''),
                  'starttime2': request.POST.get('starttime2',''),
                  'starttime3': request.POST.get('starttime3',''),
                  'starttime4': request.POST.get('starttime4',''),
                  'endtime1': request.POST.get('endtime1',''),
                  'endtime2': request.POST.get('endtime2',''),
                  'endtime3': request.POST.get('endtime3',''),
                  'endtime4': request.POST.get('endtime4',''),
                  'koutei1': value1,
                  'koutei2': value2,
                  'koutei3': value3,
                  'koutei4': value4,
                  'kouteiselect1': koutei1,
                  'kouteiselect2': koutei2,
                  'kouteiselect3': koutei3,
                  'kouteiselect4': koutei4,
                  'gyomu1': gyomu1,
                  'gyomu2': gyomu2,
                  'gyomu3': gyomu3,
                  'gyomu4': gyomu4,
                  'gyomuselect1': gyomuselect1,
                  'gyomuselect2': gyomuselect2,
                  'gyomuselect3': gyomuselect3,
                  'gyomuselect4': gyomuselect4,
                  'abs': abs,
                  'holidaykbn': hol,
                  'riyu' : riyu,
                  'chikoku' : todo0,
                  'hayade'  : todo1,
                  'soutai'  : todo2,
                  'hensoku' : todo3,
                  'midnight': todo4,
                  'holiday' : todo5,
                  'ymd': timestr,

            })
            errflg = True
        if (todo0 == ''):
            todo0db = 0
        else:
            todo0db = 1
        
        if (todo1 == ''):
            todo1db = 0
        else:
            todo1db = 1
            
        if (todo2 == ''):
            todo2db = 0
        else:
            todo2db = 1

        if (todo3 == ''):
            todo3db = 0
        else:
            todo3db = 1
        
        if (todo4 == ''):
            todo4db = 0
        else:
            todo4db = 1
            
        if (todo5 == ''):
            todo5db = 0
        else:
            todo5db = 1

        if(todo0db == 1 or todo1db == 1 or todo2db == 1 or todo3db == 1 or todo4db == 1 or todo5db == 1 ):
            todok = 1
        if errflg:
           return render(request, 'registration/kintai.html', context)
        startn = start.split(':')
        endn = end.split(':')
        starth = int(startn[0])
        endh = int(endn[0])

        startm = int(startn[1])
        endm = int(endn[1])
        min = endm - startm
        min = min / 60
        worktime = endh - starth + min - float(resttime)
        worktime = round(worktime,2)
        if(startm >  endm):
            worktime = worktime - 1
        if (resttime1 == ''):
            resttime1 = 0
        if (resttime2 == ''):
            resttime2 = 0
        if (resttime3 == ''):
            resttime3 = 0
        if (resttime4 == ''):
            resttime4 = 0
        resttime = float(resttime1) +  float(resttime2) +  float(resttime3) + float(resttime4)


        #DB格納(出勤)
        b = kintai_touroku_info(syaincd=ida,syainname = name, 
        ymd=timestr,starttime=start,endtime=end,worktime=worktime,overtime=over,
        resttime=resttime, attkbn=absdb, holidaykbn=holdb, holidayriyu=riyu,
        todoke_tikoku=todo0db, todoke_soutai=todo1db, todoke_midnight=todo2db, todoke_hayade=todo3db, 
        todoke_irregular=todo4db, todoke_holiwork=todo5db, todokekbn=todok,
        projectname1 = t1,kouteiname1 = koutei1, workname1 = gyomuselect1, start1 = starttime1, end1 = endtime1, rest1 = resttime1,
        projectname2 = t2,kouteiname2 = koutei2, workname2 = gyomuselect2, start2 = starttime2, end2 = endtime2, rest2 = resttime2,
        projectname3 = t3,kouteiname3 = koutei3, workname3 = gyomuselect3, start3 = starttime3, end3 = endtime3, rest3 = resttime3,
        projectname4 = t4,kouteiname4 = koutei4, workname4 = gyomuselect4, start4 = starttime4, end4 = endtime4, rest4 = resttime4,
        projectcd1 = projectcd1,projectcd2 = projectcd2,projectcd3 = projectcd3,projectcd4 = projectcd4,
        kouteicd1 = kouteicd1,kouteicd2 = kouteicd2,kouteicd3 = kouteicd3,kouteicd4 = kouteicd4,
        workcd1 = workcd1,workcd2 = workcd2,workcd3 = workcd3,workcd4 = workcd4)
    #DB格納(欠勤)
    else:
        print('kekkin')
        start = '00:00'
        end = '00:00'
        worktime= 0.0
        over = 0.0
        b = kintai_touroku_info(syaincd=ida,syainname = name, 
        ymd=timestr, starttime=start,endtime=end,worktime=worktime,overtime=over,attkbn=absdb, holidaykbn=holdb, holidayriyu=riyu,
        start1 = starttime1, end1 = endtime1,
        start2 = starttime2, end2 = endtime2,
        start3 = starttime3, end3 = endtime3,
        start4 = starttime4, end4 = endtime4,
        todokekbn=todok)

    listf = kintai_touroku_info.objects.filter(ymd = timestr)
    
   
    if (len(listf) == 0):
       b.save()
    else:
       print('update')
       b =  kintai_touroku_info.objects.filter(ymd = timestr)
       b.update(starttime=start,endtime=end,worktime=worktime,overtime=over,
       resttime=resttime,attkbn=absdb, holidaykbn=holdb, holidayriyu=riyu,
       todoke_tikoku=todo0db, todoke_soutai=todo1db, todoke_midnight=todo2db, todoke_hayade=todo3db, 
       todoke_irregular=todo4db, todoke_holiwork=todo5db, todokekbn=todok,
       projectname1 = t1,kouteiname1 = koutei1, workname1 = gyomuselect1, start1 = starttime1, end1 = endtime1, rest1 = resttime1,
       projectname2 = t2,kouteiname2 = koutei2, workname2 = gyomuselect2, start2 = starttime2, end2 = endtime2, rest2 = resttime2,
       projectname3 = t3,kouteiname3 = koutei3, workname3 = gyomuselect3, start3 = starttime3, end3 = endtime3, rest3 = resttime3,
       projectname4 = t4,kouteiname4 = koutei4, workname4 = gyomuselect4, start4 = starttime4, end4 = endtime4, rest4 = resttime4,
       projectcd1 = projectcd1,projectcd2 = projectcd2,projectcd3 = projectcd3,projectcd4 = projectcd4,
       kouteicd1 = kouteicd1,kouteicd2 = kouteicd2,kouteicd3 = kouteicd3,kouteicd4 = kouteicd4,
       workcd1 = workcd1,workcd2 = workcd2,workcd3 = workcd3,workcd4 = workcd4)
     
    context = {
                  'message': '勤怠登録しました',
                  'starttime':start,
                  'endtime': end,
                  'worktime': worktime,
                  'overtime': over,
                  'resttime': resttime,
                  'ymd': timestr,
                  'projectname1': t1,
                  'projectname2': t2,
                  'projectname3': t3,
                  'projectname4': t4,
                  'starttime1': request.POST.get('starttime1',''),
                  'starttime2': request.POST.get('starttime2',''),
                  'starttime3': request.POST.get('starttime3',''),
                  'starttime4': request.POST.get('starttime4',''),
                  'endtime1': request.POST.get('endtime1',''),
                  'endtime2': request.POST.get('endtime2',''),
                  'endtime3': request.POST.get('endtime3',''),
                  'endtime4': request.POST.get('endtime4',''),
                  'resttime1': request.POST.get('resttime1',''),
                  'resttime2': request.POST.get('resttime2',''),
                  'resttime3': request.POST.get('resttime3',''),
                  'resttime4': request.POST.get('resttime4',''),
                  'koutei1': value1,
                  'koutei2': value2,
                  'koutei3': value3,
                  'koutei4': value4,
                  'kouteiselect1': koutei1,
                  'kouteiselect2': koutei2,
                  'kouteiselect3': koutei3,
                  'kouteiselect4': koutei4,
                  'gyomu1': gyomu1,
                  'gyomu2': gyomu2,
                  'gyomu3': gyomu3,
                  'gyomu4': gyomu4,
                  'gyomuselect1': gyomuselect1,
                  'gyomuselect2': gyomuselect2,
                  'gyomuselect3': gyomuselect3,
                  'gyomuselect4': gyomuselect4,
                  'abs': abs,
                  'holidaykbn': hol,
                  'riyu' : riyu,
                  'chikoku' : todo0,
                  'hayade'  : todo1,
                  'soutai'  : todo2,
                  'hensoku' : todo3,
                  'midnight': todo4,
                  'holiday' : todo5,

            }
    return render(request, 'registration/kintai.html', context)


#勤怠入力画面ロード   
def kintaiload(request):
    template = loader.get_template('registration/kintai.html')
    monthyear =request.POST.get('dateselect')
    request.session['dateselect'] = request.POST.get('dateselect')
    id = request.session.get('User','')
    print(monthyear)
    listf = kintai_touroku_info.objects.filter(ymd = monthyear, syaincd = id)
    print(len(listf))
    if (len(listf) == 1):

        attkbn = listf[0].attkbn
        holidaykbn = listf[0].holidaykbn
        holidayriyu = listf[0].holidayriyu
        start = str(listf[0].starttime)
        start = start[:5]
        end = str(listf[0].endtime)
        end = end[:5]
        start1 = str(listf[0].start1)
        start1 = start1[:5]
        end1 = str(listf[0].end1)
        end1 = end1[:5]
        start2 = str(listf[0].start2)
        start2 = start2[:5]
        end2 = str(listf[0].end2)
        end2 = end2[:5]
        start3 = str(listf[0].start3)
        start3 = start3[:5]
        end3 = str(listf[0].end3)
        end3 = end3[:5]
        start4 = str(listf[0].start4)
        start4 = start4[:5]
        end4 = str(listf[0].end4)
        end4 = end4[:5]
        todo0 = listf[0].todoke_tikoku
        todo1 = listf[0].todoke_soutai
        todo2 = listf[0].todoke_midnight
        todo3 = listf[0].todoke_hayade
        todo4 = listf[0].todoke_irregular
        todo5 = listf[0].todoke_holiwork
        print(start2)
        print(end2)
        koutei1 = project_work.objects.filter(projectname=listf[0].projectname1).distinct('kouteiname')
        koutei2 = project_work.objects.filter(projectname=listf[0].projectname2).distinct('kouteiname')
        koutei3 = project_work.objects.filter(projectname=listf[0].projectname3).distinct('kouteiname')
        koutei4 = project_work.objects.filter(projectname=listf[0].projectname4).distinct('kouteiname')
        gyomu1 = project_work.objects.filter(projectname=listf[0].projectname1,kouteiname=listf[0].kouteiname1)
        gyomu2 = project_work.objects.filter(projectname=listf[0].projectname2,kouteiname=listf[0].kouteiname2)
        gyomu3 = project_work.objects.filter(projectname=listf[0].projectname3,kouteiname=listf[0].kouteiname3)
        gyomu4 = project_work.objects.filter(projectname=listf[0].projectname4,kouteiname=listf[0].kouteiname4)
        
        if (attkbn == 0 ):
            attkbn = '出勤'
        if (attkbn == 1 ):
            attkbn = '欠勤'
        if (holidaykbn == 0 ):
            holidaykbn = '取得なし'
        if (holidaykbn == 1 ):
            holidaykbn = '有給休暇'
        if (holidaykbn == 2 ):
            holidaykbn = '特休・その他休暇'
        if (holidaykbn == 3 ):
            holidaykbn = '代休'
        if (holidaykbn == 4 ):
            holidaykbn = 'その他'
        if (holidaykbn == 5 ):
            holidaykbn = '半休等'
        if (todo0 == 1 ):
            todo0 = '遅刻'
        else:
            todo0 = ''
        if (todo1 == 1 ):
            todo1 = '早出有'
        else:
            todo1 = ''
        if (todo2 == 1 ):
            todo2 = '早退'
        else:
            todo2 = ''
        if (todo3 == 1 ):
            todo3 = '変則勤務'
        else:
            todo3 = ''
        if (todo4 == 1 ):
            todo4 = '深夜有'
        else:
            todo4 = ''
        if (todo5 == 1 ):
            todo5 = '休日出勤'
        else:
            todo5 = ''
        context = {
                      'starttime':start,
                      'endtime': end,
                      'worktime': listf[0].worktime,
                      'overtime': listf[0].overtime,
                      'resttime': listf[0].resttime,
                      'ymd':      monthyear,
                      'projectname1':listf[0].projectname1,
                      'projectname2':listf[0].projectname2,
                      'projectname3':listf[0].projectname3,
                      'projectname4':listf[0].projectname4,
                      'koutei1': koutei1,
                      'koutei2': koutei2,
                      'koutei3': koutei3,
                      'koutei4': koutei4,
                      'kouteiselect1': listf[0].kouteiname1,
                      'kouteiselect2': listf[0].kouteiname2,
                      'kouteiselect3': listf[0].kouteiname3,
                      'kouteiselect4': listf[0].kouteiname4,
                      'gyomu1':   gyomu1,
                      'gyomu2':   gyomu2,
                      'gyomu3':   gyomu3,
                      'gyomu4':   gyomu4,
                      'gyomuselect1': listf[0].workname1,
                      'gyomuselect2': listf[0].workname2,
                      'gyomuselect3': listf[0].workname3,
                      'gyomuselect4': listf[0].workname4,
                      'starttime1':start1,
                      'endtime1': end1,
                      'resttime1':   listf[0].rest1,
                      'starttime2':start2,
                      'endtime2': end2,
                      'resttime2':   listf[0].rest2,
                      'starttime3':start3,
                      'endtime3': end3,
                      'resttime3':   listf[0].rest3,
                      'starttime4':start4,
                      'endtime4': end4,
                      'resttime4':   listf[0].rest4,
                      'holidaykbn': holidaykbn,
                      'abs': attkbn,
                      'riyu': holidayriyu,
                      'chikoku': todo0,
                      'hayade': todo1,
                      'soutai': todo2,
                      'hensoku': todo3,
                      'midnight': todo4,
                      'holiday': todo5,
                }      
        return render(request, 'registration/kintai.html', context)
    context = {
                      'ymd':      monthyear,
                }      
    return render(request, 'registration/kintai.html', context)
