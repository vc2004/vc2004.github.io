---
layout: blog
title: Blog
---

Welcome to my blog! Here you'll find my thoughts and experiences in software engineering, system architecture, and cloud computing.

## Recent Posts

{% for post in site.posts %}
- [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %} 