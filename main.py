import wechat
import sqlite3

subscribes={}

def get_subscribes(connection):
	connection.execute('select * from subscribe')
	temp=connection.fetchall()
	subscribes_wechat=[]
	for row in temp:
		if row[1] == 'wechat':
			temp_wechat={'name':row[0],'code':row[2],'url':row[3]}
			subscribes_wechat.append(temp_wechat)
	subscribes['wechat']=subscribes_wechat		
	return subscribes

def load_wechat_data(connection,data,database):
	name=data['name']
	code=data['code']
	url=data['url']
	temp=wechat.subscribe(code)
	temp_title=temp[code][0]
	temp_digest=temp[code][1]
	temp_url=temp[code][2]
	temp_title_in=connection.execute('select title from wechat where code=:code',{'code':code}).fetchall()
	temp_title_in_parse=[j[0] for j in temp_title_in]
	if len(temp_title)>0:
		for i in range(len(temp_title)):
			if not (temp_title[i] in temp_title_in_parse):
				connection.execute("insert into wechat values (?, ?, ?, ?, ?)", (name,code,temp_title[i], temp_digest[i],url+temp_url[i]))
				database.commit()

def link_database():
	conn=sqlite3.connect('database.db')
	c=conn.cursor()
	a=get_subscribes(c)
	for data in a['wechat']:
		load_wechat_data(c,data,conn)
	conn.close()
	return a
