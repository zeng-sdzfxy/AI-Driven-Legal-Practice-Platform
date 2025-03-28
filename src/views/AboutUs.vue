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
          <li><i class="fas fa-at"></i> Email: contact@example.com</li>
          <li><i class="fas fa-phone-alt"></i> Phone: +123 456 7890</li>
          <li>
            <i class="fas fa-map-marker-alt"></i> Address: 123 法律大道, 科技城,
            高新区
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
/* 整个页面使用和首页一致的背景渐变或图片 */
.home-page {
  min-height: 100vh;
  background: linear-gradient(to bottom right, #f0f8ff, #b0e0e6);
  padding: 20px;
  font-family: "Arial", sans-serif;
  color: #333;
}

/* 顶部Hero区 */
.hero-section {
  text-align: center;
  padding: 60px 40px;
  background: rgba(255, 255, 255, 0.8);
  margin-bottom: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}
.hero-section h1 {
  font-size: 48px;
  margin-bottom: 20px;
}
.hero-section h1 i {
  margin-right: 10px;
}
.hero-section p {
  font-size: 20px;
  color: #666;
}

/* 中间内容区 */
.content-section {
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
  justify-content: center;
  margin-bottom: 60px;
}
.card {
  flex: 1 1 400px;
  max-width: 600px;
  background: #fff;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}
.card:hover {
  transform: scale(1.03);
}
.card h2 {
  margin-bottom: 25px;
  color: #007bff;
  display: flex;
  align-items: center;
}
.card h2 i {
  margin-right: 10px;
}
.card ul {
  list-style: none;
  padding: 0;
}
.card ul li {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}
.card ul li i {
  margin-right: 10px;
}
.card p {
  margin-bottom: 15px;
}
.card p strong {
  color: #007bff;
}
</style>
