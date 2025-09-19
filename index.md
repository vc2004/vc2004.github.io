---
layout: homepage
---

## About Me

Chief Engineer leading research in 4G/5G communications technologies research projects, specializing in 5G data plane and virtualization, with 19 years of experience in IP and telecom networks (2G-5G), Software-Defined Networking (SDN), cloud computing, and network function virtualization.

<p style="text-align: center;"><a href="/learning/Deep%20Sea%20Spectrum.html">My 20-Year Competence Map (深海光谱配色）</a></p>

<div class="competence-embed">
  <iframe id="competence-iframe" src="/learning/Deep%20Sea%20Spectrum.html?embed=1" style="width:100%; border:0;" loading="lazy" title="My 20-Year Competence Map (深海光谱配色)"></iframe>
</div>

## Awards & Patents

- Geneva 🥇 * 2
- Geneva 🥈 * 2
- Asia Invention 🥈 * 1
- Patents * 6

## Learning Notes

- **[epoll技术图解]** [epoll技术图解](/learning/epoll.html)
- **[eBPF 技术图解]** [eBPF 技术图解](/learning/eBPF.html)
- **[AWS Well-Architected Framework]** [AWS Well-Architected Framework](/learning/AWS_Well_Architecture.html)
- **[Flink 与 CDC]** [Flink 与 CDC](/learning/flink_and_cdc.html)
- **[网络加速方案比较]** [网络加速方案比较](/learning/Accelerated%20Path.html)

## Revisit the Classic Literature

- **[致橡树]** [舒婷《致橡树》](/essay/love.html) 
- **[我与地坛]** [史铁生《我与地坛》](/essay/me_and_ditan.html)
- **[一只特立独行的猪]** [王小波《一只特立独行的猪》](/essay/pig.html)
- **[生死场]** [萧红《生死场》](/essay/birth_and_death.html)
- **[呼兰河传]** [萧红《呼兰河传》尾声](/essay/hulan_river.html)
- **[张爱玲]** [张爱玲 Eileen Chang](/essay/Eileen_Chang.html)
- **[张爱玲 cont.]** [张爱玲 Eileen Chang cont.](/essay/Eileen_Chang_1.html)
- **[张爱玲 cont.2]** [张爱玲 Eileen Chang cont.2](/essay/Eileen_Chang_2.html)
- **[中国现代诗歌]** [中国现代诗歌](/essay/new_poems.html)
- **[冯至《十四行诗之一》]** [冯至《十四行诗之一》](/essay/comet.html)

## Old Blogs {#old-blogs}

- **[eBPF Deep Dive: Architecture, Development, and a Practical Tutorial]** [eBPF Deep Dive: Architecture, Development, and a Practical Tutorial](/technology/ebpf/linux/kernel/deep%20dive/2025/07/06/ebpf-introduction-and-tutorial.html)
- **[Transformer Architecture Deep Dive: From Attention to Modern LLMs]** [Transformer Architecture Deep Dive: From Attention to Modern LLMs](/machine%20learning/nlp/transformer/deep%20learning/llm/2025/01/15/transformer-architecture-deep-dive.html)
- **[Welcome to My Blog]** [Welcome to My Blog](/2024/03/08/welcome.html)
- **[TCP BBR: A New Congestion Control Algorithm]** [TCP BBR: A New Congestion Control Algorithm](/networking/performance/2024/03/01/bbr.html)
- **[Linux Networking Optimization Guide - Part III]** [Linux Networking Optimization Guide - Part III](/linux/networking/2024/02/17/linux-networking-optimisation-guide-3.html)
- **[Linux Networking Optimization Guide - Part II]** [Linux Networking Optimization Guide - Part II](/linux/networking/2024/02/16/linux-networking-optimisation-guide-2.html)
- **[Linux Networking Optimization Guide - Part I]** [Linux Networking Optimization Guide - Part I](/linux/networking/2024/02/15/linux-networking-optimisation-guide.html)
- **[OVS 2.7.0 Release Notes and Analysis]** [OVS 2.7.0 Release Notes and Analysis](/networking/sdn/2024/02/10/ovs-2-7-0.html)
- **[Understanding OVN and Geneve Protocol]** [Understanding OVN and Geneve Protocol](/networking/sdn/2024/02/08/ovn-and-geneve.html)
- **[Recent Advances in Networking: A Reading List]** [Recent Advances in Networking: A Reading List](/networking/research/2024/02/05/recent-networking-advance-readlist.html)

<style>
/* 为"重读经典"部分添加思源宋体 */
h2:contains("重读经典") {
  font-size: 1.2em !important;
}

h2:contains("重读经典") + ul,
h2:contains("重读经典") + ul li,
h2:contains("重读经典") + ul li a {
  font-family: 'Noto Serif SC', serif !important;
}
</style>

<style>
.competence-embed{
  margin: 10px 0 0 0;
}
.competence-embed iframe{
  display: block;
}
.competence-embed + h2{
  margin-top: 12px;
}
@media (max-width: 768px){
  .competence-embed iframe{
    height: auto;
  }
}
</style>

<script>
  // Auto-resize iframe to match inner canvas height
  document.addEventListener('DOMContentLoaded', function(){
    var iframe = document.getElementById('competence-iframe');
    if(!iframe) return;
    function resize() {
      try{
        var doc = iframe.contentDocument || iframe.contentWindow.document;
        if(!doc) return;
        var canvas = doc.getElementById('competenceCanvas');
        if(canvas){
          var rect = canvas.getBoundingClientRect();
          var h = Math.ceil(rect.height || canvas.height);
          iframe.style.height = h + 'px';
        } else {
          // fallback to document height
          var body = doc.body, html = doc.documentElement;
          var h = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
          iframe.style.height = h + 'px';
        }
      }catch(e){ /* cross-origin safe */ }
    }
    iframe.addEventListener('load', function(){
      resize();
      // Re-check after a tick to ensure scripts finished drawing
      setTimeout(resize, 300);
    });
    // Recalculate on window resize
    window.addEventListener('resize', function(){ setTimeout(resize, 100); });

    // Listen for precise size from child
    window.addEventListener('message', function(ev){
      try{
        var data = ev.data || {};
        if(data.type === 'competence-embed-size' && typeof data.height === 'number'){
          iframe.style.height = Math.max(100, data.height) + 'px';
        }
      }catch(e){ /* no-op */ }
    });
  });
</script>

