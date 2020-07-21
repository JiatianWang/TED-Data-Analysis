import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns 
import json 
from datetime import datetime
#from pandas.io.jason import jason_normalize
#from worldcloud import worldcloud, STOPWORDS


df = pd.read_csv('ted_main.csv')
df.columns
df.shape

# convert the unix timestamp string to readable date

df['film_date'] = df['film_date'].apply(lambda x: datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d'))
df['published_date'] = df['published_date'].apply(lambda x: datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d'))

# most viewd talks of all time 

pop_talk = df[['views','title','main_speaker','film_date','published_date']].sort_values('views',ascending = False)[:15]
published_date = df[['title','published_date']].sort_values('published_date')

# =============================================================================
# Observations:
# 1,Ken Robinson's talk on Do schools kill creativity? is the most popular TED talk of all time with 47.2 million views
# 2,Also coincidentally, it is also one of the first talks to ever be uploaded on the TED site
# 3,Robinson's talk is closely followed by Amy Cuddy's talk on Your body language may shape who you are
# 4,There are only 2 talks that surpassed the 40 millions mark and 4 talks that have crossed 30 million mark
# =============================================================================


# bar chart to visualise these 15 talks in terms of number of views

pop_talk['abbr_name'] = pop_talk['main_speaker'].apply(lambda x: x[0:3])
sns.set_style('whitegrid')
plt.figure(figsize = (10,6))
sns.barplot(x = 'abbr_name' , y = 'views',data = pop_talk)


# statistics and distribution 

ax = sns.distplot(df['views'])
ax1 = sns.distplot(df[df['views'] < 0.4e7]['views'])
df['views'].describe()

# =============================================================================
# The average number of views on TED Talk in 1.6 millon, and the meadian number of views is 1.12,
# whcih is the positve skewed
# This suggests a very high average high level of popularity of TED talks. 
# we also notice that the majority of talks have 
# views less than 4 million. we will condider this as the cutoff point when constructing box plots in teh later sections.
# =============================================================================

#  Commnets
# =============================================================================
# Although the TED website give us access to all the comments posted publicly, this dataset 
# only gives us teh number of comments. we will therefore have to restrict our analysis to this feature only.
# you could try performing textual analysis by scraping the website for commments.
# =============================================================================


df['comments'].describe()

# =============================================================================
# # observations:
# 1, On average, there are 191.56 commentss on every TED talks. Assuming the comments are constructive criticism,
# we can conclude that the TED Online Community is highly involved in disscussions revoling TED talks 
# 2, There is a huge std associated with the comments. In fact, it is even larger than the mean suggesting that 
# the measures may be sentive to outliers. We shall plot his to check the nature of the distribution 
# 3， The minimum number of comments on a talk is 2 and the maximum is 6404. The range is 6402. The minimum number,
# though, may be as a result of the talk being posted extremely recently
# =============================================================================

sns.distplot(df['comments'])
sns.distplot(df[df['comments'] < 500]['comments'])

# =============================================================================
# # From the plot above, we can see that the bulk of the talks have fewer than 500 comments.
# # This clearly suggests that the mean obtained above has been heavily influenced by outliers. 
# # This is possible because the number of sample is only 2550 talks.
# # Another question that I am interested in is if the number of views is correlated with the number of comments.
# # we should think that this is the case as more popularvideo tend to have more comments.
# =============================================================================

# To find out whether popular video have more comments 

# Draw a scatter plot with marginal histograms:

j = sns.jointplot(x = 'views', y = 'comments', data = df, kind = 'reg')
j.annotate(stats.pearsonr)
# sns.jointplot(x = 'views', y = 'comments', data = df, kind = 'kde', color = 'g')
# sns.jointplot(x = 'views', y = 'comments', data = df).plot_joint(sns.kdeplot, zorder = 0, n_levels = 6)
# sns.jointplot(x = 'views', y = 'comments', data = df, kind = 'hex')

df[['views','comments']].corr()

# =============================================================================
# As the scatterplot and the correlatoin matrix show, the person coefficient is slightly more than 0.5.
# This suggest a medium to strong correlation between the two quantities. This was pretty expected as mentioned above
# =============================================================================

# check number of views and comments on the 10 most commented TED Talk of all time














