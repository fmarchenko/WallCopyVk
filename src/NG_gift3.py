#!/usr/bin/env python
# -*- coding: utf-8 -*-
import vk_api,time
sleep_time1 = 0.2
sleep_time2 = 0.3
page_begin = open("page_begin.html","r+")
page_begin = page_begin.read();
page_begin = page_begin.decode('utf-8')

template_post = open("template_post.html","r+")
template_post = template_post.read();
template_post = template_post.decode('utf-8')
coment_block_template=u'''
<div class ='comments_block'>
						<font color=#5566FF face="ArialBlack" size=3><b>Комментарии:</b></font></br>
						{COMENTS}
</div>
'''
page_end =u'''

</body>

</html>
'''

photos_template= open("photos_template.html","r+")
photos_template = photos_template.read();
photos_template = photos_template.decode('utf-8')

audio_block_template= open("audio_block_template.html","r+")
audio_block_template = audio_block_template.read();
audio_block_template = audio_block_template.decode('utf-8')

audio_song_template = u'''
<div class='audio' ><img src='vk_audio.jpg' width = 20px> <font color=#5566FF face="ArialBlack" size=3>{AUTHOR}</font>- 
{NAME}(Марина Цветаева)</div>	
'''


photo_templ=u'''
<div class='photo' >
						<img class ='photo' hspace="5" vspace="5" src='{PHOTO_PATH}' >
						</div>
'''

comment_template= open("comment_template.html","r+")
comment_template = comment_template.read();
comment_template = comment_template.decode('utf-8')

video_block_template=u'''
<div class='video_block'>
						<font color=#5566FF face="ArialBlack" size=3><b>Видеозаписи:</b></font></br>
{VIDEOS}
</div>					
'''
def main():
	tom=400
	offset = 0
	count = 4000#2948
	step = 50
	id_group = -39576543
	login = u'email'
	password = u'passwd'
	iteratin = 0
	try:
		vk = vk_api.VkApi(login, password)  # Авторизируемся
	except vk_api.authorization_error, error_msg:
		print error_msg  # В случае ошибки выведем сообщение
		return  # и выйдем
	ans = vk.method('groups.getById', {'gids':"%s"%(-id_group),'fields':'photo'}) 
	photo_group =  ans[0]['photo_big']	

	f = open("res.html",'w+')
	f.write(page_begin.encode('utf-8'))
	while(iteratin*step<count):
		values = {
			'owner_id':"%s"%(id_group)
			,'offset':offset+iteratin*step
			,'count':step
			}
		response = vk.method('wall.get', values)  # С использованием метода wall.get
		iteratin+=1
		time.sleep(sleep_time2)
		print u"итерация номер:",iteratin,u" Кол-во скачаных постов:",len(response)
		for post in response[1:]:
			try:
				has_some = False
				post_data = post['text']
				user = post['from_id']
				com_count = post['comments']['count']
				
				if(len(post_data)>0):
					has_some = True
				other = ""
				print post['id']
				if(user<0):
					user_photo = photo_group
				else:
					user_photo=vk.method('users.get', {'uids':"%s"%(user),'fields':'photo'})
					time.sleep(sleep_time2)
					user_photo =  ans[0]['photo_big']
				if(post.has_key('attachments')):
					attachments = post['attachments']
					coun_photo = 0
					coun_audio = 0
					coun_link= 0
					coun_video= 0
					photos_html = photos_template
					audio_html = audio_block_template
					videos_html=video_block_template
					for att in attachments:
						if att['type']=='photo':
							coun_photo+=1
							photo_tmp = photo_templ
							photo_src = att['photo']['src_big']
							photo_tmp=photo_tmp.replace(u"{PHOTO_PATH}",""+photo_src)
							photos_html=photos_html.replace(u"{PHOTOS}",photo_tmp+u"{PHOTOS}")
						elif att['type']=='audio':
							coun_audio+=1
							audio_song= audio_song_template.replace(u"{AUTHOR}",att['audio']['performer']).replace(u"{NAME}",att['audio']['title'])	
							audio_html = audio_html.replace(u"{SONGS}",audio_song+u"{SONGS}")																																																													
						elif att['type']=='link':
							coun_link+=1
							link_templ=u'''<div class='link'><img src='vk_link.png' width = 20px>{LINK}</div>'''
							link_templ = link_templ.replace("{LINK}",att['link']['url'])
							other+=link_templ
						elif att['type']=='video':
								coun_video+=1
								video_tmpl=u'''<div class='audio' ><img src='vk_video.jpg' width = 20px> <font color=#5566FF face="ArialBlack" size=3>{TITLE}</font></div>'''
								video_tmpl = video_tmpl.replace("{TITLE}", att['video']['title'])
								videos_html = videos_html.replace("{VIDEOS}",	video_tmpl+"{VIDEOS}")			
						else:
							print att['type']
					audio_html = audio_html.replace(u"{SONGS}","")
					photos_html=photos_html.replace(u"{PHOTOS}","")
					videos_html=videos_html.replace(u"{VIDEOS}","")
					
					if(coun_photo>0):
						has_some = True
						other=other+photos_html
					if(coun_audio>0):
						has_some = True
						other=other+audio_html
					if(coun_video>0):
						other=other+videos_html
				if(com_count>0):
						post_id= post['id']
						print u"К посту",post_id,com_count,u"коментариев"
						comments_response = vk.method('wall.getComments', {'owner_id':"%s"%(id_group)
																			,'post_id':"%s"%(post_id)
																			,'sort':'asc'})
						time.sleep(sleep_time2)
						coments_block_html = coment_block_template
						for comment in comments_response[1:]:
							from_id =  comment['from_id']
							user_response = vk.method('users.get', {'uids':"%s"%(from_id)
																	,'fields':"photo"})
							time.sleep(sleep_time2)
							photo_coment = user_response[0]['photo']
							first_name = 	user_response[0]['first_name']
							last_name = 	user_response[0]['last_name']
							text = comment['text']
							coment_html = comment_template
							coment_html = coment_html.replace("{NAME_SURNAME}",first_name+" "+last_name)
							coment_html = coment_html.replace("{COMMENT_DATA}",text)
							coment_html = coment_html.replace("{PHOTO_COMMENT}",photo_coment)
							coments_block_html = coments_block_html.replace("{COMENTS}",coment_html+"{COMENTS}")
						coments_block_html = coments_block_html.replace("{COMENTS}","")
						other=other+coments_block_html							
				post_html = template_post
				post_html = post_html.replace(u"{GROUP_PHOTO}",user_photo)
				post_html = post_html.replace(u"{POST_DATA}",post_data)
				post_html = post_html.replace(u"{OTHER}",other)
				if(has_some):
					f.write(post_html.encode('utf-8'))
			except Exception as inst:
				print "error",inst
				logfile = open("log.txt",'a+')
				logfile.write("error"+str(inst))
				logfile.write("\n")
				logfile.close()
				time.sleep(1)
	f.close()
main()	
