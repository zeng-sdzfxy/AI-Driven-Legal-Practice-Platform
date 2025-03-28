import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Chat from "@/views/Chat.vue";
import AboutUs from "@/views/AboutUs.vue";
const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/chat",
    name: "Chat",
    component: Chat,
  },
  {
    path: "/AboutUs",
    name: "AboutUs",
    component: AboutUs,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
