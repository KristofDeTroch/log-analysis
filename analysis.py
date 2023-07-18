import os
import pandas as pd
import matplotlib.pyplot as plt

def percentile(n):
    def percentile_(x):
        return x.quantile(n)
    percentile_.__name__ = 'percentile_{:02.0f}'.format(n*100)
    return percentile_

def experiment1(df):
    sub_data_frame = df[(df['time'] > "11:30:00") & (df['time'] < "12:15:00")]
    test = sub_data_frame[['cs-method','cs-uri-stem', 'time-taken']].groupby(['cs-uri-stem', 'cs-method']).agg(['count', 'mean', 'min', 'max', percentile(0.5), percentile(0.95)])
    test.columns = ['count','mean','max', 'min','percentile_50', 'percentile_95']

    # Sort the results by 'time-taken_mean' in descending order
    test = test.sort_values('mean', ascending=False)

    # Save the results to CSV
    test.to_csv('experiment1.csv')

def experiment2(df):
    
    df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'])

    # Step 3: Drop the original 'date' and 'time' columns
    df.drop(columns=['date', 'time'], inplace=True)

    # Step 4: Group the data by minute and response code
    df['minute'] = df['timestamp'].dt.to_period('T')  # Extracting minute from timestamp
    grouped_data = df.groupby(['minute', 'sc-status']).size().reset_index(name='count')

    response_bins = [0, 199, 299, 399, 499, 600]  # You can adjust the bins as needed
    response_labels = ['Other', '2xx', '3xx', '4xx', '5xx']

    grouped_data['response_group'] = pd.cut(grouped_data['sc-status'], bins=response_bins, labels=response_labels)

    # Step 5: Pivot the data to have response codes as columns
    grouped_data = grouped_data.groupby(['minute', 'response_group'])['count'].sum().unstack().fillna(0)

    # Step 6: Save the result to a new CSV file
    output_csv = "experiment2.csv"
    grouped_data.to_csv(output_csv)



inputFolder = 'cf-2023-06-28-processed'

files = os.listdir(inputFolder)

df = pd.concat([pd.read_csv(f'{inputFolder}/{file_name}', sep='\t') for file_name in files])
experiment2(df.copy())

print("Output CSV file saved successfully!")



