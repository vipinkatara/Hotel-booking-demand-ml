# -*- coding: utf-8 -*-
"""classification-and-prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/vipinkatara/Hotel-booking-demand-ml/blob/master/classification-and-prediction.ipynb

Context

Have you ever wondered when the best time of year to book a hotel room is? Or the optimal length of stay in order to get the best daily rate? What if you wanted to predict whether or not a hotel was likely to receive a disproportionately high number of special requests?

This hotel booking dataset can help you explore those questions!
Content

This data set contains booking information for a city hotel and a resort hotel, and includes information such as when the booking was made, length of stay, the number of adults, children, and/or babies, and the number of available parking spaces, among other things.

All personally identifying information has been removed from the data.
Acknowledgements

The data is originally from the article Hotel Booking Demand Datasets, written by Nuno Antonio, Ana Almeida, and Luis Nunes for Data in Brief, Volume 22, February 2019.

The data was downloaded and cleaned by Thomas Mock and Antoine Bichat for #TidyTuesday during the week of February 11th, 2020.
Inspiration

This data set is ideal for anyone looking to practice their exploratory data analysis (EDA) or get started in building predictive models!

If you're looking for inspiration on data visualizations, check out the #TidyTuesday program, a free, weekly online event that encourages participants to create and share their code and visualizations for a given data set on Twitter.

If you'd like to dive into predictive modeling, Julia Silge has an accessible and fantastic walk-through which highlights the tidymodels R package.

hotel

Hotel (H1 = Resort Hotel or H2 = City Hotel)
is_canceled

Value indicating if the booking was canceled (1) or not (0)
lead_time

Number of days that elapsed between the entering date of the booking into the PMS and the arrival date
arrival_date_year

Year of arrival date
arrival_date_month

Month of arrival date
arrival_date_week_number

Week number of year for arrival date
arrival_date_day_of_month

Day of arrival date
stays_in_weekend_nights

Number of weekend nights (Saturday or Sunday) the guest stayed or booked to stay at the hotel
stays_in_week_nights

Number of week nights (Monday to Friday) the guest stayed or booked to stay at the hotel
adults

Number of adults
children

Number of children
babies

Number of babies
meal

Type of meal booked. Categories are presented in standard hospitality meal packages: Undefined/SC – no meal package; BB – Bed & Breakfast; HB – Half board (breakfast and one other meal – usually dinner); FB – Full board (breakfast, lunch and dinner)
country

Country of origin. Categories are represented in the ISO 3155–3:2013 format
market_segment

Market segment designation. In categories, the term “TA” means “Travel Agents” and “TO” means “Tour Operators”
distribution_channel

Booking distribution channel. The term “TA” means “Travel Agents” and “TO” means “Tour Operators”
is_repeated_guest

Value indicating if the booking name was from a repeated guest (1) or not (0)
previous_cancellations

Number of previous bookings that were cancelled by the customer prior to the current booking
previous_bookings_not_canceled

Number of previous bookings not cancelled by the customer prior to the current booking
reserved_room_type

Code of room type reserved. Code is presented instead of designation for anonymity reasons.
assigned_room_type

Code for the type of room assigned to the booking. Sometimes the assigned room type differs from the reserved room type due to hotel operation reasons (e.g. overbooking) or by customer request. Code is presented instead of designation for anonymity reasons.

booking_changes

Number of changes/amendments made to the booking from the moment the booking was entered on the PMS until the moment of check-in or cancellation
deposit_type

Indication on if the customer made a deposit to guarantee the booking. This variable can assume three categories: No Deposit – no deposit was made; Non Refund – a deposit was made in the value of the total stay cost; Refundable – a deposit was made with a value under the total cost of stay.
agent

ID of the travel agency that made the booking
company

ID of the company/entity that made the booking or responsible for paying the booking. ID is presented instead of designation for anonymity reasons
days_in_waiting_list

Number of days the booking was in the waiting list before it was confirmed to the customer
customer_type

Type of booking, assuming one of four categories:

Contract - when the booking has an allotment or other type of contract associated to it; Group – when the booking is associated to a group; Transient – when the booking is not part of a group or contract, and is not associated to other transient booking; Transient-party – when the booking is transient, but is associated to at least other transient booking
adr

Average Daily Rate as defined by dividing the sum of all lodging transactions by the total number of staying nights
required_car_parking_spaces

Number of car parking spaces required by the customer
total_of_special_requests

Number of special requests made by the customer (e.g. twin bed or high floor)
reservation_status

Reservation last status, assuming one of three categories: Canceled – booking was canceled by the customer; Check-Out – customer has checked in but already departed; No-Show – customer did not check-in and did inform the hotel of the reason why
reservation_status_date

Date at which the last status was set. This variable can be used in conjunction with the ReservationStatus to understand when was the booking canceled or when did the customer checked-out of the hotel

# Importing Libraries
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import decomposition
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

"""# Loading the data"""

df = pd.read_csv('hotel_bookings.csv', encoding='utf8')
df.head(10)

df.columns

df



"""# Checking Null values"""

df.isnull().sum()

"""# removing columns and dropping null"""

df.dropna(subset=['country', 'children'], inplace=True)

df.isnull().sum()

df.shape

df[df['agent'].isnull()]

df['agent'].value_counts()



#dropping agent, country, arrival_date_week_number columns 
df.drop('agent', axis=1, inplace=True)
df.drop('company', axis=1, inplace=True)
df.drop('arrival_date_week_number', axis=1, inplace=True)

df

df.isnull().sum()

df['arrival_date_month'].unique()

d = {'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November':11, 'December': 12,
       'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6}

df['arrival_date_month'] = df['arrival_date_month'].map(d)

df['arrival_date_month'].iloc[0]

df['arrival_date_day_of_month']=df['arrival_date_day_of_month'].apply(str)
df['arrival_date_month'] = df['arrival_date_month'].apply(str)
df['arrival_date_year']=df['arrival_date_year'].apply(str)

"""# Deduplication"""

df = df.drop_duplicates()

df

"""# Merging necessary columns"""

df['arrival_date'] = df[['arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month']].agg('-'.join, axis=1)

df

df.drop(['arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month'], axis=1, inplace=True)

df

df.columns

"""# Initializing the label encoder"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

for i in df.columns:
    print(i)
    print(type(df[i].iloc[0]))

df['hotel'] = le.fit_transform(df['hotel'])
df['country'] = le.fit_transform(df['country'])
df['market_segment'] = le.fit_transform(df['market_segment'])
df['reserved_room_type'] = le.fit_transform(df['reserved_room_type'])
df['assigned_room_type'] = le.fit_transform(df['assigned_room_type'])
df['deposit_type'] = le.fit_transform(df['deposit_type'])
df['customer_type'] = le.fit_transform(df['customer_type'])
df['reservation_status'] = le.fit_transform(df['reservation_status'])
df['meal'] = le.fit_transform(df['meal'])
df['distribution_channel'] = le.fit_transform(df['distribution_channel'])

df

#converting dates to unix timestamp
dates = pd.to_datetime(df['arrival_date'])
df['arrival_date'] = (dates - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s') 

dates = pd.to_datetime(df['reservation_status_date'])
df['reservation_status_date'] = (dates - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

for i in df.columns:
    print(type(df[i].iloc[0]))

"""# Spliting the dataset into feature and label"""

label = df['reservation_status']
df.drop('reservation_status', axis=1, inplace=True)

"""# Spliting the dataset into training and testing data"""

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(df,label, test_size=0.3, random_state=0)

"""# Classification and prediction"""

#using decision tree
from sklearn import tree
clf_tree = tree.DecisionTreeClassifier()
clf_tree.fit(x_train,y_train)

pred = clf_tree.predict(x_test)
print(classification_report(y_test, pred))
print()
print('Confusion Matrix:\n',confusion_matrix(y_test, pred))
print()
print('Accuracy : ',accuracy_score(y_test, pred))

#using randomforestclassifier
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(x_train, y_train)

pred = clf.predict(x_test)
print(classification_report(y_test, pred))
print()
print('Confusion Matrix:\n',confusion_matrix(y_test, pred))
print()
print('Accuracy : ',accuracy_score(y_test, pred))





