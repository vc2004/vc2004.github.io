---
layout: poetry
title: 每日诗词
permalink: /poetry/
---

<div class="poetry-container">
  {% assign poems = site.data.poems %}
  {% assign today_seed = "now" | date: "%Y%m%d" | to_integer %}
  {% assign poem_index = today_seed | modulo: poems.size %}
  {% assign poem = poems[poem_index] %}
  
  <div class="poem-header">
    <h2 class="poem-title">{{ poem.title }}</h2>
    <p class="poem-info">【{{ poem.dynasty }}】{{ poem.author }}</p>
  </div>

  <div class="maxim-container">
    <i class="fas fa-quote-left quote-left"></i>
    <div class="maxim-grid">
      {% assign lines = poem.content | newline_to_br | strip_newlines | split: '<br />' %}
      {% for line in lines %}
        <div class="maxim-line">{{ line | strip }}</div>
      {% endfor %}
    </div>
    <i class="fas fa-quote-right quote-right"></i>
  </div>
</div>

<style>
.poetry-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 200px);
  padding: 2rem;
  margin: 0 auto;
}

.poem-header {
  margin-bottom: 2rem;
  font-family: "LXGW WenKai", serif;
  text-align: center;
}

.poem-title {
  font-size: 1.8rem;
  color: #2d3748;
  margin: 0 0 0.5rem 0;
  font-family: "LXGW WenKai", serif;
}

.poem-info {
  color: #666;
  font-size: 1.1rem;
  margin: 0;
  font-family: "LXGW WenKai", serif;
}

.maxim-container {
  margin: 0 auto;
  max-width: 500px;
  text-align: center;
}

@media (prefers-color-scheme: dark) {
  .poem-title {
    color: #e2e8f0;
  }
  
  .poem-info {
    color: #999;
  }
}

@media (max-width: 768px) {
  .poetry-container {
    padding: 1rem;
  }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  // 这里可以添加加载诗词的 JavaScript 代码
  // 例如通过 API 获取随机诗词
});
</script> 