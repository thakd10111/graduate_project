import dbConnection as database
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import sklearn

MyDB = database.MyDB('address', port, 'id','pw','db_name')

# example : 
# mydb.dic_execute('select * from USER where user_num = '+str(1))
# MyDB.execute('select * from USER where user_num = 1')
# A = mydb.dic_fetchall()

# changed USER table : user_num sex  age bodypart  health_point  label
def user_grouping(cluster_count) :

	MyDB.dic_execute('select * from USER')
	ALL_USER_DATA =  MyDB.dic_fetchall()
	ALL_USER_DATA = pd.DataFrame(ALL_USER_DATA)

	# Clustering user data, X-axis = sex, Y-axis = age, Z-axis = health_point
	f1 = ALL_USER_DATA.sex.map({'f': 0, 'm': 1})
	f2 = ALL_USER_DATA.age
	f3 = ALL_USER_DATA.health_point

	X_f = np.array(list(zip(f1, f2, f3)))

	# set Number of clusters
	kmeans = KMeans(n_clusters = cluster_count)

	# Fitting the input data
	kmeans = kmeans.fit(X_f)
	# Getting the cluster labels
	labels = kmeans.predict(X_f)
	centroids = kmeans.cluster_centers_

	ALL_USER_DATA['label'] = labels

	plt.rcParams['figure.figsize'] = (16, 9)
	plt.style.use('ggplot')

	colors = ['r','g','b','y','c','m']
	fig, ax = plt.subplots()

	# Data Visualization
	for i in range(cluster_count) :
		points = np.array([X_f[j] for j in range(len(X_f)) if labels[j] == i])
		ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])

	ax.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=200, c='#050505')

	#Labeling
	for i in range(len(ALL_USER_DATA)) :
		MyDB.execute('update USER set label = %s where user_num = %s' %(str(ALL_USER_DATA.iloc[i]['label']), str(ALL_USER_DATA.iloc[i]['user_num'])))
		MyDB.commit()




def bodypart_update() :

	MyDB.dic_execute('select * from HISTORY')
	HISTORY = MyDB.dic_fetchall()
	history_db_df = pd.DataFrame(HISTORY)
	history_crosstab = pd.crosstab(history_db_df.user_num, history_db_df.video_num)

	for i in history_crosstab.index :
	    
	    temp = history_crosstab.loc[history_crosstab.index == i]
	    temp_s = temp.T.sort_values(by=i, ascending=False).T
	    
	    max_video_num = temp_s.columns[0]
	    max_watch = temp_s.iloc[:, 0].values[0]
	    
	    
	    second_watch = temp_s.iloc[:, 1].values[0]
	    

	    if max_watch - second_watch >= 2 :
        	MyDB.execute('select bodypart from EXERCISE where video_num in ('+str(max_video_num)+') UNION select bodypart from ROUTINE where video_num in ('+str(max_video_num)+')')
        	temp_video = MyDB.fetchone()
        	new_bodypart = temp_video[0]
        	MyDB.execute('update USER set bodypart = \''+new_bodypart+'\' where user_num = '+str(i))
        	MyDB.commit()





if __name__ == '__main__' :
	user_grouping(6)
