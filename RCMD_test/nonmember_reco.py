from rcmd_func import dbConnection as database
from rcmd_func import youtube_api as YT
from rcmd_func import dataProcessor

from datetime import datetime, timedelta
import time
import random
import pandas as pd
import numpy as np
import sys

MyDB = database.MyDB('address', port, 'id','pw','db_name')

 # $time_gap -> parameter from php (i want...)

def main() :
	now = datetime.now()

	# Setting timegap days = 1~14
	timegap = timedelta(days=10)
	now = now.date() - timegap

	MyDB.execute('select video_num from HISTORY where time >= \'%s\'' %now)
	recent_video = list(MyDB.fetchall())

	recent_video_list = {i[0] for i in recent_video}
	recent_video_list = list(recent_video_list)

	MyDB.execute('select video_num from ROUTINE UNION select video_num from EXERCISE')
	all_video = list(MyDB.fetchall())

	all_video_list = {i[0] for i in all_video}
	all_video_list = list(all_video_list)

	# Empty set case
	if not recent_video_list :

		MyDB.execute('select url from ROUTINE UNION select url from EXERCISE')
		all_video_url = list(MyDB.fetchall())

		all_video_url_list = {i[0] for i in all_video_url}
		all_video_url_list = list(all_video_url_list)


		selected_video_url = sorted(all_video_url_list, key=lambda k: random.random())[:15]

		recommend_video_list = YT.youtube_rating_sort(selected_video_url)


	else :

		# Warning !!
		# if recent_video_list == all_video_list, all data will discared in v2v_top_k_video function

		video_similarity = dataProcessor.jaccard_similarity(recent_video_list, all_video_list)
		top_video_list = dataProcessor.v2v_top_k_video(video_similarity, 10)

		MyDB.execute('select url from ROUTINE where video_num in %s UNION select url from EXERCISE where video_num in %s' %(str(tuple(top_video_list)), str(tuple(top_video_list))))
		video_url = list(MyDB.fetchall())

		video_url_list = {i[0] for i in video_url}
		video_url_list = list(video_url_list)

		recommend_video_list = YT.youtube_rating_sort(video_url_list)

	for i in recommend_video_list :
		print(i)


if __name__ == '__main__' :
	main()