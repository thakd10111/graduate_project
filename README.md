# ATTA Player #
*Personalization recommend health training player*

**********************************************

## Rcmd Func ##

* Processing
```
> Grouping user data using Kmeans algorithm.
X-axis = sex, Y-axis = age, Z-axis = health_point
```

* DataProcessor
	* Jaccard similarity
	![codecogseqn](https://user-images.githubusercontent.com/25345968/45470906-5c6f1400-b76a-11e8-969e-4cbccc13cc3f.gif)

	```
	> Convert user attribute(string type) to num and Calculate jaccard similarity
	with row video and column video

	```
	--------------------
	* Add Weight
	```
	> Check how many matched active user's attributes with the video attributes
	if matched at least one, add weight
	```
	-----------------------
	* Singular Value Decomposition - SVD recommend
	![schematic-representation-for-singular-value-decomposition-svd-analysis](https://user-images.githubusercontent.com/25345968/45471412-f71c2280-b76b-11e8-931e-1e8def15e0d1.png)
	<https://www.researchgate.net/figure/Schematic-representation-for-singular-value-decomposition-SVD-analysis_fig2_323907837>


	```
	> Divide watching history matrix and
	decompositioned matrix to predict user's watching rate.
	```

* Youtube API
```
> get video data(likeCount, dislikeCount, viewCount) through youtube video_id.
Sorting with likeCount/dislikeCount and viewCount.
```

**************

## Recommend ##

* Nonmemer *index, exercise, routine page*

```
> Bring the latest popular video in Database and
recommend using video_popularity sorting.
```

* Member *index, exercise, routine page*

```
> Recommend as an SVD model, with user charactaristics
and viewing records weighted
```