#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# wget -B -k -r -l0 --force-html -i test.html  -P ./pics

import vk_auth
import vkontakte
import os
import re
import time
import getpass 
import shutil
import codecs	
from templates_html import *

from optparse import OptionParser
RECURSE_TRY = 100
FOLDER_RESULT = "../res/"
parser = OptionParser()
parser.add_option("-e", "--email", dest="email",
                  help=" user email", metavar="EMAIL")
parser.add_option("-p", "--passwd", dest="passwd",
                  help="user password", metavar="PASSWD")
parser.add_option("-i", "--groupid", dest="gid",
                  help="group or public ID", metavar="GID")
parser.add_option("-c", "--count", dest="count",
                  help="count of posts to load", metavar="COUNT")                 
parser.add_option("-f", "--offset", dest="offset",
                  help="Begin loading from OFFSET post", metavar="OFFSET")                 
parser.add_option("-s", "--split", dest="split",
                  help="Spliting on SPLIT_NUM html blocks", metavar="SPLIT_NUM")
parser.add_option("-a", "--app_id", dest="app_id",
                  help="Application Id", metavar="APP_ID")
parser.add_option("-d", "--download_all", dest="download_all",
                  help="if 1 then all information (pics,audios) will be downloaded", metavar="DOWNLOAD")
                  
(options, args) = parser.parse_args()  

def wall_getComments(vk,owner_id,post_id,count,offset=0,recurce = 0):
	if (recurce ==RECURSE_TRY):
		print "%s Failure"%"wall_getComments" 
		return []
	try:
		com  = vk.get('wall.getComments', owner_id=owner_id,post_id=post_id,count=count,offset=offset)
		if(recurce>0):
			print "%s Succes!"%"wall_getComments" 
	except:
		time.sleep(1)
		print "Error wall_getComments try ",recurce
		com = wall_getComments(vk,owner_id,post_id,count,recurce = recurce+1)
	return com
def wall_get(vk,owner_id,offset,count,recurce = 0):
	if (recurce ==RECURSE_TRY):
		print "%s Failure"%"wall_get" 
		return []
	try:		
		res = vk.get('wall.get', owner_id=owner_id,offset=offset,count=count)
		if(recurce>0):
			print "%s Succes!"%"wall_get" 
	except:
		time.sleep(1)
		print "Error wall_get try ",recurce
		res = wall_get(vk,owner_id,offset,count,recurce = recurce +1)
	return res
def users_get(vk,uids,fields,recurce = 0):
	if (recurce ==RECURSE_TRY):
		print "%s Failure"%"users_get" 
		return []
	try:
		res = vk.get('users.get',uids=uids,fields="photo")
		if(recurce>0):
			print "%s Succes!"%"users_get" 
	except:
		time.sleep(1)
		print "Error users_get try ",recurce
		res = users_get(vk,uids,fields,recurce = recurce +1)
	return res
def groups_getById(vk,group_ids,recurce = 0):
	if (recurce ==RECURSE_TRY):
		print "%s Failure"%"groups_getById" 
		return []
	try:
		res = vk.get('groups.getById', group_ids=group_ids)
		if(recurce>0):
			print "%s Succes!"%"groups_getById" 
	except:
		time.sleep(1)
		print "Error groups_getById try ",recurce
		res = groups_getById(vk,group_ids,recurce = recurce +1)
	return res

def convert_links(txt,folder):
	# txt is text, where links will be converved ( string)
	# folder is folder where will be all media . Must be Short path
	out = re.sub("http://",folder,txt)
	return out
def download_media(basename,folder):
	# basename is file name thats. you neet to read, path must be long
	# folder is folder where media will bee. path must be long
	print "Start downloading ",basename
	os_str = u"wget -B -k -r -l0 --force-html -i %s  -P ./%s"%(basename.replace(" ","\ "),folder.replace(" ","\ "))
	print os_str.encode('utf-8')
	os.system(os_str.encode('utf-8'))
def get_comments(vk,owner_id,post_id,count):
	size = 50
	comments = []
	if(count<size):
		com  = wall_getComments(vk,owner_id=owner_id,post_id=post_id,count=count)# vk.get('wall.getComments', owner_id=owner_id,post_id=post_id,count=count)
		comments += com[1:]
	else:
		offset = 0
		while(offset<count):
			com = wall_getComments(vk,owner_id=owner_id,post_id=post_id,count=size,offset=offset) # vk.get('wall.getComments', owner_id=owner_id,post_id=post_id,count=size,offset=offset)
			comments += com[1:]
			offset+=size
	return 	comments
	
def get_posts(vk,owner_id,offset,count):
	posts = wall_get(vk,owner_id=owner_id,offset=offset,count=count)
	for i in range(1,len(posts)):
		cur = posts[i]
		coments_count = posts[i]['comments']['count']
		if(coments_count>0):
			post_id = posts[i]['id']
			comments = get_comments(vk,owner_id,post_id,coments_count)
			posts[i]['comments']['data']=comments
	return posts


def posts_to_html(vk,posts):
	if (posts == None):
		return ""
	group_info = groups_getById(vk,group_ids=options.gid) #vk.get('groups.getById', group_ids=options.gid)
	name = group_info[0]["name"]
	i = 0
	posts_html = ""
	for post in posts[1:]:
		i+=1
		has_some = False # if there are some information in post
		post_id = post['id']
		post_data = post['text']
		user = post['from_id']
		com_count = post['comments']['count']
		other = "" # html of non text information 
		if(user<0):
			photo =  group_info[0]['photo_big']	
		else:
			user_photo= users_get(vk,uids=user,fields = 'photo')
			time.sleep(sleep_time2)
			if(len(user_photo)>0):
				photo =  ans[0]['photo_big']
			else:
				photo = ""
		if(len(post_data)>0):
			has_some = True
		if(post.has_key('attachments')):
			attachments = post['attachments']
			count_photo = 0
			count_audio = 0
			count_link  = 0
			count_video = 0
			photos_html = photos_template
			audio_html = audio_block_template
			videos_html=video_block_template
			for att in attachments:
				if att['type']=='photo':
							count_photo+=1
							photo_tmp = photo_templ
							photo_src = att['photo']['src_big']
							photo_tmp=photo_tmp.replace(u"{PHOTO_PATH}",""+photo_src)
							photos_html=photos_html.replace(u"{PHOTOS}",photo_tmp+u"{PHOTOS}")
							
				elif att['type']=='audio':
							count_audio+=1
							audio_song= audio_song_template.replace(u"{AUTHOR}",att['audio']['performer']).replace(u"{NAME}",att['audio']['title']).replace(u"{SONG_HREF}",att['audio']['url'])	
							audio_html = audio_html.replace(u"{SONGS}",audio_song+u"{SONGS}")		
				elif att['type']=='link':
							count_link+=1
							link_templ=u'''<div class='link'><img src='vk_link.png' width = 20px>{LINK}</div>'''
							link_templ = link_templ.replace("{LINK}",att['link']['url'])
							other+=link_templ
				elif att['type']=='video':
							count_video+=1
							video_tmpl=u'''<div class='audio' ><img src='vk_video.jpg' width = 20px> <font color=#5566FF face="ArialBlack" size=3>{TITLE}</font></div>'''
							video_tmpl = video_tmpl.replace("{TITLE}", att['video']['title'])
							videos_html = videos_html.replace("{VIDEOS}",	video_tmpl+"{VIDEOS}")			
				else:
						print att['type']
			audio_html = audio_html.replace(u"{SONGS}","")
			photos_html=photos_html.replace(u"{PHOTOS}","")
			videos_html=videos_html.replace(u"{VIDEOS}","")
				
			if(count_photo>0):
						has_some = True
						other=other+photos_html
			if(count_audio>0):
						has_some = True
						other=other+audio_html
			if(count_video>0):
						has_some = True
						other=other+videos_html
			
		if(com_count>0):
			coments_block_html = coment_block_template
			comments = []
			if(post['comments'].has_key("data")):
				comments = post['comments']['data']
			else:
				print "Some err"	
				try:
					comments = get_comments(vk,-int(options.gid),post_id,com_count)
					print "Err repaired"
				except:
					print "Some Error post = ",post_id,"comcount =", com_count
			for comment in comments[1:]:
				from_id =  comment['from_id']
				user_comment = users_get(vk,uids=from_id,fields="photo")# vk.get('users.get',uids=from_id,fields="photo")
				photo_coment = user_comment[0]['photo']
				first_name = 	user_comment[0]['first_name']
				last_name = 	user_comment[0]['last_name']
				text = comment['text']	
				coment_html = comment_template
				coment_html = coment_html.replace("{NAME_SURNAME}",first_name+" "+last_name)
				coment_html = coment_html.replace("{COMMENT_DATA}",text)
				coment_html = coment_html.replace("{PHOTO_COMMENT}",photo_coment)
				coments_block_html = coments_block_html.replace("{COMENTS}",coment_html+"{COMENTS}")
			coments_block_html = coments_block_html.replace("{COMENTS}","")
			other=other+coments_block_html
		post_html = template_post
		post_html = post_html.replace(u"{GROUP_PHOTO}",photo)
		post_html = post_html.replace(u"{POST_DATA}",post_data)
		post_html = post_html.replace(u"{OTHER}",other)
		posts_html = posts_html+post_html
	return posts_html
	

def main():
	
	if (options.gid == None):
		print "set group id ( use -h for help) "
		exit(1)
	if (options.email == None):
		print "set Email ( use -h for help ) "
		exit(1)
	if (options.passwd == None):
		options.passwd  = getpass.getpass("Enter your password:")
	if (options.app_id == None):
		options.app_id = '3715935'
	if(options.split == None):
		options.split = '1'
	if(options.offset == None):
		options.offset = '0'
	if(options.download_all == None):
		options.download_all = '0'
	greeting = u'''Program will load %s posts from %s public, begining from %s post and split it on %s html blocks . 
Auth data:
	email: %s 
	passwd: %s 
	app id: %s '''%(options.count,options.gid,options.offset,options.split,options.email,"*"*len(options.passwd),options.app_id)
	print greeting
	(token,user_id) = vk_auth.auth(options.email, options.passwd, options.app_id, 'friends')
	vk = vkontakte.API(token=token)
	server_time = vk.getServerTime() #check working
	if(server_time):
		group_info = groups_getById(vk,group_ids=options.gid)
		name = group_info[0]["name"]
		print "Auth is success, for ",name
		try:
			os.mkdir(FOLDER_RESULT+name) # make the directory with the name of the publick

		except (OSError):
			print "Directory Exist"
		ava = "ava.jpg"
		vk_link = "vk_link.png"
		vk_audio = "vk_audio.jpg"
		vk_video =  "vk_video.jpg"
		shutil.copyfile(FOLDER_SERVICE+ava,FOLDER_RESULT+"%s/%s"%(name,ava))
		shutil.copyfile(FOLDER_SERVICE+vk_link,FOLDER_RESULT+"%s/%s"%(name,vk_link))
		shutil.copyfile(FOLDER_SERVICE+vk_video,FOLDER_RESULT+"%s/%s"%(name,vk_video))
		shutil.copyfile(FOLDER_SERVICE+vk_audio,FOLDER_RESULT+"%s/%s"%(name,vk_audio))
		if(options.count == None):
			temp = get_posts(vk,-int(options.gid),0,1)
			print "Post count = ",temp[0]
			count = temp[0]
		else:
			count = int(options.count) 
		tom_count = int(options.split)
		offset = int(options.offset)# frow where gell posts. This value will be chaged by iterations 
		posts_by_tom = count/tom_count 
		iteration = 0 #global iteration
		curr_tom = 0
		iteration = 1
		tom_iteration = 0 # curr count of posts in current tom
		step = 90
		downloaded = 0
		print posts_by_tom
		name_tom = "%s_%i.html"%(name,curr_tom)
		tom_file = open(FOLDER_RESULT+"%s/%s"%(name,name_tom),'w+') # open first tom file
		tom_file.write(page_begin.encode('utf-8'))
		while(iteration*step < count):		
			if(tom_iteration*step>=posts_by_tom):
				tom_file.close()
				tom_iteration = 0;
				curr_tom+=1
				name_tom = "%s_%i.html"%(name,curr_tom)
				tom_file = open(FOLDER_RESULT+"%s/%s"%(name,name_tom),'w+') # open cur tom file
				tom_file.write(page_begin.encode('utf-8'))			
			posts = get_posts(vk,-int(options.gid),offset,step)
			downloaded+=len(posts)-1
			print "Скачано:",downloaded
			posts_html = posts_to_html(vk,posts)
			tom_file.write(posts_html.encode('utf-8'))
			iteration +=1
			tom_iteration +=1
			offset+=step
		tom_file.close()
		
		if(options.download_all =='1'):
			for i in range(curr_tom+1):
				name_cur = "%s_%i.html"%(name,i)
				long_name = FOLDER_RESULT+"%s/%s"%(name,name_cur)
				folder = "%s_%sdata/"%(name,i)
				long_folder = FOLDER_RESULT+"%s/%s"%(name,folder)
				tom_file =  codecs.open(long_name, "r", "utf-8")
				converted = FOLDER_RESULT+"%s/%s_%s_converted.html"%(name,name,i)
				print converted
				converted = open(converted,'w+')
				data = tom_file.read()
				download_media(long_name,FOLDER_RESULT+"%s/%s"%(name,folder))
				new_data = convert_links(data,"./%s"%folder)
				#tom_file.seek(0)
				converted.write(new_data.encode("utf-8"))
				tom_file.close()
				converted.close()
	return 0 	

if __name__ == '__main__':
	main()
