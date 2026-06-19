<template>
  <div id="home">
    <!-- ===== Section 1: Hero 大横幅 ===== -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="hero-text">
          <p class="hero-tagline">AI 驱动的法律实践平台</p>
          <h1 class="hero-title">模拟<span class="hero-highlight">法庭</span></h1>
          <p class="hero-subtitle">
            选择角色，进入庭审，体验真实的法庭对抗<br />
            2D / 3D 双重模式，开启你的法律之旅
          </p>
          <div class="hero-buttons">
            <button @click="navigateTo('/chat')" class="btn-hero-primary">
              <i class="fa-solid fa-gavel"></i> 开始体验
            </button>
            <button @click="scrollToCaseLibrary" class="btn-hero-secondary">
              浏览案例 <i class="fa-solid fa-arrow-down"></i>
            </button>
          </div>
        </div>

        <!-- 法庭建筑插画 -->
        <div class="court-building" aria-hidden="true">
          <div class="court-emblem">
            <i class="fa-solid fa-scale-balanced"></i>
          </div>
          <div class="court-columns"></div>
          <div class="court-base"></div>
        </div>
      </div>

      <!-- 波浪分隔 -->
      <div class="wave-divider">
        <svg viewBox="0 0 1440 80" preserveAspectRatio="none">
          <path d="M0,40 C240,80 480,0 720,40 C960,80 1200,0 1440,40 L1440,80 L0,80 Z" fill="var(--color-bg-warm)" />
        </svg>
      </div>
    </section>

    <!-- ===== Section 2: 数据展示条 ===== -->
    <section class="stats-section">
      <div class="stats-row">
        <div class="stat-item">
          <span class="stat-number">8<span class="stat-plus">+</span></span>
          <span class="stat-label">案件类型</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-number">3<span class="stat-plus">种</span></span>
          <span class="stat-label">模拟角色</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-number">4.8</span>
          <span class="stat-label">
            <i class="fa-solid fa-star"></i> 平均评分
          </span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-number">1000<span class="stat-plus">+</span></span>
          <span class="stat-label">对话完成</span>
        </div>
      </div>
    </section>

    <!-- ===== Section 3: 核心功能 ===== -->
    <section class="features-section">
      <div class="section-header">
        <h2>核心功能</h2>
        <div class="golden-line"></div>
        <p>专为法律模拟训练打造的完整解决方案</p>
      </div>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fa-solid fa-user-tie"></i>
          </div>
          <h3>角色扮演</h3>
          <p>自由选择法官、原告律师或被告律师，体验不同法律角色的思维方式与表达技巧</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fa-solid fa-landmark"></i>
          </div>
          <h3>庭审模拟</h3>
          <p>2D 对话模式 + 3D 沉浸式场景，真实还原法庭环境，支持语音输入与实时对话</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fa-solid fa-chart-line"></i>
          </div>
          <h3>智能评价</h3>
          <p>AI 驱动的多维评估报告，涵盖法律专业性、逻辑清晰度、证据运用等维度</p>
        </div>
      </div>
    </section>

    <!-- ===== Section 4: 庭审流程 ===== -->
    <section class="process-section">
      <div class="process-inner">
        <div class="section-header">
          <h2>庭审流程</h2>
          <div class="golden-line"></div>
          <p>模拟真实法庭的完整流程</p>
        </div>
        <div class="process-timeline">
        <div class="process-step">
          <div class="step-circle">1</div>
          <h4>开庭</h4>
          <p>法官核对身份<br />宣布庭审规则</p>
        </div>
        <div class="process-connector"></div>
        <div class="process-step">
          <div class="step-circle">2</div>
          <h4>陈述</h4>
          <p>原告陈述诉求<br />被告进行答辩</p>
        </div>
        <div class="process-connector"></div>
        <div class="process-step">
          <div class="step-circle">3</div>
          <h4>举证</h4>
          <p>双方提交证据<br />进行质证环节</p>
        </div>
        <div class="process-connector"></div>
        <div class="process-step">
          <div class="step-circle">4</div>
          <h4>辩论</h4>
          <p>双方展开辩论<br />阐述法律观点</p>
        </div>
        <div class="process-connector"></div>
        <div class="process-step">
          <div class="step-circle">5</div>
          <h4>判决</h4>
          <p>法官宣布判决<br />庭审结束</p>
        </div>
      </div>
      </div>
    </section>

    <!-- ===== Section 5: 精选案例库 ===== -->
    <section class="cases-section" id="case-library">
      <div class="section-header">
        <h2>精选案例库</h2>
        <div class="golden-line"></div>
        <p>热门庭审案例，选择你感兴趣的开始模拟</p>
      </div>
      <div class="cases-grid">
        <div class="case-card">
          <div class="case-card-top business">
            <span class="case-category">商事案件</span>
            <span class="case-difficulty medium">中级难度</span>
          </div>
          <div class="case-card-body">
            <h3>股权转让合同纠纷</h3>
            <p>原告与被告就某科技公司的股权转让事宜签订合同后，因付款时间问题产生争议...</p>
            <div class="case-card-footer">
              <div class="case-stats">
                <span><i class="fa-solid fa-users"></i> 328人参与</span>
                <span class="case-rating"><i class="fa-solid fa-star"></i> 4.8</span>
              </div>
              <a href="#" class="case-link">查看详情 <i class="fa-solid fa-arrow-right"></i></a>
            </div>
          </div>
        </div>

        <div class="case-card">
          <div class="case-card-top criminal">
            <span class="case-category">刑事案件</span>
            <span class="case-difficulty hard">高级难度</span>
          </div>
          <div class="case-card-body">
            <h3>故意杀人案的辩护</h3>
            <p>被告因被控在争吵中持刀杀害被害人，公诉机关以故意杀人罪提起公诉...</p>
            <div class="case-card-footer">
              <div class="case-stats">
                <span><i class="fa-solid fa-users"></i> 256人参与</span>
                <span class="case-rating"><i class="fa-solid fa-star"></i> 4.9</span>
              </div>
              <a href="#" class="case-link">查看详情 <i class="fa-solid fa-arrow-right"></i></a>
            </div>
          </div>
        </div>

        <div class="case-card">
          <div class="case-card-top civil">
            <span class="case-category">民事案件</span>
            <span class="case-difficulty easy">初级难度</span>
          </div>
          <div class="case-card-body">
            <h3>房屋租赁合同纠纷</h3>
            <p>原告与被告签订房屋租赁合同，后因房屋维修责任和租金调整问题产生争议...</p>
            <div class="case-card-footer">
              <div class="case-stats">
                <span><i class="fa-solid fa-users"></i> 412人参与</span>
                <span class="case-rating"><i class="fa-solid fa-star"></i> 4.7</span>
              </div>
              <a href="#" class="case-link">查看详情 <i class="fa-solid fa-arrow-right"></i></a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== Section 6: CTA 行动号召 ===== -->
    <section class="cta-section">
      <div class="cta-content">
        <h2>准备好开始你的法庭之旅了吗？</h2>
        <p>立即选择角色，进入模拟法庭，体验真实的法律对抗</p>
        <button @click="navigateTo('/chat')" class="btn-cta">
          <i class="fa-solid fa-gavel"></i> 立即开始
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const navigateTo = (page) => {
  router.push(page);
};

const scrollToCaseLibrary = () => {
  const element = document.getElementById('case-library');
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
};
</script>

<style scoped>
/* ===== 全局基础 ===== */
#home {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  color: var(--color-text-primary);
}

/* ===== Section 1: Hero ===== */
.hero-section {
  background: var(--gradient-hero-light);
  min-height: 85vh;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 2px,
    rgba(255,255,255,0.008) 2px,
    rgba(255,255,255,0.008) 4px
  );
  pointer-events: none;
}

.hero-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 40px;
  gap: 60px;
  position: relative;
  z-index: 1;
}

.hero-text {
  flex: 0 0 480px;
}

.hero-tagline {
  color: var(--color-gold);
  font-size: 14px;
  letter-spacing: 4px;
  text-transform: uppercase;
  margin-bottom: 16px;
}

.hero-title {
  font-size: 64px;
  font-weight: 800;
  color: var(--color-text-on-primary);
  line-height: 1.15;
  margin: 0 0 20px 0;
}

.hero-highlight {
  color: var(--color-gold);
  position: relative;
}

.hero-highlight::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--gradient-gold);
  border-radius: 2px;
}

.hero-subtitle {
  font-size: 17px;
  color: var(--color-text-on-dark);
  line-height: 1.8;
  margin-bottom: 36px;
  opacity: 0.9;
}

.hero-buttons {
  display: flex;
  gap: 16px;
}

.btn-hero-primary {
  background: var(--gradient-gold);
  color: #1A0A0A;
  border: none;
  padding: 14px 32px;
  font-size: 16px;
  font-weight: 700;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-normal);
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-hero-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.btn-hero-secondary {
  background: transparent;
  color: var(--color-text-on-primary);
  border: 1.5px solid rgba(255,255,255,0.3);
  padding: 14px 32px;
  font-size: 16px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-normal);
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-hero-secondary:hover {
  border-color: var(--color-gold);
  color: var(--color-gold);
}

/* ===== 法庭建筑插画 ===== */
.court-building {
  flex: 0 0 360px;
  height: 460px;
  position: relative;
  z-index: 2;
}

/* 山形墙 (三角屋顶) */
.court-building::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 145px solid transparent;
  border-right: 145px solid transparent;
  border-bottom: 90px solid var(--color-primary);
  filter: drop-shadow(0 4px 12px rgba(0,0,0,0.3));
}

/* 山形墙金色边框线 */
.court-building::after {
  content: '';
  position: absolute;
  top: 90px;
  left: 50%;
  transform: translateX(-50%);
  width: 256px;
  height: 3px;
  background: var(--gradient-gold);
}

/* 天平徽章 */
.court-emblem {
  position: absolute;
  top: 22px;
  left: 50%;
  transform: translateX(-50%);
  width: 52px;
  height: 52px;
  background: var(--gradient-gold);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

.court-emblem i {
  font-size: 22px;
  color: #1A0A0A;
}

/* 立柱阵列 — 6根柱子 */
.court-columns {
  position: absolute;
  top: 93px;
  left: 20px;
  width: 16px;
  height: 240px;
  background: var(--color-primary);
  box-shadow:
    48px 0 0 var(--color-primary),
    96px 0 0 var(--color-primary),
    144px 0 0 var(--color-primary),
    192px 0 0 var(--color-primary),
    240px 0 0 var(--color-primary);
  border-radius: 3px 3px 0 0;
  opacity: 0.9;
}

/* 立柱金色柱头装饰 */
.court-columns::before {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  width: 24px;
  height: 6px;
  background: var(--color-gold);
  border-radius: 2px;
  box-shadow:
    48px 0 0 var(--color-gold),
    96px 0 0 var(--color-gold),
    144px 0 0 var(--color-gold),
    192px 0 0 var(--color-gold),
    240px 0 0 var(--color-gold);
}

/* 基座/台阶 */
.court-base {
  position: absolute;
  bottom: 60px;
  left: 8px;
  right: 8px;
  height: 0;
}

.court-base::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 28px;
  background: var(--color-primary);
  border-radius: 4px 4px 0 0;
  box-shadow: 0 8px 0 rgba(139,26,26,0.4), 0 -8px 0 rgba(201,169,110,0.5);
}

.court-base::after {
  content: '';
  position: absolute;
  bottom: 48px;
  left: -16px;
  right: -16px;
  height: 16px;
  background: var(--color-primary-dark);
  border-radius: 3px 3px 0 0;
}

/* 波浪分隔 */
.wave-divider {
  width: 100%;
  height: 80px;
  margin-top: auto;
}

.wave-divider svg {
  width: 100%;
  height: 100%;
  display: block;
}

/* ===== Section 2: 数据展示条 ===== */
.stats-section {
  background: var(--color-bg-warm);
  padding: 60px 40px;
}

.stats-row {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: var(--color-bg-white);
  border-radius: var(--radius-lg);
  padding: 40px 20px;
  box-shadow: var(--shadow-md);
  margin-top: -40px;
  position: relative;
  z-index: 2;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 42px;
  font-weight: 800;
  color: var(--color-primary);
  line-height: 1;
  margin-bottom: 8px;
}

.stat-plus {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-gold);
}

.stat-label {
  font-size: 14px;
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.stat-label .fa-star {
  color: var(--color-gold);
  font-size: 12px;
}

.stat-divider {
  width: 1px;
  height: 50px;
  background: var(--color-border);
}

/* ===== Section 通用标题 ===== */
.section-header {
  text-align: center;
  margin-bottom: 50px;
}

.section-header h2 {
  font-size: 36px;
  font-weight: 700;
  color: var(--color-primary);
  margin: 0 0 12px 0;
}

.golden-line {
  width: 60px;
  height: 3px;
  background: var(--gradient-gold);
  margin: 0 auto 16px;
  border-radius: 2px;
}

.section-header p {
  color: var(--color-text-secondary);
  font-size: 16px;
  margin: 0;
}

/* ===== Section 3: 核心功能 ===== */
.features-section {
  padding: 80px 40px;
  background: var(--color-bg-warm);
}

.features-grid {
  max-width: 1000px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.feature-card {
  background: var(--color-bg-white);
  border-radius: var(--radius-lg);
  padding: 40px 30px;
  text-align: center;
  transition: var(--transition-normal);
  border: 1px solid var(--color-border-light);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg);
  border-color: var(--color-primary);
}

.feature-icon {
  width: 72px;
  height: 72px;
  background: var(--color-bg-red-light);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  transition: var(--transition-normal);
}

.feature-card:hover .feature-icon {
  background: var(--color-primary);
}

.feature-icon i {
  font-size: 28px;
  color: var(--color-primary);
  transition: var(--transition-normal);
}

.feature-card:hover .feature-icon i {
  color: var(--color-text-on-primary);
}

.feature-card h3 {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 12px 0;
}

.feature-card p {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.7;
  margin: 0;
}

/* ===== Section 4: 庭审流程 ===== */
.process-section {
  padding: 80px 40px;
  background: var(--color-bg-warm);
}

.process-inner {
  max-width: 1000px;
  margin: 0 auto;
  background: var(--color-bg-white);
  border-radius: var(--radius-lg);
  padding: 50px 40px;
  box-shadow: var(--shadow-sm);
}

.process-timeline {
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 0;
}

.process-step {
  text-align: center;
  flex: 0 0 130px;
}

.step-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--gradient-primary);
  color: var(--color-text-on-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  margin: 0 auto 16px;
  transition: var(--transition-normal);
}

.process-step:hover .step-circle {
  transform: scale(1.15);
  box-shadow: var(--shadow-md);
}

.process-step h4 {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 8px 0;
}

.process-step p {
  font-size: 13px;
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0;
}

.process-connector {
  flex: 0 0 60px;
  height: 3px;
  background: linear-gradient(to right, var(--color-primary), var(--color-gold));
  margin-top: 22px;
  border-radius: 2px;
}

/* ===== Section 5: 案例库 ===== */
.cases-section {
  padding: 80px 40px;
  background: var(--color-bg-warm);
}

.cases-grid {
  max-width: 1050px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.case-card {
  background: var(--color-bg-white);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: var(--transition-normal);
}

.case-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-lg);
}

.case-card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
}

.case-card-top.business { background: linear-gradient(135deg, #6a5acd, #7c6ed8); }
.case-card-top.criminal { background: linear-gradient(135deg, #c0392b, #e74c3c); }
.case-card-top.civil   { background: linear-gradient(135deg, #27ae60, #2ecc71); }

.case-category {
  color: white;
  font-weight: 600;
  font-size: 13px;
}

.case-difficulty {
  color: rgba(255,255,255,0.9);
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 12px;
  background: rgba(255,255,255,0.2);
}

.case-difficulty.hard { background: rgba(255,255,255,0.3); }
.case-difficulty.medium { background: rgba(255,255,255,0.2); }
.case-difficulty.easy { background: rgba(255,255,255,0.15); }

.case-card-body {
  padding: 20px 24px 24px;
}

.case-card-body h3 {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 10px 0;
}

.case-card-body > p {
  font-size: 13px;
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0 0 20px 0;
}

.case-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.case-stats {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.case-stats i {
  color: var(--color-gold);
  margin-right: 4px;
}

.case-rating {
  font-weight: 700;
  color: var(--color-primary) !important;
}

.case-link {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-primary);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: var(--transition-fast);
}

.case-link:hover {
  color: var(--color-accent);
  gap: 8px;
}

/* ===== Section 6: CTA ===== */
.cta-section {
  background: var(--gradient-hero-light);
  padding: 80px 40px;
  text-align: center;
  position: relative;
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
}

.cta-content h2 {
  font-size: 36px;
  font-weight: 700;
  color: var(--color-text-on-primary);
  margin: 0 0 16px 0;
}

.cta-content p {
  font-size: 17px;
  color: var(--color-text-on-dark);
  opacity: 0.85;
  margin: 0 0 36px 0;
}

.btn-cta {
  background: var(--gradient-gold);
  color: #1A0A0A;
  border: none;
  padding: 16px 48px;
  font-size: 18px;
  font-weight: 700;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-normal);
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.btn-cta:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold);
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .hero-content {
    flex-direction: column;
    padding: 40px 20px;
    gap: 30px;
    text-align: center;
  }

  .hero-text {
    flex: 0 0 auto;
  }

  .hero-title {
    font-size: 42px;
  }

  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }

  .court-building {
    flex: 0 0 280px;
    width: 260px;
    height: 340px;
    margin: 0 auto;
  }

  .court-building::before {
    border-left-width: 105px;
    border-right-width: 105px;
    border-bottom-width: 65px;
  }

  .court-building::after {
    width: 186px;
    top: 65px;
  }

  .court-emblem {
    top: 14px;
    width: 40px;
    height: 40px;
  }

  .court-emblem i {
    font-size: 18px;
  }

  .court-base::before {
    left: -10px;
    right: -10px;
  }

  .stats-row {
    flex-direction: column;
    gap: 20px;
    padding: 30px 20px;
  }

  .stat-divider {
    width: 60px;
    height: 1px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .process-timeline {
    flex-direction: column;
    align-items: center;
    gap: 0;
  }

  .process-connector {
    width: 3px;
    height: 30px;
    flex: 0 0 30px;
    margin: 0;
  }

  .cases-grid {
    grid-template-columns: 1fr;
  }

  .cta-content h2 {
    font-size: 28px;
  }
}
</style>
