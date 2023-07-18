# Introduction

This repo was used to analyse AWS Cloud Front logs to find the cause of performance issues.
It takes the raw cv's as input. Then preprocesses them with a TS script. The final analysis happens with Pandas in Python.

This is a personal repo where I keep track of different versions and changes. It was used to gather insights for a specific product. Your use case may vary, but I hope it helps you.

# Pre processing

The raw files obtained from AWS need to be appended with '.csv' to be accepted by the script. It then removes the unnecessary lines starting with a '#' and formats the header to allign with the separators on other lines. The final processed csv is stored in a different folder to be more easily managed. [source](./transformer.ts)

# Analysis

It is difficult to obtain actionable metrics from logs. I created a number of experiments that all output a separate csv as a result. Each experiment can be run individually and they can be extended as well. I found Python cumbersome to display the data in usefull formats so I used Google Sheets for visualizations. [source](./analysis.py)

I will detail each experiment below and why I found this usefull.

## Experiment 1

This experiment aggregates latency per route within a specific time range. It lists the number of calls this route received, the mean, maximum, minimum, 50 percentile and the 95 percentile. 

The resulting csv gives insights in the bottlenecks as well as the frequently accessed routes within that period. I used this to analyse where certain performance degradation peaks come from.

## Experiment 2

This experiment counts the response types per minute. Types are grouped by 100's to track success, redirect, client-side errors and server-side errors. 

The final data is easily visualised in Google Sheets where it can be overlaid with database loads or other metrics to find server performance tipovers. Especially the 5xx status code responses give an interesting view.

