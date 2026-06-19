<template>
  <div id="app">
    <!-- 顶部导航栏 -->
    <nav class="top-nav fixed-top">
      <div class="nav-left"><i class="fa-solid fa-scale-balanced"></i>    模拟法庭</div>
      <div class="nav-right">
        <div class="nav-links" v-if="!isMobile">
          <button @click="navigateTo('/home')">首页</button>
          <button @click="navigateTo('/chat')">开始对话</button>
          <button @click="navigateTo('/history')">历史对话</button>
          <button @click="navigateTo('/about')">关于我们</button>
          
          <!-- 根据登录状态显示不同按钮 -->
          <template v-if="isLoggedIn">
            <button class="btn btn-outline logout-btn" @click="handleLogout">退出登录</button>
          </template>
          <template v-else>
            <button class="btn btn-outline login-btn" @click="navigateTo('/login')">登录</button>
            <!-- 已移除注册按钮 -->
          </template>
        </div>
        <div class="hamburger" v-if="isMobile" @click="toggleMobileMenu">☰</div>
      </div>
    </nav>

    <!-- 移动端菜单 -->
    <transition name="fade">
      <div class="mobile-menu" v-if="isMobile && mobileMenuOpen">
        <button @click="navigateTo('/home')">首页</button>
        <button @click="navigateTo('/chat')">开始对话</button>
        <button @click="navigateTo('/history')">历史对话</button>
        <button @click="navigateTo('/about')">关于我们</button>
        
        <!-- 移动端登录状态按钮 -->
        <template v-if="isLoggedIn">
          <button class="btn btn-outline logout-btn" @click="handleLogout">退出登录</button>
        </template>
        <template v-else>
          <button class="btn btn-outline login-btn" @click="navigateTo('/login')">登录</button>
          <!-- 已移除注册按钮 -->
        </template>
      </div>
    </transition>

    <transition name="slide">
      <RouterView />
    </transition>

    <!-- 底部区域 -->
    <footer class="footer">
      <div class="footer-nav">
        <div class="footer-column">
          <h3>产品</h3>
          <button @click="navigateTo('/features')">功能</button>
          <button @click="navigateTo('/pricing')">定价</button>
          <button @click="navigateTo('/security')">安全</button>
        </div>
        <div class="footer-column">
          <h3>公司</h3>
          <button @click="navigateTo('/careers')">职业发展</button>
          <button @click="navigateTo('/contact')">联系我们</button>
        </div>
        <div class="footer-column">
          <h3>资源</h3>
          <button @click="navigateTo('/docs')">文档</button>
          <button @click="navigateTo('/blog')">博客</button>
          <button @click="navigateTo('/help')">帮助中心</button>
        </div>
        <div class="footer-column">
          <h3>法律</h3>
          <button @click="navigateTo('/privacy')">隐私</button>
          <button @click="navigateTo('/terms')">条款</button>
          <button @click="navigateTo('/cookies')">Cookies</button>
        </div>
      </div>
      <div class="social">
        <a href="https://twitter.com" target="_blank">Twitter</a>
        <a href="https://linkedin.com" target="_blank">LinkedIn</a>
      </div>
      <div class="copyright">© 2025 山政网安开发团队版权所有</div>
    </footer>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { ref, onMounted, onBeforeUnmount, watchEffect } from 'vue'
import { STORAGE_KEYS } from './constants'

export default {
  setup() {
    const router = useRouter()
    const isMobile = ref(false)
    const mobileMenuOpen = ref(false)
    const isLoggedIn = ref(false)  // 登录状态标识

    // 检查登录状态
    const checkLoginStatus = () => {
      isLoggedIn.value = !!localStorage.getItem(STORAGE_KEYS.TOKEN)
    }

    // 退出登录处理
    const handleLogout = () => {
      // 清除本地存储的登录信息
      localStorage.removeItem(STORAGE_KEYS.TOKEN)
      localStorage.removeItem(STORAGE_KEYS.USERNAME)
      localStorage.removeItem(STORAGE_KEYS.ROLE)
      
      // 更新登录状态
      isLoggedIn.value = false
      
      // 跳转到登录前的首页
      router.push('/home')
      
      // 关闭移动端菜单（如果打开）
      mobileMenuOpen.value = false
    }

    const checkMobile = () => {
      isMobile.value = window.innerWidth < 768
      if (!isMobile.value) {
        mobileMenuOpen.value = false
      }
    }

    const toggleMobileMenu = () => {
      mobileMenuOpen.value = !mobileMenuOpen.value
    }

    const navigateTo = (page) => {
      router.push(page)
      // 导航后关闭移动端菜单
      if (isMobile.value) {
        mobileMenuOpen.value = false
      }
    }

    onMounted(() => {
      checkMobile()
      checkLoginStatus()  // 初始化时检查登录状态
      window.addEventListener('resize', checkMobile)
      
      // 监听路由变化，实时更新登录状态
      watchEffect(() => {
        checkLoginStatus()
        if (isLoggedIn.value && 
      (router.currentRoute.value.path === '/login' || 
       router.currentRoute.value.path === '/register')) {
    router.push('/home')
  }
      })
    })

    onBeforeUnmount(() => {
      window.removeEventListener('resize', checkMobile)
    })

    return {
      isMobile,
      mobileMenuOpen,
      isLoggedIn,
      toggleMobileMenu,
      navigateTo,
      handleLogout
    }
  },
}
</script>

<style scoped>
/* 样式部分保持不变 */

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: var(--color-bg-warm);
  color: var(--color-text-primary);
  padding-top: 70px;
}

.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #ffffff;
  padding: 14px 24px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  border-bottom: 1px solid var(--color-border);
}

.nav-left {
  font-size: 24px;
  font-weight: bold;
  color: var(--color-primary);
}

.nav-links {
  display: flex;
  align-items: center;
}

.nav-links button {
  background: none;
  border: none;
  margin-left: 18px;
  padding: 8px 14px;
  cursor: pointer;
  border-radius: 6px;
  font-weight: 500;
  transition: 0.3s;
}

.nav-links button:hover {
  background: var(--color-bg-red-light);
  color: var(--color-primary);
}

/* 按钮样式优化 - 增加特异性避免被覆盖 */
.btn {
  padding: 8px 18px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  border: none;
  display: inline-flex; /* 确保按钮正确显示 */
  align-items: center;
  justify-content: center;
}

/* 登录/注册/退出按钮单独设置样式，提高优先级 */
.btn-outline.login-btn,
.btn-outline.logout-btn {
  width: 100px;
  background: transparent;
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  margin-left: 18px; /* 确保间距一致 */
}

.btn-primary.register-btn {
  background: var(--gradient-primary);
  color: white; /* 修复注册按钮文字颜色 */
  border: none;
  margin-left: 10px;
}

.btn-outline:hover {
  background-color: var(--color-primary);
  color: white;
  box-shadow: var(--shadow-md);
}

.btn-primary:hover {
  background: var(--gradient-primary-hover);
  box-shadow: var(--shadow-md);
}

.hamburger {
  font-size: 26px;
  cursor: pointer;
  padding: 6px;
  background: var(--color-primary);
  color: white;
  border-radius: 6px;
  transition: var(--transition-normal);
}

.hamburger:hover {
  background-color: var(--color-primary-dark);
}

.mobile-menu {
  background: #ffffff;
  padding: 16px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  border-radius: 0 0 8px 8px;
}

.mobile-menu button {
  margin: 8px 0;
  padding: 12px;
  text-align: left;
  background: none;
  border: none;
  border-radius: 6px;
  transition: 0.3s;
}

.mobile-menu button:hover {
  background-color: var(--color-bg-red-light);
}

/* 移动端按钮样式 */
.mobile-menu .btn {
  width: 100%;
  justify-content: center;
  margin: 8px 0;
}

/* --- Footer 样式开始 --- */
.footer {
  background-color: var(--color-bg-red-light);
  padding: 40px 20px;
  text-align: center;
  border-top: 1px solid var(--color-border);
  margin-top: 80px;
}

.footer-nav {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
  margin-bottom: 20px;
  text-align: left;
}

.footer-column {
  width: 200px;
  flex-shrink: 0;
}

.footer-column h3 {
  font-size: 16px;
  margin-bottom: 10px;
  color: var(--color-primary);
}

.footer-column button {
  display: block;
  background: none;
  border: none;
  color: #555;
  margin: 4px 0;
  text-align: left;
  padding: 6px 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.footer-column button:hover {
  background-color: var(--color-bg-warm);
}

.social a {
  margin: 0 12px;
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
}

.social a:hover {
  text-decoration: underline;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.slide-enter-active, .slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter-from, .slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .nav-links {
    display: none;
  }

  .footer-nav {
    flex-direction: column;
    align-items: center;
  }

  .footer-column {
    width: 100%;
    max-width: 300px;
    text-align: center;
  }

  .footer-column button {
    text-align: center;
  }
}
</style>