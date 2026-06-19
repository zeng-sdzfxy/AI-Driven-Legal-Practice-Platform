<template>
  <div class="court-room-view">
    <div class="page-header">
      <h1>3D法庭模拟</h1>
      <p>交互式法庭场景模拟系统</p>
    </div>
    <div class="court-content">
      <CourtRoom3D />
    </div>
  </div>
</template>

<script>
import CourtRoom3D from '../components/CourtRoom3D.vue';

export default {
  name: 'CourtRoomView',
  components: {
    CourtRoom3D
  },
  setup() {
    // 可以在这里添加页面级别的逻辑
    return {
      // 导出需要在模板中使用的数据或方法
    };
  }
};
</script>

<style scoped>
.court-room-view {
  width: 100%;
  min-height: 100vh;
  background-color: #1a1a2e;
  color: white;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.page-header {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.page-header h1 {
  margin: 0;
  font-size: 2.5em;
  color: #64ffda;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.page-header p {
  margin: 10px 0 0;
  font-size: 1.2em;
  color: #ffffff;
  opacity: 0.8;
}

.court-content {
  width: 100%;
  height: calc(100vh - 140px);
  overflow: hidden;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header h1 {
    font-size: 1.8em;
  }
  
  .page-header p {
    font-size: 1em;
  }
  
  .court-content {
    height: calc(100vh - 120px);
  }
}
</style>