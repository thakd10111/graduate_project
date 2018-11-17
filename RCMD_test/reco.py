
from rcmd_func import dbConnection as database

import sys
import random
import time

MyDB = database.MyDB('115.68.99.11', 3306, 'ksunk','!@ksunk','ksunkDB')

def main(theme_num) :

	lowLevel_rcmd_list = []
	midLevel_rcmd_list = []
	highLevel_rcmd_list = []

	# ========= select video_dictionary having same attribute =====================

	for i in range(4) :
		step_num = i+1
		
		MyDB.dic_execute('select length, timing, bodypart, excer_type, equipment from DETAILSTEP where theme_num = %s and step_num = %s' %(str(theme_num), str(step_num)))
		video_attribute = MyDB.dic_fetchone()
		

		length_i = video_attribute['length']
		length_list = range(length_i-5, length_i+5, 1)
		bodypart_list = video_attribute['bodypart'].split(',')
		excer_type_list = video_attribute['excer_type'].split(',')
		equipment_list = video_attribute['equipment'].split(',')


		sql = ('select sex, level, url from EXERCISE where length in %s and bodypart in (' %(str(tuple(length_list))))

		for j in bodypart_list :
			sql = sql + '\''+j+'\''
			sql += ','
		sql = sql[:-1]
		
		sql += ') and excer_type in ('

		for j in excer_type_list :
			sql = sql + '\''+j+'\''
			sql += ','
		sql = sql[:-1]
		
		sql += ')'

		if equipment_list[0] != 'dc':
			sql += 'and equipment in ('
			for j in equipment_list :
				sql = sql + '\''+j+'\''
				sql += ','
			sql = sql[:-1]
			sql += ')'

		# print(sql)
		MyDB.dic_execute(sql)

		# step_list feature :: [{'sex':'f', 'level':'l', 'url':'rcmdrecommend'},{'sex':'m','level':'m','url':'thakd101'},{'sex':'h','level':'h','url':'xodusWkd'}]
		# level optimize

		if i==0 :
			step1_list = list(MyDB.dic_fetchall())

		elif i==1 :
			step2_list = list(MyDB.dic_fetchall())

		elif i==2 :
			step3_list = list(MyDB.dic_fetchall())

		else :
			step4_list = list(MyDB.dic_fetchall())

	# ========================== selecting end ==================================================

	# sample data input

	# step1_list = [{'sex':'f', 'level':'l', 'url':'step1_low'}, {'sex':'f', 'level':'m', 'url':'step1_mid'}, {'sex':'m', 'level':'h', 'url':'step1_high'}]
	# step2_list = [{'sex':'f', 'level':'h', 'url':'step2_high'}, {'sex':'f', 'level':'m', 'url':'step2_mid'}, {'sex':'m', 'level':'l', 'url':'step2_low'}]
	# step3_list = [{'sex':'f', 'level':'m', 'url':'step3_mid'}, {'sex':'f', 'level':'m', 'url':'step3_mid'}, {'sex':'m', 'level':'l', 'url':'step3_low'}]
	# step4_list = [{'sex':'f', 'level':'l', 'url':'step4_low'}, {'sex':'f', 'level':'l', 'url':'step4_low'}, {'sex':'m', 'level':'h', 'url':'step4_high'}]


	# ========================= while - combination =====================================================
	
	level_combination = tuple()
	timeout = time.time() + 10 # time limit 120seca

	while(True) :
		# Make High Level combination randomly
		temp_combi_list = []
		for i in range(4) :

			if i==0 :
				temp_combi_list += sorted(step1_list, key=lambda k: random.random())[:1]

			elif i==1 :
				temp_combi_list += sorted(step2_list, key=lambda k: random.random())[:1]

			elif i==2 :
				temp_combi_list += sorted(step3_list, key=lambda k: random.random())[:1]

			else :
				temp_combi_list += sorted(step4_list, key=lambda k: random.random())[:1]


		high_count = len([item for item in temp_combi_list if item['level']=='h'])
		mid_count = len([item for item in temp_combi_list if item['level']=='m'])
		low_count = len([item for item in temp_combi_list if item['level']=='l'])


		# (1, 2, 1) = high=1, mid=2, low=1
		level_combination = level_combination + tuple([high_count]) + tuple([mid_count]) + tuple([low_count])


		if len(highLevel_rcmd_list)==0 or len(midLevel_rcmd_list)==0 or len(lowLevel_rcmd_list)==0:
			if level_combination == (4, 0, 0) or level_combination == (3, 1, 0) or level_combination == (3, 0, 1) or level_combination == (2, 2, 0) :
				highLevel_rcmd_list = [item['url'] for item in temp_combi_list]


			if level_combination == (0, 4, 0) or level_combination == (1,3,0) or level_combination == (0, 3, 1) or level_combination == (1, 2, 1) or level_combination == (1, 1, 2) or level_combination == (2, 1, 1) :
				midLevel_rcmd_list = [item['url'] for item in temp_combi_list]


			if level_combination == (0, 0, 4) or level_combination == (1, 0, 3) or level_combination == (0, 1, 3) or level_combination == (0, 2, 2) :
				lowLevel_rcmd_list = [item['url'] for item in temp_combi_list]


		# if len(midLevel_rcmd_list)==0 :
		# 	if level_combination == (0, 4, 0) or level_combination == (1,3,0) or level_combination == (0, 3, 1) or level_combination == (1, 2, 1) or level_combination == (1, 1, 2) or level_combination == (2, 1, 1) :
		# 		midLevel_rcmd_list = [item['url'] for item in temp_combi_list]


		# if len(lowLevel_rcmd_list)==0 :
		# 	if level_combination == (0, 0, 4) or level_combination == (1, 0, 3) or level_combination == (0, 1, 3) or level_combination == (0, 2, 2) :
		# 		lowLevel_rcmd_list = [item['url'] for item in temp_combi_list]
		# 		# temp_combi_list['url']


		temp_combi_list = []

		if (time.time() > timeout) :
			break;

	# ============== while combination end ========================================

	# WARNING :: We can't make all level list!!
	

	if len(highLevel_rcmd_list) == 4 :
		print('h')
		for i in highLevel_rcmd_list:
			print(i)

	if len(midLevel_rcmd_list) == 4 :
		print('m')
		for i in midLevel_rcmd_list:
			print(i)

	if len(lowLevel_rcmd_list) == 4 :
		print('l')
		for i in lowLevel_rcmd_list:
			print(i)


if __name__ == '__main__' :
	THEME_NUM = sys.argv[1]
	main(THEME_NUM)