#!/bin/bash

ip_1="192.168.122.187"
ip_2="192.168.1.142"

ip_1_net="192.168.122.0/24"
ip_1_int="enp1s0"
ip_1_gateway="192.168.122.1"

ip_2_net="192.168.122.0/24"
ip_2_int="enp6s0"
ip_2_gateway="192.168.1.142"


echo $ip_1

ip rule add from $ip_1 table 1
ip rule add from $ip_2 table 2

  # Configure the two different routing tables
ip route add $ip_1_net dev $ip_1_int scope link table 1
ip route add default via $ip_1_gateway dev $ip_1_int table 1

ip route add $ip_2_net dev $ip_2_int scope link table 2
ip route add default via $ip_2_gateway dev $ip_2_int table 2

  # default route for the selection process of normal internet-traffic
ip route add default scope global nexthop via $ip_1_gateway dev $ip_1_int