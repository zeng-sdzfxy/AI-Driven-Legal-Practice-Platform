// src/main.js
import { createApp } from "vue";
import App from "./App.vue";
// 修改导入路径
import router from "./router";
import "./theme.css";
import axios from 'axios';

const app = createApp(App);
// 使用路由
app.use(router);
// 挂载应用
app.mount("#app");
// 在main.js或请求工具文件中
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
