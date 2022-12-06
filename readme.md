# IP Multicast test

ip_multicast_test.py is python script that joins specified [IP Multicast groups](https://en.wikipedia.org/wiki/IP_multicast) and prints the payload coming in on those groups.

This tool comes in handy when devices use IP Multicast for [heartbeat](https://en.wikipedia.org/wiki/Heartbeat_(computing)) signals and one quickly needs to check which devices are online.

```
usage: ip_multicast_test.py [-h] [--if_addr IF_ADDR]
                            [--multicast_group MULTICAST_GROUP]
                            [--multicast_port MULTICAST_PORT] [--print_data]

optional arguments:
  -h, --help            show this help message and exit
  --if_addr IF_ADDR     Ip address of interface which we want to join the
                        multicast group on. If 0.0.0.0 (default) the multicast
                        group will be joined on each interface individually.
  --multicast_group MULTICAST_GROUP
                        Multicast group to join. Default is 239.0.0.0.
  --multicast_port MULTICAST_PORT
                        Port to bind to multicast group. Default is 40000.
  --print_data          If set the payload coming in over IP multicast will be
                        printed as hex payload (e.g DE AD BE EF).
```