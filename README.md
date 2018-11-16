# aws_cost project

## Overview

This is a tool designed to pull cost data from AWS cost explorer

## Command Line Examples

example usage:
```bash

# look up all service totals for account 357849880876 for July, 2018
./aws_cost.py 357849880876 -m 2018-07
Dates: 2018-07-01 - 2018-07-31
account_id   service                                      total
357849880876 AWS Budgets                                  $0.52
357849880876 AWS Cost Explorer                           $59.84
357849880876 AWS Data Transfer                            $0.00
357849880876 AWS Support (Business)                       $6.80
357849880876 EC2 - Other                                  $3.52
357849880876 Amazon Elastic Compute Cloud - Compute       $4.03
357849880876 Amazon Simple Notification Service           $0.00
357849880876 Amazon Simple Storage Service                $0.00
357849880876 AmazonCloudWatch                             $0.00
357849880876 Total                                       $74.71

# look up all service totals for account 123456789012, current month
./aws_cost.py 123456789012
Dates: 2018-11-01 - 2018-11-07
account_id   service                                      total
....

# look up cost of "AWS Support (Business)" for account 123456789012, current month
./aws_cost.py 123456789012 -s "AWS Support (Business)"
Dates: 2018-11-01 - 2018-11-07
account_id   service                                      total
357849880876 AWS Support (Business)                        $6.8
357849880876 Total                                         $6.8

# look up all totals using a cross account role
./aws_cost.py 123456789012 -r CloudShift_CostExplorerRole
```

Here is an example [cloud formation template](https://s3-us-west-2.amazonaws.com/cfn.cloudshift.cc/CssCostExplorerRole.json) that creates an IAM role in the target account with cost explorer access.

## Module examples
This library is not currently designed to be used as a module in your python apps

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
                   [--month MONTH] [--role-name ROLE_NAME]
                   ACCOUNT_ID

Use AWS Cost Explorer API to look up costs for an account

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

logging:
  Detailed control of logging output

  --loglvl {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set explicit log level
  --logfile LOGFILE     Ouput log messages to file
  --logfmt LOGFMT       Log message format
```
