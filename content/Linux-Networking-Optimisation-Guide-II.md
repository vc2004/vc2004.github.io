# Linux Networking Optimisation Guide Part II (Cont.)

- date: 2016-12-13
- category: Networking
- tags: networking, Linux

----------------

### Taskset/Isolcpus

It is better to pin the process on specific CPUs and make that CPU isolated

In the following example, CPU 1-15, 17-31 are isolated, leaving CPU 0 and CPU 32 processing the other system and user task. Those CPU could be used to pin KVM/QEMU or netperf session.

```

#vi /etc/default/grub

GRUB_DEFAULT=0
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash default_hugepagesz=1G hugepagesz=1G hugepages=16 hugepagesz=2M hugepages=2048 intel_iommu=off isolcpus=1-15,17-31"
GRUB_CMDLINE_LINUX="clocksource=tsc ipv6.disable=1"

#update-grub

Generating grub configuration file ...
Found linux image: /boot/vmlinuz-3.16.0-4-amd64
Found initrd image: /boot/initrd.img-3.16.0-4-amd64
Found memtest86+ image: /boot/memtest86+.bin
Found memtest86+ multiboot image: /boot/memtest86+_multiboot.bin
done
```

### RPS

For those ethernet card which DO NOT support RSS or multiple queue, it is better configure RPS. If RSS is already configured, then RPS may lead some performance drop.

In addition, if a particular traffic receiving on the server is dominant (GRE/UDP/specific TCP), RPS may have better performance than RSS.

```
#/etc/init.d/set_rps.sh status

/sys/class/net/eth0/queues/rx-0/rps_cpus 00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,000000ff
/sys/class/net/eth0/queues/rx-0/rps_flow_cnt 4096
/sys/class/net/eth1/queues/rx-0/rps_cpus 00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,000000ff
/sys/class/net/eth1/queues/rx-0/rps_flow_cnt 4096
/proc/sys/net/core/rps_sock_flow_entries 8192

```

In the scenario that high load of GRE or UDP packets are not RSS to the different CPU, try use RPS instead. 

### NIC ring buffer


* Increasing ring buffer may lead to higher latency in certain circumstance (mainly on transmit end), where as the throughput is increased as well.
* If packet are receiving too fast, small ring buffer may need to packet loss.

Tune to the maximum of pre-set on Rx setting. For example, configure to 2040 on eth0

```

#ethtool -g eth0

Ring parameters for eth0:
Pre-set maximums:
RX:        2040
RX Mini:    0
RX Jumbo:    8160
TX:        255
Current hardware settings:
RX:        2040
RX Mini:    0
RX Jumbo:    0
TX:        255
```

```
ethtool -G eth0 rx 2040
```

### SoftIRQ 

To check the SoftIRQ

```
watch -n1 grep RX /proc/softirqs
watch -n1 grep TX /proc/softirqs
```

In the /proc/net/softnet_stat

```
#cat /proc/net/softnet_stat

a1f2d52e 0003bb1a 008bf81d 00000000 00000000 00000000 00000000 00000000 00000000 d2711d13 00000000
aba687fe 00038122 008ac060 00000000 00000000 00000000 00000000 00000000 00000000 cb49f8b4 00000000
ce145ec6 0003d512 008ae0bf 00000000 00000000 00000000 00000000 00000000 00000000 f08f0303 00000000
15dc9267 0003c306 0087799a 00000000 00000000 00000000 00000000 00000000 00000000 b0960b17 00000000
0660ac7b 0003bf5d 00872565 00000000 00000000 00000000 00000000 00000000 00000000 e437ec3d 00000000
d2578b45 0003e436 00835c20 00000000 00000000 00000000 00000000 00000000 00000000 e9dd448e 00000000
136320b0 0003732e 0087ca4a 00000000 00000000 00000000 00000000 00000000 00000000 b92b37df 00000000
e11fee84 0003b335 008cb2bb 00000000 00000000 00000000 00000000 00000000 00000000 ee76d89a 00000000
```

In kernel version 3.16, according the related code, the  

```

146 static int softnet_seq_show(struct seq_file *seq, void *v)
147 {
148        struct softnet_data *sd = v;
149        unsigned int flow_limit_count = 0;
150
151 #ifdef CONFIG_NET_FLOW_LIMIT
152        struct sd_flow_limit *fl;
153
154        rcu_read_lock();
155        fl = rcu_dereference(sd->flow_limit);
156        if (fl)
157                flow_limit_count = fl->count;
158        rcu_read_unlock();
159 #endif
160
161        seq_printf(seq,
162                    "%08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x\n",
163                    sd->processed, sd->dropped, sd->time_squeeze, 0,
164                    0, 0, 0, 0, /* was fastroute */
165                    sd->cpu_collision, sd->received_rps, flow_limit_count);
166        return 0;
167 }


```

So the column names is processed, dropped, time_squeeze, null, null, null, null, null, cpu_collision, received_rps, flow_limit_count. And each row represent the different CPU.

if the third column is increasing, increase the netdev_budget. The polling routine has a budget which determines the CPU time the code is allowed. This is required to prevent SoftIRQs from monopolizing the CPU. The 3rd column is the number of times ksoftirqd ran out of netdev_budget or CPU time when there was still work to be done (time_squeeze). The more messages the CPU get from the buffer (600), the more time the SoftIRQ spent on CPU to process more messages. It avoid buffer flows. 

```
sysctl -w net.core.netdev_budget=600
```

The netdev_budget meaning:

```
netdev_budget
-------------

Maximum number of packets taken from all interfaces in one polling cycle (NAPI
poll). In one polling cycle interfaces which are registered to polling are
probed in a round-robin manner.
```

### Adapter Queue

If the second column of softnet_stat is increasing, the frame is dropping at the queue. To avoid dropping the packets, the netdev_max_backlog should be increased. This option increase the maximum queue length (Within Kernel, before processing by the IP Stack, and after the NIC receive the packets) to avoid overflow.

```
netdev_max_backlog
------------------

Maximum number  of  packets,  queued  on  the  INPUT  side, when the interface
receives packets faster than kernel can process them.
```

It is the reverse side of qlen, the start point should be set to 300000

```
sysctl -w net.core.netdev_max_backlog=300000
net.core.netdev_max_backlog = 300000
```

