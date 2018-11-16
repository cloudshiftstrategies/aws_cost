#!/usr/bin/env python3

import boto3, datetime, begin, calendar, datetime, logging
"""
example usage:
# look up all service totals for account 123456789012 this month
./aws_cost.py 123456789012

# look up all service totals for account 123456789012 September, 2018
./aws_cost.py 123456789012 -m 2018-09

# look up all Support totals for account 123456789012 this month
./aws_cost.py 123456789012 -s "AWS Support (Business)"

# look up all totals using a cross account role
./aws_cost.py 123456789012 -r CloudShift_CostExplorerRole
"""

#role_name = 'CloudShift_CostExplorerRole'
# Make botocore  and urllib3 shut up thier excessive logging!
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

@begin.start
@begin.logging
def run(account_id, service=None, month='current', role_name=None):
    "Use AWS Cost Explorer API to look up costs for an account"
    if service:
        logging.debug(f"requested service: {service}")
        services = [service]
    else:
        logging.debug(f"no service specified, checking all services")
        services = []
    if month == 'current':
        logging.debug(f"no month specified, checking current month")
        start_date = datetime.date.today().strftime('%Y-%m-01')
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    else:
        logging.debug(f"requested month: {month}")
        start_date = month + "-01"
        end_date = month + "-%s" %calendar.monthrange(int(month.split("-")[0]), int(month.split("-")[1]))[1]
    if role_name:
        logging.debug(f"requested role name: {role_name}")
        RoleArn = 'arn:aws:iam::%s:role/%s' %(account_id, role_name)
        logging.debug(f"role arn: {RoleArn}")
        # Create a session in the main account
        logging.debug(f"getting boto3 session")
        session = boto3.Session()
        # Get an sts client
        logging.debug(f"getting sts client")
        sts_client = session.client('sts')
        # Get creds to switch roles to target account
        logging.debug(f"getting assume role aws credentials")
        awscreds = sts_client.assume_role(
            RoleArn = RoleArn,
            RoleSessionName = 'InvoiceAuditSession'
        )['Credentials']

        # Create a cost explorer client for target account
        logging.debug(f"using assume role credentials to request cost explorer client")
        ce_client = boto3.client("ce",
                aws_access_key_id = awscreds['AccessKeyId'],
                aws_secret_access_key= awscreds['SecretAccessKey'],
                aws_session_token = awscreds['SessionToken'])
    else:
        logging.debug("no role name specified, using creds from environment variables")
        ce_client = boto3.client("ce")

    # If a specific service wasnt requested, get them all
    if not services:
        response = ce_client.get_dimension_values(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Dimension='SERVICE',
            Context='COST_AND_USAGE')
        for service in response['DimensionValues']:
            services.append(service['Value'])
        logging.debug(f"found {len(services)} services active for this account/time period")

    # Get the total for the service
    print(f"Dates: {start_date} - {end_date}")
    print("%-13s%-40s%10s" %('account_id','service','total'))
    total = 0.0
    for service in services:
        amount = None
        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=[
                'UnblendedCost',
            ],
            Filter= {'Dimensions': { 'Key': 'SERVICE', 'Values': [service] } }
        )
        amount = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
        total += float(amount)
        amount = "$" + str(round(float(amount),2))
        print("%-13s%-40s%10s" %(account_id, service[:39], amount))

    total = "$" + str(round(float(total),2))
    print("%-13s%-40s%10s" %(account_id, 'Total', total))
