<template>
  <div class="chat-page">
    <h1 class="page-title">{{ !showViewSelectionComplete ? "模拟法庭" : (viewToggle ? "2D" : "3D") + " 模拟法庭对话" }}</h1>
    <!-- 新增：视图选择页面 -->
    <div v-if="!showViewSelectionComplete" class="view-selection-section">
      <h2 class="selection-title">请选择视图模式</h2>
      <div class="view-options">
        <div class="view-option" @click="selectView(false)">
          <div class="view-icon d3-icon">
            <i class="fa fa-cube fa-4x"></i>
          </div>
          <h3>3D 视图</h3>
          <p>沉浸式三维法庭环境，更具真实感</p>
        </div>
        <div class="view-option" @click="selectView(true)">
          <div class="view-icon d2-icon">
            <i class="fa fa-square fa-4x"></i>
          </div>
          <h3>2D 视图</h3>
          <p>简洁平面布局，专注对话内容</p>
        </div>
      </div>
    </div>
    <!-- 初始阶段：提示先查看流程 -->
    <div v-if="showViewSelectionComplete && !showProcess && !showConversation" class="intro-section initial-stage">
      <h2 class="intro-text">点击下面按钮查看法庭流程说明，然后进入对话。</h2>
      <button class="btn btn-primary" @click="showProcess = true">
        显示流程
      </button>
    </div>
    <!-- 流程说明 -->
    <div v-if="showViewSelectionComplete && showProcess && !showConversation" class="process-section show-process">
      <h2>法庭流程说明</h2>
      <ol>
        <li>法官核对当事人身份并告知庭审规则</li>
        <li>原告及律师陈述起诉请求、事实和理由</li>
        <li>被告律师进行答辩</li>
        <li>双方进行举证、质证和辩论</li>
        <li>最后陈述、法官宣布休庭或判决</li>
      </ol>
      <button class="btn btn-success" @click="showConversation = true">
        进入对话
      </button>
    </div>
    <!-- 正式对话区域 -->
    <div v-if="showViewSelectionComplete && showConversation" class="conversation-section">
      <!-- 控制面板 -->
      <div class="control-panel">
        <div class="row">
          <!-- 案件选择下拉框 -->
          <select v-model="selectedCaseId" class="input-field" @change="loadSelectedCase">
            <option value="">选择已有案件</option>
            <option v-for="caseItem in savedCases" :value="caseItem.id" :key="caseItem.id">
              {{ caseItem.theme }} ({{ caseItem.createdAt }})
            </option>
          </select>
          
          <select v-model="userRole" class="input-field">
            <option value="法官">法官</option>
            <option value="原告律师">原告律师</option>
            <option value="被告律师">被告律师</option>
          </select>
          
          <!-- 打开案件信息弹窗的按钮 -->
          <button class="btn btn-case-info" @click="openCaseInfoModal">
            案件信息
          </button>
        </div>
        <div class="row">
          <button class="btn btn-start" @click="checkCaseInfoAndInit" :disabled="conversationRunning || !caseInfoComplete">
            开始对话
          </button>
          <button class="btn btn-stop" @click="stopConversation" :disabled="!conversationRunning">
            停止对话
          </button>
          <button class="btn btn-toggle" @click="toggleView">切换视图</button>
          <button class="btn btn-evaluate" @click="showEvaluation" :disabled="!isConversationCompleted">
            查看评价
          </button>
        </div>
      </div>
      <!-- 阶段说明 -->
      <div class="phase-indicator" :style="{ backgroundColor: phaseColor }">
        <strong>{{ currentPhase }}</strong>
      </div>
      <!-- 时间提醒 -->
      <div class="time-indicator">
        <strong>时间提醒: {{ currentTime }}</strong>
      </div>
      <!-- 3D 视图或 2D 视图 -->
      <div id="unity-container" v-if="!viewToggle" class="unity-container">
        <iframe
          id="unity-iframe"
          src="index.html"
          frameborder="0"
          allowfullscreen
        ></iframe>
        <!-- 3D视图对话框（投名状风格背景） -->
        <div class="chat-dialog-3d">
          <div class="scroll-decoration top"></div>
          <div class="dialog-content-3d" ref="messages">
            <div
              v-for="(message, index) in conversationHistory"
              :key="index"
              :class="['message', message.type]"
              v-html="message.content"
            ></div>
          </div>
          <div class="scroll-decoration bottom"></div>
        </div>
      </div>
      <div id="d2-container" v-if="viewToggle" class="unity-container">
        <!-- 2D视图实现 -->
        <div class="d2-dialog">
          <div class="dialog-content" ref="messages">
            <!-- 对话内容 -->
            <div
              v-for="(message, index) in conversationHistory"
              :key="index"
              :class="['message', message.type]"
              v-html="message.content"
            ></div>
          </div>
        </div>
        <div class="d2-roles">
          <div
            v-for="(role, index) in roles"
            :key="index"
            :class="['role', { active: roleSequence[currentMessage] === role }]"
          >
            <img :src="getImageForRole(role)" :alt="role" />
            <span>{{ role }}</span>
          </div>
        </div>
      </div>
      <!-- 用户输入框（仅在轮到用户时显示） -->
      <div v-if="isUserTurn" class="user-input">
        <input
          v-model="userMessage"
          type="text"
          placeholder="请输入你的发言"
          @keyup.enter="submitUserMessage()"
          :disabled="!conversationRunning"
        />
        <button class="btn btn-speech" @click="toggleSpeechInput" :disabled="!conversationRunning">
          {{ isRecordingSpeech ? '停止语音转文字输入' : '语音转文字输入' }}
        </button>
        <button class="btn btn-direct-speech" @click="toggleDirectSpeechInput" :disabled="!conversationRunning">
          {{ isRecordingDirectSpeech ? '停止直接语音输入' : '直接语音输入' }}
        </button>
        <button class="btn btn-send" @click="submitUserMessage" :disabled="!conversationRunning || !userMessage.trim()">
          发送
        </button>
      </div>
      <div class="remaining-turns" v-if="false">
        剩余对话总数：{{ totalMessages - currentMessage }}
      </div>
    </div>
    <!-- 评价报告模态框 -->
    <div v-if="showEvaluationModal" class="evaluation-modal">
      <div class="modal-content">
        <h2 class="modal-title">模拟法庭对话评价报告</h2>
        
        <!-- 加载状态 -->
        <div v-if="isEvaluating" class="loading-state">
          <div class="spinner"></div>
          <p>正在生成评价报告，请稍候...</p>
        </div>
        
        <!-- 错误状态 -->
        <div v-if="evaluationError && !isEvaluating" class="error-state">
          <i class="fa fa-exclamation-circle"></i>
          <p>{{ evaluationError }}</p>
          <button class="btn btn-retry" @click="generateEvaluation()">重试</button>
        </div>
        
        <!-- 评价内容 -->
        <div v-if="!isEvaluating && !evaluationError" class="modal-body">
          <div class="evaluation-section">
            <h3>对话主要内容</h3>
            <p>{{ evaluation.summary }}</p>
          </div>
          
          <div class="evaluation-section">
            <h3>综合评分</h3>
            <div class="score">
              <span class="score-value">{{ evaluation.overallScore }}/100</span>
              <div class="star-rating">
                <i v-for="i in 5" :key="i" class="fa fa-star" :class="{ 'active': i <= Math.round(evaluation.overallScore/20) }"></i>
              </div>
            </div>
          </div>
          
          <div class="evaluation-section">
            <h3>分项评分</h3>
            <div class="score-categories">
              <div class="score-category" v-for="(score, category) in evaluation.categoryScores" :key="category">
                <span class="category-name">{{ category }}</span>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: score + '%' }"></div>
                </div>
                <span class="category-score">{{ score }}/100</span>
              </div>
            </div>
          </div>
          
          <div class="evaluation-section">
            <h3>优点分析</h3>
            <ul>
              <li v-for="(point, index) in evaluation.strengths" :key="index">{{ point }}</li>
              <li v-if="evaluation.strengths.length === 0">暂无优点分析</li>
            </ul>
          </div>
          
          <div class="evaluation-section">
            <h3>改进建议</h3>
            <ul>
              <li v-for="(point, index) in evaluation.improvements" :key="index">{{ point }}</li>
              <li v-if="evaluation.improvements.length === 0">暂无改进建议</li>
            </ul>
          </div>
          
          <div class="evaluation-section">
            <h3>专业点评</h3>
            <p>{{ evaluation.professionalComment }}</p>
          </div>
        </div>
        
        <div v-if="!isEvaluating && !evaluationError" class="modal-footer">
          <button class="btn btn-close" @click="showEvaluationModal = false">关闭</button>
          <button class="btn btn-save" @click="saveEvaluation">保存报告</button>
        </div>
      </div>
    </div>
    <!-- 案件信息弹窗 -->
    <div v-if="showCaseInfoModal" class="case-info-modal">
      <div class="modal-content case-info-content">
        <h2 class="modal-title">案件信息</h2>
        
        <div class="case-form">
          <div class="form-group">
            <label>案件类型</label>
            <input
              v-model="caseInfo.theme"
              type="text"
              placeholder="如：合同纠纷案、侵权责任案、婚姻家庭案、劳动纠纷案、其他等"
            />
          </div>
          
          <div class="form-section">
            <h3>原告信息</h3>
            <div class="form-group">
              <input
                v-model="caseInfo.plaintiff.name"
                type="text"
                placeholder="原告相关信息"
              />
            </div>
          </div>
          
          <div class="form-section">
            <h3>被告信息</h3>
            <div class="form-group">
              <input
                v-model="caseInfo.defendant.name"
                type="text"
                placeholder="被告相关信息"
              />
            </div>
          </div>
          
          <div class="form-section">
            <h3>案件详情</h3>
            <div class="form-group">
              <label>案件事实与经过</label>
              <textarea
                v-model="caseInfo.details"
                rows="4"
                placeholder="详细描述案件的发生时间、地点、经过等关键信息"
              ></textarea>
            </div>
            
            <div class="form-group">
              <label>证据材料</label>
              <textarea
                v-model="caseInfo.evidence"
                rows="3"
                placeholder="列举相关证据，如合同、照片、录音、证人等"
              ></textarea>
            </div>
            
            <div class="form-group">
              <label>诉讼请求</label>
              <textarea
                v-model="caseInfo.claims"
                rows="3"
                placeholder="原告的具体诉求，如赔偿金额、道歉、履行合同等"
              ></textarea>
            </div>
          </div>
          
          <div class="modal-footer">
            <button class="btn btn-close" @click="showCaseInfoModal = false">取消</button>
            <button class="btn btn-save" @click="saveCaseInfo">保存案件</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { API_BASE_URLS } from '../constants'

export default {
  name: "Chat",
  data() {
    return {
      showViewSelectionComplete: false, // 新增：是否已完成视图选择
      showProcess: false, // 是否显示流程介绍
      showConversation: false, // 是否进入正式对话
      API_ENDPOINT: `${API_BASE_URLS.MAIN}/api/chat`,
      EVALUATION_ENDPOINT: `${API_BASE_URLS.MAIN}/evaluate`,
      NEXT_SPEAKER_ENDPOINT: `${API_BASE_URLS.MAIN}/api/determine-next-speaker`,
      // 新增：对话记录保存接口（对应case_model.py的/api/dialogues）
      SAVE_DIALOGUE_ENDPOINT: `${API_BASE_URLS.CASE}/api/dialogues`,
      
      roles: ["法官", "原告律师", "被告律师"],
      userRole: "法官",
      conversationRunning: false,
      conversationHistory: [],
      userMessage: "",
      roleSequence: [], // 动态生成的角色顺序
      totalMessages: 0,
      currentMessage: 0, // 当前发言序号
      currentRound: 0, // 当前回合数
      recognitionSpeech: null,
      recognitionDirectSpeech: null,
      currentPhase: "初始阶段",
      phaseColor: "#ddd",
      viewToggle: false, // false表示3D视图，true表示2D视图
      timer: null,
      currentTime: "00:00",
      isRecordingSpeech: false, // 语音转文字状态
      isRecordingDirectSpeech: false, // 直接语音输入状态
      showEvaluationModal: false, // 评价模态框显示状态
      isEvaluating: false,  // 是否正在生成评价
      evaluationError: "",  // 评价错误信息
      evaluation: {
        summary: "",
        overallScore: 0,
        categoryScores: {
          "法律专业性": 0,
          "逻辑清晰度": 0,
          "证据运用": 0,
          "表达流畅度": 0,
          "角色适应性": 0
        },
        strengths: [],
        improvements: [],
        professionalComment: ""
      },
      // 案件信息相关
      showCaseInfoModal: false, // 案件信息弹窗显示状态
      caseInfo: {
        id: this.generateCaseId(),
        theme: "",
        plaintiff: {
          name: "",
          contact: "",
          address: ""
        },
        defendant: {
          name: "",
          contact: "",
          address: ""
        },
        details: "",
        evidence: "",
        claims: "",
        createdAt: ""
      },
      savedCases: [], // 保存的案件列表
      selectedCaseId: "" // 当前选择的案件ID
    };
  },
  computed: {
    // 是否轮到用户说话
    isUserTurn() {
      if (
        !this.conversationRunning ||
        this.currentMessage >= this.totalMessages ||
        this.isConversationCompleted
      ) {
        return false;
      }
      const currentRole = this.roleSequence[this.currentMessage];
      return currentRole === this.userRole;
    },
    // 提取用户的发言
    userContributions() {
      return this.conversationHistory
        .filter(msg => msg.type === 'user')
        .map(msg => msg.content);
    },
    // 检查是否已结束对话（正常结束、强制停止或闭庭）
    isConversationCompleted() {
      return !this.conversationRunning && this.conversationHistory.length > 0;
    },
    // 检查案件信息是否完整
    caseInfoComplete() {
      return this.caseInfo.theme && 
             this.caseInfo.plaintiff.name && 
             this.caseInfo.defendant.name && 
             this.caseInfo.details && 
             this.caseInfo.claims;
    }
  },
  methods: {
    // 新增：选择视图模式
    selectView(is2D) {
      this.viewToggle = is2D;
      // 添加选择动画效果
      const selectedOption = document.querySelector(`.view-option:nth-child(${is2D ? 2 : 1})`);
      selectedOption.classList.add('selected');
      
      // 短暂延迟后进入下一步
      setTimeout(() => {
        this.showViewSelectionComplete = true;
      }, 800);
    },
    
    // 初始化对话前检查案件信息
    checkCaseInfoAndInit() {
      if (!this.caseInfoComplete) {
        this.openCaseInfoModal();
        alert("请完善案件基本信息后再开始对话");
        return;
      }
      this.initConversation();
    },
    
    // 初始化对话，生成角色顺序并开始
    initConversation() {
      this.conversationRunning = true;
      this.currentRound = 0;
      // 初始化角色序列，从法官开场开始
      this.roleSequence = ["法官"];
      this.totalMessages = 1; // 初始只有法官开场
      
      this.currentMessage = 0;
      this.conversationHistory = [];
      this.addSystemMessage(
        `
        <strong>法庭流程开始：</strong><br>
        案件类型：${this.caseInfo.theme}<br>
        原告：${this.caseInfo.plaintiff.name}<br>
        被告：${this.caseInfo.defendant.name}<br>
        （以下开始模拟法庭多方对话，请注意区分角色。当法官宣布"闭庭"或"休庭"时，模拟将自动结束。）
      `,
        true
      );
      // 自动点击开庭（等待 Unity 加载完毕后发送消息）
      this.openCourt();
      this.nextTurn();
      this.startTimer();
    },
    // 自动点击开庭，等待 Unity 实例加载后发送消息
    openCourt() {
      const iframe = document.getElementById("unity-iframe");
      if (!iframe) return;
      
      const sendStart = () => {
        // 发送开庭消息
        iframe.contentWindow.postMessage(
          JSON.stringify({
            type: "startCourt",
          }),
          "*"
        );
      };
      const checkUnityReady = () => {
        // 检查 iframe 内是否已经加载了 unityInstance
        try {
          if (
            iframe.contentWindow &&
            iframe.contentWindow.window &&
            iframe.contentWindow.window.unityInstance &&
            typeof iframe.contentWindow.window.unityInstance.SendMessage ===
              "function"
          ) {
            sendStart();
          } else {
            setTimeout(checkUnityReady, 500);
          }
        } catch (err) {
          setTimeout(checkUnityReady, 500);
        }
      };
      checkUnityReady();
    },
    // 进入下一次发言
    nextTurn() {
      if (!this.conversationRunning || this.isConversationCompleted) {
        return;
      }
      
      if (this.currentMessage >= this.totalMessages) {
        // 如果没有更多发言安排，但对话仍在进行，则添加法官发言
        this.roleSequence.push("法官");
        this.totalMessages++;
      }
      const currentRole = this.roleSequence[this.currentMessage];
      // 系统提示当前发言角色
      this.addSystemMessage(`<em>当前发言角色：${currentRole}</em>`, true);
      // 更新阶段信息
      if (currentRole === "法官") {
        this.currentPhase = "法官发言";
        this.phaseColor = "#f5deb3";
      } else if (currentRole === "原告律师") {
        this.currentPhase = "原告律师发言";
        this.phaseColor = "#add8e6";
      } else if (currentRole === "被告律师") {
        this.currentPhase = "被告律师发言";
        this.phaseColor = "#e6e6fa";
      }
      // 切换到实际发言摄像头
      const iframe = document.getElementById("unity-iframe");
      if (iframe) {
        iframe.contentWindow.postMessage(
          JSON.stringify({
            type: "switchCamera",
            role: currentRole,
            isSystem: false,
          }),
          "*"
        );
      }
      // 播放对应角色的语音
      this.playAudio(currentRole);
      // 调用3D模型的动作
      this.trigger3DModelAction(currentRole);
      // 若为用户回合，则等待输入，否则 AI 自动发言
      if (currentRole === this.userRole) {
        return;
      } else {
        this.streamAIResponse(currentRole);
      }
    },
    // 播放对应角色的语音
    playAudio(role) {
      try {
        const audio = new Audio(`/audio/${role}.mp3`); // 假设音频文件名为角色名.mp3
        audio.play().catch((error) => {
          console.error(`音频播放失败: ${error}`);
        });
      } catch (error) {
        console.error(`播放音频时出错: ${error}`);
      }
    },
    // 调用3D模型的动作
    trigger3DModelAction(role) {
      const iframe = document.getElementById("unity-iframe");
      if (iframe) {
        iframe.contentWindow.postMessage(
          JSON.stringify({
            type: "triggerAction",
            role: role,
          }),
          "*"
        );
      }
    },
    // 停止对话
    stopConversation() {
      if (!this.conversationRunning) return;
      
      this.conversationRunning = false;
      this.addSystemMessage("<strong>对话已强制停止</strong>");
      this.stopTimer();
      this.stopSpeechInput();
      this.stopDirectSpeechInput();
    },

    // -------------------------- 核心修改1：用户发言保存到数据库 --------------------------
    // 用户提交发言
    submitUserMessage() {
      const message = this.userMessage.trim();
      if (!message || !this.conversationRunning || this.isConversationCompleted) return;
      
      // 1. 添加用户发言到本地对话历史
      this.conversationHistory.push({
        role: this.userRole,
        content: message,
        type: "user",
      });
      this.userMessage = "";
      
      // 2. 调用方法保存用户发言到数据库（核心新增）
      this.saveDialogueToDatabase(this.userRole, message);
      
      // 3. 原有逻辑：检查是否闭庭
      if (this.userRole === "法官" && this.checkForClosingStatement(message)) {
        this.handleCourtClosing();
        return;
      }
      
      // 4. 原有逻辑：处理发言后流程
      this.handleAfterSpeech(this.userRole);
      this.currentMessage++;
      this.nextTurn();
    },
    
    // -------------------------- 核心修改2：新增对话记录保存方法 --------------------------
    // 保存对话记录到数据库（对接case_model.py的/api/dialogues接口）
    async saveDialogueToDatabase(speaker, content) {
      // 校验必要条件：案件ID必须存在
      if (!this.caseInfo.id || !this.caseInfo.theme) {
        console.error("保存对话失败：案件ID或案件类型不存在");
        return;
      }
      
      try {
        // 1. 获取用户登录令牌（与案件保存、评价生成共用令牌）
        const token = localStorage.getItem('rbac_auth_token');
        
        // 2. 构造请求参数（严格匹配case_model.py的DialogueCreate模型）
        const dialogueData = {
          content: content,          // 发言内容
          speaker: speaker,          // 发言人（法官/原告律师/被告律师）
          case_type: this.caseInfo.theme, // 案件类型
          case_id: this.caseInfo.id  // 关联的案件ID
        };
        
        // 3. 调用后端接口保存对话
        const response = await fetch(this.SAVE_DIALOGUE_ENDPOINT, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": token ? `Bearer ${token}` : "" // 携带权限令牌
          },
          body: JSON.stringify(dialogueData)
        });
        
        // 4. 处理响应
        if (!response.ok) {
          const errorMsg = await response.text();
          throw new Error(`接口返回错误: ${response.status} - ${errorMsg}`);
        }
        
        const result = await response.json();
        console.log(`对话记录保存成功（${speaker}）:`, result);
      } catch (error) {
        // 错误不阻断用户操作，仅打印日志
        console.error(`保存对话记录失败（${speaker}）:`, error.message);
      }
    },
    
    // 检查法官发言中是否包含闭庭关键词
    checkForClosingStatement(content) {
      const closingKeywords = ["闭庭", "庭审结束", "现在闭庭", "法庭结束"];
      const contentLower = content.toLowerCase();
      return closingKeywords.some(keyword => contentLower.includes(keyword.toLowerCase()));
    },
    
    // 处理法庭闭庭逻辑
    handleCourtClosing() {
      this.addSystemMessage("<strong>法官已宣布闭庭，模拟法庭结束。</strong>");
      this.conversationRunning = false;
      this.stopTimer();
      this.stopSpeechInput();
      this.stopDirectSpeechInput();
    },
    
    // 处理发言后的逻辑，确定下一个发言人
    async handleAfterSpeech(role) {
      // 如果是法官发言，需要确定下一个发言人
      if (role === "法官") {
        // 获取法官最后的发言内容
        const judgeLastMessage = this.conversationHistory
          .filter(msg => msg.role === "法官" && msg.content)
          .pop()?.content || "";
          
        // 确定下一个发言人
        let nextSpeaker;
        try {
          // 调用API获取下一个发言人
          nextSpeaker = await this.determineNextSpeaker(judgeLastMessage);
        } catch (error) {
          console.error("获取下一个发言人失败，使用默认值", error);
          // 如果API调用失败，默认交替发言
          nextSpeaker = this.currentRound % 2 === 0 ? "原告律师" : "被告律师";
        }
        
        // 添加下一个发言人
        this.roleSequence.push(nextSpeaker);
        this.totalMessages++;
      } 
      // 如果是原告或被告发言，下一个一定是法官
      else if (["原告律师", "被告律师"].includes(role)) {
        this.roleSequence.push("法官");
        this.totalMessages++;
        this.currentRound++;
      }
    },
    
    // 调用API确定下一个发言人
    async determineNextSpeaker(judgeMessage) {
      try {
        const response = await fetch(this.NEXT_SPEAKER_ENDPOINT, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: judgeMessage,
            theme: this.caseInfo.theme,
            history: this.conversationHistory,
            caseInfo: this.caseInfo
          }),
        });
        
        if (!response.ok) {
          throw new Error(`API请求失败: ${response.status}`);
        }
        
        const result = await response.json();
        // 确保返回的是有效的角色
        if (["原告律师", "被告律师"].includes(result.nextSpeaker)) {
          return result.nextSpeaker;
        } else {
          throw new Error("无效的发言人");
        }
      } catch (error) {
        console.error("确定下一个发言人时出错:", error);
        throw error;
      }
    },

    // -------------------------- 核心修改3：AI发言保存到数据库 --------------------------
    // AI 流式响应
    async streamAIResponse(role) {
      if (!this.conversationRunning || this.isConversationCompleted) return;
      
      // 1. 初始化AI流式消息
      const streamingMessage = {
        role: role,
        content: "",
        type: "streaming",
        streaming: true,
      };
      this.conversationHistory.push(streamingMessage);
      
      try {
        // 2. 调用AI接口获取响应
        const response = await fetch(this.API_ENDPOINT, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            role,
            theme: this.caseInfo.theme,
            history: this.conversationHistory,
            caseInfo: this.caseInfo
          }),
        });
        
        if (!response.ok) {
          throw new Error(`API请求失败: ${response.status}`);
        }
        
        // 3. 处理AI流式响应
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullAIContent = ""; // 存储完整AI响应内容
        
        while (true) {
          if (!this.conversationRunning || this.isConversationCompleted) break;
          
          const { done, value } = await reader.read();
          if (done) {
            streamingMessage.streaming = false;
            break;
          }
          
          const chunk = decoder.decode(value);
          const lines = chunk.split("\n");
          lines.forEach((line) => {
            if (line.startsWith("data:")) {
              const data = line.replace(/^data: /, "");
              if (data === "[DONE]") return;
              try {
                const parsed = JSON.parse(data);
                if (parsed.content) {
                  streamingMessage.content += parsed.content;
                  fullAIContent += parsed.content; // 累加完整内容
                }
              } catch (e) {
                console.error("解析错误:", e);
              }
            }
          });
        }
        
        // 4. AI响应完成后，保存到数据库（核心新增）
        if (fullAIContent.trim()) {
          this.saveDialogueToDatabase(role, fullAIContent);
        }
        
      } catch (error) {
        console.error("请求失败:", error);
        streamingMessage.content += "<em>（系统错误，请重试）</em>";
        this.stopConversation();
      }
      
      // 5. 原有逻辑：处理AI发言后流程
      if (this.conversationRunning && !this.isConversationCompleted) {
        if (role === "法官" && this.checkForClosingStatement(streamingMessage.content)) {
          this.handleCourtClosing();
          return;
        }
        
        await this.handleAfterSpeech(role);
        this.currentMessage++;
        this.nextTurn();
      }
    },
    
    // 添加系统消息
    addSystemMessage(content, isSystem = false) {
      this.conversationHistory.push({
        role: "系统",
        content,
        type: "system",
      });
      this.scrollToBottom();
    },
    // 滚动到对话底部
    scrollToBottom() {
      this.$nextTick(() => {
        if (this.$refs.messages) {
          this.$refs.messages.scrollTop = this.$refs.messages.scrollHeight;
        }
      });
    },
    // 切换语音转文字输入
    toggleSpeechInput() {
      if (this.isRecordingSpeech) {
        this.stopSpeechInput();
      } else {
        this.startSpeechInput();
      }
    },
    // 开始语音转文字输入
    startSpeechInput() {
      let SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert("抱歉，当前浏览器不支持语音输入功能。");
        return;
      }
      this.recognitionSpeech = new SpeechRecognition();
      this.recognitionSpeech.continuous = false;
      this.recognitionSpeech.interimResults = false;
      this.recognitionSpeech.lang = "zh-CN";
      this.recognitionSpeech.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        this.userMessage = transcript;
        this.recognitionSpeech.stop();
        this.isRecordingSpeech = false;
      };
      this.recognitionSpeech.onend = () => {
        this.recognitionSpeech = null;
        this.isRecordingSpeech = false;
      };
      this.recognitionSpeech.onerror = (event) => {
        console.error("语音识别错误:", event.error, event.message);
        switch (event.error) {
          case "no-speech":
            alert("没有检测到语音输入，请再试一次。");
            break;
          case "not-allowed":
          case "service-not-allowed":
            alert("语音识别服务被禁止或未启用。");
            break;
          case "bad-grammar":
            alert("语法错误。");
            break;
          case "audio-capture":
            alert("音频设备无法访问。");
            break;
          default:
            alert("语音识别时发生错误，请稍后再试。");
        }
        this.recognitionSpeech = null;
        this.isRecordingSpeech = false;
      };
      this.recognitionSpeech.start();
      this.isRecordingSpeech = true;
    },
    // 停止语音转文字输入
    stopSpeechInput() {
      if (this.recognitionSpeech) {
        this.recognitionSpeech.stop();
        this.recognitionSpeech = null;
      }
      this.isRecordingSpeech = false;
    },
    // 切换直接语音输入
    toggleDirectSpeechInput() {
      if (this.isRecordingDirectSpeech) {
        this.stopDirectSpeechInput();
      } else {
        this.startDirectSpeechInput();
      }
    },
    // 开始直接语音输入
    startDirectSpeechInput() {
      let SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert("抱歉，当前浏览器不支持语音输入功能。");
        return;
      }
      this.recognitionDirectSpeech = new SpeechRecognition();
      this.recognitionDirectSpeech.continuous = true;
      this.recognitionDirectSpeech.interimResults = true;
      this.recognitionDirectSpeech.lang = "zh-CN";
      this.recognitionDirectSpeech.onresult = (event) => {
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            this.userMessage = event.results[i][0].transcript;
            this.recognitionDirectSpeech.stop();
            this.isRecordingDirectSpeech = false;
            this.submitUserMessage();
          } else {
            this.userMessage = event.results[i][0].transcript;
          }
        }
      };
      this.recognitionDirectSpeech.onend = () => {
        this.recognitionDirectSpeech = null;
        this.isRecordingDirectSpeech = false;
      };
      this.recognitionDirectSpeech.onerror = (event) => {
        console.error("语音识别错误:", event.error, event.message);
        switch (event.error) {
          case "no-speech":
            alert("没有检测到语音输入，请再试一次。");
            break;
          case "not-allowed":
          case "service-not-allowed":
            alert("语音识别服务被禁止或未启用。");
            break;
          case "bad-grammar":
            alert("语法错误。");
            break;
          case "audio-capture":
            alert("音频设备无法访问。");
            break;
          default:
            alert("语音识别时发生错误，请稍后再试。");
        }
        this.recognitionDirectSpeech = null;
        this.isRecordingDirectSpeech = false;
      };
      this.recognitionDirectSpeech.start();
      this.isRecordingDirectSpeech = true;
    },
    // 停止直接语音输入
    stopDirectSpeechInput() {
      if (this.recognitionDirectSpeech) {
        this.recognitionDirectSpeech.stop();
        this.recognitionDirectSpeech = null;
      }
      this.isRecordingDirectSpeech = false;
    },
    // 切换视图
    toggleView() {
      this.viewToggle = !this.viewToggle;
    },
    // 开始计时器
    startTimer() {
      const startTime = Date.now();
      this.timer = setInterval(() => {
        const elapsedTime = Date.now() - startTime;
        const minutes = Math.floor((elapsedTime / (1000 * 60)) % 60);
        const seconds = Math.floor((elapsedTime / 1000) % 60);
        this.currentTime = `${minutes.toString().padStart(2, "0")}:${seconds
          .toString()
          .padStart(2, "0")}`;
      }, 1000);
    },
    // 停止计时器
    stopTimer() {
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
    },
    // 根据角色获取对应的图像
    getImageForRole(role) {
      return `/images/${role}.png`;
    },
    generateCaseId() {
      return 'case_' + Date.now() + '_' + Math.floor(Math.random() * 10000);
    },
    // 生成评价报告 - 调用后端API获取专业评价
    async generateEvaluation() {
      this.isEvaluating = true;
      this.evaluationError = null;
      this.showEvaluationModal = true; // 无论成功失败都显示弹窗
      try {
        // 获取JWT令牌（假设已存储在localStorage中）
        const token = localStorage.getItem('rbac_auth_token');
        
        const response = await fetch(this.EVALUATION_ENDPOINT, {
          method: "POST",
          headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify({
            theme: this.caseInfo.theme,
            userRole: this.userRole,
            conversationHistory: this.conversationHistory,
            userContributions: this.userContributions,
            caseInfo: this.caseInfo,
            case_id: this.caseInfo.id
          }),
        });
        
        if (!response.ok) {
          throw new Error(`服务器错误：${response.status} ${response.statusText}`);
        }
        
        const text = await response.text();
        try {
          const evaluationData = JSON.parse(text);
          this.evaluation = { ...this.evaluation, ...evaluationData };
        } catch (jsonError) {
          console.error("解析评价JSON失败:", jsonError, "响应内容:", text);
          throw new Error("评价数据格式错误，无法解析");
        }
      } catch (error) {
        console.error("生成评价失败:", error);
        this.evaluationError = `生成评价失败: ${error.message}`;
      } finally {
        this.isEvaluating = false;
      }
    },
    
    // 保存评价报告到数据库
    async saveEvaluationToDatabase(evaluationData) {
      try {
        const token = localStorage.getItem('rbac_auth_token');
        
        // 转换评价数据以匹配后端模型
        const reportData = {
          case_id: this.caseInfo.id,
          topic: this.caseInfo.theme,
          role: this.userRole,
          time: new Date().toISOString(),
          summary: evaluationData.summary,
          professional: evaluationData.categoryScores["法律专业性"],
          logic: evaluationData.categoryScores["逻辑清晰度"],
          evidence: evaluationData.categoryScores["证据运用"],
          expression: evaluationData.categoryScores["表达流畅度"],
          adaptation: evaluationData.categoryScores["角色适应性"],
          total_score: evaluationData.overallScore,
          strengths: JSON.stringify(evaluationData.strengths),
          improvements: JSON.stringify(evaluationData.improvements),
          comments: evaluationData.professionalComment
        };
        
        const response = await fetch(this.EVALUATION_ENDPOINT, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(reportData)
        });
        
        if (!response.ok) {
          throw new Error(`保存评价报告失败: ${response.status}`);
        }
        
        const savedReport = await response.json();
        console.log("评价报告已保存到数据库:", savedReport);
        
        // 将报告ID关联到案件信息
        this.caseInfo.evaluationId = savedReport.id;
        this.saveCaseInfo(); // 更新案件信息
        
        return savedReport;
      } catch (error) {
        console.error("保存评价到数据库失败:", error);
        // 不阻断用户操作，仅记录错误
      }
    },
    
    // 显示评价报告
    showEvaluation() {
      // 检查对话历史是否为空
      if (this.conversationHistory.length === 0) {
        alert("请先进行对话再查看评价");
        return;
      }
      
      // 检查对话是否已结束
      if (this.conversationRunning) {
        alert("请先结束对话再查看评价");
        return;
      }
      
      this.generateEvaluation();
    },
    
    // 保存评价报告
    saveEvaluation() {
      // 创建评价报告文本
      const report = `模拟法庭对话评价报告
=========================
案件类型: ${this.caseInfo.theme}
用户角色: ${this.userRole}
原告: ${this.caseInfo.plaintiff.name}
被告: ${this.caseInfo.defendant.name}
生成日期: ${new Date().toLocaleString()}
对话摘要:
${this.evaluation.summary}
综合评分: ${this.evaluation.overallScore}/100
分项评分:
${Object.entries(this.evaluation.categoryScores)
  .map(([category, score]) => `${category}: ${score}/100`)
  .join('\n')}
优点分析:
${this.evaluation.strengths.length > 0 
  ? this.evaluation.strengths.map((s, i) => `${i+1}. ${s}`).join('\n')
  : "无"}
改进建议:
${this.evaluation.improvements.length > 0
  ? this.evaluation.improvements.map((i, idx) => `${idx+1}. ${i}`).join('\n')
  : "无"}
专业点评:
${this.evaluation.professionalComment}
`;
      
      // 创建下载链接
      try {
        const blob = new Blob([report], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `法庭对话评价_${this.caseInfo.theme}_${new Date().toISOString().slice(0,10)}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      } catch (error) {
        console.error("保存报告失败:", error);
        alert("无法保存报告，请手动复制。");
      }
    },
    
    // 打开案件信息弹窗
    openCaseInfoModal() {
      this.showCaseInfoModal = true;
    },
    
    // 保存案件信息
    async saveCaseInfo() {
      // 生成唯一ID和创建时间
      if (!this.caseInfo.id) {
        this.caseInfo.id = this.generateCaseId();
        this.caseInfo.createdAt = new Date().toISOString();
      }
      // 准备提交给后端的数据（增加基础校验）
      const caseData = {
        id: this.caseInfo.id,
        theme: this.caseInfo.theme || "", // 确保必填字段有默认值
        plaintiff: this.caseInfo.plaintiff || {},
        defendant: this.caseInfo.defendant || {},
        details: this.caseInfo.details || "",
        evidence: this.caseInfo.evidence || [],
        claims: this.caseInfo.claims || [],
        created_at: this.caseInfo.createdAt
      };
      try {
        const token = localStorage.getItem('rbac_auth_token');
        const response = await fetch("http://localhost:8004/api/cases", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": token ? `Bearer ${token}` : ""
          },
          body: JSON.stringify(caseData)
        });
        // 解析后端响应
        let responseData;
        try {
          responseData = await response.json();
        } catch (e) {
          responseData = { message: "后端返回非JSON格式响应" };
        }
        if (!response.ok) {
          throw new Error(
            `保存失败: ${responseData.detail || responseData.message || response.statusText}`
          );
        }
        // 成功逻辑
        console.log("数据库保存成功:", responseData);
        this.updateLocalStorage(caseData);
        alert('案件信息已保存（本地+数据库）');
        this.showCaseInfoModal = false;
      } catch (error) {
        console.error("完整错误信息:", error);
        alert(`保存失败: ${error.message}\n仍将保存到本地，但未同步到数据库`);
        this.updateLocalStorage(caseData);
        this.showCaseInfoModal = false;
      }
    },
    
    // 提取本地存储逻辑为独立方法
    updateLocalStorage(caseToSave) {
      const existingIndex = this.savedCases.findIndex(c => c.id === caseToSave.id);
      if (existingIndex >= 0) {
        this.savedCases.splice(existingIndex, 1, caseToSave);
      } else {
        this.savedCases.push(caseToSave);
      }
      localStorage.setItem('courtSimulationCases', JSON.stringify(this.savedCases));
      this.selectedCaseId = caseToSave.id;
    },
    
    // 加载选中的案件
    loadSelectedCase() {
      if (!this.selectedCaseId) {
        return;
      }
      
      const selectedCase = this.savedCases.find(c => c.id === this.selectedCaseId);
      if (selectedCase) {
        this.caseInfo = JSON.parse(JSON.stringify(selectedCase));
      }
    }
  },
  mounted() {
    // 从localStorage加载保存的案件
    const savedCasesStr = localStorage.getItem('courtSimulationCases');
    if (savedCasesStr) {
      try {
        this.savedCases = JSON.parse(savedCasesStr);
      } catch (e) {
        console.error('加载保存的案件失败', e);
        this.savedCases = [];
      }
    }
  },
  beforeDestroy() {
    // 组件销毁前清理资源
    this.stopTimer();
    this.stopSpeechInput();
    this.stopDirectSpeechInput();
  }
};
</script>

<style scoped>
.chat-page {
  padding: 20px;
  background: linear-gradient(to right, #F5F5F5, #F5F5F5);
  font-family: 'Helvetica Neue', sans-serif;
  color: #2B2B2B;
  max-width: 1400px;
  margin: 0 auto;
}
.page-title {
  font-size: 42px;
  color: #D7000F;
  font-weight: bold;
  margin-bottom: 30px;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
  text-align: center;
}
/* 新增：视图选择页面样式 */
.view-selection-section {
  background-color: #FFFFFF;
  border-radius: 12px;
  padding: 40px 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.05);
  margin-bottom: 20px;
  min-height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.selection-title {
  font-size: 28px;
  margin-bottom: 40px;
  color: #343a40;
}
.view-options {
  display: flex;
  gap: 40px;
  justify-content: center;
  width: 100%;
  max-width: 800px;
}
.view-option {
  flex: 1;
  padding: 30px 20px;
  border-radius: 16px;
  background-color: #f8f9fa;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  position: relative;
  overflow: hidden;
}
.view-option:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.1);
}
.view-option.selected {
  animation: selectedPulse 0.8s ease;
}
@keyframes selectedPulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); box-shadow: 0 0 20px rgba(215, 0, 15, 0.3); }
  100% { transform: scale(1); }
}
.view-icon {
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.d3-icon {
  background-color: rgba(215, 0, 15, 0.1);
  color: var(--color-accent);
}
.d2-icon {
  background-color: rgba(201, 169, 110, 0.15);
  color: var(--color-gold);
}
.view-option h3 {
  font-size: 22px;
  margin-bottom: 10px;
  color: #343a40;
}
.view-option p {
  color: #6c757d;
  font-size: 16px;
  line-height: 1.5;
}
.intro-section,
.process-section {
  background-color: #FFFFFF;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.05);
  margin-bottom: 20px;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.conversation-section {
  background-color: #FFFFFF;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.05);
  margin-bottom: 20px;
}
.intro-text {
  font-size: 20px;
  line-height: 1.5;
  margin-bottom: 20px;
  text-align: center;
  max-width: 600px;
}
button.btn {
  padding: 12px 24px;
  border-radius: 12px;
  border: none;
  font-size: 16px;
  transition: background-color 0.3s ease, transform 0.3s ease;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  margin: 5px;
  cursor: pointer;
}
button.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}
button.btn:hover:not(:disabled) {
  transform: scale(1.05);
}
.btn-primary {
  background-color: #D7000F;
  color: white;
}
.btn-primary:hover:not(:disabled) {
  background-color: #a0000a;
}
.btn-success {
  background-color: #D7000F;
  color: white;
}
.btn-success:hover:not(:disabled) {
  background-color: #a0000a;
}
.btn-start {
  background-color: #D7000F;
  color: white;
}
.btn-start:hover:not(:disabled) {
  background-color: #a0000a;
}
.btn-stop {
  background-color: #D7000F;
  color: white;
}
.btn-stop:hover:not(:disabled) {
  background-color: #a0000a;
}
.btn-toggle {
  background-color: #6c757d;
  color: white;
}
.btn-toggle:hover:not(:disabled) {
  background-color: #545b62;
}
.btn-speech,
.btn-direct-speech,
.btn-send {
  background-color: #ffc107;
  color: #1d2024;
}
.btn-speech:hover:not(:disabled),
.btn-direct-speech:hover:not(:disabled),
.btn-send:hover:not(:disabled) {
  background-color: #e0a800;
}
.btn-evaluate {
  background-color: #28a745;
  color: white;
}
.btn-evaluate:hover:not(:disabled) {
  background-color: #218838;
}
.btn-close {
  background-color: #6c757d;
  color: white;
}
.btn-close:hover:not(:disabled) {
  background-color: #545b62;
}
.btn-save {
  background-color: var(--color-primary);
  color: white;
}
.btn-save:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
}
.btn-retry {
  background-color: #D7000F;
  color: white;
  margin-top: 20px;
}
.btn-retry:hover:not(:disabled) {
  background-color: #a0000a;
}
.control-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}
.control-panel .row {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}
.input-field {
  padding: 10px;
  border: 2px solid #ced4da;
  border-radius: 10px;
  font-size: 16px;
  width: 200px;
}
.phase-indicator,
.time-indicator {
  padding: 10px;
  border-radius: 12px;
  margin: 15px auto;
  width: fit-content;
  font-weight: bold;
  background-color: #f1f3f5;
  color: #495057;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
.unity-container {
  border: 2px solid #dee2e6;
  border-radius: 16px;
  overflow: hidden;
  background-color: #fff;
  position: relative;
  min-height: 500px;
}
#unity-iframe {
  width: 100%;
  height: 75vh;
  border: none;
  border-radius: 16px 16px 0 0;
}
/* 3D视图对话框样式 - 投名状风格 */
.chat-dialog-3d {
  position: absolute;
  bottom: 30px;
  left: 11.5%;
  right: 11.5%;
  max-height: 280px;
  border: 10px solid transparent;
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0);
  transition: all 0.3s ease;
}
.dialog-content-3d {
  max-height: 240px;
  overflow-y: auto;
  padding: 20px 30px;
  line-height: 1.8;
  font-family: "SimSun", "STSong", serif;
  color: #3a2e18;
}
/* 卷轴装饰 */
.scroll-decoration {
  height: 20px;
  background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGD4z0AswK4SAFXuAf8EPy+xAAAAABJRU5ErkJggg==');
  background-repeat: repeat-x;
  opacity: 0;
}
.scroll-decoration.top {
  border-bottom: 1px solid rgba(101, 67, 33, 0);
}
.scroll-decoration.bottom {
  border-top: 1px solid rgba(101, 67, 33, 0.2);
}
/* 3D视图消息样式 */
.chat-dialog-3d .message {
  padding: 8px 15px;
  margin: 8px 0;
  border-radius: 5px;
  position: relative;
  font-size: 15px;
}
.chat-dialog-3d .message::before {
  content: "";
  position: absolute;
  left: -5px;
  top: 10px;
  height: 0;
  width: 0;
  border: 5px solid transparent;
  border-right-color: inherit;
}
.chat-dialog-3d .message.user {
  background-color: rgba(255, 255, 255, 0.5);
  border: 1px solid #ecebe884;
  margin-left: auto;
  max-width: 75%;
}
.chat-dialog-3d .message.system {
  background-color: rgba(245, 240, 220, 0.2);
  border: 1px solid rgba(245, 240, 220, 0.2);
  color: #1a1614;
  margin-left: auto;
  margin-right: auto;
  max-width: 90%;
}
.chat-dialog-3d .message.streaming {
  background-color: rgba(230, 220, 200, 0.2);
  border: 1px solid rgba(230, 220, 200, 0.2);
  color: #382721;
  max-width: 75%;
}
/* 2D视图样式保持不变 */
.d2-dialog {
  position: relative;
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
  background: #f8f9fa;
  border-top: 1px solid #dee2e6;
  border-radius: 16px 16px 0 0;
}
.message {
  padding: 10px 15px;
  margin: 5px 0;
  border-radius: 12px;
  max-width: 80%;
  word-break: break-word;
  box-shadow: 0 2px 8px rgba(45, 2, 2, 0.058);
}
.message.user {
  background-color: #e9ecef;
  margin-left: auto;
}
.message.system {
  color: #314768eb;
  background-color: #f8f9fa;
  margin-left: auto;
  margin-right: auto;
  max-width: 90%;
}
.message.streaming {
  color: #44428cd7;
  background-color: #f0f4ff;
}
.d2-roles {
  display: flex;
  justify-content: space-around;
  margin-top: 15px;
  gap: 10px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 0 0 16px 16px;
}
.role {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-weight: bold;
  color: #495057;
  padding: 10px;
  border-radius: 12px;
  transition: all 0.3s ease;
}
.role.active {
  background-color: #e9ecef;
  box-shadow: 0 4px 8px rgba(0,0,0,0.05);
  transform: scale(1.05);
}
.role img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 50%;
  margin-bottom: 5px;
  border: 2px solid #dee2e6;
}
.user-input {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}
.user-input input[type="text"] {
  padding: 10px;
  border-radius: 10px;
  border: 2px solid #ced4da;
  width: 300px;
  font-size: 16px;
}
.remaining-turns {
  margin-top: 15px;
  font-size: 14px;
  color: #6c757d;
  font-style: italic;
  text-align: center;
}
/* 评价模态框样式 */
.evaluation-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  padding: 20px;
}
.modal-content {
  background-color: white;
  border-radius: 16px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}
.modal-title {
  font-size: 28px;
  color: #D7000F;
  font-weight: bold;
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
  margin: 0;
  text-align: center;
}
.modal-body {
  padding: 20px;
}
.evaluation-section {
  margin-bottom: 30px;
}
.evaluation-section h3 {
  font-size: 20px;
  color: #343a40;
  margin-bottom: 10px;
  padding-bottom: 5px;
  border-bottom: 2px solid #f1f3f5;
}
.evaluation-section p {
  line-height: 1.6;
  margin-bottom: 15px;
  text-align: justify;
}
.evaluation-section ul {
  padding-left: 20px;
  margin: 0;
}
.evaluation-section ul li {
  margin-bottom: 8px;
  line-height: 1.5;
  text-align: justify;
}
.score {
  display: flex;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
  color: #D7000F;
  margin-bottom: 15px;
}
.score-value {
  margin-right: 15px;
}
.star-rating {
  display: flex;
}
.star-rating i {
  color: #ffc107;
  margin-right: 3px;
}
.star-rating i.active {
  text-shadow: 0 0 5px rgba(255, 193, 7, 0.8);
}
/* 分项评分样式 */
.score-categories {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.score-category {
  display: flex;
  align-items: center;
  gap: 10px;
}
.category-name {
  width: 120px;
  font-weight: bold;
}
.progress-bar {
  flex-grow: 1;
  height: 10px;
  background-color: #e9ecef;
  border-radius: 5px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background-color: #D7000F;
  transition: width 0.5s ease;
}
.category-score {
  width: 80px;
  text-align: right;
  font-weight: bold;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: 20px;
  border-top: 1px solid #e9ecef;
}
/* 加载状态样式 */
.loading-state {
  text-align: center;
  padding: 40px 20px;
}
.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 20px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #D7000F;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
/* 错误状态样式 */
.error-state {
  text-align: center;
  padding: 40px 20px;
  color: #dc3545;
}
.error-state i {
  font-size: 48px;
  margin-bottom: 20px;
}
/* 案件信息弹窗样式 */
.case-info-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}
.case-info-content {
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto
  /* 续上之前的样式 */
}
.case-form {
  padding: 20px;
}
.form-section {
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e9ecef;
}
.form-section:last-child {
  border-bottom: none;
}
.form-section h3 {
  font-size: 18px;
  margin-bottom: 15px;
  color: #D7000F;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #343a40;
}
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 16px;
}
.form-group textarea {
  resize: vertical;
}
.btn-case-info {
  background-color: var(--color-primary);
  color: white;
}
.btn-case-info:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
}
/* 响应式调整 */
@media (max-width: 768px) {
  .page-title {
    font-size: 32px;
  }
  
  .view-options {
    flex-direction: column;
    gap: 20px;
  }
  
  .view-option {
    padding: 20px 15px;
  }
  
  .control-panel .row {
    flex-direction: column;
  }
  
  .input-field {
    width: 100%;
    max-width: 300px;
  }
  
  .chat-dialog-3d {
    left: 5%;
    right: 5%;
    bottom: 15px;
  }
  
  .dialog-content-3d {
    padding: 15px;
  }
  
  .modal-content {
    width: 95%;
  }
  
  .case-info-content {
    width: 95%;
  }
}
</style>