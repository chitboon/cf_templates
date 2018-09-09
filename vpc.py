from troposphere import *
from troposphere.ec2 import *

t = Template()

t.add_version('2018-9-9')
t.add_description('Single ec2 instance in private subnet sample created using troposphere')

ref_stack_id = Ref('AWS::StackId')
ref_region = Ref('AWS::Region')

vpc = t.add_resource (
        VPC
        (
            'VPC',
            CidrBlock='10.0.0.0/16',
            Tags = Tags(Application=ref_stack_id)
        )
    )

internetGateway = t.add_resource (
        InternetGateway
        (
            'InternetGateway',
            Tags = Tags(Application=ref_stack_id)
        )
    )

gatewayAttachment = t.add_resource(
        VPCGatewayAttachment
        (
            'AttachGateway',
            VpcId = Ref(vpc),
            InternetGatewayId = Ref(internetGateway)
        )
    )

nat_eip = t.add_resource(
        EIP
        (
            'NatEip',
            Domain="vpc",
        )
    )

subnet1 = t.add_resource(
        Subnet(
            'PublicSubnet',
            CidrBlock='10.0.0.0/24',
            VpcId=Ref(vpc),
            Tags=Tags(Application=ref_stack_id)
        )
    )

subnet2 = t.add_resource(
        Subnet(
            'PrivateSubnet',
            CidrBlock='10.0.1.0/24',
            VpcId=Ref(vpc),
            Tags=Tags(Application=ref_stack_id)
        )
    )

nat = t.add_resource(
        NatGateway
        (
            'Nat',
            AllocationId=GetAtt(nat_eip, 'AllocationId'),
            SubnetId = Ref(subnet1)
        )
    )

private_route_table = t.add_resource(
        RouteTable
        (
            'PrivateRouteTable',
            VpcId=Ref(vpc)
        )
    )

public_route_table = t.add_resource(
        RouteTable
        (
            'PublicRouteTable',
            VpcId=Ref(vpc)
        )
    )

public_route_association = t.add_resource(
        SubnetRouteTableAssociation
        (
            'PublicRouteAssociation',
            SubnetId=Ref(subnet1),
            RouteTableId=Ref(public_route_table)
        )
    )

default_public_route = t.add_resource(
        Route
        (
            'PublicDefaultRoute',
            RouteTableId=Ref(public_route_table),
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=Ref(internetGateway)
        )
    )

private_route_association = t.add_resource(
        SubnetRouteTableAssociation
        (
            'PrivateRouteAssociation',
            SubnetId=Ref(subnet2),
            RouteTableId=Ref(private_route_table)
        )
    )

default_private_route = t.add_resource(
        Route
        (
            'PrivateDefaultRoute',
            RouteTableId=Ref(private_route_table),
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=Ref(nat)
        )
    )

print(t.to_yaml())
