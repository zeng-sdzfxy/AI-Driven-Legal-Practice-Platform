<template>
  <div class="chat-page">
    <h1 class="page-title">模拟法庭对话</h1>

    <!-- 初始阶段：提示先查看流程 -->
    <div v-if="!showProcess && !showConversation" class="intro-section">
      <p>点击下面按钮查看法庭流程说明，然后进入对话。</p>
      <button class="btn btn-primary" @click="showProcess = true">
        显示流程
      </button>
    </div>

    <!-- 流程说明 -->
    <div v-if="showProcess && !showConversation" class="process-section">
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
    <div v-if="showConversation" class="conversation-section">
      <!-- 控制面板 -->
      <div class="control-panel">
        <div class="row">
          <input
            v-model="theme"
            type="text"
            class="input-field"
            placeholder="请输入主题（如：合同纠纷案）"
            @click="$event.target.select()"
          />
          <span>回合数：</span>
          <input
            v-model.number="rounds"
            type="number"
            class="input-field"
            placeholder="回合数"
          />
          <select v-model="userRole" class="input-field">
            <option value="法官">法官</option>
            <option value="原告律师">原告律师</option>
            <option value="被告律师">被告律师</option>
          </select>
        </div>
        <div class="row">
          <button class="btn btn-start" @click="initConversation">
            开始对话
          </button>
          <button class="btn btn-stop" @click="stopConversation">
            停止对话
          </button>
        </div>
      </div>

      <!-- 对话内容显示 -->
      <div class="conversation" ref="conversationContainer">
        <div
          v-for="(msg, index) in conversationHistory"
          :key="index"
          :class="['message', msg.type]"
        >
          <strong>{{ msg.role }}：</strong>
          <span v-html="msg.content"></span>
          <span v-if="msg.streaming" class="streaming-cursor"></span>
        </div>
      </div>

      <!-- 用户输入框（仅在轮到用户时显示） -->
      <div v-if="isUserTurn" class="user-input">
        <input
          v-model="userMessage"
          type="text"
          placeholder="请输入你的发言"
          @keyup.enter="submitUserMessage"
        />
        <button class="btn btn-speech" @click="startVoiceInput">
          语音输入
        </button>
        <button class="btn btn-send" @click="submitUserMessage">发送</button>
      </div>

      <div class="remaining-turns">
        剩余对话总数：{{ totalMessages - currentMessage }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Chat",
  data() {
    return {
      showProcess: false, // 是否显示流程介绍
      showConversation: false, // 是否进入正式对话
      API_ENDPOINT: "http://localhost:8000/api/chat",
      roles: ["法官", "原告律师", "被告律师"],
      theme: "",
      rounds: 3, // 默认回合数
      userRole: "法官",
      conversationRunning: false,
      conversationHistory: [],
      userMessage: "",
      roleSequence: [], // 自定义的角色顺序
      totalMessages: 0,
      currentMessage: 0, // 当前发言序号
      recognition: null,
    };
  },
  computed: {
    // 是否轮到用户说话
    isUserTurn() {
      if (
        !this.conversationRunning ||
        this.currentMessage >= this.totalMessages
      ) {
        return false;
      }
      const currentRole = this.roleSequence[this.currentMessage];
      return currentRole === this.userRole;
    },
  },
  methods: {
    // 初始化对话，生成角色顺序并开始
    initConversation() {
      this.conversationRunning = true;
      this.generateRoleSequence();

      this.currentMessage = 0;
      this.conversationHistory = [];

      this.addSystemMessage(`
        <strong>法庭流程开始：</strong><br>
        主题：${this.theme}<br>
        计划回合数：${this.rounds}<br>
        （以下开始模拟法庭多方对话，请注意区分角色。）<br>
      `);
      this.nextTurn();
    },

    // 生成自定义的角色顺序
    // 前 (rounds - 1) 轮：法官、原告律师、被告律师依次发言
    // 最后一轮：只有法官
    generateRoleSequence() {
      this.roleSequence = [];
      const validRounds = Math.max(1, this.rounds);

      // 前 (validRounds - 1) 轮
      for (let i = 0; i < validRounds - 1; i++) {
        this.roleSequence.push(...this.roles); // 法官、原告律师、被告律师
      }
      // 最后一轮：只有法官
      this.roleSequence.push("法官");

      this.totalMessages = this.roleSequence.length;
    },

    // 进入下一次发言
    nextTurn() {
      // 如果对话已经停止
      if (!this.conversationRunning) {
        this.addSystemMessage("<strong>对话已停止</strong>");
        return;
      }
      // 如果已经发完所有消息
      if (this.currentMessage >= this.totalMessages) {
        this.addSystemMessage("<strong>法庭审理结束</strong>");
        return;
      }

      // 如果当前是最后一条消息（this.currentMessage === this.totalMessages - 1）
      // 则先提示“这是最后一轮...”
      if (this.currentMessage === this.totalMessages - 1) {
        this.addSystemMessage(
          "<strong>这是最后一轮对话，下面请法官进行最后总结</strong>"
        );
      }

      // 取当前角色
      const currentRole = this.roleSequence[this.currentMessage];
      this.addSystemMessage(`<em>当前发言角色：${currentRole}</em>`);

      // 若是用户回合，就等待输入，否则AI自动发言
      if (currentRole === this.userRole) {
        return;
      } else {
        this.streamAIResponse(currentRole);
      }
    },

    // 停止对话
    stopConversation() {
      this.conversationRunning = false;
      this.addSystemMessage("<strong>对话已强制停止</strong>");
    },

    // 提交用户发言
    submitUserMessage() {
      const message = this.userMessage.trim();
      if (!message) return;

      this.conversationHistory.push({
        role: this.userRole,
        content: message,
        type: "user",
      });
      this.userMessage = "";

      // 本轮结束，进入下一发言
      this.currentMessage++;
      this.nextTurn();
    },

    // AI流式响应
    async streamAIResponse(role) {
      const streamingMessage = {
        role: role,
        content: "",
        type: "streaming",
        streaming: true,
      };
      this.conversationHistory.push(streamingMessage);

      try {
        const response = await fetch(this.API_ENDPOINT, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            role,
            theme: this.theme,
            history: this.conversationHistory,
          }),
        });
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
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
                streamingMessage.content += parsed.content;
              } catch (e) {
                console.error("解析错误:", e);
              }
            }
          });
        }
      } catch (error) {
        console.error("请求失败:", error);
        streamingMessage.content += "<em>（响应生成失败）</em>";
        this.stopConversation();
      }

      // AI 发言结束
      this.currentMessage++;
      this.nextTurn();
    },

    // 添加系统消息
    addSystemMessage(content) {
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
        if (this.$refs.conversationContainer) {
          this.$refs.conversationContainer.scrollTop =
            this.$refs.conversationContainer.scrollHeight;
        }
      });
    },

    // 开始语音输入
    startVoiceInput() {
      if (!("webkitSpeechRecognition" in window)) {
        alert("抱歉，当前浏览器不支持语音输入功能。");
        return;
      }

      this.recognition = new webkitSpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;
      this.recognition.lang = "zh-CN";

      this.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        this.userMessage = transcript;
      };

      this.recognition.onend = () => {
        this.recognition = null;
      };

      this.recognition.onerror = (event) => {
        console.error("语音识别错误:", event.error);
        this.recognition = null;
      };

      this.recognition.start();
    },
  },
};
</script>

<style scoped>
.chat-page {
  padding: 10px;
}
.page-title {
  text-align: center;
  font-size: 26px;
  margin-bottom: 20px;
}

/* 初始流程介绍 */
.intro-section,
.process-section {
  text-align: center;
  margin-top: 30px;
}
.process-section ol {
  text-align: left;
  display: inline-block;
  margin: 20px auto;
}

/* 对话区域 */
.conversation-section {
  margin-top: 20px;
}

/* 控制面板 */
.control-panel {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
}
.row {
  display: flex;
  align-items: center;
  gap: 10px;
}
.input-field {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

/* 对话框 */
.conversation {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  min-height: 300px;
  max-height: 450px;
  overflow-y: auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
}
.message {
  margin-bottom: 10px;
  padding: 8px;
  border-radius: 6px;
}
.message.user {
  background-color: #d1e7dd;
  border-left: 4px solid #0d6efd;
}
.message.system {
  background-color: #e2e3e5;
  border-left: 4px solid #6c757d;
}
.message.streaming {
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
}

/* 动态光标 */
.streaming-cursor {
  display: inline-block;
  width: 8px;
  height: 16px;
  background-color: #000;
  animation: blink 1s infinite;
  margin-left: 4px;
}
@keyframes blink {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

/* 用户输入 */
.user-input {
  display: flex;
  justify-content: center;
  gap: 10px;
}
.user-input input {
  flex: 1;
  padding: 8px;
  border: 1px solid #007bff;
  border-radius: 6px;
}

/* 剩余对话数 */
.remaining-turns {
  text-align: center;
  margin-top: 10px;
  color: #666;
}

/* 按钮示例 */
.btn {
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  border: none;
  font-weight: 500;
}
.btn-primary {
  background-color: #007bff;
  color: #fff;
}
.btn-success {
  background-color: #28a745;
  color: #fff;
}
.btn-start {
  background-color: #17a2b8;
  color: #fff;
}
.btn-stop {
  background-color: #dc3545;
  color: #fff;
}
.btn-send {
  background-color: #ffc107;
  color: #fff;
}
.btn-speech {
  background-color: #3498db;
  color: #fff;
}
</style>
