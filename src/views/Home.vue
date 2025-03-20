<template>
  <div class="home-page">
    <div class="hero-section">
      <h1>欢迎来到 AI 模拟法庭</h1>
      <p>在这里，你可以体验基于人工智能的法庭模拟，学习并提升法律实务能力。</p>
    </div>

    <div class="content-section">
      <div class="card">
        <h2>热门法律事件</h2>
        <ul>
          <li>合同纠纷案例</li>
          <li>侵权赔偿案例</li>
          <li>知识产权纠纷案例</li>
        </ul>
      </div>

      <div class="card">
        <h2>用户反馈</h2>
        <ul>
          <li>“这个系统对模拟实训帮助很大！” — 学生A</li>
          <li>“法庭对话环节非常真实。” — 律师B</li>
        </ul>
      </div>
    </div>

    <div class="flowchart-section">
      <h2>模拟法庭流程图</h2>
      <img
        src="@/assets/falvliucheng.png"
        alt="法庭流程图"
        class="flowchart-image"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
};
</script>

<style scoped>
/* 整个首页使用一个背景渐变或图片，可以更换为自己喜欢的背景 */
.home-page {
  min-height: 100%;
  background: linear-gradient(to bottom right, #fff, #e9ecef);
  padding: 20px;
}

/* 顶部Hero区 */
.hero-section {
  text-align: center;
  padding: 40px 20px;
  background: rgba(255, 255, 255, 0.6);
  margin-bottom: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.hero-section h1 {
  font-size: 36px;
  margin-bottom: 15px;
}
.hero-section p {
  font-size: 18px;
  color: #666;
}

/* 中间内容区 */
.content-section {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 40px;
}
.card {
  flex: 1 1 300px;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}
.card h2 {
  margin-bottom: 15px;
}
.card ul {
  list-style: inside;
  color: #666;
}

/* 流程图区 */
.flowchart-section {
  text-align: center;
}
.flowchart-section h2 {
  margin-bottom: 20px;
}
.flowchart-image {
  max-width: 600px;
  width: 100%;
  border: 2px solid #ccc;
  border-radius: 8px;
}
</style>
