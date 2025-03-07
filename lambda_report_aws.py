import boto3
import sys
import datetime
from tabulate import tabulate

# Constants for metric retrieval
METRIC_NAMESPACE = "AWS/Lambda"
METRIC_NAME = "Invocations"
PERIOD = 86400  # 1 day
START_TIME = datetime.datetime.utcnow() - datetime.timedelta(days=1440) #datetime.datetime(2025,2,1,0,0,0)
END_TIME = datetime.datetime.utcnow() 

#START_TIME = datetime.datetime(2022,2,1,0,0,0)
#END_TIME = datetime.datetime(2024,2,1,0,0,0)

def get_lambda_functions(region):
    """Fetch Lambda functions and their metadata from a given AWS region."""
    session = boto3.Session(region_name=region)
    lambda_client = session.client("lambda")
    try:
        response = lambda_client.list_functions()
        functions = response.get("Functions", [])
        result = []
        for function in functions:
            function_name = function["FunctionName"]
            creation_date = function["LastModified"]  # Format: '2024-02-29T14:00:00.000+0000'
            # Get last invocation time and total invocations from CloudWatch
            last_invoked, invocations = get_lambda_metrics(region, function_name)
            result.append([function_name, creation_date, last_invoked, invocations, region])
        return result
    except Exception as e:
        print(f"Error fetching Lambda functions in {region}: {e}")
        return []
    
def get_lambda_metrics(region, function_name):
    """Fetch the last execution time and total invocations of a Lambda function using CloudWatch."""
    session = boto3.Session(region_name=region)
    cloudwatch = session.client("cloudwatch")
    try:
        response = cloudwatch.get_metric_statistics(
            Namespace=METRIC_NAMESPACE,
            MetricName=METRIC_NAME,
            Dimensions=[{"Name": "FunctionName", "Value": function_name}],
            StartTime=START_TIME,
            EndTime=END_TIME,
            Period=PERIOD,  # 86400 seconds (1 day)
            Statistics=["Sum"]
        )
        datapoints = response.get("Datapoints", [])
        if datapoints:
            # Last execution time (most recent timestamp)
            last_executed = max(datapoints, key=lambda x: x["Timestamp"])["Timestamp"]
            last_executed = last_executed.strftime("%Y-%m-%d %H:%M:%S UTC")
            # Total invocations over the period
            total_invocations = sum(dp["Sum"] for dp in datapoints)
        else:
            last_executed = "Never Executed"
            total_invocations = 0
        return last_executed, int(total_invocations)
    except Exception as e:
        print(f"Error fetching CloudWatch metrics for {function_name}: {e}")
        return "Error", "Error"
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <region1> <region2> ...")
        sys.exit(1)
    regions = sys.argv[1:]
    all_results = []
    row_number = 1
    for region in regions:
        print(f"Fetching Lambda functions in {region}...")
        region_results = get_lambda_functions(region)
        for entry in region_results:
            all_results.append([row_number] + entry)  # Add row number
            row_number += 1
    # Print assumptions before displaying the table
    print("\nAssumptions for CloudWatch Metrics:")
    print(f"- Namespace: {METRIC_NAMESPACE}")
    print(f"- Region(s): {regions}")
    print(f"- Metric Name: {METRIC_NAME}")
    print(f"- Period: {PERIOD} seconds (1 day)")
    print(f"- Start Time: {START_TIME.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"- End Time: {END_TIME.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    # Display results in tabular format
    if all_results:
        print("\nLambda Function Report")
        print(tabulate(all_results, headers=["#", "Function Name", "Creation Date", "Last Executed", "Invocations", "Region"], tablefmt="grid"))
    else:
        print("No Lambda functions found.")