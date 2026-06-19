<template>
  <div class="history-page">
    <h1 class="page-title">模拟法庭评价报告记录</h1>

    <!-- 评价报告筛选区域 -->
    <div class="filter-section">
      <div class="filter-group">
        <label>案件类型:</label>
        <select v-model="selectedType" @change="filterReports" class="form-select">
          <option value="">全部类型</option>
          <option value="合同纠纷">合同纠纷</option>
          <option value="侵权责任">侵权责任</option>
          <option value="婚姻家庭">婚姻家庭</option>
          <option value="劳动争议">劳动争议</option>
          <option value="其他">其他</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>角色:</label>
        <select v-model="selectedRole" @change="filterReports" class="form-select">
          <option value="">全部角色</option>
          <option value="法官">法官</option>
          <option value="原告律师">原告律师</option>
          <option value="被告律师">被告律师</option>
        </select>
      </div>
      
      <div class="filter-group date-range">
        <label>日期范围:</label>
        <input type="date" v-model="startDate" @change="filterReports" class="form-input">
        <span class="date-separator">至</span>
        <input type="date" v-model="endDate" @change="filterReports" class="form-input">
      </div>
      
      <div class="filter-actions">
        <button class="btn btn-reset" @click="resetFilters" :class="{ 'pulse': isResetting }">
          <i class="fa fa-refresh"></i> 重置筛选
        </button>
        <button class="btn btn-delete-all" @click="confirmDeleteAll" :disabled="filteredReports.length === 0">
          <i class="fa fa-trash"></i> 清空报告
        </button>
      </div>
    </div>

    <!-- 评价报告列表 -->
    <div class="history-list card">
      <div class="history-header">
        <div class="history-column theme-column">案件主题</div>
        <div class="history-column role-column">扮演角色</div>
        <div class="history-column date-column">日期时间</div>
        <div class="history-column score-column">综合评分</div>
        <div class="history-column action-column">操作</div>
      </div>

      <!-- 空状态 -->
      <div v-if="filteredReports.length === 0" class="empty-state">
        <div class="empty-icon">
          <i class="fa fa-folder-open-o"></i>
        </div>
        <p>暂无评价报告记录</p>
        <button class="btn btn-primary" @click="goToChat">
          <i class="fa fa-plus-circle"></i> 开始新的模拟
        </button>
      </div>

      <!-- 评价报告项 -->
      <div 
        v-for="report in filteredReports" 
        :key="report.id" 
        class="history-item"
        :class="{ 'highlight': hoveredRecordId === report.id }"
        @mouseenter="hoveredRecordId = report.id"
        @mouseleave="hoveredRecordId = null"
        transition="fade-in"
      >
        <div class="history-column theme-column">
          <div class="theme-text">{{ report.topic }}</div>
        </div>
        <div class="history-column role-column">
          <div class="role-badge" :class="roleBadgeClass(report.role)">{{ report.role }}</div>
        </div>
        <div class="history-column date-column">
          {{ formatDate(report.time) }}
        </div>
        <div class="history-column score-column">
          <div class="score-display">
            <span class="score-value">{{ report.total_score }}</span>
            <div class="star-rating">
              <i v-for="i in 5" :key="i" class="fa fa-star" :class="{ 'active': i <= Math.round(report.total_score/20) }"></i>
            </div>
          </div>
        </div>
        <div class="history-column action-column">
          <div class="action-buttons">
            <button class="btn btn-view" @click="viewReport(report.id)" title="查看详情">
              <i class="fa fa-eye"></i>
            </button>
            <button class="btn btn-evaluation" @click="viewEvaluation(report.id)" title="评价详情">
              <i class="fa fa-file-text-o">评价</i>
            </button>
            <button class="btn btn-delete" @click="confirmDelete(report.id)" title="删除">
              <i class="fa fa-trash-o">删除</i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 报告详情弹窗 -->
    <div v-if="showRecordDetail" class="modal-backdrop" @click="showRecordDetail = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">案件详情 - {{ currentReport.topic }}</h2>
          <button class="btn-close" @click="showRecordDetail = false">×</button>
        </div>
        
        <div class="modal-body">
          <div class="case-info-summary card">
            <div class="info-row">
              <span class="info-label">案件主题:</span>
              <span class="info-value">{{ currentReport.topic }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">扮演角色:</span>
              <span class="info-value role-badge" :class="roleBadgeClass(currentReport.role)">{{ currentReport.role }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">生成时间:</span>
              <span class="info-value">{{ formatDate(currentReport.time) }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">综合评分:</span>
              <span class="info-value">
                <span class="score-value">{{ currentReport.total_score }}</span>
                <div class="star-rating inline">
                  <i v-for="i in 5" :key="i" class="fa fa-star" :class="{ 'active': i <= Math.round(currentReport.total_score/20) }"></i>
                </div>
              </span>
            </div>
          </div>
          
          <div class="evaluation-section">
            <h3>对话摘要</h3>
            <p>{{ currentReport.summary }}</p>
          </div>
          
          <div class="evaluation-section">
            <h3>分项评分</h3>
            <div class="score-categories">
              <div class="score-category">
                <span class="category-name">法律专业性:</span>
                <div class="category-score">
                  <span>{{ currentReport.professional }}/100</span>
                  <div class="star-rating">
                    <i v-for="i in 5" :key="i" class="fa fa-star" :class="{ 'active': i <= Math.round(currentReport.professional/20) }"></i>
                  </div>
                </div>
              </div>
              <div class="score-category">
                <span class="category-name">逻辑清晰度:</span>
                <div class="category-score">
                  <span>{{ currentReport.logic }}/100</span>
                  <div class="star-rating">
                    <i v-for="i in 5" :key="i" class="fa fa-star" :class="{ 'active': i <= Math.round(currentReport.logic/20) }"></i>
                  </div>
                </div>
              </div>
              <div class="score-category">
                <span class="category-name">证据运用:</span>
                <div class="category-score">
                  <span>{{ currentReport.evidence }}/100</span>
                  <div class="star-rating">
                    <i v-for="i in 5" :key="i" class="fa fa-star" :class="{ 'active': i <= Math.round(currentReport.evidence/20) }"></i>
                  </div>
                </div>
              </div>
              <div class="score-category">
                <span class="category-name">表达流畅度:</span>
                <div class="category-score">
                  <span>{{ currentReport.expression }}/100</span>
                  <div class="star-rating">
                    <i v-for="i in 5" :key="i" class="fa fa-star" :class="{ 'active': i <= Math.round(currentReport.expression/20) }"></i>
                  </div>
                </div>
              </div>
              <div class="score-category">
                <span class="category-name">角色适应性:</span>
                <div class="category-score">
                  <span>{{ currentReport.adaptation }}/100</span>
                  <div class="star-rating">
                    <i v-for="i in 5" :key="i" class="fa fa-star" :class="{ 'active': i <= Math.round(currentReport.adaptation/20) }"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="evaluation-section">
            <h3>优点分析</h3>
            <ul v-if="currentReport.strengths.length > 0">
              <li v-for="(strength, index) in currentReport.strengths" :key="index">{{ strength }}</li>
            </ul>
            <p v-else>无</p>
          </div>
          
          <div class="evaluation-section">
            <h3>改进建议</h3>
            <ul v-if="currentReport.improvements.length > 0">
              <li v-for="(improvement, index) in currentReport.improvements" :key="index">{{ improvement }}</li>
            </ul>
            <p v-else>无</p>
          </div>
          
          <div class="evaluation-section">
            <h3>专业点评</h3>
            <p>{{ currentReport.comments }}</p>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showRecordDetail = false">关闭</button>
          <button class="btn btn-replay" @click="replayRecord(currentReport.case_id)">
            <i class="fa fa-repeat"></i> 重新模拟
          </button>
          <button class="btn btn-save" @click="saveEvaluation">
            <i class="fa fa-download"></i> 保存报告
          </button>
        </div>
      </div>
    </div>

    <!-- 确认删除弹窗 -->
    <div v-if="showDeleteConfirm" class="modal-backdrop" @click="showDeleteConfirm = false">
      <div class="modal-content confirm-modal" @click.stop>
        <h3 class="modal-title">确认删除</h3>
        <p>{{ deleteAll ? '确定要删除所有评价报告吗？此操作不可恢复。' : '确定要删除这份报告吗？此操作不可恢复。' }}</p>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showDeleteConfirm = false">取消</button>
          <button class="btn btn-danger" @click="executeDelete">
            <i class="fa fa-exclamation-triangle"></i> 确认删除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { API_BASE_URLS } from '../constants'
export default {
  name: "EvaluationHistory",
  data() {
    return {
      // 评价报告数据
      evaluationReports: [],
      filteredReports: [],
      
      // 筛选条件
      selectedType: "",
      selectedRole: "",
      startDate: "",
      endDate: "",
      
      // 动画状态
      isResetting: false,
      
      // 弹窗状态
      showRecordDetail: false,
      showDeleteConfirm: false,
      
      // 当前操作的报告
      currentReport: null,
      hoveredRecordId: null,
      deleteTargetId: null,
      deleteAll: false,
      
      // API端点 - 只保留评价报告相关
      EVALUATION_ENDPOINT: `${API_BASE_URLS.COURT}/api/evaluation`
    };
  },
  mounted() {
    // 加载评价报告记录
    this.loadEvaluationReports();
  },
  methods: {
    // 检查令牌有效性
    checkToken() {
      const token = localStorage.getItem('rbac_auth_token');
      if (!token) {
        this.$router.push('/login');
        alert("请先登录");
        return false;
      }
      return token;
    },
    
    // 加载评价报告记录
    async loadEvaluationReports() {
      try {
        const token = this.checkToken();
        if (!token) return;
        
        const response = await fetch(this.EVALUATION_ENDPOINT, {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });
        
        if (!response.ok) {
          if (response.status === 401) {
            // Token 无效或过期，清除旧 Token 并跳转登录
            localStorage.removeItem('token');
            this.$router.push('/login');
            alert("登录已过期，请重新登录");
            return;
          } else if (response.status === 403) {
            alert("您没有访问评价报告的权限");
          }
          throw new Error(`加载评价报告失败: ${response.status}`);
        }
        
        const data = await response.json();
        // 解析JSON字段
        this.evaluationReports = data.map(report => ({
          ...report,
          strengths: JSON.parse(report.strengths || '[]'),
          improvements: JSON.parse(report.improvements || '[]')
        }));
        
        this.filteredReports = [...this.evaluationReports];
      } catch (error) {
        console.error("加载评价报告出错:", error);
        alert("无法加载评价报告，请稍后重试");
      }
    },
    
    // 筛选评价报告
    filterReports() {
      this.filteredReports = this.evaluationReports.filter(report => {
        // 案件类型筛选
        if (this.selectedType && !report.topic.includes(this.selectedType)) {
          return false;
        }
        
        // 角色筛选
        if (this.selectedRole && report.role !== this.selectedRole) {
          return false;
        }
        
        // 日期筛选
        const reportDate = new Date(report.time).toISOString().split('T')[0];
        if (this.startDate && reportDate < this.startDate) {
          return false;
        }
        if (this.endDate && reportDate > this.endDate) {
          return false;
        }
        
        return true;
      });
    },
    
    // 重置筛选条件
    resetFilters() {
      // 添加重置动画效果
      this.isResetting = true;
      setTimeout(() => {
        this.selectedType = "";
        this.selectedRole = "";
        this.startDate = "";
        this.endDate = "";
        this.filteredReports = [...this.evaluationReports];
        this.isResetting = false;
      }, 300);
    },
    
    // 查看报告详情
    async viewReport(reportId) {
      try {
        const token = this.checkToken();
        if (!token) return;
        
        const response = await fetch(`${this.EVALUATION_ENDPOINT}/${reportId}`, {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });
        
        if (!response.ok) {
          throw new Error(`获取报告详情失败: ${response.status}`);
        }
        
        let report = await response.json();
        // 解析JSON字段
        report = {
          ...report,
          strengths: JSON.parse(report.strengths || '[]'),
          improvements: JSON.parse(report.improvements || '[]')
        };
        
        this.currentReport = report;
        this.showRecordDetail = true;
      } catch (error) {
        console.error("查看报告详情出错:", error);
        alert("无法加载报告详情，请稍后重试");
      }
    },
    
    // 查看评价报告（与查看详情合并）
    viewEvaluation(reportId) {
      this.viewReport(reportId);
    },
    
    // 保存评价报告
    saveEvaluation() {
      if (!this.currentReport) return;
      
      const report = `模拟法庭对话评价报告
=========================

案件主题: ${this.currentReport.topic}
用户角色: ${this.currentReport.role}
生成日期: ${new Date().toLocaleString()}

对话摘要:
${this.currentReport.summary}

综合评分: ${this.currentReport.total_score}/100

分项评分:
法律专业性: ${this.currentReport.professional}/100
逻辑清晰度: ${this.currentReport.logic}/100
证据运用: ${this.currentReport.evidence}/100
表达流畅度: ${this.currentReport.expression}/100
角色适应性: ${this.currentReport.adaptation}/100

优点分析:
${this.currentReport.strengths.length > 0 
  ? this.currentReport.strengths.map((s, i) => `${i+1}. ${s}`).join('\n')
  : "无"}

改进建议:
${this.currentReport.improvements.length > 0
  ? this.currentReport.improvements.map((i, idx) => `${idx+1}. ${i}`).join('\n')
  : "无"}

专业点评:
${this.currentReport.comments}
`;
      
      // 创建下载链接
      try {
        const blob = new Blob([report], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `模拟法庭评价报告_${this.currentReport.topic}_${new Date().getTime()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      } catch (error) {
        console.error("保存评价报告失败:", error);
        alert("无法保存评价报告，请稍后重试");
      }
    },
    
    // 重新模拟该案件
    replayRecord(caseId) {
      // 关闭详情弹窗
      this.showRecordDetail = false;
      // 跳转到聊天页面并传递案件ID
      this.$router.push({ name: 'Chat', params: { caseId: caseId } });
    },
    
    // 前往聊天页面
    goToChat() {
      this.$router.push({ name: 'Chat' });
    },
    
    // 确认删除单个报告
    confirmDelete(reportId) {
      this.deleteTargetId = reportId;
      this.deleteAll = false;
      this.showDeleteConfirm = true;
    },
    
    // 确认删除所有报告
    confirmDeleteAll() {
      this.deleteTargetId = null;
      this.deleteAll = true;
      this.showDeleteConfirm = true;
    },
    
    // 执行删除操作
    async executeDelete() {
      try {
        const token = this.checkToken();
        if (!token) return;
        
        if (this.deleteAll) {
          // 删除所有报告 - 注意：后端可能没有直接删除所有的接口，可能需要调整
          // 这里采用批量删除的方式
          const deletePromises = this.evaluationReports.map(report => 
            fetch(`${this.EVALUATION_ENDPOINT}/${report.id}`, {
              method: 'DELETE',
              headers: {
                "Authorization": `Bearer ${token}`
              }
            })
          );
          
          const responses = await Promise.all(deletePromises);
          const failed = responses.some(res => !res.ok);
          if (failed) {
            throw new Error("部分报告删除失败");
          }
        } else if (this.deleteTargetId) {
          // 删除单个报告
          const response = await fetch(`${this.EVALUATION_ENDPOINT}/${this.deleteTargetId}`, {
            method: 'DELETE',
            headers: {
              "Authorization": `Bearer ${token}`
            }
          });
          if (!response.ok) {
            throw new Error(`删除报告失败: ${response.status}`);
          }
        }
        
        // 刷新报告列表
        this.loadEvaluationReports();
        this.showDeleteConfirm = false;
        alert(this.deleteAll ? "所有评价报告已删除" : "报告已删除");
      } catch (error) {
        console.error("删除报告出错:", error);
        alert("删除报告失败，请稍后重试");
      }
    },
    
    // 格式化日期
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    // 角色标签样式
    roleBadgeClass(role) {
      switch (role) {
        case '法官':
          return 'badge-judge';
        case '原告律师':
          return 'badge-plaintiff';
        case '被告律师':
          return 'badge-defendant';
        default:
          return '';
      }
    }
  }
};
</script>
<style scoped>
/* 基础样式 */
.history-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-title {
  text-align: center;
  color: var(--color-primary);
  margin-bottom: 30px;
  font-size: 2rem;
}

/* 筛选区域样式 */
.filter-section {
  background-color: white;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: center;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-group label {
  color: #34495e;
  font-weight: 500;
}

.form-select, .form-input {
  padding: 8px 12px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-select:focus, .form-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.date-range {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-separator {
  color: #7f8c8d;
}

.filter-actions {
  margin-left: auto;
  display: flex;
  gap: 10px;
}

/* 列表样式 */
.history-list {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.history-header {
  display: flex;
  background-color: var(--color-primary-dark);
  color: white;
  font-weight: 600;
  padding: 15px 20px;
}

.history-column {
  flex: 1;
  padding: 0 10px;
}

.theme-column {
  flex: 0.4;
   max-width: 300px;
  /* 超出部分显示省略号 */
  overflow: hidden;
}

.role-column, .duration-column, .score-column, .action-column {
  flex: 0.4;
  text-align: center;
}

.date-column {
  flex: 0.4;
  text-align: center;
}

.history-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #ecf0f1;
  transition: background-color 0.2s;
}

.history-item:hover {
  background-color: var(--color-bg-red-light);
}

.history-item.highlight {
  background-color: var(--color-bg-red-light);
}

.theme-text {
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 5px;
  /* 强制文本单行显示 */
  white-space: nowrap;
  /* 超出部分显示省略号 */
  text-overflow: ellipsis;
  /* 确保内容不会溢出容器 */
  overflow: hidden;
  /* 增加内边距让文本显示更美观 */
  padding-right: 10px;
}

.case-parties {
  font-size: 13px;
  color: #7f8c8d;
  display: flex;
  gap: 10px;
}

.role-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  color: white;
}

.badge-judge {
  background-color: var(--color-gold);
  color: var(--color-text-primary);
}

.badge-plaintiff {
  background-color: #2ecc71;
}

.badge-defendant {
  background-color: var(--color-primary-light);
}

.score-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.score-value {
  font-weight: 600;
  color: #e67e22;
}

.star-rating {
  color: #bdc3c7;
}

.star-rating.inline {
  display: inline-block;
  margin-left: 10px;
}

.star-rating .active {
  color: #f39c12;
}

.action-buttons {
  display: flex;
  gap: 5px;
  justify-content: center;
}

/* 按钮样式 */
.btn {
  border: none;
  border-radius: 4px;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background-color: var(--color-primary-dark);
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.btn-danger {
  background-color: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background-color: #c0392b;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(231, 76, 60, 0.2);
}

.btn-view {
  background-color: var(--color-primary);
  color: white;
  padding: 8px 12px;
}

.btn-view:hover {
  background-color: var(--color-primary-dark);
}

.btn-evaluation {
  background-color: var(--color-gold);
  color: var(--color-text-primary);
  padding: 8px 12px;
}

.btn-evaluation:hover {
  background-color: var(--color-gold-light);
}

.btn-replay {
  background-color: #f39c12;
  color: white;
}

.btn-replay:hover {
  background-color: #d35400;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(243, 156, 18, 0.2);
}

.btn-save {
  background-color: #2ecc71;
  color: white;
}

.btn-save:hover {
  background-color: #27ae60;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(46, 204, 113, 0.2);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-reset {
  background-color: #f1c40f;
  color: #333;
}

.btn-reset:hover {
  background-color: #f39c12;
}

.btn-reset.pulse {
  animation: pulse 0.5s;
}

@keyframes pulse {
  0% { background-color: #f1c40f; }
  50% { background-color: #f39c12; }
  100% { background-color: #f1c40f; }
}

.btn-delete-all {
  background-color: #e74c3c;
  color: white;
}

.btn-delete-all:hover {
  background-color: #c0392b;
}

/* 空状态样式 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #8eb0b3;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 20px;
  color: #bdc3c7;
}

/* 弹窗样式 */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.confirm-modal {
  max-width: 500px;
  max-height: auto;
  overflow-y: visible;
}

.evaluation-modal {
  max-width: 800px;
}

.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #ecf0f1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  margin: 0;
  color: var(--color-primary);
  font-size: 1.5rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
  padding: 0 10px;
}

.btn-close:hover {
  color: var(--color-primary);
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #ecf0f1;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* 详情页样式 */
.case-info-summary {
  margin-bottom: 20px;
  padding: 15px;
  background-color: var(--color-bg-red-light);
  border-radius: 6px;
}

.info-row {
  margin-bottom: 10px;
  display: flex;
  flex-wrap: wrap;
}

.info-label {
  flex: 0 0 120px;
  font-weight: 500;
  color: #34495e;
}

.info-value {
  flex: 1;
  color: #2c3e50;
}

.conversation-history {
  margin-top: 20px;
}

.dialog-content {
  padding: 15px;
  background-color: var(--color-bg-red-light);
  border-radius: 6px;
  max-height: 400px;
  overflow-y: auto;
  margin-top: 10px;
}

.message {
  margin-bottom: 15px;
  max-width: 80%;
  padding: 10px 15px;
  border-radius: 8px;
  position: relative;
}

.message.user {
  background-color: #dcf8c6;
  margin-left: auto;
}

.message.system {
  background-color: var(--color-bg-red-light);
}

/* 评价报告样式 */
.evaluation-section {
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f1f1f1;
}

.evaluation-section:last-child {
  border-bottom: none;
}

.evaluation-section h3 {
  color: var(--color-primary);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 8px;
  margin-bottom: 15px;
  font-weight: 600;
}

.score {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.score-categories {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.score-category {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-name {
  font-weight: 500;
  color: #34495e;
}

.category-score {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>