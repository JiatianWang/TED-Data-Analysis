import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns 
import json 
from datetime import datetime
import calendar
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


m = df[['title','main_speaker','views','comments']].sort_values('comments', ascending = False).head(10)

# =============================================================================
# As can be seen above, Richard Dawkins' talk on Militant atheism generated the greateest amount of discussion 
# and opinions despite having significantly lesser views than Ken Robinosns' talk, which is second in the list.
# This raises some interesting questions
# 
# which talk tend to attract the largest amount of discussion ?
# 
# To ansewer this question, we will define a new feature discussion quotient which is simply the ratio of the 
# number of comments to the number of views. we will them check which talks have the largest dicussion quotient
# =============================================================================

df['dis_quo'] = df['comments'] / df['views']

d = df[['title','description', 'main_speaker','views','comments','dis_quo','film_date']].sort_values('dis_quo',ascending = False).head(10)

# =============================================================================
# quesitons? i think it only 3 or 4 would be categoried to faith and religion
# 
# This analysis has acutally raised extremely intersting insight. Half of the talks in the top 10 are on the lines of 
# Faith and Religion. I suspect science and religion is still a very hotly debaed topic in 21st century. We shall
# come back to this hypothesis in a later section 
# 
# 
# The most discusses talk, thoughm is The case for same sex marriage(which has religious undertones). this is not 
# that surprising considering the amount of debate the topic caused back in 2009
# =============================================================================


# Analysing TED talks by the month and the year

# =============================================================================
# # Context
# # TED(especially TEDx) talks tend to occur all throughout the year. is there a hot month as far as TED is concerned
# In other words, how are the talks distributed thoughout the month since its inception?
# =============================================================================

# 1month_abbr = {'01': 'Jan', '02': 'Feb', '03': 'Mar', 
#               '04': 'Apr', '05': 'May', '06': 'Jun', 
#               '07': 'Jul', '08': 'Aug', '09': 'Sep',
#               '10': 'Oct', '11': 'Nov', '12': 'Dec'}



df['month'] = df['film_date'].apply(lambda x: x.split('-')[1])
# df['months'] = df['month'].map(month_abbr)
df['month'] = df['month'].apply(lambda x: calendar.month_abbr[int(x)])

month_count = df['month'].value_counts().reset_index().rename(columns = {'index': 'Month_name', 'month': 'Month_view'})
sns.barplot(x = 'Month_name', y = 'Month_view', data = month_count, order = calendar.month_abbr)

# =============================================================================
# February is clearly the most popular month for TED Conferences whereas August and January are 
# the least popular. February's is largely due to the fact that the official TED Conference are held in Februart.
# =============================================================================


# distribution for TEDx talks only

df_TEDx = df[df['event'].str.contains('TEDx')]

x_month_count = df_TEDx['month'].value_counts().reset_index().rename(columns = {'index':'Month_name' , 'month':'Month_view'})

sns.barplot(x = 'Month_name',y = 'Month_view', data = x_month_count,order = calendar.month_abbr)












































