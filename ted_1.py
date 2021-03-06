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
# As the scatterplot and the correlatoin matrix show, the pearson coefficient is slightly more than 0.5.
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

# =============================================================================
# As far as TEDx talks are concerned, November is the most popular month.However, we cannot take this result
# at face value as very few of TEDx talks are actually uploaded to the TED and therefore,it is entirely possible that
# the sample in our dateset is not at all representative of all TEDx talks. A slightly more accurate statement would be 
# that the most popular TEDx talks take place the most in October and Novermber.
# =============================================================================

# =============================================================================
# The next question im interested in is the most popular days for conducting TED and TEDx conferences. The tools 
# applied are very sensible to the procedure applied for months.
# =============================================================================

df['day'] = pd.to_datetime(df['film_date']).dt.weekday
df['day'] = df['day'].apply(lambda x: calendar.day_abbr[int(x)])

day_count = df['day'].value_counts().reset_index().rename(columns = { 'index' :'day','day': 'talks' })

sns.barplot(x = 'day', y ='talks',data = day_count, order = calendar.day_abbr)


# =============================================================================
# The distribution of day is almost a positve skewed bell curve with Tuesday and Wednesday being the most popluar days.
# To my surprise, the Saturday is being least popluar day and sunday is penultimate day. This is prett intereting 
# because i was of the option that most TED Conferences would happend sometime in the weekned.
# =============================================================================

# visualize the number of TED talks through the year and check if our hunch that they have grown significantly is indeed true

df['year'] = df['film_date'].apply(lambda x: x.split('-')[0])

year_count = df['year'].value_counts().reset_index().sort_values(by = 'index')
year_count.columns = ['year', 'talks']

plt.figure(figsize = (18,5))
# plt.plot(year_count['year'],year_count['talks'],color = 'r',marker = 'o')

sns.pointplot(x = 'year', y = 'talks', data = year_count)

# =============================================================================
# Observations:
# 
# 1, As expected, the number of TED talks have gradually increased over the years since its inception in 1984
# 2, There was a sharp increase in the number if talks in 2009. It might be interesting to know the reason behind
# 2009 being the tipping point where the number of talks increased more than twofold
# 3, the number of talks have been pretty much constant since 2009
# =============================================================================
# =============================================================================
# finally, to put it all together, let us construct a heat map that shows us the number of talks by month and year. This 
# will give us a good summary of the distribution of talks 
# =============================================================================

df_pivot = pd.pivot_table(df,values = 'title', index = 'month',columns = 'year',aggfunc = 'count')
df_pivot = df_pivot.fillna(0)

plt.figure(figsize = (12,8))
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
sns.heatmap(df_pivot, annot = True,linewidth = 0.2, yticklabels = month_order )

#  Who are the most popular TED speakers

speaker_df = df.groupby('main_speaker').count()['comments'].reset_index()
speaker_df.columns = ['main_speaker','appearances']
speaker_df = speaker_df.sort_values(by = 'appearances', ascending = False)
speaker_df.head(10)

# =============================================================================
# Observation
# Hans Rosling is clearly the most popular TED Speaker, with 9 appearance on te TED Forum,
# Juan Enriquez comes a close second with 7 appearances. Rive and Marco Tempest 
# have graced the TED platform 6 times
# =============================================================================

# =============================================================================
# which occupation should you choose if you want ot become a TED Speaker?
# let us have a look what kind of people TED is most interested in inviting to its event
# =============================================================================
occupation_df = df.groupby('speaker_occupation').count().reset_index()[['speaker_occupation', 'comments']]
occupation_df.columns = ['occupation', 'appearances']
occupation_df = occupation_df.sort_values('appearances', ascending=False)
plt.figure(figsize=(15,5))
sns.barplot(x='occupation', y='appearances', data=occupation_df.head(10))
plt.show()

# =============================================================================
# Observation:
# Writers are the most popular with more than 45 speaker identifying themselves as the aforementioed
# Artist and Designers come a distant second with around 35 speakers in each catrgory
# This results must be taken with a pinch of salt as a considerable number of speaker identify themselves with
# mutiple professions(for example, writer/entrepreneur).
# 
# =============================================================================

# mutiple professions analysis
# =============================================================================
# 
# mutiple_df = df[['main_speaker','speaker_occupation']]
# m = mutiple_df['speaker_occupation'].value_counts(dropna = False)
# m.isnull().sum()
# =============================================================================

# do some professions tend to attract a larger number of viewers? do answer let us visualise the relationship 
# between the top 10 most professions and the views they garnered in the form of a boxplot

fig, ax = plt.subplots(nrows=1, ncols=1,figsize=(15, 8))
sns.boxplot(x='speaker_occupation', y='views', data=df[df['speaker_occupation'].isin(occupation_df.head(10)['occupation'])], palette="muted", ax =ax)
ax.set_ylim([0, 0.8e7])
plt.show()

# on average, out of the top 10 most popular professions, psychologists tend to garner the most views.
# writers have the greatest range of views between the first and the third quartile


#check the number of talks which have had more than one speaker

df['num_speaker'].value_counts()

# =============================================================================
# almost every talk has just one speaker. There are close to 50 talks where two people shared the stage.
# The maximum number of speakers to share a single stage was 5. 
# have a look at he it with 5 speakers
# =============================================================================

five = df[df['num_speaker'] == 5][['title','description','main_speaker','event']]

# =============================================================================
# it turns out the talk titled as A dance to honor Mother earth by Jon Boogz and Lil Buck at the TED 2017 Conference
# =============================================================================

# which ted event tend to hold the most number of ted.com upload worthy events? 

event_df = df[['title','event']].groupby('event').count().reset_index()
event_df.columns = ['event','talks']
event_df = event_df.sort_values(by = 'talks', ascending = False)
event_df.head(10)



#  TED languages 
df['languages'].describe()

# =============================================================================
# on average, a TED talk is avaiable in 27 different languages. The maximum number of languages a TED talk is 
# aviable in is a staggering 72.
# =============================================================================

lan = df[df['languages'] == 72]

# =============================================================================
# The most translated TED talk of all time is Matt Cutts' Try something new in 30 days. the talk does have a very 
# universal theme of exploration. The sheer number of languages its aviable in denmands a little more inspection though
# as it has just over 8 millions, far fewer than the most popular TED talk.
# 
# Finally, let us check if there is a correlation between the number of views and the number of languages a talk is 
# available in. we would think that this should be the case since the talk is more accessible to a larger numbre of people 
# but as mattcutts' talk shows, it may not really be the case 
# =============================================================================


sns.jointplot(x = 'languages', y = 'views',data = df).annotate(stats.pearsonr)

# =============================================================================
# The Pearson coefficient is 0.38 suggesting a medium correlation between the aforementioned quantites
# =============================================================================

#  TED themes

#  try to find the most popular themes in the TED conferences

import ast
df['tags'] = df['tags'].apply(lambda x: ast.literal_eval(x))

tags = df['tags'].apply(pd.Series).stack().reset_index(level =1, drop = True)
tags.name = 'theme'

theme_df = df.drop('tags', axis = 1).merge(tags,right_index = True, left_index = True)
theme_df.head()

len(theme_df['theme'].value_counts())
# =============================================================================
# TED define a a staggering 416 different categories for its talks
# =============================================================================

# most popular themes

pop_themes = pd.DataFrame(theme_df['theme'].value_counts()).reset_index()
pop_themes.columns = ['themes','talks']
pop_themes.head(10)

plt.figure(figsize = (15,8))
sns.barplot(x = 'themes', y = 'talks',data = pop_themes.head(10))
plt.show()

# =============================================================================
# As may have been expectedm,Technology is the most popular topic for talks. The other two orginal factions,
# Design and Entertainment, also make it to the list of top 10 themes.
# Science and Global issures are the second and third most popular themes repectively 
# =============================================================================

# Has the demand for technology talks increased?
# do certain years have a disproportionate share of talks related to golbal issue?


pop_theme_talks = theme_df[(theme_df['theme'].isin(pop_themes.head(8)['themes'])) & (theme_df['theme'] != 'TEDx')]

pop_theme_talks['year'] = pop_theme_talks['year'].astype('int')

pop_theme_talks = pop_theme_talks[pop_theme_talks['year'] > 2008]

themes = list(pop_themes['themes'].head(8))

themes.remove('TEDx')

ctab = pd.crosstab(pop_theme_talks['year'] ,pop_theme_talks['theme'])
ctab = ctab.apply(lambda x: x/x.sum(), axis = 1 )



ctab.plot(kind = 'bar', stacked = True, colormap = 'rainbow', figsize = (12,8)).legend(loc = 'center left',bbox_to_anchor=(1,0.5))

axs = ctab.plot(kind='line', stacked=False, colormap='rainbow', figsize=(12,8)).legend(loc = 'center left',bbox_to_anchor=(1,0.5))

plt.show()


# =============================================================================
# The proporTion of technology talks has steadily increased over the years with a slight dip in 2010.
# This is understandable considering the boom of techonologies such as blockchain, deep learning, and augmentaed 
# reality capturing people's imagination 
# 
# Talks on culture have witnessed a dip, decreasing steadily starting 2013. The share of culture talks has been the 
# least in 2017. Entertainment talks also seem to have witnessed a slight decline in popularity since 2009
# =============================================================================

# =============================================================================
# like with the speakder occupations, let us investigate if certain topic tend to garner more views than certain 
# other topic. we will be doing this analysis for the top ten categoreis that we discovered in an earlier cell.
# As with the speaker occupations, the box plot will be used to deduce this relation.
# =============================================================================

pop_theme_talks = theme_df[theme_df['theme'].isin(pop_themes.head(10)['themes'])]

fig,ax = plt.subplots(nrows = 1, ncols = 1, figsize = (15,8))

sns.boxplot(x = 'theme', y = 'views', data = pop_theme_talks)

ax.set_ylim([0, 0.5e7])


# =============================================================================
# Although culture has lost its share in the number of TED talks over the years, they garner the highest meadian number of views
# =============================================================================



# Talk Duration and Word Counts

# =============================================================================
# In this section, we will perform analysis on the length of TED talks. TED is famous for imposing a very strict time 
# of 18 mins. Although this is the suggested limit, there have been talks as short as 2 mins and some have stretched 
# to as long as 24 mins. 
# 
# let us get an idea of distribution of TED talk duration.
# =============================================================================

# convert to mins

df['duration'] = df['duration'] / 60
df['duration'].describe()
# =============================================================================
# TED talls, on average are 13.7 mins long. I find this statistic surprising because TED talks are often
# synonymous with 18 mins and the average is a good 3 mins shorter than that 
# 
# The shortest TED talks on record is 2.25 mins long wheras the longest talk is 87.6 mins long. I am 
# pretty sure the longest talks was not actually a TED talk. lets find out both the shortest and longest talk
# =============================================================================

shortest = df[df['duration'] == 2.25]
longest = df[df['duration'] == 87.6]

# =============================================================================
# The shortest talk was at TED2007 titled The ancestor of language by Murray Gell-Mann.
# The longest talk on TED.com as we have guessed, is not a TED talk at all. Rather, it was a 
# talk titled Parrots, the universe and everything delivered by Douglas Adams. at the University of California in 2001
# 
# Let us now check for any correlation between the popularity and the duration of TED Talk. 
# To make sure we only include TED talks, we wil consider only those talks which have a duration less than 15 mins
# =============================================================================


a  = sns.jointplot(x = 'duration', y = 'views', data = df[df['duration'] < 25 ])
a.annotate(stats.pearsonr)

plt.xlabel('Duration')
plt.ylabel('View')


# =============================================================================
# There seems to be almost no correlation between these two quantites. This strongly suggest that 
# there is no tangible correlation between the length and the popularity of a TED Talk. content is king at TED
# 
# Next, we look at transcripts ot get an idea of word count. For this, we introduce our second dataset, the one
# which contains all transcripts
# =============================================================================

df2 = pd.read_csv('transcripts.csv')
df2.head()

#  merge two dataframe on url feature to include word counts for every talks
#  left: use only keys from left frame. 
df3 = pd.merge(left = df, right = df2, how = 'left',left_on = 'url',right_on = 'url')
df3.head()

df3['transcript'] = df3['transcript'].fillna('')
df3['wordcount'] = df3['transcript'].apply(lambda x: len(x.split()))
df3['wordcount'].describe()


# =============================================================================
# we can see that average TED talk has around 1971 words and there is a significantly large stdof 1009 words.
# The longest talk is more than 9044 words in length 
# 
# like duration, there should not be any correlation between number of workd and views. 
# we will proceed to look at a more interesting statistic: 
# 
# =============================================================================
# the number of words per minute. 

df3['wpm'] = df3['wordcount'] / df3['duration']
df3['wpm'].describe()

# =============================================================================
# The average TED Speaker enunciates 142 words per mintue. The fastest talker spoke a staggering 247 words a minute
# which is much higher than the average of 125 to 150 words per minute in english.
# =============================================================================

# let us see who did it?


f = df3[df3['wpm'] > 245]


# =============================================================================
# The person is Mae Jemison with a talk on Teach arts and sciences together at Ted 2002 conference.
# We should take this result with a pinch of salt because i went ahead and had a look at the talk and 
# she did not really seem to speak that fast.
# =============================================================================

# =============================================================================
# Finally, in this section, i would like to see if there is any correlation between words per minute and popularity 
# =============================================================================

dp = sns.jointplot(x = 'wpm', y = 'views', data = df3[df3['duration'] < 25 ])

dp.annotate(stats.pearsonr)

# =============================================================================
# Again, there is practically no correlation. If you are going to give a TED talk, you probably 
# should not worry if you are speaking a little faster or a little slower than usual 
# =============================================================================


# TED ratings 

# =============================================================================
# Ted allows its users to rate a particular talk on a variety of metrics. We therefore have data on how many 
# ppl found a particular talk funny,inspiring, creative, and a myriad of other verbs.
# =============================================================================

# let us inspect how this ratings dic actually looks like. 

df.iloc[1]['ratings']

df['ratings'] = df['ratings'].apply(lambda x: ast.literal_eval(x))

df['funny'] = df['ratings'].apply(lambda x: x[0]['count'])
df['jawdrop'] = df['ratings'].apply(lambda x: x[-3]['count'])
df['beautiful'] = df['ratings'].apply(lambda x: x[3]['count'])
df['confusing'] = df['ratings'].apply(lambda x: x[2]['count'])
df.head()

# =============================================================================
# Funniest Talks of all time 
# =============================================================================

funniest = df[['title','main_speaker','views','published_date','funny']].sort_values('funny',ascending = False)


# =============================================================================
# Most beautiful talks of all time 
# =============================================================================

beautiful = df[['title','main_speaker','views','published_date','beautiful']].sort_values('beautiful',ascending = False)

# =============================================================================
# most jaw dropping talks of all time
# =============================================================================

jawdrop = df[['title','main_speaker','views','published_date','jawdrop']].sort_values('jawdrop', ascending = False)

# =============================================================================
# most confusing talks of all time
# =============================================================================
confusing = df[['title','main_speaker','views','published_date','confusing']].sort_values('confusing', ascending = False)


# Related videos

# =============================================================================
# In this last section, we will have a look at how every TED talk is related to every other TED talk by 
# constructing a graph with all the talk as nodes and edges defined between two talks if one talks is on the list of 
# recommended watches of the other.Considering the fact that TED talks are extremely diverse, it would be interesting 
# to see how dense or sparse our graph will be  
# =============================================================================


df['related_talks'] = df['related_talks'].apply(lambda x: ast.literal_eval(x))

s = df['related_talks'].apply(pd.Series).stack().reset_index(level = 1, drop = True)

s.name = 'related'

related_df = df.drop('related_talks',axis = 1 ).merge(s,left_index = True, right_index = True)

related_df['related'] = related_df['related'].apply(lambda x: x['title'])


d = dict(related_df['title'].drop_duplicates())
d = {v: k for k,v in d.items()}  # key become value and value become key

related_df['title'] = related_df['title'].apply(lambda x: d[x])



# =============================================================================
# The TED Wrold Cloud
# 
# I was curious about which words are most often used by TED speakers. Could we create a Word Cloud out of 
# all TED speeches? luckily, Python has a very useful word cloud generating library that allows us to do just that 
# 
# python string join() method
# 
# join all items in a tuple into a string , using ' ' character separator
# 
# =============================================================================
ww = ''.join(df2['transcript'])

from wordcloud import WordCloud, STOPWORDS

wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white',width=2400,height=2000).generate(ww)
plt.figure(figsize=(12,15))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()


# =============================================================================
# # The word one is the most popular word across the corpus of all TED  transcript which I think encapsulates
# # the idea of TED pretty well. Now ,think, know, see, people, laugther are among the most popupar words usedin TEd 
# # speeches. TED speeched seem to place a lot of emphasis on knowledge, insight, the present and of course the people
# =============================================================================
 
























