# aws_cost project

## Overview

This is a tool designed to pull cost data from AWS cost explorer

## Command Line Examples

example usage:
```bash
# look up all service totals for account 123456789012 this month
./aws_cost.py 123456789012

# look up all service totals for account 123456789012 September, 2018
./aws_cost.py 123456789012 -m 2018-09

# look up all Support totals for account 123456789012 this month
./aws_cost.py 123456789012 -s "AWS Support (Business)"

# look up all totals using a cross account role
./aws_cost.py 123456789012 -r CloudShift_CostExplorerRole
```

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
