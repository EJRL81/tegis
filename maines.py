import json

dic_data={
    {
        "provider": {
            "aws": {
                "region": "us-east-1"
            }
        },
        "resource": {
            "aws_vpc": {
                "main": {
                    "cidr_block": "10.0.0.0/16"
                }
            },
            "aws_subnet": {
                "subnet_1": {
                    "vpc_id": "${aws_vpc.main.id}",
                    "cidr_block": "10.0.1.0/24",
                    "availability_zone": "us-east-1a"
                },
                "subnet_2": {
                    "vpc_id": "${aws_vpc.main.id}",
                    "cidr_block": "10.0.2.0/24",
                    "availability_zone": "us-east-1b"
                }
            },
            "aws_security_group": {
                "web_sg": {
                    "vpc_id": "${aws_vpc.main.id}",
                    "ingress": [
                        {
                            "from_port": 80,
                            "to_port": 80,
                            "protocol": "tcp",
                            "cidr_blocks": ["0.0.0.0/0"]
                        },
                        {
                            "from_port": 22,
                            "to_port": 22,
                            "protocol": "tcp",
                            "cidr_blocks": ["0.0.0.0/0"]
                        }
                    ],
                    "egress": [
                        {
                            "from_port": 0,
                            "to_port": 0,
                            "protocol": "-1",
                            "cidr_blocks": ["0.0.0.0/0"]
                        }
                    ],
                    "tags": {
                        "Name": "web_sg"
                    }
                },
                "ftp_sg": {
                    "vpc_id": "${aws_vpc.main.id}",
                    "ingress": [
                        {
                            "from_port": 21,
                            "to_port": 21,
                            "protocol": "tcp",
                            "cidr_blocks": ["0.0.0.0/0"]
                        },
                        {
                            "from_port": 22,
                            "to_port": 22,
                            "protocol": "tcp",
                            "cidr_blocks": ["0.0.0.0/0"]
                        }
                    ],
                    "egress": [
                        {
                            "from_port": 0,
                            "to_port": 0,
                            "protocol": "-1",
                            "cidr_blocks": ["0.0.0.0/0"]
                        }
                    ],
                    "tags": {
                        "Name": "ftp_sg"
                    }
                }
            },
            "aws_key_pair": {
                "deployer_key": {
                    "key_name": "deployer_key",
                    "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAsamplePublicKey..."
                }
            },
            "aws_instance": {
                "server1": {
                    "ami": "ami-0b69ea66ff7391e80",
                    "instance_type": "t2.micro",
                    "subnet_id": "${aws_subnet.subnet_1.id}",
                    "security_groups": ["${aws_security_group.web_sg.name}"],
                    "key_name": "${aws_key_pair.deployer_key.key_name}",
                    "tags": {
                        "Name": "Servidor 1"
                    },
                    "user_data": "#!/bin/bash\napt-get update\napt-get install -y apache2\nsystemctl start apache2\nsystemctl enable apache2"
                },
                "server2": {
                    "ami": "ami-0b69ea66ff7391e80",
                    "instance_type": "t2.micro",
                    "subnet_id": "${aws_subnet.subnet_2.id}",
                    "security_groups": ["${aws_security_group.ftp_sg.name}"],
                    "key_name": "${aws_key_pair.deployer_key.key_name}",
                    "tags": {
                        "Name": "Servidor 2"
                    },
                    "user_data": "#!/bin/bash\napt-get update\napt-get install -y vsftpd\nsystemctl start vsftpd\nsystemctl enable vsftpd"
                }
            }
        }
    }
}

print(json.dumps(dic_data, indent=2))


if __name__ == '__main__':
    pass