---
layout: blog
title: "Recent Advances in Networking: A Reading List"
date: 2024-02-05
categories: [Networking, Research]
tags: [Networking, Research, Papers]
---

# Networking Fundamental and Recent Advance Reading List

- date: 2016-08-03
- category: Networking
- tags: networking, sdn

----------------

Complied by Liang Dong

### Update 

* 2016-12-13 Add several paper about BBR congestion control and P4 Dataplane Programming
* 2016-09-20 Add two thesis about load balancing service in Cloud Networking

### Foreword

This is a small reading list about recent advance on networking. It also cover some basic fundamental knowledges of TCP/IP.

###Data Center Networking:

**A Scalable, Commodity Data Center Network Architecture**, Mohammad Al-Fares, Alexander Loukissas, Amin Vahdat, University of California, San Diego, Sigcomm 2008

**Jupiter Rising: A Decade of Clos Topologies and Centralized Control in Google's Datacenter Network**, Arjun Singh, Joon Ong, Amit Agarwal, Glen Anderson, Ashby Armistead, Roy Bannon, Seb Boving, Gaurav Desai, Bob Felderman, Paulie Germano, Anand Kanagala, Jeff Provost, Jason Simmons, Eiichi Tanda, Jim Wanderer, Urs Hölzle, Stephen Stuart, and Amin Vahdat. Sigcomm 2016.

**Inside the Social Network's (Datacenter) Network, Arjun Roy**, Hongyi Zeng, Jasmeet Bagga, George Porter, and Alex C. Snoeren, Sigcomm 2015

**Introducing data center fabric, the next-generation Facebook data centre network**, Alexey Andreyev, Facebook

###Software Defined Networking:

**Openflow: Enable Innovation in Campus Networks**, Nick McKeown, Tom Anderson, Hari Balakrishnan, Guru Parulkar, Larry Peterson, Jennifer Rexford, Scott Shenker, Jonathan Turner, CCR 2008

**The Future of Networking, and the Past of Protocols** - Scott Shenker

**The Design and Implementation of Open vSwitch**, Ben Pfaff, Justin Pettit, Teemu Koponen, Ethan Jackson, Andy Zhou, Jarno Rajahalme, Jesse Gross, Alex Wang, Joe Stringer, and Pravin Shelar, VMware, Inc.; Keith Amidon, Awake Networks; Martín Casado, VMware, Inc, NSDI 2015

**B4: Experience with a Globally-Deployed Software Defined WAN**, Sushant Jain, Alok Kumar, Subhasree Mandal, Joon Ong, Leon Poutievski, Arjun Singh, Subbaiah Venkata, Jim Wanderer, Junlan Zhou, Min Zhu, Jonathan Zolla, Urs Hölzle, Stephen Stuart and Amin Vahdat, Sigcomm 2013

###Dataplane Programming

**P4: Programming Protocol-Independent Packet Processors**, Pat Bosshart, Dan Daly, Glen Gibb, Martin Izzard, Nick McKeown, Jennifer Rexford, Cole Schlesinger, Dan Talayco, Amin Vahdat, George Varghese, David Walker

###Network Virtualisation & Cloud Networking:

**VL2: A Scalable and Flexible Data Centre Network**, Albert Greenberg, Srikanth Kandula,  David A. Maltz , James R. Hamilton, Changhoon Kim, Parveen Patel , Navendu Jain, Parantap Lahiri, Sudipta Sengupta, Microsoft Research, Sigcomm 2009

**Network Virtualization in Multi-tenant Datacenters**, Teemu Koponen, Keith Amidon, Peter Balland, Martín Casado, Anupam Chanda, Bryan Fulton, Igor Ganichev, Jesse Gross, Natasha Gude, Paul Ingram, Ethan Jackson, Andrew Lambeth, Romain Lenglet, Shih-Hao Li, Amar Padmanabhan, Justin Pettit, Ben Pfaff, and Rajiv Ramanathan, VMware; Scott Shenker, International Computer Science Institute and the University of California, Berkeley; Alan Shieh, Jeremy Stribling, Pankaj Thakkar, Dan Wendlandt, Alexander Yip, and Ronghua Zhang, VMware, NSDI 2014

**Maglev: A Fast and Reliable Software Network Load Balancer**, Daniel E. Eisenbud, Cheng Yi, Carlo Contavalli, Cody Smith, Roman Kononov, Eric Mann-Hielscher, Ardas Cilingiroglu, and Bin Cheyney, Google Inc.; Wentao Shang, University of California, Los Angeles; Jinnah Dylan Hosein, SpaceX

**Ananta: Cloud Scale Load Balancing**, Parveen Patel, Deepak Bansal, Lihua Yuan, Ashwin Murthy, Albert Greenberg, David A. Maltz, Randy Kern, Hemant Kumar, Marios Zikos, Hongyu Wu, Changhoon Kim, Naveen Karri, Microsoft.

###Transport Protocols:

**RFC 5681, TCP Congestion Control**, IETF

**Data Center TCP (DCTCP)**, Mohammad Alizadeh, Albert Greenberg, David A. Maltz, Jitendra Padhye, Parveen Patel, Balaji Prabhakar, Sudipta Sengupta, Murari Sridharan, Sigcomm 2010

**Understanding TCP Incast Throughput Collapse in Datacenter Networks**, Yanpei Chen, Rean Griffith, Junda Liu, Randy H. Katz, Anthony D. Joseph, Sigcomm 2009

**Bufferbloat: Dark Buffers in the Internet, Networks without effective AQM may again be vulnerable to congestion collapse**, Jim Gettys, Bell Labs, Alcatel-Lucent; and Kathleen Nichols, Pollere Inc, ACMQueue Volume 9, issue 11

**BBR: Congestion-Based Congestion Control, Measuring bottleneck bandwidth and round-trip propagation time**, Neal Cardwell, Yuchung Cheng, C. Stephen Gunn, Soheil Hassas Yeganeh, Van Jacobson, ACMQueue Volume 14, issue 5

###Network Measurement:

**Pingmesh: A Large-Scale System for Data CenterNetwork Latency Measurement and Analysis**, Chuanxiong Guo, Lihua Yuan, Dong Xiang, Yingnong Dang, Ray Huang, Dave Maltz, Zhaoyi Liu, Vin Wang, Bin Pang, Hua Chen, Zhi-Wei Lin, Varugis Kurien, Microsoft, Midfin Systems, Sigcomm 2015
