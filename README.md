# aws_cost project

## Overview

This is a tool designed to pull cost data from AWS cost explorer

## Command Line Examples

example usage:
```bash

# look up all service totals for account 123456789012 for July, 2018
./aws_cost.py -a 123456789012 -m 2018-07
Dates: 2018-07-01 - 2018-07-31
account_id   service                                      total
123456789012 AWS Budgets                                  $0.52
123456789012 AWS Cost Explorer                           $59.84
123456789012 AWS Data Transfer                            $0.00
123456789012 AWS Support (Business)                       $6.80
123456789012 EC2 - Other                                  $3.52
123456789012 Amazon Elastic Compute Cloud - Compute       $4.03
123456789012 Amazon Simple Notification Service           $0.00
123456789012 Amazon Simple Storage Service                $0.00
123456789012 AmazonCloudWatch                             $0.00
123456789012 Total                                       $74.71

# look up all service totals for account 123456789012, current month
./aws_cost.py -a 123456789012
Dates: 2018-11-01 - 2018-11-07
account_id   service                                      total
....

# look up cost of "AWS Support (Business)" for account 123456789012, current month
./aws_cost.py -a 123456789012 -s "AWS Support (Business)"
Dates: 2018-11-01 - 2018-11-07
account_id   service                                      total
123456789012 AWS Support (Business)                        $6.8
123456789012 Total                                         $6.8

# look up cost of 2 AWS services in this account, current month
./aws_cost.py -s "AWS Greengrass,AWS IoT"
Dates: 2018-12-01 - 2018-12-04
Account ID   Service                                      Total
150337127586 AWS Greengrass                               $0.32
150337127586 AWS IoT                                      $0.01
150337127586 Total                                        $0.33

# look up all totals using a cross account role
./aws_cost.py -a 123456789012 -r CloudShift_CostExplorerRole

# print with json output
./aws_cost.py -a 123456789012 --json-out
{
  "attributes": {
    "account_id": "123456789012",
    "start_date": "2018-10-01",
    "end_date": "2018-10-31"
  },
  "services": {
    "AWS Budgets": 0.56,
    "AWS Cost Explorer": 0.02,
    "AWS Key Management Service": 6e-05,
    "AWS Lambda": 0.10275,
    "AWS Support (Business)": 5.44214,
    "Amazon API Gateway": 0.04487,
    "Amazon EC2 Container Registry (ECR)": 0.47212,
    "Amazon EC2 Container Service": 23.97375,
    "EC2 - Other": 4.308,
    "Amazon Elastic Compute Cloud - Compute": 4.06755,
    "Amazon Relational Database Service": 20.10401,
    "Amazon Simple Email Service": 0.0009,
    "Amazon Simple Notification Service": 0.0,
    "Amazon Simple Queue Service": 0.0,
    "Amazon Simple Storage Service": 0.03576,
    "AmazonCloudWatch": 0.01252
  },
  "Total": 59.14443
}
```

Here is an example [cloud formation template](https://s3-us-west-2.amazonaws.com/cfn.cloudshift.cc/CssCostExplorerRole.json) that creates an IAM role in the target account with cost explorer access.

## Module examples
You can call this code as a module from your python scripts
```python
>>> from aws_cost.aws_cost import get_aws_cost
>>> get_aws_cost(account_id=123456789012)
{'attributes': {'account_id': 123456789012, 'start_date': '2018-11-01', 'end_date': '2018-11-16'}, 'services': {'AWS Budgets': 0.26, 'AWS Cost Explorer': 1.38, 'AWS Key Management Service': 0.0, 'AWS Lambda': 0.00673, 'AWS Support (Business)': 1.62824, 'Amazon API Gateway': 0.03483, 'Amazon EC2 Container Registry (ECR)': 0.37609, 'Amazon EC2 Container Service': 0.15696, 'EC2 - Other': 2.2167, 'Amazon Elastic Compute Cloud - Compute': 3.90029, 'Amazon Relational Database Service': 7.84742, 'Amazon Simple Email Service': 0.0005, 'Amazon Simple Notification Service': 0.0, 'Amazon Simple Storage Service': 0.0344, 'AmazonCloudWatch': 0.00628}, 'Total': 17.84844}
```

## Requirements
0. an AWS account with API credentials
1. git (to download this repository)
1. python3 or greater
2. `boto3` pip module installed
3. `begins` pip module installed

## Installation on Linux/mac

1. Clone this repo
```
git clone https://github.com/cloudshiftstrategies/aws_cost
```

2. Create a virtual environment and install the libraries
```bash
cd aws_pricing
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

3. Setup your AWS credentials 
Either [set AWS API environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-environment.html)
or
[Use credentials file](https://docs.aws.amazon.com/cli/latest/userguide/cli-multiple-profiles.html)


## CLI Usage
There is extensive help on the commands and subcommands with -h
```
usage: aws_cost.py [-h] [-v | -q]
                   [--loglvl {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [--logfile LOGFILE] [--logfmt LOGFMT] [--service SERVICE]
                   [--month MONTH] [--role-name ROLE_NAME] [--json-out]
                   [--no-json-out]
                   ACCOUNT_ID

positional arguments:
  ACCOUNT_ID

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increse logging output
  -q, --quiet           Decrease logging output
  --service SERVICE, -s SERVICE
                        (default: None)
  --month MONTH, -m MONTH
                        (default: current)
  --role-name ROLE_NAME, -r ROLE_NAME
                        (default: None)
  --json-out            (default: False)
  --no-json-out

logging:
  Detailed control of logging output

  --loglvl {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set explicit log level
  --logfile LOGFILE     Ouput log messages to file
  --logfmt LOGFMT       Log message format
```
