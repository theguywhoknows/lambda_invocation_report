# AWS Lambda Functions Reporter - Comprehensive Lambda Usage Analytics Across Regions

A Python utility that generates detailed reports of AWS Lambda functions across multiple regions. It leverages CloudWatch metrics to track creation dates, execution times, and invocation counts, helping DevOps teams and AWS administrators monitor Lambda usage patterns through an easy-to-read tabular format.

## Repository Structure
```
.
├── lambda_report_aws.py    # Main script for Lambda function reporting
└── README.md              # Documentation and usage instructions
```

## Usage Instructions
### Prerequisites
- Access to AWS CloudShell from AWS Console
- AWS SDK for Python (boto3) 
- Tabulate library installed 

### Installation
```bash
# In AWS CloudShell:
# Clone the repository
git clone git@github.com:theguywhoknows/lambda_invocation_report.git
cd lambda_invocation_report

# Install tabulate if not already available
pip3 install tabulate boto3
```

### Quick Start
1. If using AWS CloudShell, your credentials are automatically configured. 

2. Run the script specifying one or more AWS regions:
```bash
python3 lambda_report_aws.py us-east-1 us-west-2
```

### More Detailed Examples
1. Generate a report for a single region:
```bash
python3 lambda_report_aws.py us-east-1
```

2. Generate a multi-region report:
```bash
python3 lambda_report_aws.py us-east-1 eu-west-1 ap-southeast-1
```

Example output:
```
Assumptions for CloudWatch Metrics:
- Namespace: AWS/Lambda
- Region(s): ['us-east-1']
- Metric Name: Invocations
- Period: 86400 seconds (1 day)
- Start Time: 2024-02-29 14:00:00 UTC
- End Time: 2024-02-29 14:00:00 UTC

Lambda Function Report
+----+---------------+---------------------+---------------------+-------------+----------+
| #  | Function Name | Creation Date      | Last Executed      | Invocations | Region   |
+====+===============+=====================+=====================+=============+==========+
| 1  | myFunction    | 2024-02-29T14:00:00| 2024-02-29 14:00:00| 150         | us-east-1|
+----+---------------+---------------------+---------------------+-------------+----------+