from rcmd_func import dbConnection as database
from rcmd_func import youtube_api as YT
from rcmd_func import dataProcessor

import sys
import numpy as np
import pandas as pd
import time
from operator import itemgetter
import random
from collections import OrderedDict


MyDB = database.MyDB('address', port, 'id','pw','db_name')

class InsufficiencyException(Exception) :
	pass




def main(user_num) :

	RECOMMEND_VIDEO_LIST = []

	active_user_data = dataProcessor.get_active_user_data(user_num)

	ac_user_sex = active_user_data.iloc[0]['sex']
	ac_user_bodypart = active_user_data.iloc[0]['bodypart']
	ac_user_hp = active_user_data.iloc[0]['health_point']
	ac_user_label = active_user_data.iloc[0]['label']

	ac_user_level = ''

	if ac_user_sex == 'f' :

		if ac_user_hp >= 40 :
			ac_user_level = 'h'
		elif ac_user_hp < 40 and ac_user_hp >= 33 :
			ac_user_level = 'm'
		else :
			ac_user_level = 'l'

	else :

		if ac_user_hp >= 50 :
			ac_user_level = 'h'
		elif ac_user_hp < 50 and ac_user_hp >= 44 :
			ac_user_level = 'm'
		else :
			ac_user_level = 'l'

	# user_data don't have 'dc' value.
	ac_user_bodypart = [ac_user_bodypart] + ['dc']
	ac_user_sex = [ac_user_sex] + ['dc']
	ac_user_level = [ac_user_level] + ['dc']

	MyDB.dic_execute('select * from HISTORY')
	history_db = MyDB.dic_fetchall()
	
	# if history_db return empty set
	if not history_db :
		MyDB.execute('select url from ROUTINE where bodypart in %s and sex in %s and level in %s'
			%(str(tuple(ac_user_bodypart)), str(tuple(ac_user_sex)), str(tuple(ac_user_level))))
		same_cate_video = MyDB.fetchall()

		MyDB.execute('select url from EXERCISE where bodypart in %s and sex in %s and level in %s'
			%(str(tuple(ac_user_bodypart)), str(tuple(ac_user_sex)), str(tuple(ac_user_level))))
		same_cate_video += MyDB.fetchall()

		same_cate_video_list = {i[0] for i in same_cate_video}
		same_cate_video_list = list(same_cate_video_list)

		selected_video_url = sorted(same_cate_video_list, key=lambda k: random.random())[:15]
		RECOMMEND_VIDEO_LIST += YT.youtube_rating_sort(selected_video_url)


	else :
		history_db_df = pd.DataFrame(history_db)
		# have no errors
		default_crosstab = pd.crosstab(history_db_df.user_num, history_db_df.video_num)

		# convert nonzero value to 1
		for i in default_crosstab.index :
			default_crosstab.loc[default_crosstab.index == i] = default_crosstab.where(default_crosstab.loc[default_crosstab.index == i] == 0,1)


		# case 1 : default_crosstab don't have active_user's history

		if default_crosstab.loc[default_crosstab.index == int(user_num)].empty :
			# if you want to recommend less 15, change value 15 -> v
			if len(default_crosstab.columns) < 15 :
				semi_recommend = pd.DataFrame(0, index=['total'], columns = default_crosstab.columns)

				for i in default_crosstab.columns :
					semi_recommend.loc['total'][i] = default_crosstab[i].sum()

				semi_recommend = semi_recommend.sort_values(by='total', ascending=False, axis=1)
				semi_recommend_list = []

				for i in semi_recommend.columns :
					semi_recommend_list.append(i)

				for i in semi_recommend_list :
					MyDB.execute('select url from ROUTINE where video_num = %s UNION select url from EXERCISE where video_num = %s' %(str(i), str(i)))
					temp_url = MyDB.fetchone()[0]
					RECOMMEND_VIDEO_LIST.append(temp_url)

				
				# ============= append more random url list -> change list size if you want============

				MyDB.execute('select url from ROUTINE where bodypart in %s and sex in %s and level in %s'
					%(str(tuple(ac_user_bodypart)), str(tuple(ac_user_sex)), str(tuple(ac_user_level))))
				same_cate_video = MyDB.fetchall()

				MyDB.execute('select url from EXERCISE where bodypart in %s and sex in %s and level in %s'
					%(str(tuple(ac_user_bodypart)), str(tuple(ac_user_sex)), str(tuple(ac_user_level))))
				same_cate_video += MyDB.fetchall()

				same_cate_video_list = {i[0] for i in same_cate_video}
				same_cate_video_list = list(same_cate_video_list)

				selected_video_url = sorted(same_cate_video_list, key=lambda k: random.random())[:15]
				RECOMMEND_VIDEO_LIST += YT.youtube_rating_sort(selected_video_url)
				# =====================================================================================


			else :
				# video_list's len > 15
				# add active_user's watching rate(all zero) into the crosstab to add weight
				default_crosstab = default_crosstab.append(pd.DataFrame(0, index=[user_num], columns = default_crosstab.columns))

				# add_weight : input=crosstab, output = weighted crosstab
				# add weight to video by active user's attribute and same label user's history
				weighted_crosstab = dataProcessor.add_weight(default_crosstab, active_user_data)

				# N : return recommend video, K = decomposition matrix size
				# Adjust K value to find the optimum matrix size
				row_size = default_crosstab.shape[0]
				k = int((row_size/3)*2)

				RECOMMEND_VIDEO_LIST += dataProcessor.SVD_recommend(default_crosstab, weighted_crosstab, user_num, K = k, N = 10)


		else :
			# case 2 : default_crosstab have active user data == active user has seen some video.

			MyDB.execute('select user_num from USER where label = ' + str(ac_user_label))
			same_user_group = MyDB.fetchall()
			same_user_group = [i[0] for i in same_user_group]

			other_user_group = [x for x in default_crosstab.index if x not in same_user_group]
			reduced_size_crosstab = default_crosstab.drop(index = other_user_group)


			if len(reduced_size_crosstab.columns) < 15 :

				reduced_semi_recommend = pd.DataFrame(0, index = ['total'], columns = reduced_size_crosstab.columns)

				for i in reduced_size_crosstab.columns :
					reduced_semi_recommend.loc['total', i] = reduced_size_crosstab[i].sum()

				reduced_semi_recommend = reduced_semi_recommend.sort_values(by='total', ascending=False, axis=1)
				reduced_semi_recommend_list = []
	
				for i in reduced_semi_recommend.columns :
					reduced_semi_recommend_list.append(i)

				for i in reduced_semi_recommend_list :
					MyDB.execute('select url from ROUTINE where video_num = %s UNION select url from EXERCISE where video_num = %s' %(str(i), str(i)))
					RECOMMEND_VIDEO_LIST += MyDB.fetchone()

				# ============= append more random url list -> change list size if you want============
				MyDB.execute('select url from ROUTINE where bodypart in %s and sex in %s and level in %s'
					%(str(tuple(ac_user_bodypart)), str(tuple(ac_user_sex)), str(tuple(ac_user_level))))
				same_cate_video = MyDB.fetchall()

				MyDB.execute('select url from EXERCISE where bodypart in %s and sex in %s and level in %s'
					%(str(tuple(ac_user_bodypart)), str(tuple(ac_user_sex)), str(tuple(ac_user_level))))
				same_cate_video += MyDB.fetchall()

				same_cate_video_list = {i[0] for i in same_cate_video}
				same_cate_video_list = list(same_cate_video_list)

				selected_video_url = sorted(same_cate_video_list, key=lambda k: random.random())[:15]
				RECOMMEND_VIDEO_LIST += YT.youtube_rating_sort(selected_video_url)

				# =====================================================================================


			else :
				row_size = default_crosstab.shape[0]
				k = int((row_size/3)*2)

				weighted_crosstab = dataProcessor.add_weight(default_crosstab, active_user_data)
				RECOMMEND_VIDEO_LIST += dataProcessor.SVD_recommend(default_crosstab, weighted_crosstab, user_num, K = k, N = 10)

	RECOMMEND_VIDEO_LIST = list(OrderedDict.fromkeys(RECOMMEND_VIDEO_LIST))
	for i in RECOMMEND_VIDEO_LIST[:10] :
		print(i)





if __name__ == '__main__' :
	
	USER_NUM = sys.argv[1]
	start = time.time()
	main(USER_NUM)
	end = time.time()
	print(end-start)