#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
<div class='audio' ><img src='vk_audio.jpg' width = 20px>
<a href="{SONG_HREF}">
<font color=#5566FF face="ArialBlack" size=3>{AUTHOR}</font>- 
{NAME}(Марина Цветаева)
</a>
</div>	
'''


photo_templ=u'''
<div class='photo' >
<a href = '{PHOTO_PATH}'>
						<img class ='photo' hspace="5" vspace="5" src='{PHOTO_PATH}' >
</a>						
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

