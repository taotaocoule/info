from bs4 import BeautifulSoup
import requests
import re
import json

url=r'http://weixin.sogou.com/weixin'

para={'query':r'story63'}
r=requests.get(url,params=para)
soup=BeautifulSoup(r.text)
m=soup.find('a',{'uigs':"account_name_0"})
s=m.attrs['href']
t=BeautifulSoup(requests.get(s).text)

if t is None:
	print('Need verification code:  {}'.format(s))

def subscribe(wechat):
	titles=[]
	contents=[]
	urls=[]
	para={'query':wechat}
	r=requests.get(url,params=para)
	soup=BeautifulSoup(r.text)
	m=soup.find('a',{'uigs':"account_name_0"})
	s=m.attrs['href']
	t=BeautifulSoup(requests.get(s).text)
	m=t.find_all('script')
	target=m[-2]
	data=target.string
	p=re.compile(r'var msgList =(.*?);\r\n')
	q=p.findall(data)
	try:
		z=json.loads(q[0])
	except:
		print('Need verification code:  {}'.format(s))
	else:	
		d=z['list']
		for i in d:
			s=i['app_msg_ext_info']
			t=s['multi_app_msg_item_list']	
			titles.append(s['title'])
			contents.append(s['digest'])
			urls.append(s['content_url'].replace('&amp;','&'))
			for j in t:
				titles.append(j['title'])
				contents.append(j['digest'])
				urls.append(j['content_url'].replace('&amp;','&'))
		result={}
		result[wechat]=[titles,contents,urls]
		return result	