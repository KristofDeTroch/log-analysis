import os
import pandas as pd
import matplotlib.pyplot as plt


class CSVHeaders:
    date = "date"
    time = "time"
    x_edge_location = "x-edge-location"
    sc_bytes = "sc-bytes"
    c_ip = "c-ip"
    cs_method = "cs-method"
    cs_host = "cs-host"
    cs_uri_stem = "cs-uri-stem"
    sc_status = "sc-status"
    cs_referer = "cs-referer"
    cs_user_agent = "cs-user-agent"
    cs_uri_query = "cs-uri-query"
    cs_cookie = "cs-cookie"
    x_edge_result_type = "x-edge-result-type"
    x_edge_request_id = "x-edge-request-id"
    x_host_header = "x-host-header"
    cs_protocol = "cs-protocol"
    cs_bytes = "cs-bytes"
    time_taken = "time-taken"
    x_forwarded_for = "x-forwarded-for"
    ssl_protocol = "ssl-protocol"
    ssl_cipher = "ssl-cipher"
    x_edge_response_result_type = "x-edge-response-result-type"
    cs_protocol_version = "cs-protocol-version"
    fle_status = "fle-status"
    fle_encrypted_fields = "fle-encrypted-fields"
    c_port = "c-port"
    time_to_first_byte = "time-to-first-byte"
    x_edge_detailed_result_type = "x-edge-detailed-result-type"
    sc_content_type = "sc-content-type"
    sc_content_len = "sc-content-len"
    sc_range_start = "sc-range-start"
    sc_range_end = "sc-range-end"


def percentile(n):
    def percentile_(x):
        return x.quantile(n)

    percentile_._value__ = "percentile_{:02.0f}".format(n * 100)
    return percentile_


def latency_per_route(df):
    START_TIME = "11:30:00"
    END_TIME = "12:15:00"
    sub_data_frame = df[
        (df[CSVHeaders.time] > START_TIME) & (df[CSVHeaders.time] < END_TIME)
    ]
    test = (
        sub_data_frame[
            [CSVHeaders.cs_method, CSVHeaders.cs_uri_stem, CSVHeaders.time_taken]
        ]
        .groupby([CSVHeaders.cs_method, CSVHeaders.cs_uri_stem])
        .agg(["count", "mean", "min", "max", percentile(0.5), percentile(0.95)])
    )
    test.columns = ["count", "mean", "max", "min", "percentile_50", "percentile_95"]

    # Sort the results by 'time-taken_mean' in descending order
    test = test.sort_values("mean", ascending=False)

    # Save the results to CSV
    test.to_csv("latency_per_route.csv")


def status_codes_per_minute(df):
    df["timestamp"] = pd.to_datetime(df[CSVHeaders.date] + " " + df[CSVHeaders.time])

    # Step 3: Drop the original 'date' and 'time' columns
    df.drop(columns=[CSVHeaders.date, CSVHeaders.time], inplace=True)

    # Step 4: Group the data by minute and response code
    df["minute"] = df["timestamp"].dt.to_period("T")  # Extracting minute from timestamp
    grouped_data = (
        df.groupby(["minute", CSVHeaders.sc_status]).size().reset_index(name="count")
    )

    response_bins = [0, 199, 299, 399, 499, 600]  # You can adjust the bins as needed
    response_labels = ["Other", "2xx", "3xx", "4xx", "5xx"]

    grouped_data["response_group"] = pd.cut(
        grouped_data[CSVHeaders.sc_status],
        bins=response_bins,
        labels=response_labels,
    )

    # Step 5: Pivot the data to have response codes as columns
    grouped_data = (
        grouped_data.groupby(["minute", "response_group"])["count"]
        .sum()
        .unstack()
        .fillna(0)
    )

    # Step 6: Save the result to a new CSV file
    output_csv = "status_codes_per_minute.csv"
    grouped_data.to_csv(output_csv)


def aggregate_above_threshold(df):
    sub_data_frame = df[df[CSVHeaders.time_taken] > 10]
    test = (
        sub_data_frame[
            [
                CSVHeaders.cs_uri_stem,
                CSVHeaders.cs_method,
                CSVHeaders.time_taken,
                CSVHeaders.time,
            ]
        ]
        .groupby([CSVHeaders.cs_uri_stem, CSVHeaders.cs_method])
        .agg(
            {
                CSVHeaders.time_taken: ["count"],
                CSVHeaders.time: ["min", "max"],
            }
        )
    )
    test.columns = ["count", "min", "max"]
    # Step 6: Save the result to a new CSV file
    output_csv = "aggregate_above_threshold.csv"
    test.to_csv(output_csv)


def filter_by(df):
    ROUTE = "/api/v2/fan-group-owner/waiting-lists/b69ccdb4-3c34-4b67-93a2-525d14b57165/seats"
    METHOD = "PUT"

    sub_data_frame = df[
        (df[CSVHeaders.cs_uri_stem] == ROUTE) & (df[CSVHeaders.cs_method] == METHOD)
    ]
    sub_data_frame.sort_values(CSVHeaders.time, ascending=False)

    output_csv = "filter_by.csv"
    sub_data_frame.to_csv(output_csv, sep="\t")


inputFolder = "cf-2023-06-28-processed"


def filterCSV(file_name: str):
    return file_name.endswith(".csv")


files = filter(filterCSV, os.listdir(inputFolder))

df = pd.concat(
    [pd.read_csv(f"{inputFolder}/{file_name}", sep="\t") for file_name in files]
)
filter_by(df.copy())

print("Output CSV file saved successfully!")
