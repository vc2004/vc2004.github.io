---
layout: blog
title: Blog
---

Welcome to my blog! Here you'll find my thoughts and experiences in software engineering, system architecture, and cloud computing.

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

## Recent Posts

{% for post in site.posts %}
- [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %} 