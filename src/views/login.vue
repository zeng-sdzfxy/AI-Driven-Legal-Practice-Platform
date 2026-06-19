<template>
  <div class="login-container">
    <div class="container">
      <!-- 1. 登录界面 -->
      <div id="login-section" class="section" v-if="currentSection === 'login'">
        <div class="card">
          <h2 class="card-title">
            <i class="fa fa-sign-in"></i> 用户登录
          </h2>
          <!-- 登录错误提示 -->
          <div id="login-alert" class="alert error" v-if="loginAlert.show">
            <i class="fa fa-exclamation-circle"></i>
            <span>{{ loginAlert.message }}</span>
          </div>
          <!-- 登录表单 -->
          <form @submit.prevent="handleLogin">
            <div class="form-group">
              <label class="form-label" for="login-username">用户名</label>
              <input 
                type="text" 
                id="login-username" 
                class="form-input" 
                placeholder="输入默认账号：court_user" 
                v-model="loginForm.username"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label" for="login-password">密码</label>
              <input 
                type="password" 
                id="login-password" 
                class="form-input" 
                placeholder="输入默认密码：Court123456" 
                v-model="loginForm.password"
                required
              >
            </div>
            <button type="submit" class="login-btn login-btn-primary">
              <i class="fa fa-rocket"></i> 登录系统
            </button>
          </form>
          <!-- 切换到注册 -->
          <div class="toggle-link" @click="switchSection('register')">
            还没有账号？点击注册新账号
          </div>
        </div>
      </div>

      <!-- 2. 注册界面 -->
      <div id="register-section" class="section" v-if="currentSection === 'register'">
        <div class="card">
          <h2 class="card-title">
            <i class="fa fa-user-plus"></i> 用户注册
          </h2>
          <!-- 注册提示（错误/成功） -->
          <div 
            id="register-alert" 
            class="alert" 
            :class="{ error: registerAlert.type === 'error', success: registerAlert.type === 'success' }"
            v-if="registerAlert.show"
          >
            <i class="fa fa-info-circle"></i>
            <span>{{ registerAlert.message }}</span>
          </div>
          <!-- 注册表单 -->
          <form @submit.prevent="handleRegister">
            <div class="form-group">
              <label class="form-label" for="register-username">用户名</label>
              <input 
                type="text" 
                id="register-username" 
                class="form-input" 
                placeholder="3-50位字母/数字/下划线" 
                v-model="registerForm.username"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label" for="register-password">密码</label>
              <input 
                type="password" 
                id="register-password" 
                class="form-input" 
                placeholder="至少6位，建议包含字母和数字" 
                v-model="registerForm.password"
                required
              >
            </div>
            <div class="form-group">
              <label class="form-label" for="register-role">选择角色</label>
              <select 
                id="register-role" 
                class="form-select" 
                v-model="registerForm.role"
                required
              >
                <option value="" disabled>请选择您的角色</option>
                <option value="模拟法庭">模拟法庭用户</option>
                <option value="敏感数据">敏感数据管理员</option>
                <option value="任务管理系统">任务管理管理员</option>
              </select>
            </div>
            <button type="submit" class="login-btn login-btn-primary">
              <i class="fa fa-check"></i> 注册账号
            </button>
          </form>
          <!-- 切换到登录 -->
          <div class="toggle-link" @click="switchSection('login')">
            已有账号？点击返回登录
          </div>
        </div>
      </div>

      <!-- 3. 模拟法庭工作台 -->
      <div id="court-dashboard" class="section" v-if="currentSection === 'court'">
        <div class="card">
          <div class="dashboard-header">
            <div>
              <div class="dashboard-welcome">欢迎您，{{ username }}！</div>
              <div class="dashboard-role">角色：模拟法庭用户</div>
            </div>
            <div style="display: flex; gap: 10px;">
              <button class="login-btn login-btn-primary" @click="goToHome">
                <i class="fa fa-home"></i> 首页
              </button>
              <button class="login-btn login-btn-logout" @click="logout">
                <i class="fa fa-sign-out"></i> 退出登录
              </button>
            </div>
          </div>
          <h3 style="color: var(--color-primary); margin-bottom: 1rem;">模拟法庭功能</h3>
          <div class="func-cards">
            <div class="func-card">
              <i class="fa fa-balance-scale"></i>
              <div class="func-card-title">案件报名</div>
              <div class="func-card-desc">浏览并报名新庭审案件</div>
            </div>
            <div class="func-card">
              <i class="fa fa-file-text-o"></i>
              <div class="func-card-title">资料下载</div>
              <div class="func-card-desc">获取庭审所需材料</div>
            </div>
            <div class="func-card">
              <i class="fa fa-video-camera"></i>
              <div class="func-card-title">模拟庭审</div>
              <div class="func-card-desc">进入庭审房间</div>
            </div>
            <div class="func-card">
              <i class="fa fa-history"></i>
              <div class="func-card-title">庭审记录</div>
              <div class="func-card-desc">查看历史庭审记录</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 4. 敏感数据管理员工作台 -->
      <div id="data-dashboard" class="section" v-if="currentSection === 'data'">
        <div class="card">
          <div class="dashboard-header">
            <div>
              <div class="dashboard-welcome">欢迎您，{{ username }}！</div>
              <div class="dashboard-role">角色：敏感数据管理员</div>
            </div>
            <div style="display: flex; gap: 10px;">
              <button class="login-btn login-btn-primary" @click="goToHome">
                <i class="fa fa-home"></i> 首页
              </button>
              <button class="login-btn login-btn-logout" @click="logout">
                <i class="fa fa-sign-out"></i> 退出登录
              </button>
            </div>
          </div>
          <h3 style="color: var(--color-primary); margin-bottom: 1rem;">敏感数据管理功能</h3>
          <div class="func-cards">
            <div class="func-card">
              <i class="fa fa-database"></i>
              <div class="func-card-title">数据查询</div>
              <div class="func-card-desc">查询系统敏感数据</div>
            </div>
            <div class="func-card">
              <i class="fa fa-lock"></i>
              <div class="func-card-title">加密配置</div>
              <div class="func-card-desc">设置数据加密规则</div>
            </div>
            <div class="func-card">
              <i class="fa fa-history"></i>
              <div class="func-card-title">操作日志</div>
              <div class="func-card-desc">审计数据访问记录</div>
            </div>
            <div class="func-card">
              <i class="fa fa-user-circle"></i>
              <div class="func-card-title">权限管理</div>
              <div class="func-card-desc">管理数据访问权限</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 5. 任务管理管理员工作台 -->
      <div id="task-dashboard" class="section" v-if="currentSection === 'task'">
        <div class="card">
          <div class="dashboard-header">
            <div>
              <div class="dashboard-welcome">欢迎您，{{ username }}！</div>
              <div class="dashboard-role">角色：任务管理管理员</div>
            </div>
            <div style="display: flex; gap: 10px;">
              <button class="login-btn login-btn-primary" @click="goToHome">
                <i class="fa fa-home"></i> 首页
              </button>
              <button class="login-btn login-btn-logout" @click="logout">
                <i class="fa fa-sign-out"></i> 退出登录
              </button>
            </div>
          </div>
          <h3 style="color: var(--color-primary); margin-bottom: 1rem;">任务管理功能</h3>
          <div class="func-cards">
            <div class="func-card">
              <i class="fa fa-plus-circle"></i>
              <div class="func-card-title">创建任务</div>
              <div class="func-card-desc">新建任务并设置详情</div>
            </div>
            <div class="func-card">
              <i class="fa fa-users"></i>
              <div class="func-card-title">任务分配</div>
              <div class="func-card-desc">分配任务给指定用户</div>
            </div>
            <div class="func-card">
              <i class="fa fa-tasks"></i>
              <div class="func-card-title">进度跟踪</div>
              <div class="func-card-desc">查看任务完成进度</div>
            </div>
            <div class="func-card">
              <i class="fa fa-bar-chart"></i>
              <div class="func-card-title">任务报表</div>
              <div class="func-card-desc">生成任务统计报表</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'
import { STORAGE_KEYS, API_BASE_URLS } from '../constants'

// 基础配置
const RBAC_API_BASE = API_BASE_URLS.RBAC;

// 初始化路由实例
const router = useRouter();

// 状态管理
const currentSection = ref('login'); // 当前显示的界面
const username = ref(''); // 当前登录用户名
const userRole = ref(''); // 当前用户角色

// 登录表单数据
const loginForm = ref({
  username: '',
  password: ''
});

// 登录提示信息
const loginAlert = ref({
  show: false,
  message: ''
});

// 注册表单数据
const registerForm = ref({
  username: '',
  password: '',
  role: ''
});

// 注册提示信息
const registerAlert = ref({
  show: false,
  type: '', // error 或 success
  message: ''
});

// 界面切换
const switchSection = (sectionId) => {
  currentSection.value = sectionId;
  // 清空提示信息
  loginAlert.value.show = false;
  registerAlert.value.show = false;
};

// 显示提示信息
const showAlert = (target, type, message) => {
  if (target === 'login') {
    loginAlert.value.show = true;
    loginAlert.value.message = message;
  } else if (target === 'register') {
    registerAlert.value.show = true;
    registerAlert.value.type = type;
    registerAlert.value.message = message;
  }
};

// 登录处理
const handleLogin = async () => {
  if (!loginForm.value.username) {
    return showAlert('login', 'error', '请输入用户名');
  }
  if (!loginForm.value.password) {
    return showAlert('login', 'error', '请输入密码');
  }

  try {
    const response = await fetch(`${RBAC_API_BASE}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ 
        username: loginForm.value.username, 
        password: loginForm.value.password 
      }),
      credentials: "include"
    });

    const responseData = await response.json();
    if (!response.ok) {
      throw new Error(responseData.detail || "登录失败，请检查账号密码");
    }

    localStorage.setItem(STORAGE_KEYS.TOKEN, responseData.access_token);
    localStorage.setItem(STORAGE_KEYS.USERNAME, responseData.username);
    localStorage.setItem(STORAGE_KEYS.ROLE, responseData.role);

    username.value = responseData.username;
    userRole.value = responseData.role;

    // 登录成功后跳转到首页
    router.push('/');
     window.location.reload();

  } catch (error) {
    showAlert('login', 'error', error.message);
  }
};

// 注册处理
const handleRegister = async () => {
  if (registerForm.value.username.length < 3 || registerForm.value.username.length > 50) {
    return showAlert('register', 'error', '用户名需3-50位字符');
  }
  if (registerForm.value.password.length < 6) {
    return showAlert('register', 'error', '密码需至少6位字符');
  }
  if (!registerForm.value.role) {
    return showAlert('register', 'error', '请选择角色');
  }

  try {
    const response = await fetch(`${RBAC_API_BASE}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ 
        username: registerForm.value.username, 
        password: registerForm.value.password,
        role: registerForm.value.role
      }),
      credentials: "include"
    });

    const responseData = await response.json();
    if (!response.ok) {
      throw new Error(responseData.detail || "注册失败，请重试");
    }

    showAlert(
      'register', 
      'success', 
      `注册成功！用户名：${responseData.username}，2秒后跳转到登录页`
    );
    
    setTimeout(() => {
      switchSection('login');
      registerForm.value = { username: '', password: '', role: '' };
    }, 2000);

  } catch (error) {
    showAlert('register', 'error', error.message);
  }
};

// 跳转到对应工作台（保持原功能，供其他场景使用）
const redirectToDashboard = (role) => {
  if (!['模拟法庭', '管理员'].includes(role)) {
    showAlert('login', 'error', '该角色无权限访问历史记录');
  }
  switch (role) {
    case "模拟法庭":
      currentSection.value = 'court';
      break;
    case "敏感数据":
      currentSection.value = 'data';
      break;
    case "任务管理系统":
      currentSection.value = 'task';
      break;
    default:
      showAlert('login', 'error', '未知角色，无法跳转');
      currentSection.value = 'login';
  }
};

// 退出登录
const logout = () => {
  localStorage.removeItem(STORAGE_KEYS.TOKEN);
  localStorage.removeItem(STORAGE_KEYS.USERNAME);
  localStorage.removeItem(STORAGE_KEYS.ROLE);
  
  username.value = '';
  userRole.value = '';
  loginForm.value = { username: '', password: '' };
  
  currentSection.value = 'login';
  // 退出后跳转到登录页
  router.push('/login');
};

// 跳转到首页
const goToHome = () => {
  router.push('/');
};

// 页面加载时检查登录状态
onMounted(() => {
  const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
  const role = localStorage.getItem(STORAGE_KEYS.ROLE);
  const storedUsername = localStorage.getItem(STORAGE_KEYS.USERNAME);
  
  if (token && role && storedUsername) {
    username.value = storedUsername;
    userRole.value = role;
    // 已登录状态下，如果当前页面是登录页，则跳转到首页
    if (router.currentRoute.value.path === '/login') {
      router.push('/');
    } else {
      redirectToDashboard(role);
    }
  } else {
    currentSection.value = 'login';
  }
});
</script>

<style scoped>
.login-container {
  background: var(--gradient-hero);
  min-height: 100vh;
  padding: 3rem 1rem;
}

.container {
  max-width: 500px;
  margin: 0 auto;
}

.section {
  animation: fadeIn 0.3s ease;
}

.card {
  background: var(--color-bg-white);
  border-radius: var(--radius-lg);
  padding: 2.5rem;
  box-shadow: var(--shadow-lg);
  margin-bottom: 2rem;
  border-top: 4px solid var(--color-primary);
}

.card-title {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-primary);
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.card-title i {
  color: var(--color-accent);
  font-size: 1.8rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  color: #475569;
  margin-bottom: 0.5rem;
}

.form-input, .form-select {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(139, 26, 26, 0.1);
}

.login-btn {
  width: 100%;
  padding: 0.9rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.login-btn-primary {
  background: var(--gradient-primary);
  color: white;
}

.login-btn-primary:hover {
  background: var(--gradient-primary-hover);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.login-btn-logout {
  background-color: #ef4444;
  color: white;
  padding: 0.6rem 1.2rem;
  width: auto;
}

.login-btn-logout:hover {
  background-color: #dc2626;
}

.alert {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.alert.error {
  background-color: #fee2e2;
  color: #dc2626;
  border: 1px solid #fecdd3;
}

.alert.success {
  background-color: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.toggle-link {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: var(--color-primary);
  cursor: pointer;
}

.toggle-link:hover {
  text-decoration: underline;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-welcome {
  font-size: 1.2rem;
  font-weight: 500;
  color: var(--color-primary);
}

.dashboard-role {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  margin-top: 0.3rem;
}

.func-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 1.5rem;
}

.func-card {
  background-color: var(--color-bg-red-light);
  border-radius: var(--radius-md);
  padding: 1.2rem;
  text-align: center;
  transition: transform var(--transition-fast);
  border: 1px solid var(--color-border-light);
}

.func-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-sm);
}

.func-card i {
  font-size: 1.8rem;
  color: var(--color-accent);
  margin-bottom: 0.8rem;
}

.func-card-title {
  font-weight: 500;
  color: var(--color-primary);
  margin-bottom: 0.3rem;
}

.func-card-desc {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>