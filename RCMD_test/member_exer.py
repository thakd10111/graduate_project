from rcmd_func import dbConnection as database
from rcmd_func import youtube_api as YT
from rcmd_func import dataProcessor

import sys
import numpy as np
import pandas as pd
import time
from operator import itemgetter
import random



MyDB = database.MyDB('address', port, 'id','pw','db_name')



# parameter order from php : user_num, length, bodypart, exer_type, trainer, equipment, timing, level

def main(user_num, length, bodypart, excer_type, trainer, equipment, timing, level) :

	# convert string to list type

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
	

	active_user_data = dataProcessor.get_active_user_data(user_num)

	MyDB.execute(sql)
	exercise_vid_num = list(MyDB.fetchall())

	exercise_vid_num_list = {i[0] for i in exercise_vid_num}
	exercise_vid_num_list = list(exercise_vid_num_list)

	RECOMMEND_LIST = []

	if len(exercise_vid_num_list) < 15 :
		ac_user_num = active_user_data.iloc[0]['user_num']
		
		MyDB.execute('select video_num from HISTORY where user_num = ' + str(ac_user_num))
		ac_users_history = MyDB.fetchall()

		ac_users_vid_list = {i[0] for i in ac_users_history}
		ac_users_vid_list = list(ac_users_vid_list)

		if not ac_users_vid_list :
			# if ac_users doesn't see anything
			MyDB.execute('select url from EXERCISE where video_num in ' + str(tuple(exercise_vid_num_list)))
			exercise_url = MyDB.fetchall()

			exercise_url_list = {i[0] for i in exercise_url}
			exercise_url_list = list(exercise_url_list)

			RECOMMEND_LIST += YT.youtube_rating_sort(exercise_url_list)

		else :
			# if ac_users have history data
			video_similarity = dataProcessor.jaccard_similarity(ac_users_vid_list, exercise_vid_num_list)
			top_video_list = dataProcessor.v2v_top_k_video(video_similarity, 15)

			MyDB.execute('select url from EXERCISE where video_num in ' + str(tuple(top_video_list)))
			video_url = list(MyDB.fetchall())

			video_url_list = {i[0] for i in video_url}
			video_url_list = list(video_url_list)

			RECOMMEND_LIST += YT.youtube_rating_sort(video_url_list)

	else :
		MyDB.dic_execute('select * from HISTORY where video_num in ' + str(tuple(exercise_vid_num_list)))
		history_db = MyDB.dic_fetchall()

		if not history_db : 
			# if history_db_query return empty set, you can't make dataframe
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

			# selected attribute video not played yet.
			# best case -> same len
			if len(exercise_vid_num_list) != len(default_crosstab.columns.values) :
				# add not played video column to default_df, all value is zero.
				for i in exercise_vid_num_list :
					if i not in default_crosstab.columns.values :
						temp_df = pd.DataFrame(0, index = default_crosstab.index.values, columns = [i])
						default_crosstab = default_crosstab.join(temp_df)

				default_crosstab = default_crosstab.sort_index(axis=1)


			if user_num not in default_crosstab.index.values :

				default_crosstab = default_crosstab.append(pd.DataFrame(0, index = [user_num], columns = default_crosstab.columns))
				default_crosstab = default_crosstab.sort_index(axis=0)
				
				row_size = default_crosstab.shape[0]
				k = int((row_size/3)*2)

				weighted_crosstab = dataProcessor.add_weight(default_crosstab, active_user_data)
				RECOMMEND_LIST += dataProcessor.SVD_recommend(origin_crosstab, weighted_crosstab, user_num, K = k, N = 10)



			else :
				row_size = default_crosstab.shape[0]
				k = int((row_size/3)*2)

				weighted_crosstab = dataProcessor.add_weight(default_crosstab, active_user_data)
				RECOMMEND_LIST += dataProcessor.SVD_recommend(default_crosstab, weighted_crosstab, user_num, K = k, N = 10)


	for i in RECOMMEND_LIST :
		print(i)



if __name__ == '__main__' :
	USER_NUM = int(sys.argv[1])
	LENGTH = sys.argv[2]
	BODYPART = sys.argv[3]
	EXCER_TYPE = sys.argv[4]
	TRAINER = sys.argv[5]
	EQUIPMENT = sys.argv[6]
	TIMING = sys.argv[7]
	LEVEL = sys.argv[8]

	main(USER_NUM, LENGTH, BODYPART,EXCER_TYPE, TRAINER, EQUIPMENT, TIMING, LEVEL)