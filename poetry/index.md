---
layout: homepage
title: 每日诗词
---

<div class="poetry-container">
  <div id="poem-content" class="poem-content">
    <div class="poem-header">
      <h2 id="poem-title" class="poem-title"></h2>
      <p id="poem-info" class="poem-info"></p>
    </div>

    <div class="maxim-container">
      <i class="fas fa-quote-left quote-left"></i>
      <div id="poem-lines" class="maxim-grid">
      </div>
      <i class="fas fa-quote-right quote-right"></i>
    </div>
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

.maxim-line {
  font-family: "LXGW WenKai", serif;
  font-size: 1.2rem;
  line-height: 2;
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
  const poems = {{ site.data.poems | jsonify }};

  function getDateString() {
    const now = new Date();
    return `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}`;
  }

  function hashCode(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash);
  }

  function displayDailyPoem() {
    const dateStr = getDateString();
    const hash = hashCode(dateStr);
    const index = hash % poems.length;
    const poem = poems[index];
    
    document.getElementById('poem-title').textContent = poem.title;
    document.getElementById('poem-info').textContent = `【${poem.dynasty}】${poem.author}`;
    
    const linesContainer = document.getElementById('poem-lines');
    linesContainer.innerHTML = '';
    const lines = poem.content.trim().split('\n');
    lines.forEach(line => {
      const div = document.createElement('div');
      div.className = 'maxim-line';
      div.textContent = line.trim();
      linesContainer.appendChild(div);
    });
  }

  displayDailyPoem();
});
</script> 