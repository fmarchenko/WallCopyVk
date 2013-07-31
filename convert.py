#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
def convert_links(txt,folder):
	# txt is text, where links will be converved ( string)
	# folder is folder where will be all media . Must be Short path
	
	out = re.sub("http://",folder,txt)
	return out
	
for i in range(13):
				name = "Евгений Онегин: Глава 11"
				name_cur = "%s_%i.html"%(name,i)
				long_name = "%s/%s"%(name,name_cur)
				folder = "%s_%sdata/"%(name,i)
				long_folder = "%s/%s"%(name,folder)
				tom_file = open(long_name,"r+")
				data = tom_file.read()
				download_media(long_name,"%s/%s"%(name,folder))
				converted = open(long_name+"converted","w+")
				new_data = convert_links(data,"./%s"%folder)
				#tom_file.seek(0)
				converted.write(new_data)
				tom_file.close()
				converted.close()
