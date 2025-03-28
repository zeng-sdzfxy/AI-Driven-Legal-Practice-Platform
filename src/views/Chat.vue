<template>
  <div class="chat-page">
    <h1 class="page-title">3D 模拟法庭对话</h1>

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

      <!-- Unity WebGL 容器 -->
      <div id="unity-container" class="unity-container">
        <iframe
          id="unity-iframe"
          src="index.html"
          frameborder="0"
          allowfullscreen
        ></iframe>
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

      this.addSystemMessage(
        `
        <strong>法庭流程开始：</strong><br>
        主题：${this.theme}<br>
        计划回合数：${this.rounds}<br>
        （以下开始模拟法庭多方对话，请注意区分角色。）<br>
      `,
        true
      );

      // 自动点击开庭（等待 Unity 加载完毕后发送消息）
      this.openCourt();

      this.nextTurn();
    },

    // 自动点击开庭，等待 Unity 实例加载后发送消息
    openCourt() {
      const iframe = document.getElementById("unity-iframe");
      const sendStart = () => {
        // 发送开庭消息，并传入摄像头索引 "0"（系统提示：下面由法官说话）
        iframe.contentWindow.postMessage(
          JSON.stringify({
            type: "startCourt",
            cameraIndex: "0",
          }),
          "*"
        );
      };

      const checkUnityReady = () => {
        // 检查 iframe 内是否已经加载了 unityInstance
        try {
          if (
            iframe.contentWindow &&
            iframe.contentWindow.unityInstance &&
            typeof iframe.contentWindow.unityInstance.SendMessage === "function"
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

    // 生成自定义的角色顺序
    generateRoleSequence() {
      this.roleSequence = [];
      const validRounds = Math.max(1, this.rounds);

      // 前 (validRounds - 1) 轮，每轮包含：法官、原告律师、被告律师
      for (let i = 0; i < validRounds - 1; i++) {
        this.roleSequence.push(...this.roles);
      }
      // 最后一轮：只有法官
      this.roleSequence.push("法官");

      this.totalMessages = this.roleSequence.length;
    },

    // 进入下一次发言
    nextTurn() {
      if (!this.conversationRunning) {
        this.addSystemMessage("<strong>对话已停止</strong>");
        return;
      }
      if (this.currentMessage >= this.totalMessages) {
        this.addSystemMessage("<strong>法庭审理结束</strong>");
        return;
      }
      if (this.currentMessage === this.totalMessages - 1) {
        this.addSystemMessage(
          "<strong>这是最后一轮对话，下面请法官进行最后总结</strong>",
          true
        );
      }

      const currentRole = this.roleSequence[this.currentMessage];
      // 系统提示当前发言角色（使用系统摄像头）
      this.addSystemMessage(`<em>当前发言角色：${currentRole}</em>`, true);

      // 切换到实际发言摄像头
      const iframe = document.getElementById("unity-iframe");
      iframe.contentWindow.postMessage(
        JSON.stringify({
          type: "switchCamera",
          role: currentRole,
          isSystem: false,
        }),
        "*"
      );

      // 若为用户回合，则等待输入，否则 AI 自动发言
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

    // 用户提交发言
    submitUserMessage() {
      const message = this.userMessage.trim();
      if (!message) return;

      this.conversationHistory.push({
        role: this.userRole,
        content: message,
        type: "user",
      });
      this.userMessage = "";

      const iframe = document.getElementById("unity-iframe");
      // 发送用户发言
      iframe.contentWindow.postMessage(
        JSON.stringify({
          type: "allMessages",
          message: `${this.userRole}：${message}`,
        }),
        "*"
      );
      // 切换到用户实际发言摄像头
      iframe.contentWindow.postMessage(
        JSON.stringify({
          type: "switchCamera",
          role: this.userRole,
          isSystem: false,
        }),
        "*"
      );

      this.currentMessage++;
      this.nextTurn();
    },

    // AI 流式响应
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

      const iframe = document.getElementById("unity-iframe");
      // 发送 AI 完成发言内容
      iframe.contentWindow.postMessage(
        JSON.stringify({
          type: "allMessages",
          message: `${streamingMessage.role}：${streamingMessage.content}`,
        }),
        "*"
      );
      // 切换到 AI 实际发言摄像头
      iframe.contentWindow.postMessage(
        JSON.stringify({
          type: "switchCamera",
          role: streamingMessage.role,
          isSystem: false,
        }),
        "*"
      );

      this.currentMessage++;
      this.nextTurn();
    },

    // 添加系统消息
    addSystemMessage(content, isSystem = false) {
      this.conversationHistory.push({
        role: "系统",
        content,
        type: "system",
      });
      this.scrollToBottom();

      const iframe = document.getElementById("unity-iframe");
      // 发送系统消息到 Unity
      iframe.contentWindow.postMessage(
        JSON.stringify({
          type: "allMessages",
          message: `系统：${content}`,
        }),
        "*"
      );
      // 如果为系统提示且内容包含角色关键字，则发送摄像头切换消息
      if (isSystem) {
        let role = "";
        if (content.indexOf("法官") !== -1) {
          role = "法官";
        } else if (content.indexOf("原告") !== -1) {
          role = "原告律师";
        } else if (content.indexOf("被告") !== -1) {
          role = "被告律师";
        }
        if (role) {
          iframe.contentWindow.postMessage(
            JSON.stringify({
              type: "switchCamera",
              role,
              isSystem: true,
            }),
            "*"
          );
        }
      }
    },

    // 滚动到对话底部
    scrollToBottom() {
      this.$nextTick(() => {
        if (this.$refs.dialogueContent) {
          this.$refs.dialogueContent.scrollTop =
            this.$refs.dialogueContent.scrollHeight;
        }
      });
    },

    // 开始语音输入
    startVoiceInput() {
      let SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert("抱歉，当前浏览器不支持语音输入功能。");
        return;
      }

      this.recognition = new SpeechRecognition();
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

/* Unity WebGL 容器 */
.unity-container {
  width: 100%;
  height: 60vh;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

/* iframe 样式 */
#unity-iframe {
  width: 100%;
  height: 100%;
  border: none;
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

/* 用户输入 */
.user-input {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
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

/* 按钮样式 */
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
