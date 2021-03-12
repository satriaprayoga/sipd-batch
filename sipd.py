import requests
import json
import csv

payload={'_token':'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx','userName':'196606021997031001','password':'bogorkab','tahunanggaran':2021,'idDaerah':11}

session=''

sipdUrl='https://sipd.kemendagri.go.id/siap/'

def login(token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', userName='adm.keuangan',password='belanja', tahunanggaran=2021,idDaerah=11):
    payload={'_token':token,'userName':userName,'password':password, 'tahunanggaran':tahunanggaran,'idDaerah':idDaerah}
    r=requests.post(sipdUrl+'login',data=payload)
    print(r.status_code)
    global session
    session=r.headers['Set-Cookie']
    print(session)
  
def getCookie():
    splitSession=session.split(';')
    split=splitSession[0].split('=')
    cookie=dict(siap_session=split[1])
    return cookie

def getAngkasGlobalSkpd(idSkpd,filename='test.csv',tahun=2021,idDaerah=11):
    cookie=getCookie()
    url=sipdUrl+"/rak-belanja/tampil-giat/daerah/main/budget/{}/{}/{}".format(tahun,idDaerah,idSkpd)
    print(url)
    p=requests.get(url,cookies=cookie)
    data=p.json()
    columns=["nama_bidang_urusan",
    "kode_bidang_urusan",
    "nama_skpd",
    "kode_sub_skpd",
    "nama_sub_skpd",
    "nama_program",
    "nama_giat",
    "kode_sub_giat",
    "nama_sub_giat",
    "kode_akun",
    "nama_akun",
    "total_rincian",
    "bulan_1",
    "bulan_2",
    "bulan_3",
    "bulan_4",
    "bulan_5",
    "bulan_6",
    "bulan_7",
    "bulan_8",
    "bulan_9",
    "bulan_10",
    "bulan_11",
    "bulan_12",
    "total_akb",
    "selisih",
    "action"]
    with open(filename,'w',encoding='UTF-8', newline='') as file:
        writer=csv.DictWriter(file,fieldnames=columns)
        writer.writeheader()
        for s in data['data']:
            params="{}.{}.{}.{}.{}.{}".format(s['id_skpd'],s['id_sub_skpd'],s['id_bidang_urusan'],s['id_program'],s['id_giat'],s['id_sub_giat'])
            rinciUrl=sipdUrl+"/rak-belanja/tampil-rincian/daerah/main/budget/{}/{}/{}".format(tahun,idDaerah,idSkpd)
            r=requests.get(rinciUrl,cookies=cookie, params={'kodesbl':params})
            rdata=r.json()
            for x in rdata['data']:
                
                writer.writerow({"nama_bidang_urusan":s["nama_bidang_urusan"],
                        "kode_bidang_urusan":s["kode_bidang_urusan"],
                        "nama_skpd":s["nama_skpd"],
                        "kode_sub_skpd":s["kode_sub_skpd"],
                        "nama_sub_skpd":s["nama_sub_skpd"],
                        "nama_program":s["nama_program"],
                        "nama_giat":s["nama_giat"],
                        "kode_sub_giat":s["kode_sub_giat"],
                        "nama_sub_giat":s["nama_sub_giat"],
                        "kode_akun":x['nama_akun'],
                        "nama_akun":x['kode_akun'],
                        "total_rincian":x['total_akb'],
                        "bulan_1":x["bulan_1"],
                        "bulan_2":x["bulan_2"],
                        "bulan_3":x["bulan_3"],
                        "bulan_4":x["bulan_4"],
                        "bulan_5":x["bulan_5"],
                        "bulan_6":x["bulan_6"],
                        "bulan_7":x["bulan_7"],
                        "bulan_8":x["bulan_8"],
                        "bulan_9":x["bulan_9"],
                        "bulan_10":x["bulan_10"],
                        "bulan_11":x["bulan_11"],
                        "bulan_12":x["bulan_12"],
                        "total_akb":x["total_akb"],
                        "selisih":x["selisih"],
                        "action":x["action"],
                                })
            #writer.writerows(rdata['data'])

def fetchAngkasBelanja():
    with open('skpd.json','r') as f:
        skpd=json.load(f)
    for s in skpd:
        idSkpd=s['idSkpd']
        filename='rak-belanja'+'/'+s['namaSkpd']+'.csv'
        getAngkasGlobalSkpd(idSkpd,filename)
     
def angkasPendapatan(idSkpd,filename,tahun=2021,idDaerah=11):
    cookie=getCookie()
    url=sipdUrl+"/rak-pendapatan/tampil-pendapatan/daerah/main/budget/{}/{}/{}".format(tahun,idDaerah,idSkpd)
    print(url)
    p=requests.get(url,cookies=cookie)
    data=p.json()
    parse=data['data']
    if len(parse)!=0:
        bulan=data['data'][0]
        bulan_keys=bulan.keys()
        print(bulan_keys)
        #print(data['data'])
        print(len(data['data']))
        with open(filename,'w',encoding='UTF-8', newline='') as f:
            writer=csv.DictWriter(f,fieldnames=bulan_keys)
            writer.writeheader()
            writer.writerows(data['data'])

def fetchAngkasPendapatan():
    with open('skpd.json','r') as f:
        skpd=json.load(f)
    for s in skpd:
        #cookie=getCookie()
        idSkpd=s['idSkpd']
        filename='rak-pendapatan'+'/'+s['namaSkpd']+'.csv'
        angkasPendapatan(idSkpd,filename)
        #url=sipdUrl+"/rak-pendapatan/tampil-pendapatan/daerah/main/budget/{}/{}/{}".format(2021,11,idSkpd)
        #p=requests.get(url,cookies=cookie)
        #data=p.json()
        #print(data['data'])
        
       

def getSkpd():
    cookie=getCookie()
    print(cookie)
    p=requests.get('https://sipd.kemendagri.go.id/siap/data/skpd/all',cookies=cookie)
    data=p.json()
    for skpd in data:
        print("{}, {}".format(skpd['idSkpd'],skpd['namaSkpd']))

#r=requests.post('https://sipd.kemendagri.go.id/siap/login',data=payload)
#print(r.headers['Set-Cookie'])
#session=r.headers['Set-Cookie'].split(';')#'siap_session=X3wE6CoqfOk64NYcJcFUsEzMcFhRiQc4UIdVwwu2; expires=Tue, 23-Feb-2021 23:47:07 GMT; Max-Age=28800; path=/; httponly'


#split=session[0].split('=')
#cookie=dict(siap_session=split[1])
#print(cookie)

#p=requests.get('https://sipd.kemendagri.go.id/siap/data/user',cookies=cookie)


