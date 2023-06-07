#!/usr/bin/env python
# coding: utf-8

# # Cancellation Analytics: Unlocking Insights in Hotel Booking Trends
# 
# ## Business Problem
# 
# ### In recent years, City hotel and Resort Hotel have seen high cancellation rates. Each hotel is now dealing with a high number of issues as a result, including fewer revenues and less than ideal hotel room use.Consequently, lowering cancellation rates is both hotels' primary goal in order to increase their efficiency in generating revenue, and for us to offer thorough advice to address this problem.
# 
# ### The analysis of hotel booking cancellations as well as other factors that have no bearing on their business and yearly revenue generation are the main topics.
# 
# ## Assumptions 
# 
# ### 1. No unusual occurences between 2015 and 2017 will have a substantial impact on the data used.
# ### 2. The information is still current and can be used to analyze a hotel's possible plans in an efficient manner.
# ### 3. There are no unanticipated negatives to the hotel employing any advised technique.
# ### 4. The hotels are not using any of the suggested solutions.
# ### 5. The biggest factor affecting the effectiveness of earning income is booking cancellations.
# ### 6. Cancellations result in vacant rooms for the booked length of time.
# ### 7. Clients make hotel reservations the same year they make cancellations.
# 
# ## Research
# 
# ### 1. What are the variables that affect hotel reservation cancellations?
# ### 2. How can we make hotel reservations cancellations better?
# ### 3. How will hotels be assisted in making pricing and promotional decisions?
# 
# ## Hypothesis
# 
# ### 1. More cancellations occur when prices are high.
# ### 2. When there is a longer waiting list, customers tend to cancel more frequently.
# ### 3. The majority of clients are coming from online travel agents to make their reservations.

# ## ANALYSIS

# # Importing Libraries

# In[178]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# # Loading the dataset

# In[179]:


df = pd.read_csv('hotel_booking.csv')


# # Exploratory Data Analysis and Data Cleaning

# In[180]:


df.head()


# In[181]:


df.tail(10)


# In[182]:


df.shape


# # Removing customers personal data

# In[183]:


df.drop(['name','email', 'phone-number', 'credit_card'], axis=1, inplace=True)


# In[184]:


df.head()


# In[185]:


df.shape


# In[186]:


df.columns


# In[187]:


df.info()


# In[188]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])


# In[189]:


df.info()


# In[190]:


df.describe(include='object')


# In[191]:


for col in df.describe(include='object').columns:
    print(col)
    print(df[col].unique())
    print('-'*50)


# In[192]:


df.isnull().sum()


# In[193]:


df.drop(['company','agent'], axis=1, inplace=True)
df.dropna(inplace=True)


# In[194]:


df.isnull().sum()


# In[195]:


df.describe()


# In[196]:


df = df[df['adr']<5000]


# In[197]:


df.describe()


# # Data Analysis and Visualization

# In[198]:


cancelled_perc = df['is_canceled'].value_counts(normalize=True)
print(cancelled_perc)

plt.figure(figsize=(5,4))
plt.title('Reservation status count')
plt.bar(['Not cancelled', 'Cancelled'],df['is_canceled'].value_counts(), edgecolor='k', width=0.7)
plt.show()


# ## Analysis and Finding
# 
# ## The accompanying bar graph shows the percentage  of reservations that are cancelled and those that are not. It is obvious that there are  still a significant number of reservations that have not been cancelled. There are still 37% of clients who cancelled their reservations, which has a significant impact  on the hotels's earnings.

# In[215]:


plt.figure(figsize = (8,4))
ax1= sns.countplot(x =  'hotel', hue='is_canceled', data = df, palette = 'Blues')
#legend_labels, _ = ax1. get_legend_handles_labels()
#ax1.legend(legend_labels,bbox_to_anchor(1,1))
legend_labels = ['Not Canceled', 'Canceled']
ax1.legend(labels=legend_labels, bbox_to_anchor=(1, 1))
plt.title('Reservation status in different hotels', size = 20)
plt.xlabel('hotel')
plt.ylabel('number of reservations')
plt.show()


# ## Finding
# 
# ### In comparison to resort hotel, city hotels have more bookings. It's possible that resort hotels are more expensive than the city hotel.

# In[200]:


resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize= True)


# In[201]:


city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize= True)


# In[202]:


resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[203]:


plt.figure(figsize=(20,8))
plt.title('Average Daily Rate in City and Resort Hotel', fontsize=30)
plt.plot(resort_hotel.index, resort_hotel['adr'], label= 'Resort Hotel')
plt.plot(city_hotel.index, city_hotel['adr'], label= 'City Hotel')
plt.legend(fontsize=20)
plt.show()


# ## Finding
#  
# ### The line graph above shows that, on certain days, the average daily rate for a city hotel is less than that of a resort hotel, and on other days, it is even less. It goes without saying that weekends and holidays may see a rise in resort hotel rates. 

# In[216]:


df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize=(16,8))
ax1 = sns.countplot(x = 'month', hue = 'is_canceled', data = df, palette='bright')
legend_labels,_ = ax1. get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Reservation status per month', size=20)
plt.xlabel('month')
plt.ylabel('number of reservations')
plt.legend(['not cancelled', 'cancelled'])
plt.show()


# ### We have developed the grouped bar graph to analyze the months with the highest and lowest reservation levels according to reservation status. It can be seen that the number of confirmed reservations is largest in the month of August, whereas January is the month with the most cancelled reservations. Also August and september are the months with the lowest reservation cancellations.

# In[205]:


plt.figure(figsize=(15,8))
plt.title('ADR per month', fontsize=30)

sns.barplot(x='month', y='adr', data = df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index())
plt.show()


# ### This bar graph demonstrates that the cancellations are most when the prices are greatest and are least when they are lowest. Therefore, the cost of the accomodation is solely responsible for the cancellation.
# 
# ### Now let's see which country has the highest reservation cancellation. The top country is Portugal with the highest number of cancellations.

# In[206]:


cancelled_data = df[df['is_canceled']==1]
top_10_country = cancelled_data['country'].value_counts()[:10]
plt.figure(figsize=(8,8))
plt.title('Top 10 countries with reservation canceled')
plt.pie(top_10_country, autopct = '%.2f', labels=top_10_country.index)
plt.show()


# In[207]:


df['market_segment'].value_counts()


# In[208]:


df['market_segment'].value_counts(normalize=True)


# ### Lets  check the area from where the guests are visiting the hotels and making the reservations. Is it coming from Direct or Groups , Online or Offline Travel Agents?

# In[209]:


cancelled_data['market_segment'].value_counts(normalize=True)


# ### Around 46% of the clients come from online travel agencies, whereas 27% come from groups. Only 4% of clients book hotels directly by visiting them and making reservations.

# In[210]:


cancelled_df_adr = cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace=True)
cancelled_df_adr.sort_values('reservation_status_date', inplace =True)

not_cancelled_data = df[df['is_canceled']==0]
not_cancelled_df_adr = not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index(inplace=True)
not_cancelled_df_adr.sort_values('reservation_status_date', inplace =True)

plt.figure(figsize=(20,6))
plt.title('Average Daily Rate')
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label='not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label='cancelled')
plt.legend()


# In[211]:


cancelled_df_adr = cancelled_df_adr[(cancelled_df_adr['reservation_status_date']>'2016') & (cancelled_df_adr['reservation_status_date']<'2017-08')]
not_cancelled_df_adr = not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date']>'2016') & (not_cancelled_df_adr['reservation_status_date']<'2017-08')]


# In[217]:


plt.figure(figsize=(20,6))
plt.title('Average Daily Rate', fontsize=30)
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label='not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label='cancelled')
plt.legend()
plt.show()


# 
# ### As seen in the graph, reservations are cancelled when the average daily rate is higher than when it is not cancelled. It clearly proves all the above analysis, that the higher price leads to higher cancellation.
# 

# ## Sugesstions
# 
# ### 1. Cancellations rates rise as the price does. In order to prevent cancellations of reservation, hotels could work on their pricing strategies and try to lower the rates for specific hotels based on locations. They can also provide some discounts to the consumers.
# 
# ### 2. As the ratio of the cancellation and not cancellation of the resort hotel is higher in the resort hotel than the city hotels. So the hotels should provide a reasonable discount on the room prices on weekends or on holidays.
# 
# ### 3. In the month of January, hotels can start campaigns or marketing with a reasonable amount to increase their revenue as the cancellation is highest in this month.
# 
# ### 4. They can also incease the quality of their hotels and their services mainly in Portugal to reduce the cancellation rate.

# In[ ]:





# In[ ]:









# In[ ]:





# In[ ]:




