#!/usr/bin/env python
# coding: utf-8

# In[162]:


#importing the libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker


# In[3]:


#Import the csv file for trip_data from December 2021 to November 2022

tripdata_2021_12 = pd.read_csv("C:/Courses/Data_Analytics/Case_Study/CaseStudy-1/Dataset/Working_dataset_2022_2021/working/202112-divvy-tripdata.csv",parse_dates=True)
tripdata_2022_01 = pd.read_csv("C:/Courses/Data_Analytics/Case_Study/CaseStudy-1/Dataset/Working_dataset_2022_2021/working/202201-divvy-tripdata.csv",parse_dates=True)
tripdata_2022_02 = pd.read_csv("C:/Courses/Data_Analytics/Case_Study/CaseStudy-1/Dataset/Working_dataset_2022_2021/working/202202-divvy-tripdata.csv",parse_dates=True)
tripdata_2022_03 = pd.read_csv("C:/Courses/Data_Analytics/Case_Study/CaseStudy-1/Dataset/Working_dataset_2022_2021/working/202203-divvy-tripdata.csv",parse_dates=True)
tripdata_2022_04 = pd.read_csv("C:/Courses/Data_Analytics/Case_Study/CaseStudy-1/Dataset/Working_dataset_2022_2021/working/202204-divvy-tripdata.csv",parse_dates=True)
tripdata_2022_05 = pd.read_csv("C:/Courses/Data_Analytics/Case_Study/CaseStudy-1/Dataset/Working_dataset_2022_2021/working/202205-divvy-tripdata.csv",parse_dates=True)
tripdata_2022_06 = pd.read_csv("C:/Courses/Data_Analytics/Case_Study/CaseStudy-1/Dataset/Working_dataset_2022_2021/working/202206-divvy-tripdata.csv",parse_dates=True)
tripdata_2022_07 = pd.read_csv("C:/Courses/Data_Analytics/Case_Study/CaseStudy-1/Dataset/Working_dataset_2022_2021/working/202207-divvy-tripdata.csv",parse_dates=True)
tripdata_2022_08 = pd.read_csv("C:/Courses/Data_Analytics/Case_Study/CaseStudy-1/Dataset/Working_dataset_2022_2021/working/202208-divvy-tripdata.csv",parse_dates=True)
tripdata_2022_09 = pd.read_csv("C:/Courses/Data_Analytics/Case_Study/CaseStudy-1/Dataset/Working_dataset_2022_2021/working/202209-divvy-tripdata.csv",parse_dates=True)
tripdata_2022_10 = pd.read_csv("C:/Courses/Data_Analytics/Case_Study/CaseStudy-1/Dataset/Working_dataset_2022_2021/working/202210-divvy-tripdata.csv",parse_dates=True)
tripdata_2022_11 = pd.read_csv("C:/Courses/Data_Analytics/Case_Study/CaseStudy-1/Dataset/Working_dataset_2022_2021/working/202211-divvy-tripdata.csv",parse_dates=True)


# In[5]:


# Joining 12 CSV's into 1 and naming it as "tripdata_21_22".

tripdata_21_22 = pd.concat([tripdata_2021_12,tripdata_2022_01,tripdata_2022_02,tripdata_2022_03,tripdata_2022_04,tripdata_2022_05,tripdata_2022_06,
              tripdata_2022_07,tripdata_2022_08,tripdata_2022_09,tripdata_2022_10,tripdata_2022_11],ignore_index = True)


# In[54]:


# Top 5 rows of the dataframe "tripdata_21_22"
tripdata_21_22.head()


# In[7]:


#checking for missing info

tripdata_21_22.info()


# In[9]:


#converting the datatype of "started_at"

tripdata_21_22["started_at"] = pd.to_datetime(tripdata_21_22["started_at"],dayfirst=True)


# In[11]:


#converting the datatype of "ended_at"

tripdata_21_22["ended_at"] = pd.to_datetime(tripdata_21_22["ended_at"],dayfirst=True)


# In[12]:


#dropping the columns which are not relevant for analysis

tripdata_21_22.drop(columns = ["start_station_name","start_station_id","end_station_name","end_station_id","start_lat","start_lng",
                              "end_lat","end_lng","ride_length"],inplace = True)


# In[13]:


#Added a new coulmn for the ride length

tripdata_21_22["ride_length"] = (tripdata_21_22["ended_at"] - tripdata_21_22["started_at"])/pd.Timedelta(minutes=1)


# In[14]:


#some of the rows in contains the negative value indication end_date is earlier than start_date

tripdata_21_22[tripdata_21_22['ride_length'] < 0].count()


# In[15]:


#some of the rows contains values less than 60 seconds.They are potentially false starts or users trying to re-dock a bike to ensure it was secure.
    
tripdata_21_22[(tripdata_21_22['ride_length'] < 1) & (tripdata_21_22['ride_length'] >= 0)].count()


# In[16]:


#removing the rows where ride length is negative and less than 60 seconds.

tripdata_21_22 = tripdata_21_22[tripdata_21_22["ride_length"] >= 1]
tripdata_21_22 = tripdata_21_22.reset_index()
tripdata_21_22 = tripdata_21_22.drop(columns=['index'])


# In[17]:


#checking for missing values

tripdata_21_22.isna().sum()


# In[18]:


#extracting the year from start_date and creating a column

tripdata_21_22['year'] = tripdata_21_22['started_at'].dt.year


# In[19]:


#extracting the month from start_date and creating a column

tripdata_21_22['month'] = tripdata_21_22['started_at'].dt.month_name()


# In[20]:


#extracting the day of a week from start_date and creating a column

tripdata_21_22['day_of_week'] = tripdata_21_22['started_at'].dt.day_name()


# In[21]:


# Extracting the hour from start_date and creating a column

tripdata_21_22['hour'] = tripdata_21_22['started_at'].dt.hour


# In[22]:


# Changing the datatype

tripdata_21_22 = tripdata_21_22.astype({'year':'int16', 'hour':'int8'})


# In[24]:


tripdata_21_22.head()


# In[196]:


#Setting style for chart
sns.set_style("darkgrid")


# In[27]:


#Rideable Type Usage Between Casual riders and Members.

tripdata_21_22.pivot_table(
    index = ["rideable_type","member_casual"],
    values = "ride_id",
    aggfunc = ["count"],
    margins = True,
    margins_name = "Total_count"
)


# In[197]:


plot_1 = tripdata_21_22.groupby(["member_casual","rideable_type"],as_index = False).count()

sns.barplot(data=plot_1, 
            x='ride_id',
            y='rideable_type',
            hue="member_casual",
            palette='magma',
            saturation = .3)
plt.xlabel("Number Of Rides",size = 10)
plt.ylabel("Rideable Type",size = 10)
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', title = 'Member / Casual')
plt.show()


# In[29]:


#Total Number Of Rides in a year

pd.pivot_table(tripdata_21_22,
               index = 'member_casual',
               values = 'ride_id',
               aggfunc = ['count'],
               margins = True,
               margins_name = 'total_count'
)


# In[198]:


plot_2 = tripdata_21_22.groupby(['member_casual'], as_index=False).count()

sns.barplot(data=plot_2, 
            x='ride_id',
            y='member_casual',
            hue="member_casual",
            palette='magma',
            saturation = .3,
            orient='h')
plt.xlabel("Number Of Rides",size = 10)
plt.ylabel("Member / Casual",size = 10)
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', title = 'Member / Casual')
plt.show()


# In[31]:


#Total Number Of Rides In A Month

pd.pivot_table(tripdata_21_22,
               index = ['year','month','member_casual'],
               values = 'ride_id',
               aggfunc = ['count'],
               margins = True,
               margins_name = 'total_count'
)


# In[199]:


plot_3 = tripdata_21_22.groupby(['year','month','member_casual'],as_index = False).count()

sns.lineplot(data=plot_3, 
            x='month',
            y='ride_id',
            hue="member_casual",
            palette='magma',
            style = "member_casual",
            markers=True
           )
plt.xlabel("Months (dec 2021 - nov 2022)",size = 10)
plt.ylabel("Number Of Rides",size = 10)
plt.xticks(rotation=90)
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', title = 'Member / Casual')
plt.show()


# In[33]:


#Total Number Of Rides Each Weekday

pd.pivot_table(tripdata_21_22,
               index = ['day_of_week','member_casual'],
               values = 'ride_id',
               aggfunc = ['count'],
               margins = True,
               margins_name = 'total_count'
)


# In[200]:


plot_4 = tripdata_21_22.groupby(['day_of_week','member_casual'],as_index = False).count()

sns.lineplot(data=plot_4, 
            x='day_of_week',
            y='ride_id',
            hue="member_casual",
            palette='magma',
            style = "member_casual",
            markers=True
           )
plt.xlabel("weekdays",size = 10)
plt.ylabel("Number Of Rides",size = 10)
plt.xticks(rotation=75)
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', title = 'Member / Casual')
plt.show()


# In[35]:


#Total Number Of Hides Per Hour

pd.pivot_table(tripdata_21_22,
              index = ['hour', 'member_casual'],
              values = 'ride_id',
              aggfunc = ['count'],
              margins = True,
              margins_name = 'Total Count')


# In[201]:


plot_5 = tripdata_21_22.groupby(['hour','member_casual'],as_index = False).count()

sns.lineplot(data=plot_5, 
            x='hour',
            y='ride_id',
            hue="member_casual",
            palette='magma',
            style = "member_casual",
            markers=True
           )
plt.xlabel("hour",size = 10)
plt.ylabel("Number Of Rides",size = 10)
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', title = 'Member / Casual')
plt.show()


# In[37]:


#Average Ride Length in 1 Year

pd.pivot_table(tripdata_21_22,
               index = ['member_casual'],
               values = 'ride_length',
               aggfunc = ['mean'],
               margins = True,
               margins_name = 'Avg_ride_length'
  )


# In[202]:


plot_6 = tripdata_21_22.groupby(['year','member_casual'],as_index = False).mean()

sns.barplot(data=plot_6, 
            x='ride_length',
            y='member_casual',
            hue="member_casual",
            palette='magma',
            saturation = .3,
            orient='h')
plt.xlabel("avg ride length in minutes",size = 10)
plt.ylabel("Member / Casual",size = 10)
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', title = 'Member / Casual')
plt.show()


# In[39]:


#Average Ride Length In Month

tripdata_21_22.groupby(["month","member_casual"])[["ride_length"]].mean()


# In[203]:


plot_7 = tripdata_21_22.groupby(["month","member_casual"],as_index = False).mean()

sns.lineplot(data=plot_7, 
            x='month',
            y='ride_length',
            hue="member_casual",
            palette='magma',
            style = "member_casual",
            markers=True
           )
plt.xlabel("month",size = 10)
plt.ylabel("avg ride length in minutes",size = 10)
plt.xticks(rotation=90)
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', title = 'Member / Casual')
plt.show()


# In[41]:


#Average Ride Length Each Weekday

tripdata_21_22.groupby(["day_of_week","member_casual"])[["ride_length"]].mean()


# In[204]:


plot_8 = tripdata_21_22.groupby(["day_of_week","member_casual"],as_index = False).mean()

sns.lineplot(data=plot_8, 
            x='day_of_week',
            y='ride_length',
            hue="member_casual",
            palette='magma',
            style = "member_casual",
            markers=True
           )
plt.xlabel("month",size = 10)
plt.ylabel("avg ride length in minutes",size = 10)
plt.xticks(rotation=90)
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', title = 'Member / Casual')
plt.show()


# In[43]:


#Average Ride Length Each Hour

tripdata_21_22.groupby(["hour","member_casual"])[["ride_length"]].mean()


# In[205]:


plot_9 = tripdata_21_22.groupby(["hour","member_casual"],as_index = False).mean()

sns.lineplot(data=plot_9, 
            x='hour',
            y='ride_length',
            hue="member_casual",
            palette='magma',
            style = "member_casual",
            markers=True
           )
plt.xlabel("hours",size = 10)
plt.ylabel("avg ride length in minutes",size = 10)
plt.xticks(rotation=90)
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', title = 'Member / Casual')
plt.show()

