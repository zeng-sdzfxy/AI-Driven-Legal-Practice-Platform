// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Chat from "../views/Chat.vue";
import AboutUs from "../views/AboutUs.vue";
import Login from "../views/login.vue";
import History from "../views/history.vue";

const routes = [
  {
    path: "/",
    redirect: "/home",
  },
  {
    path: "/home",
    name: "Home",
    component: Home,
  },
  {
    path: "/chat",
    name: "Chat",
    component: Chat,
  },
  {
    path: "/about",
    name: "AboutUs",
    component: AboutUs,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path:"/register",
    name:"Register",
    component:Login,
  },
  {
    path: "/history",
    name: "History",
    component: History,
  },
  // 你可以根据需要添加更多路由
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
