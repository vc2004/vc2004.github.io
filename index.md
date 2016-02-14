---
title       : Server Malfunction Rate Calculation
subtitle    : 
author      : Liang Dong
job         : System Administrator
framework   : io2012        # {io2012, html5slides, shower, dzslides, ...}
highlighter : highlight.js  # {highlight.js, prettify, highlight}
hitheme     : tomorrow      # 
widgets     : [mathjax]            # {mathjax, quiz, bootstrap}
mode        : selfcontained # {standalone, draft}
knit        : slidify::knit2slides
---

## Introduction



### Server Malfunction Rate Prediction

The Debian servers installed with Open vSwtich Version 2.4.0 has some bugs interconnect to the Cisco Switch configured with keepalive message. Every 10 second, the Cisco Switch will dispatch a keepalive message to the server. The server ethernet port uplink will be malfunctioned (err-disable) by Cisco Switch if the bug has happened.

The incident logs show there are 8 malfunction records in 22204800 keepalive message received on Debian servers.

--- .class #id

## Assumption

Let's assume that:

* The keepalive message recieved on servers and malfunction events are iid (independent identically-distributed)

* Server malfunction rate is constant, and it is proportional to keepalive message events.

--- .class #id 

## Poisson Distribution

Then the malfunction follow the Poisson distribution, which we can calculate the malfunction rate base on the Poisson distribution.

$$P = \frac{\lambda^ke^-k}{k!}$$

The global variables are initialized as follow:


```r
HOURS <- 24
MIN <- 60
SEC <- 60
INCIDENT <- 8
KEEPALIVE_EVENT <- 22204800
lambda <-  INCIDENT/KEEPALIVE_EVENT * (HOURS * MIN * SEC/10)
```

--- .class #id 

## Malfunction Rate Calculation
The incident rate of 50 servers in 30 days could be caculated:




```r
zero_rate <- ppois(1, lambda*servers*days) - dpois(1, lambda*servers*days)
zero_rate
```

```
## [1] 0.009379201
```


```r
once_rate <- dpois(1, lambda*servers*days)
once_rate
```

```
## [1] 0.04379393
```


```r
err_rate <- 1 - zero_rate
err_rate
```

```
## [1] 0.9906208
```

--- .class #id 

## Conclusion

So the rate for one malfunction of 50 servers in 30 days is 0.0437939, rate for no malfunction is 0.0093792, and the rate for one or more malfunction is 0.9906208. The PDF is plotted as follow:

![plot of chunk unnamed-chunk-6](assets/fig/unnamed-chunk-6-1.png)



