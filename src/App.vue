<template>
  <div id="app">
    <!-- 侧边栏（固定） -->
    <aside class="sidebar">
      <h2 class="app-title">AI 模拟法庭</h2>
      <ul class="menu">
        <li><router-link to="/" class="menu-link">首页</router-link></li>
        <li>
          <router-link to="/chat" class="menu-link">开始对话</router-link>
        </li>
        <li><a href="#" class="menu-link">历史对话</a></li>
        <li>
          <router-link to="/AboutUs" class="menu-link">关于我们</router-link>
        </li>
      </ul>
    </aside>

    <!-- 主内容区 -->
    <div class="main-container">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style scoped>
/* 让html,body,#app都占满高度，避免布局塌陷 */
html,
body,
#app {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

/* 侧边栏固定在左侧，宽度 200px，占满屏幕高度 */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 200px;
  height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: #fff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
}

.app-title {
  margin-bottom: 20px;
  font-size: 20px;
  font-weight: bold;
}

/* 菜单列表 */
.menu {
  list-style: none;
  margin: 0;
  padding: 0;
}
.menu li {
  margin-bottom: 12px;
}
.menu-link {
  display: block;
  text-decoration: none;
  color: #fff;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background 0.3s;
}
.menu-link:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* 主内容区：
   由于侧边栏是fixed，所以这里用margin-left避让 */
.main-container {
  margin-left: 200px;
  min-height: 100vh;
  background: #fff;
  overflow-y: auto;
  padding: 30px;
  box-sizing: border-box;
}
</style>
