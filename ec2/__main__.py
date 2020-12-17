# Copyright 2016-2018, Pulumi Corporation.  All rights reserved.

import pulumi
import pulumi_aws as aws

size = 't2.small'

ami = aws.get_ami(most_recent="true",
                  owners=['amazon'],
                  filters=[{"name":"name","values":["amzn-ami-hvm-*"]}])

group = aws.ec2.SecurityGroup('web-secgrp',
    description='Enable HTTP access',
    ingress=[
        { 'protocol': 'tcp', 'from_port': 80, 'to_port': 80, 'cidr_blocks': ['0.0.0.0/0'] }
    ])

user_data = """
#!/bin/bash
echo "Hello, World from Pulumi!" > index.html
nohup python -m SimpleHTTPServer 80 &
"""

instance = aws.ec2.Instance('web-server',
    instance_type=size,
    vpc_security_group_ids=[group.id],
    user_data=user_data,
    ami=ami.id,
    tags={
        "Name": "Pulumi_ec2",
    })

pulumi.export('public_ip', instance.public_ip)
pulumi.export('public_dns', instance.public_dns)
