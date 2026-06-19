<template>
  <div class="home-page">
    <div class="hero-section">
      <h1><i class="fas fa-info-circle"></i> 关于我们</h1>
      <p>了解我们是谁，我们的团队，以及我们对未来的愿景。</p>
    </div>

    <div class="content-section">
      <!-- 团队简介模块 -->
      <div class="card">
        <h2><i class="fas fa-building"></i> 团队简介</h2>
        <p>
          我们是一个专注于人工智能技术在法律领域的应用开发团队。致力于通过先进的AI技术帮助法律从业者提高工作效率和案件处理质量。
        </p>
        <p>
          我们的产品包括模拟法庭系统、智能法律助手等，旨在提供全面的法律实务解决方案。
        </p>
        <p>我们来自山东政法学院网络空间安全学院</p>
      </div>

      <!-- 团队介绍模块 -->
      <div class="card">
        <h2><i class="fas fa-users"></i> 团队介绍</h2>
        <ul>
          <li><i class="fas fa-user"></i> 1</li>
          <li><i class="fas fa-user"></i> 2</li>
          <li><i class="fas fa-user"></i>3</li>
          <!-- 更多团队成员根据需要添加 -->
        </ul>
      </div>

      <!-- 联系我们模块 -->
      <div class="card">
        <h2><i class="fas fa-envelope"></i> 联系我们</h2>
        <p>如果您有任何问题或建议，欢迎通过以下方式联系我们：</p>
        <ul>
          <li><i class="fas fa-at"></i> Email:</li>
          <li><i class="fas fa-phone-alt"></i> Phone: </li>
          <li>
            <i class="fas fa-map-marker-alt"></i> Address: 济南历下区
          </li>
        </ul>
      </div>

      <!-- 愿景使命模块 -->
      <div class="card">
        <h2><i class="fas fa-bullseye"></i> 愿景使命</h2>
        <p>
          <strong>愿景：</strong> 成为全球领先的法律人工智能解决方案提供商。
        </p>
        <p>
          <strong>使命：</strong>
          利用AI技术简化法律流程，为法律从业者提供高效、智能的工具，推动法律行业的进步。
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AboutUs",
};
</script>

<style scoped>
/* 整个页面使用和首页一致的背景和字体 */
.home-page {
  font-family: Arial, Helvetica, sans-serif;
  background-color: var(--color-bg-warm);
  color: var(--color-text-primary);
  padding: 20px;
}

/* 顶部Hero区 */
.hero-section {
  text-align: center;
  margin: 40px 0;
}
.hero-section h1 {
  font-size: 36px;
}
.hero-section p {
  font-size: 24px;
  margin-bottom: 20px;
}

/* 中间内容区 */
.content-section {
  text-align: center;
  margin: 40px 0;
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}
.card {
  background: var(--color-bg-white);
  padding: 20px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  flex: 1 1 200px;
  max-width: 300px;
  border-top: 3px solid var(--color-primary);
}
.card h2 {
  font-size: 24px;
  margin-bottom: 10px;
  color: var(--color-primary);
}
.card p {
  margin-bottom: 10px;
}
.card ul {
  list-style: none;
  padding: 0;
}
.card ul li {
  margin-bottom: 5px;
}
</style>
