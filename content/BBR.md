# BBR 测试的一点感想

- date: 2017-02-06
- category: Networking
- tags: networking, tcp, BBR

----------------

### BBR 测试的一点感想

1. BBR 只适合某些特定的场景，比如 DC 内不适用，适合的场景是长距离 Internet 中间比较多 bufferbloat 的情况。
2. BBR hardcode 了无视20%以下的丢包，这个其实有比较大的问题，不知道最新的代码 patch 了没有。

```
+/* If lost/delivered ratio > 20%, interval is "lossy" and we may be policed: */
+static const u32 bbr_lt_loss_thresh = 50;
```
3. 比较重要的一点，BBR 在无视丢包的情况下，会竞争吃掉 CUBIC 和其他 BBR 的带宽。
4. BBR 不应该和 Loss-based CUBIC 比较，实际上应该和Delay-based Vegas 比较，当然 Vegas 自己也有挺多的问题。

