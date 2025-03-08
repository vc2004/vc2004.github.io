---
layout: blog
title: "Linux Networking Optimization Guide - Part I"
date: 2024-02-15
categories: [Linux, Networking]
tags: [Linux, Performance, Networking, Optimization]
---

# Linux Networking Optimisation Guide Part I

- date: 2016-09-21
- category: Networking
- tags: networking, Linux

----------------

### Foreword:

- Plain Linux installation is NOT optimised for the best networking performance
- Almost all the optimisations have side affect. It is better to test before using it.

### Interrupt Affinity

CPU Affinity is the most important and most effective optimisation, also it is the entry level optimisation.

Turn off irqbalance if any, note it may cause performance issue on other Hardware/IO devices.

```
/etc/init.d/irqbalance stop
```

The Rx queue could be checked by -l and modified by -L

```
# ethtool -l eth4
Channel parameters for eth4:
Pre-set maximums:
RX:        0
TX:        0
Other:        1
Combined:    63
Current hardware settings:
RX:        0
TX:        0
Other:        1
Combined:    32
```

Check the interrupt number related to the eth0

```
# egrep "CPU0|eth0" /proc/interrupts
            CPU0       CPU1       CPU2       CPU3       CPU4       CPU5       CPU6       CPU7       CPU8       CPU9       CPU10      CPU11      CPU12      CPU13      CPU14      CPU15      CPU16      CPU17      CPU18      CPU19      CPU20      CPU21      CPU22      CPU23      CPU24      CPU25      CPU26      CPU27      CPU28      CPU29      CPU30      CPU31
 148:     347358          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0  IR-PCI-MSI-edge      eth0
 150:         18    1152920          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0  IR-PCI-MSI-edge      eth0-fp-0
 151:         27          0      61465          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0  IR-PCI-MSI-edge      eth0-fp-1
 152:         10          0          0      32140          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0  IR-PCI-MSI-edge      eth0-fp-2
 153:         37          0          0          0     113157          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0  IR-PCI-MSI-edge      eth0-fp-3
 154:         10          0          0          0          0      89395          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0  IR-PCI-MSI-edge      eth0-fp-4
 155:         11          0          0          0          0          0      75379          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0  IR-PCI-MSI-edge      eth0-fp-5
 156:          8          0          0          0          0          0          0     123974          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0  IR-PCI-MSI-edge      eth0-fp-6
 157:          5          0          0          0          0          0          0          0     277624          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0          0  IR-PCI-MSI-edge      eth0-fp-7
```

Echo the cpu bit mask to related interrupt number

```
echo 00000001 > /proc/irq/148/smp_affinity
```

Tips: MAC native calculator is very good at calculating cpu bit mask.

### Interrupt Coalescence

Interrupt Coalescence (IC) is the number of usec waited or frames gathered to issue a hardware interrupt. A small value or big value both has side affects. If latency is preferred over throughput, eg. the realtime streaming traffic, a small value or be disabled would be benefit. Otherwise for large throughput, a larger value should be selected.

```
ethtool -c eth0
Coalesce parameters for eth0:
Adaptive RX: off  TX: off
stats-block-usecs: 999936
sample-interval: 0
pkt-rate-low: 0
pkt-rate-high: 0

rx-usecs: 18
rx-frames: 12
rx-usecs-irq: 18
rx-frames-irq: 2

tx-usecs: 80
tx-frames: 20
tx-usecs-irq: 18
tx-frames-irq: 2

rx-usecs-low: 0
rx-frame-low: 0
tx-usecs-low: 0
tx-frame-low: 0

rx-usecs-high: 0
rx-frame-high: 0
tx-usecs-high: 0
tx-frame-high: 0
```

Some cards support adaptive changing the parameters, just turn on the adapter rx and tx.
```
ethtool -C eth0 adaptive-rx on adaptive-tx on
```

### NUMA

The network performance might increase if the NUMA node is close to the PCIe slot with ethernet card attached. But it is very tricky the performance might drop with the Tx/Rx application is on the different NUMA node or on the same logical core. So do tweaking a lots to get the best performance.

It is known that:

- Two child process on different numa node with cause L3 miss, so the performance will drop.
- Two child process on the same logical core(HT) will cause performance drop.
- Performance will be optimised if two child process on same numa node with memory also on that node.

For example, if two child process on same core 0 [0,16], the performance will drop. The same will happen on cpu0 and cpu8.

So it is important to decide which cpu to pin Tx/Rx netsurf application, otherwise you might get a drop

```
# python cpu_layout.py --status
============================================================
Core and Socket Information (as reported by '/proc/cpuinfo')
============================================================

cores =  [0, 1, 2, 3, 4, 5, 6, 7]
sockets =  [0, 1]

       Socket 0        Socket 1
       --------        --------
Core 0 [0, 16]         [8, 24]

Core 1 [1, 17]         [9, 25]

Core 2 [2, 18]         [10, 26]

Core 3 [3, 19]         [11, 27]

Core 4 [4, 20]         [12, 28]

Core 5 [5, 21]         [13, 29]

Core 6 [6, 22]         [14, 30]

Core 7 [7, 23]         [15, 31]
```

For best performance on NUMA, check which NUMA node the PCIe are connected to

```
# lspci -tv
 \-[0000:00]-+-00.0  Intel Corporation Haswell-E DMI2
             +-01.0-[02]--
             +-01.1-[05]--
             +-02.0-[06]--+-00.0  Broadcom Corporation BCM57840 NetXtreme II 10/20-Gigabit Ethernet
             |            \-00.1  Broadcom Corporation BCM57840 NetXtreme II 10/20-Gigabit Ethernet

# cat /sys/devices/pci0000\:00/0000\:00\:02.0/numa_node
0

# cat /sys/devices/pci0000\:00/0000\:00\:02.0/local_cpus
00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00ff00ff
```

0xFF00FF is CPU0-7 & 16-23, so it is better to set the affinity on CPU0-7 or CPU16-23.

Also, if two or more ports from different NIC are used, make sure they are connected to the same CPU socket.

### CPU Frequency

To maximise the CPU frequency to handle the network loads, it could be set through OS.

```
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
powersave

echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```
