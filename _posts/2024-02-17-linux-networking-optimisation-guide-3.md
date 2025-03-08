---
layout: blog
title: "Linux Networking Optimization Guide - Part III"
date: 2024-02-17
categories: [Linux, Networking]
tags: [Linux, Performance, Networking, Optimization]
---

# Linux Networking Optimisation Guide Part III (Cont.)

- date: 2017-01-20
- category: Networking
- tags: networking, Linux

----------------

### MTU

Change MTU to 9000 is going to help increase the throughput and efficiency on big packets. However all the routes/switches on the path should support jumbo-frame, e.g. over 9000.

```
ip link set eth1 mtu 9000
ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 00:1e:c9:b4:86:0e brd ff:ff:ff:ff:ff:ff
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9000 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 00:1e:c9:b4:86:10 brd ff:ff:ff:ff:ff:ff
```

### QLEN

The length of the Queuing Discipline in the packet transfer process. Increasing this value may lead to bufferbloat with increasing latency.

Normally the queue length 1000 is enough for the 10G/40G network. However if the error on ip -s link or ifconfig -a eth0 is increasing, then try to increase the qlen.

```
 ip link show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq master ovs-system state UP mode DEFAULT group default qlen 1000
    link/ether 00:22:19:5b:e2:f2 brd ff:ff:ff:ff:ff:ff

 ip -s link show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq master ovs-system state UP mode DEFAULT group default qlen 1000
    link/ether 00:22:19:5b:e2:f2 brd ff:ff:ff:ff:ff:ff
    RX: bytes  packets  errors  dropped overrun mcast
    56272058545094 237996400274 10125   0       10125   790686739
    TX: bytes  packets  errors  dropped carrier collsns
    338460632172563 338969673742 0       0       0       0
```


### Power State

CPU Power State other than C1 & C0 should all be disabled, it should first be disabled in BIOS.

The processor.max_cstate=1 and intel_idle.max_cstate=0 could be added in the grub line to override BIOS setting.

```
 vi /etc/default/grub

GRUB_DEFAULT=0
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash processor.max_cstate=1 intel_idle.max_cstate=0"
GRUB_CMDLINE_LINUX="clocksource=tsc ipv6.disable=1"

 update-grub
Generating grub configuration file ...
Found linux image: /boot/vmlinuz-3.16.0-4-amd64
Found initrd image: /boot/initrd.img-3.16.0-4-amd64
Found memtest86+ image: /boot/memtest86+.bin
Found memtest86+ multiboot image: /boot/memtest86+_multiboot.bin
done
```

It could be confirmed by

```
cat /sys/module/intel_idle/parameters/max_cstate
9
```

### Pause Frame

Pause frame are sent out once the Tx and Rx are full to local switch port, if the switch support pause frame, the switch will pause sending the packets for orders of ms or less, which is pretty enough for the processing the Tx/Rx remaining buffer. Both switch and ethernet card on the server should support Pause frame.

```
 ethtool -a eth4
Pause parameters for eth4:
Autonegotiate:    off
RX:        on
TX:        on
```

To turn on the Rx and Tx Pause Frame

```
 ethtool -A eth4 rx on
```

### TCP/UDP Parameter

There are a lot of TCP parameters on linux could be optimised:

net.ipv4.tcp_timestamps = 1

Timestamp options could avoid wrapped sequence numbers, and improve window size and buffer calculation. If bandwidth is high and TCP sequence numbers is wrapped very quickly, do turn on the tcp time stamp option. But keep in mind it does increase the CPU usage.

```
net.ipv4.tcp_sack = 0
```

Selective ack could allow sender only transmit the lost bytes other than all the bytes. Turning on the sack may increase the CPU load. Unless there is a very high latency or high packet loss link, it is suggest to turn off the tcp_sack. There are still some controversy on turning off this option.

```
net.ipv4.tcp_window_scaling = 1
```

Originally the tcp window size is 8bit, it is not enough for the bandwidth nowadays. Turning on tcp window scaling to increase the window size, and both size should both support tcp window scale to finish a successful tcp negotiation. 

```
net.ipv4.tcp_rmem=4096 87380 16777216
net.ipv4.tcp_wmem=4096 65536 16777216
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.core.wmem_default = 2097152
net.core.rmem_default = 2097152
net.core.optmem_max = 524287
```

wmem/rmem is the socket buffer size. TCP and UDP Rx and Tx buffer could be set to a large value to avoid packet errors. The command line netstat -us or -ts could be checked if there are some UDP or TCP related errors.

```
net.core.somaxconn = 8192
```

To avoid SYN Flood to stop new connection drop or SYN Cookie to send. The TCP listen back log should be increased to a larger number. It is the maximum number of unaccepted TCP connection the system could handle.

```
net.ipv4.tcp_adv_win_scale = 1
net.ipv4.tcp_fin_timeout = 15
```
To release resource more quickly by setting fin timeout to 15s. It is the timeout period of fin-wait-2 to closed. 

### MSI-X/NAPI

Check if MSI-X is enabled, normally it is enabled by default. 

```
# lspci -vvv | less
        Capabilities: [70] MSI-X: Enable+ Count=64 Masked-
                Vector table: BAR=4 offset=00000000
                PBA: BAR=4 offset=00002000
```

Normally NAPI is enabled by default.

### Module Parameters

Some Module (bnx2x or ixgbe) parameters may need to adjusted to improve the performance.

For example, the num of queues could be adjusted by load the module with new parameter value on 'num_queues', do it on the console. Normally this value doesn't need to be changed, the default value is number of the CPU.

modprobe -r bnx2x
modprobe bnx2x num_queues=2

```
 modinfo bnx2x
parm:           num_queues: Set number of queues (default is as a number of CPUs) (int)
parm:           disable_tpa: Disable the TPA (LRO) feature (int)
parm:           int_mode: Force interrupt mode other than MSI-X (1 INT#x; 2 MSI) (int)
parm:           dropless_fc: Pause on exhausted host ring (int)
parm:           mrrs: Force Max Read Req Size (0..3) (for debug) (int)
parm:           debug: Default debug msglevel (int)
```

The value could be checked in 

```
 cat /sys/module/bnx2x/parameters/int_mode
0
```

For intel ixgbe, there are lots of parameter could be modified as well

```
parm:           InterruptType:Change Interrupt Mode (0=Legacy, 1=MSI, 2=MSI-X), default IntMode (deprecated) (array of int)
parm:           IntMode:Change Interrupt Mode (0=Legacy, 1=MSI, 2=MSI-X), default 2 (array of int)
parm:           MQ:Disable or enable Multiple Queues, default 1 (array of int)
parm:           DCA:Disable or enable Direct Cache Access, 0=disabled, 1=descriptor only, 2=descriptor and data (array of int)
parm:           RSS:Number of Receive-Side Scaling Descriptor Queues, default 0=number of cpus (array of int)
parm:           VMDQ:Number of Virtual Machine Device Queues: 0/1 = disable, 2-16 enable (default=8) (array of int)
parm:           max_vfs:Number of Virtual Functions: 0 = disable (default), 1-63 = enable this many VFs (array of int)
parm:           VEPA:VEPA Bridge Mode: 0 = VEB (default), 1 = VEPA (array of int)
parm:           InterruptThrottleRate:Maximum interrupts per second, per vector, (0,1,956-488281), default 1 (array of int)
parm:           LLIPort:Low Latency Interrupt TCP Port (0-65535) (array of int)
parm:           LLIPush:Low Latency Interrupt on TCP Push flag (0,1) (array of int)
parm:           LLISize:Low Latency Interrupt on Packet Size (0-1500) (array of int)
parm:           LLIEType:Low Latency Interrupt Ethernet Protocol Type (array of int)
parm:           LLIVLANP:Low Latency Interrupt on VLAN priority threshold (array of int)
parm:           FdirPballoc:Flow Director packet buffer allocation level:
            1 = 8k hash filters or 2k perfect filters
            2 = 16k hash filters or 4k perfect filters
            3 = 32k hash filters or 8k perfect filters (array of int)
parm:           AtrSampleRate:Software ATR Tx packet sample rate (array of int)
parm:           FCoE:Disable or enable FCoE Offload, default 1 (array of int)
parm:           MDD:Malicious Driver Detection: (0,1), default 1 = on (array of int)
parm:           LRO:Large Receive Offload (0,1), default 0 = off (array of int)
parm:           allow_unsupported_sfp:Allow unsupported and untested SFP+ modules on 82599 based adapters, default 0 = Disable (array of int)
parm:           dmac_watchdog:DMA coalescing watchdog in microseconds (0,41-10000), default 0 = off (array of int)
parm:           vxlan_rx:VXLAN receive checksum offload (0,1), default 1 = Enable (array of int)
```

### Conntrack Parameters

nf_conntrack_max and related hash size needs to optimise the conntrack based on the free memory. 

```
# sysctl net.netfilter.nf_conntrack_max
net.netfilter.nf_conntrack_max = 1000000
```

The hash size could be setup dynamically by changing the parameter 

```
# echo 1000000 > /sys/module/nf_conntrack/parameters/hashsize
# cat /sys/module/nf_conntrack/parameters/hashsize
1000448
```

Normally the hash size is the 1/8 of the nf_conntrack_max. However in order to increase the efficiency, 1:1 could be set if you have enough memory.

In case of 1M nf_conntrack_max setting, the total memory used is 

```
total mem = conntrack_max * sizeof(struct ip_conntrack) + hash_size * sizeof(struct list_head)
          = 1M * 328B + 1M * 16B = 344MB
```

There is a script for calculating the required memory, note the hash size and max is 1:8 in this case, it is not the optimised case.

```
 python conn_table_mem.py 1000
On this machine, each conntrack entry requires 328 bytes of kernel memory, and each hash table entry requires 16.

Therefore to consume a maximum of 1000 MiB of kernel memory:
 - conntrack_max should be set to 3177503
 - Using the kernel's default ratio, the nf_conntrack module's `hashsize' parameter should be set to 397188
```

The timeout value could also be optimised 

It is ok to set generic timeout to 30 ~ 120s, also the tcp_timeout_established should to modified to smaller value

```
net.netfilter.nf_conntrack_generic_timeout = 120
net.netfilter.nf_conntrack_tcp_timeout_established = 86400
```

Please note in the situation of long tcp sessions, for example, 5 days of single tcp connection of online gaming, it is better keep tcp_timeout_established valued to its original value.

### Hardware Offload

Hardware offload are ethernet card's embedded function to offload some load from CPU. If the performance is extremely poor, tweak the GRO/TSO/LRO configuration. If UDP performance is extremely poor, try to turn off UFO. Likewise turn off the TSO, provided that the TCP performance is low. 

```
 ethtool -k eth0
Features for eth0:
rx-checksumming: on
tx-checksumming: on
    tx-checksum-ipv4: on
    tx-checksum-ip-generic: off [fixed]
    tx-checksum-ipv6: on
    tx-checksum-fcoe-crc: off [fixed]
    tx-checksum-sctp: off [fixed]
scatter-gather: on
    tx-scatter-gather: on
    tx-scatter-gather-fraglist: off [fixed]
tcp-segmentation-offload: on
    tx-tcp-segmentation: on
    tx-tcp-ecn-segmentation: on
    tx-tcp6-segmentation: on
udp-fragmentation-offload: off [fixed]
generic-segmentation-offload: on
generic-receive-offload: on
large-receive-offload: off [fixed]
```

As the result of the TSO/GSO, the data in the ring buffer will also greatly increase, consequently the latency would also raise. Tweaking these features to balance in CPU load/Throughput with Latencies.

### Queueing Disciplines

The default QDisc for linux is pfifo_fast, it is far from best queuing strategy because of the deep buffer in the single queue. As a result the latency will grow, coupled with bufferbloat effect. Moreover, the different traffic class may not get well prioritised by default pfifo_fast strategy. Multiple other choices could be selected, it seems now fq_codel is now the best choice. However the actually selection is quite depending on the actual traffic pattern.

### Memory

Each memory channel should have at least one memory DIMM(at least 4G) inserted to max performance.

```
 dmidecode -t memory | grep Locator
    Locator: PROC 1 DIMM 1
    Bank Locator: Not Specified
    Locator: PROC 1 DIMM 2
    Bank Locator: Not Specified
    Locator: PROC 1 DIMM 3
    Bank Locator: Not Specified
    Locator: PROC 1 DIMM 4
    Bank Locator: Not Specified
    Locator: PROC 1 DIMM 5
    Bank Locator: Not Specified
    Locator: PROC 1 DIMM 6
    Bank Locator: Not Specified
    Locator: PROC 1 DIMM 7
    Bank Locator: Not Specified
    Locator: PROC 1 DIMM 8
    Bank Locator: Not Specified
    Locator: PROC 2 DIMM 1
    Bank Locator: Not Specified
    Locator: PROC 2 DIMM 2
    Bank Locator: Not Specified
    Locator: PROC 2 DIMM 3
    Bank Locator: Not Specified
    Locator: PROC 2 DIMM 4
    Bank Locator: Not Specified
    Locator: PROC 2 DIMM 5
    Bank Locator: Not Specified
    Locator: PROC 2 DIMM 6
    Bank Locator: Not Specified
    Locator: PROC 2 DIMM 7
    Bank Locator: Not Specified
    Locator: PROC 2 DIMM 8
    Bank Locator: Not Specified
```

### PCI-E Slots

Gen3 PCI-E slots have larger throughput than Gen2 PCI-E slots.

Make sure the PCI-slot with ethernet card inserted support speed with 20G or more, Gen2 slot typically does NOT support 20G or more bandwidth.

```
 lspci -s 04:00.0 -vvv | grep LnkSta
        LnkSta:    Speed 5GT/s, Width x8, TrErr- Train- SlotClk+ DLActive- BWMgmt- ABWMgmt-
        LnkSta2: Current De-emphasis Level: -6dB, EqualizationComplete-, EqualizationPhase1-
```

```
 dmidecode --type 9
# dmidecode 2.12
SMBIOS 2.8 present.

Handle 0x0900, DMI type 9, 17 bytes
System Slot Information
    Designation: PCIe Slot 1
    Type: x16 PCI Express 3
    Current Usage: Available
    Length: Long
    Characteristics:
        3.3 V is provided
        PME signal is supported

Handle 0x0901, DMI type 9, 17 bytes
System Slot Information
    Designation: PCIe Slot 2
    Type: x8 PCI Express 3 x16
    Current Usage: Available
    Length: Long
    Characteristics:
        3.3 V is provided
        PME signal is supported

Handle 0x0902, DMI type 9, 17 bytes
System Slot Information
    Designation: PCIe Slot 3
    Type: x8 PCI Express 3 x16
    Current Usage: In Use
    Length: Long
    Characteristics:
        3.3 V is provided
        PME signal is supported
    Bus Address: 0000:04:00.0
    
```

5Gt/s * 8 Lanes = 40Gt/s * (8b/10b) = 32Gbps

So theoretically it could provide 32Gbps input/output

```

May 26 11:37:30 kernel: [    2.899292] ixgbe 0000:04:00.0: PCI Express bandwidth of 32GT/s available
May 26 11:37:30 kernel: [    2.899294] ixgbe 0000:04:00.0: (Speed:5.0GT/s, Width: x8, Encoding Loss:20%)
May 26 11:37:30 kernel: [    2.899378] ixgbe 0000:04:00.0: MAC: 2, PHY: 15, SFP+: 5, PBA No: E66560-002
```


For PCIe 2.0, the overhead is 2b/10b, for PCIe 3.0, the overhead is 2b/130b.

### BIOS

* Select max performance in Power Management Options
* Disable CPU power state such as C6, C3, C1E or similar, leaving only C1 and C0
* Turn on HT(Hyper Threading)
* PCI configuration of 'extended_tag' has big impact on small packet performance of 40G ethernet interface. (also setpci could be used)

### Intel specific

#### UDP Flow Hash

Intel ethernet card support RSS, but on UDP packets. Ixgbe driver will send UDP packets with fragmentation bit set to CPU0 other than other CPUs. This default behaviour is set to avoid UDP packets out of order. This have performance degrade on UDP packets especially on VxLAN tunnel performance on 10G nic. 

ethtool -N eth0 rx-flow-hash udp4 sdfn

#### Burst Length

setpci modify the adapter's configuration register to allow it to read up to 4k bytes at a time (Tx only). Use it with caution, it may lead some system to unstable state, restart to set it back or use value 22 to setpci back. 

```
 lspci -nn | grep 82599
04:00.0 Ethernet controller [0200]: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection [8086:10fb] (rev 01)
04:00.1 Ethernet controller [0200]: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection [8086:10fb] (rev 01)
```
```
setpci -d 8086:1a48 e6.b=2e
```


