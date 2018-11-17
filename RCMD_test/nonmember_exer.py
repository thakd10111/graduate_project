# data input from php : $length $part ($exer_type $trainer $equipment) $timing $level

from rcmd_func import dbConnection as database
from rcmd_func import youtube_api as YT
from rcmd_func import dataProcessor

import random
import pandas as pd
import numpy as np
import sys
import time

MyDB = database.MyDB('address', port, 'id','pw','db_name')

def main(length, bodypart, excer_type, trainer, equipment, timing, level) :

	# convert string to list type
	# 5, 10, 15, 20, 40, 60
	length = int(length)

	if length == 5 :
		front_length = 0
		end_length = 6

	elif length == 10 :
		front_length = 7
		end_length = 12

	elif length == 15 :
		front_length = 13
		end_length = 17

	elif length == 20 :
		front_length = 18
		end_length = 29

	elif length == 40 :
		front_length = 30
		end_length = 49

	elif length == 60 :
		front_length = 50
		end_length = 240

	else :
		# user don't select length
		front_length = 0
		end_length = 240

	sql = ('select video_num from EXERCISE where length between %s and %s' %(str(front_length), str(end_length))) + ' and '

	if bodypart != 'dc' :
		sql += ('bodypart in %s' %(str(tuple([bodypart]+['dc'])))) + ' and '


	if excer_type != 'dc' :
		sql += ('excer_type in %s' %(str(tuple([excer_type]+['dc'])))) + ' and '


	if trainer != 'dc' :
		sql += ('trainer in %s' %(str(tuple([trainer]+['dc'])))) + ' and '


	if equipment != 'dc' :
		sql += ('equipment in %s' %(str(tuple([equipment]+['dc'])))) + ' and '


	if timing != 'dc' :
		sql += ('timing in %s' %(str(tuple([timing]+['dc'])))) + ' and '


	if level != 'dc' :
		sql += ('level = \''+level+'\'') + ' and '


	sql = sql[:-5]

	# Assume you have enough data (at least one...)

	MyDB.execute(sql)
	exercise_vid_num = list(MyDB.fetchall())

	exercise_vid_num_list = {i[0] for i in exercise_vid_num}
	exercise_vid_num_list = list(exercise_vid_num_list)

	RECOMMEND_LIST = []

	if len(exercise_vid_num_list) < 15 :

		MyDB.execute('select url from EXERCISE where video_num in ' + str(tuple(exercise_vid_num_list)))

		exercise_url = MyDB.fetchall()
		exercise_url_list = {i[0] for i in exercise_url}
		exercise_url_list = list(exercise_url_list)

		RECOMMEND_LIST += YT.youtube_rating_sort(exercise_url_list)

	# number of video list >= 15
	else :
		MyDB.dic_execute('select * from HISTORY where video_num in ' + str(tuple(exercise_vid_num_list)))
		history_db = MyDB.dic_fetchall()

		if not history_db :
			# if history_db query return empty set, you can't make dataframe
			MyDB.execute('select url from EXERCISE where video_num in ' + str(tuple(exercise_vid_num_list)))
			exercise_url = MyDB.fetchall()

			exercise_url_list = {i[0] for i in exercise_url}
			exercise_url_list = list(exercise_url_list)

			selected_video_url = sorted(exercise_url_list, key=lambda k: random.random())[:15]
			RECOMMEND_LIST += YT.youtube_rating_sort(selected_video_url)

		else :
			# have no errors

			history_db_df = pd.DataFrame(history_db)
			default_crosstab = pd.crosstab(history_db_df.user_num, history_db_df.video_num)

			# convert nonzero value to 1
			for i in default_crosstab.index :
				default_crosstab.loc[default_crosstab.index == i] = default_crosstab.where(default_crosstab.loc[default_crosstab.index == i] == 0,1)

			semi_recommend = pd.DataFrame(0, index=['total'], columns = default_crosstab.columns)

			for i in default_crosstab.columns :
				semi_recommend.loc['total'][i] = default_crosstab[i].sum()

			semi_recommend = semi_recommend.sort_values(by='total', ascending=False, axis=1)
			semi_recommend_list = []

			for i in semi_recommend.columns :
				semi_recommend_list.append(i)

			for i in semi_recommend_list :
				MyDB.execute('select url from EXERCISE where video_num = ' + str(i))
				RECOMMEND_LIST += MyDB.fetchone()

			if len(RECOMMEND_LIST) < 15 :
				MyDB.execute('select url from EXERCISE where video_num in ' + str(tuple(exercise_vid_num_list)))
				exercise_url = MyDB.fetchall()

				exercise_url_list = {i[0] for i in exercise_url}
				exercise_url_list = list(exercise_url_list)

				selected_video_url = sorted(exercise_url_list, key=lambda k: random.random())[:15]

				temp_yt_url = YT.youtube_rating_sort(selected_video_url)
				temp_yt_url = [x for x in temp_yt_url if x not in RECOMMEND_LIST]

				RECOMMEND_LIST += temp_yt_url
				RECOMMEND_LIST = RECOMMEND_LIST[:15]


	for i in RECOMMEND_LIST :
		print(i)



if __name__ == '__main__' :
	LENGTH = sys.argv[1]
	BODYPART = sys.argv[2]
	EXCER_TYPE = sys.argv[3]
	TRAINER = sys.argv[4]
	EQUIPMENT = sys.argv[5]
	TIMING = sys.argv[6]
	LEVEL = sys.argv[7]

	main(LENGTH, BODYPART, EXCER_TYPE, TRAINER, EQUIPMENT, TIMING, LEVEL)