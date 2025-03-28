<template>
  <div class="home-page">
    <div class="hero-section">
      <h1>欢迎来到 AI 模拟法庭</h1>
      <p>在这里，你可以体验基于人工智能的法庭模拟，学习并提升法律实务能力。</p>
    </div>
    <div class="content-section">
      <div class="card" @click="handleCardClick('模拟对话')">
        <h2>模拟对话</h2>
        <p>开始你的法庭模拟对话。</p>
      </div>
      <div class="card" @click="handleCardClick('热门法律事件')">
        <h2>热门法律事件</h2>
        <ul>
          <li>合同纠纷案例</li>
          <li>侵权赔偿案例</li>
          <li>知识产权纠纷案例</li>
        </ul>
      </div>
      <div class="card" @click="handleCardClick('用户反馈')">
        <h2>用户反馈</h2>
        <ul>
          <li>“这个系统对模拟实训帮助很大！” — 学生A</li>
          <li>“法庭对话环节非常真实。” — 律师B</li>
        </ul>
      </div>
      <div class="card" @click="handleCardClick('法条速递')">
        <h2>法条速递</h2>
        <p>访问最新的法律条款和法规。</p>
        <a
          href="https://www.ilawpress.com/law/detail?lang=cn&id=czJcPFCbVLxrNLhWTPcQww"
          class="link-item"
        >
          全国人民代表大会关于修改《中华人民共和国全国人民代表大会和地方各级人民代表大会代表法》的决定（2025）
        </a>
        <a
          href="https://www.ilawpress.com/law/detail?lang=cn&id=tGDpvatbA5_NITseRYAXeA"
          class="link-item"
        >
          国务院关于涉外知识产权纠纷处理的规定
        </a>
      </div>
      <div class="card" @click="handleCardClick('友情链接')">
        <h2>友情链接</h2>
        <p>浏览相关法律机构的网站。</p>
        <a
          href="https://www.12348.gov.cn/#/publicies/sfks/sfks"
          class="link-item"
        >
          中国法律服务网
        </a>
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
import { useRouter } from "vue-router";

export default {
  name: "Home",
  setup() {
    const router = useRouter();
    const handleCardClick = (title) => {
      if (title === "模拟对话") {
        router.push("/chat");
      }
      console.log(`点击了 ${title} 模块`);
    };
    return {
      handleCardClick,
    };
  },
};
</script>

<style scoped>
/* 整个首页使用一个背景渐变或图片，可以更换为自己喜欢的背景 */
.home-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #e1f5fe, #b3e5fc, #81d4fa);
  padding: 40px;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

/* 顶部Hero区 */
.hero-section {
  text-align: center;
  padding: 60px 20px;
  background: rgba(255, 255, 255, 0.8);
  margin-bottom: 50px;
  border-radius: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}
.hero-section h1 {
  font-size: 48px;
  margin-bottom: 20px;
  color: #333;
  font-weight: 600;
}
.hero-section p {
  font-size: 20px;
  color: #666;
}

/* 中间内容区 */
.content-section {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  margin-bottom: 60px;
  justify-content: center;
}
.card {
  flex: 1 1 350px;
  background: linear-gradient(135deg, #ffffff, #f1f8e9);
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}
.card h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
  font-weight: 600;
}
.card ul {
  list-style: inside;
  color: #666;
  font-size: 18px;
}
.link-item {
  display: block;
  margin-top: 15px;
  color: #007bff;
  text-decoration: none;
  font-size: 18px;
}
.link-item:hover {
  text-decoration: underline;
}

/* 流程图区 */
.flowchart-section {
  text-align: center;
}
.flowchart-section h2 {
  margin-bottom: 30px;
  font-size: 32px;
  color: #333;
  font-weight: 600;
}
.flowchart-image {
  max-width: 800px;
  width: 100%;
  border: none;
  border-radius: 20px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}
</style>
