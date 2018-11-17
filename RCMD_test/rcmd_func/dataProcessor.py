from . import dbConnection as database
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
from scipy.spatial import distance
from sklearn.metrics import jaccard_similarity_score
from operator import itemgetter
import random
import sklearn
import scipy.stats
from scipy.sparse.linalg import svds
from sklearn.metrics import mean_absolute_error
import math
from math import sqrt


MyDB = database.MyDB('address', port, 'id','pw','db_name')

# example : 
# mydb.dic_execute('select * from USER where user_num = '+str(1))
# MyDB.execute('select * from USER where user_num = 1')
# A = mydb.dic_fetchall()
# changed USER table : user_num sex  age bodypart  health_point  label

def get_active_user_data (user_id) :
    # if serve PROCESSED DATA into Database, don't need CURSOR query
    MyDB.dic_execute('select * from USER where user_num = ' + str(user_id))
    active_user_data = MyDB.dic_fetchall()

    active_user_data_df = pd.DataFrame(active_user_data)
    
    return active_user_data_df


# if you add some attribute into the database, modify dictionary.
def convert_cate_num(x) :
	return {'thigh':1, 'chest':2, 'arm':3, 'hip':4, 'leg':5, 'back_arm':6, 'belly':7, 'front_arm':8, 'waist':9, 'side neck':10, 
			'upper':11, 'back':12, 'calf':13, 'side':14, 'shoulder':15, 'whole':16, 'lower':17, 'pec_dec_fly':18, 'babell':19, 
			'leg_press':20, 'gym_ball':21, 'leg_extension':22, 'shoulder_press':23, 'chest_press':24, 'cable':25, 'leg_curl':26,
			'dumbbell':27, 'butterfly':28, 'bench_press':29, 'latpull_down':30, 'abdominal_machine':31, 'treadmill':32, 'lifting_strap':33, 'foam_roller':34,
			'stretching':35, 'circuit':36, 'weight':37, 'interval':38, 'm':39, 'h':40, 'l':41, 'overeating':42, 'daily':43, 'morning':44,'scene_stealer':45,
			'denial':46, 'kanghana':47, 'tiffany_rothe':48, 'rebecca_louise':49, 'juwon_HT':50, 'cash_ho':51, 'dano':52, 'dc':53}.get(x, 0)

			# add -- equipment : lifting_strap, formroller | trainer : dano_TV


def jaccard_similarity(row_video, col_video) :

	"""
	jaccard_similarity : J(X,Y) = |X∩Y| / |X∪Y|
	input result into dataframe and return that.

	"""

	similarity_result = np.zeros((len(row_video), len(col_video)))

	similarity_result = np.column_stack((row_video, similarity_result))

	temp_col = [np.nan] + col_video
	similarity_result = np.row_stack((temp_col, similarity_result))


	# criteria video's data to dataframe
	MyDB.dic_execute('select * from ROUTINE where video_num in ' + str(tuple(row_video)))
	row_video_tuple = list(MyDB.dic_fetchall())

	MyDB.dic_execute('select * from EXERCISE where video_num in ' + str(tuple(row_video)))
	row_video_tuple += list(MyDB.dic_fetchall())

	row_video_df = pd.DataFrame(row_video_tuple)


	#compared video's data to dataframe

	MyDB.dic_execute('select * from ROUTINE where video_num in ' + str(tuple(col_video)))
	col_video_tuple = list(MyDB.dic_fetchall())

	MyDB.dic_execute('select * from EXERCISE where video_num in ' + str(tuple(col_video)))
	col_video_tuple += list(MyDB.dic_fetchall())

	col_video_df = pd.DataFrame(col_video_tuple)

	# EXERCISE and ROUTINE table have different size of columns.
	# So, make same size of matrix to calculate jaccard distance

	if len(row_video_df.columns) == 7:
		row_video_df.insert(loc=1, column='equipment', value=np.zeros((len(row_video_df), 1)))
		row_video_df.insert(loc=2, column='excer_type', value=np.zeros((len(row_video_df), 1)))
		row_video_df.insert(loc=7, column='trainer', value=np.zeros((len(row_video_df), 1)))
	
	if len(col_video_df.columns) == 7:
		col_video_df.insert(loc=1, column='equipment', value=np.zeros((len(col_video_df), 1)))
		col_video_df.insert(loc=2, column='excer_type', value=np.zeros((len(col_video_df), 1)))
		col_video_df.insert(loc=7, column='trainer', value=np.zeros((len(col_video_df), 1)))


	# all row_video data convert to number
	for i in row_video_df.columns.values :
		if i=='length' or i=='url' or i=='video_num' :
			continue;

		# sex = 'f' or 'm', but 'm' is overlapped dataType of level column.
		elif i=='sex' :
			for j, v in row_video_df[i].items():
				if v=='f':
					row_video_df.loc[j, i] = 51
				elif v=='m' :
					row_video_df.loc[j, i] = 52
				else :
					s = convert_cate_num(v)
					row_video_df.loc[j, i] = s
		else :
			for j, v in row_video_df[i].items():
				s = convert_cate_num(v)
				row_video_df.loc[j, i] = s


	# all column_video data convert to number
	for i in col_video_df.columns.values :
		if i=='length' or i=='url' or i=='video_num' :
			continue;

		elif i=='sex' :
			for j, v in col_video_df[i].items() :
				if v=='f' :
					col_video_df.loc[j, i] = 51
				elif v=='m' :
					col_video_df.loc[j, i] = 52
				else :
					s = convert_cate_num(v)
					col_video_df.loc[j, i] = s

		else :
			for j, v in col_video_df[i].items():
				s = convert_cate_num(v)
				col_video_df.loc[j, i] = s


	row_video_df = row_video_df.sort_values(by=['video_num'])
	col_video_df = col_video_df.sort_values(by=['video_num'])

	for i in range(len(row_video)-1) :

		temp_row_value = row_video_df.iloc[i].values

		for j in range(len(col_video)) :
			temp_col_value = col_video_df.iloc[j].values
			similarity_result[i+1, j+1] = 1 - distance.jaccard(temp_row_value, temp_col_value)


	similarity_result = pd.DataFrame(similarity_result[1:, 1:], index = similarity_result[1:, 0], columns = similarity_result[0, 1:])


	return similarity_result


def v2v_top_k_video(rating_df, k) :
	
	#each column's max rate
	top_rate_df = pd.DataFrame(0, index=['top_rate'], columns = rating_df.columns)
	top_rate_df.loc['top_rate'] = pd.DataFrame(rating_df.idxmax()).T.values[0]

	top_rate_df = top_rate_df.sort_values(by = 'top_rate', ascending=False, axis=1)

	recommend_list = list(top_rate_df.columns.values)
	recommend_list = [x for x in recommend_list if x not in rating_df.index]

	return recommend_list[:k]


def add_weight(user_to_video_crosstab, active_user_data) :
	# add_weight : input = crosstab, output = weighted crosstab
	active_user_data_attribute = []

	ac_user_num = active_user_data.iloc[0]['user_num']
	ac_user_sex = active_user_data.iloc[0]['sex']
	ac_user_hp = active_user_data.iloc[0]['health_point']
	ac_user_label = active_user_data.iloc[0]['label']

	if ac_user_sex == 'f' :
		active_user_data_attribute += [51]
		if ac_user_hp >= 40 :
			active_user_data_attribute += [convert_cate_num('h')]
		elif ac_user_hp < 40 and ac_user_hp >= 33:
			active_user_data_attribute += [convert_cate_num('m')]
		else :
			active_user_data_attribute += [convert_cate_num('l')]

	else :
		active_user_data_attribute += [52]
		if ac_user_hp >= 50 :
			active_user_data_attribute += [convert_cate_num('h')]
		elif ac_user_hp < 50 and ac_user_hp >=44 :
			active_user_data_attribute += [convert_cate_num('m')]
		else :
			active_user_data_attribute += [convert_cate_num('l')]

	active_user_data_attribute += [convert_cate_num(active_user_data.iloc[0]['bodypart'])]
	# active_user_data_attribute = [sex, level, bodypart] -> compared with video attribute


	vid_weight_exponent = pd.DataFrame(0, index=['weight_num'], columns=user_to_video_crosstab.columns)

	for i in vid_weight_exponent.columns :
		MyDB.execute('select sex, level, bodypart from ROUTINE where video_num = %s UNION select sex, level, bodypart from EXERCISE where video_num = %s' %(str(i), str(i)))
		attribute_list = list(MyDB.fetchone())
		# ['sex', 'level', 'bodypart']

		for j in range(3) :
			if j==0 :
				if attribute_list[j] == 'm' :
					attribute_list[j] = 52
				elif attribute_list[j] == 'f' :
					attribute_list[j] = 51
				else :
					attribute_list[j] = convert_cate_num(attribute_list[j])
			else :
				attribute_list[j] = convert_cate_num(attribute_list[j])

		vid_weight_exponent.loc['weight_num', i] = vid_weight_exponent.iloc[0][i] + 3 - jaccard_similarity_score(active_user_data_attribute, attribute_list, normalize=False)

	
	for i in vid_weight_exponent.columns :
		n = vid_weight_exponent.loc['weight_num'][i]
		# arithmetic sequence = a_n
		# a_n+1 = a_n * 0.8 + 0.3 (not more than 1.5)
		a_n = 1.5 - (0.4 * (0.8 ** (n-1)))

		if n==0 :
			vid_weight_exponent.loc['weight_num', i] = 0.3
		else :
			vid_weight_exponent.loc['weight_num', i] = a_n


		user_to_video_crosstab.loc[:, i] += vid_weight_exponent.loc['weight_num'][i]



	MyDB.execute('select user_num from USER where label = ' + str(ac_user_label))
	same_label_user = MyDB.fetchall()
	same_label_user = [i[0] for i in same_label_user]

	for i in user_to_video_crosstab.index :
		if i in same_label_user :
			user_to_video_crosstab.loc[i] += 0.3


	# weight to video watched 7 days ago
	temp_time = datetime.now()
	timegap = timedelta(days=7)
	temp_time = temp_time.date() - timegap

	MyDB.execute('select video_num from HISTORY where user_num = ' + str(ac_user_num) + ' and time >= \'%s\'' %temp_time)
	watched_video = MyDB.fetchall()
	watched_Video = [i[0] for i in watched_video]

	for i in user_to_video_crosstab.columns : 
		if i in watched_video :
			user_to_video_crosstab.loc[:, i] += 0.1


	return user_to_video_crosstab



def RMSE(origin_data, calculated_data) :
	# RMSE = [sum((Zo - Zp)^2) / N] ^ (1/2)

	o = origin_data.flatten()
	c = calculated_data.flatten()

	sqrt_array = (o - c)**2
	s = sqrt_array.sum()
	rmse = math.sqrt(s / float(len(o)))

	return rmse

def MAE(origin_data, calculated_data) :
	return mean_absolute_error(origin_data, calculated_data)


def SVD_recommend(origin_crosstab, weighted_crosstab, user_id, K, N) :

	W = weighted_crosstab.as_matrix()

	user_ratings_mean = np.mean(W, axis = 1)
	W_demeaned = W - user_ratings_mean.reshape(-1, 1)

	U, s, Vt = svds(W_demeaned, k = K)
	S = np.diag(s)

	all_user_predicted_ratings = np.dot(np.dot(U, S), Vt) + user_ratings_mean.reshape(-1, 1)
	predicted_df = pd.DataFrame(all_user_predicted_ratings, columns = weighted_crosstab.columns)

	# print('\n')
	# print(RMSE(origin_crosstab.as_matrix(), all_user_predicted_ratings))
	# print('\n')
	# print(MAE(origin_crosstab.as_matrix(), all_user_predicted_ratings))
	# print('\n')

	rec_video_num = predicted_df[predicted_df.index == int(user_id)]

	rec_video_num = rec_video_num.sort_values(by = int(user_id), ascending = False, axis = 1).columns

	rec_video_url = []

	for i in rec_video_num : 
		MyDB.execute('select url from ROUTINE where video_num = %s UNION select url from EXERCISE where video_num = %s' %(str(i), str(i)))
		rec_video_url += MyDB.fetchone()

	return rec_video_url[:N]