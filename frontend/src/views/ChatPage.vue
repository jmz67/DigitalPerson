<template>
  <div class="layout fade-in">
    <!-- 第一个区域 -->
    <div class="top-area">
      <img class="logo" src="../assets/hospital-logo.png" alt="Logo" />
      <p class="description">
        为了让医生更全面地了解您的病情，以便为您提供更好的诊疗服务，AI助手将询问您相关问题，麻烦您用几分钟的时间如实回答以下问题，感谢您的配合!
      </p>
    </div>

    <!-- 第二个区域 -->
    <div class="middle-area">
      <div class="flex items-center justify-evenly w-full mt-2">
        <div class="flex-1 text-center">
          <p>患者姓名：<span class="text-lg font-bold">{{ patient.name }}</span></p>
        </div>
        <div class="flex-1 text-center">
          <p>年龄：<span class="font-bold">{{ patient.age }}岁</span></p>
        </div>
        <div class="flex-1 text-center">
          <p>挂号科室：<span class="font-bold">{{ patient.department }}</span></p>
        </div>
      </div>
    </div>

    <!-- 第三个区域 -->
    <div class="bottom-area flex flex-col flex-grow pt-4 pb-24">
      <!-- 聊天主页面 -->
      <div class="flex flex-grow overflow-hidden">
        <!-- 左侧 数字人 App 区域 -->
        <div class="w-1/3 p-4">
          <div class="h-full flex items-center justify-center">
            <!-- 数字人内容占位 -->
          </div>
        </div>

        <!-- 右侧 聊天区域 -->
        <div class="w-2/3 flex flex-col flex-grow p-6">
          <div
            class="container px-4 sm:px-6 lg:px-8 flex flex-col flex-grow overflow-y-auto"
            ref="chatContainer"
          >
            <transition-group name="message" tag="div">
              <!-- 遍历消息列表，渲染每条消息 -->
              <div
                v-for="(msg, index) in messages"
                :key="msg.id"
                class="flex items-start mb-2"
                :class="msg.sender === 'user' ? 'justify-end' : 'justify-start'"
              >
                <!-- Assistant Message -->
                <div
                  v-if="msg.sender === 'assistant' || msg.sender === 'loading'"
                  class="flex-shrink-0 mr-2"
                >
                  <img
                    v-if="msg.sender === 'assistant'"
                    src="../assets/doctor.svg"
                    alt="AI Avatar"
                    class="ai-avatar rounded-full"
                  />
                </div>

                <!-- Message Bubble -->
                <div>
                  <transition name="fade">
                    <div
                      v-if="msg.sender !== 'loading'"
                      :class="[
                        msg.sender === 'user'
                          ? 'bg-gradient-to-r from-sky-400 to-blue-400 text-white user-message-bubble'
                          : 'bg-white text-gray-800',
                        'px-4 py-2 shadow-md ai-message-bubble'
                      ]"
                      class="inline-block break-words"
                    >
                      {{ msg.text }}
                    </div>
                  </transition>

                  <!-- Loading Spinner -->
                  <transition name="fade">
                    <div
                      v-if="msg.sender === 'loading'"
                      class="bg-gray-200 text-gray-800 rounded-lg px-4 py-2 shadow-md inline-block"
                    >
                      <LoadingSpinner />
                    </div>
                  </transition>

                  <!-- 推荐回答 -->
                  <transition-group
                    v-if="msg.sender === 'assistant'
                           && index === lastAssistantMessageIndex
                           && displayedRecommendations.length > 0"
                    name="recommendation"
                    tag="div"
                    class="mt-2 flex flex-wrap max-w-lg"
                  >
                    <div
                      v-for="rec in displayedRecommendations"
                      :key="rec"
                      class="m-1"
                    >
                      <div
                        :class="[
                          'recommendation-bubble',
                          selectedRecommendations.includes(rec) ? 'selected' : ''
                        ]"
                        @click="toggleRecommendation(rec)"
                      >
                        {{ rec }}
                      </div>
                    </div>
                  </transition-group>
                </div>

                <!-- User Message -->
                <div v-if="msg.sender === 'user'">
                  <img
                    src="../assets/patient.svg"
                    alt="User Avatar"
                    class="w-10 h-10 rounded-full ml-2"
                  />
                </div>
              </div>
            </transition-group>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="fixed bottom-4 left-1/2 transform -translate-x-1/2 w-full max-w-4xl px-4">
        <div class="bg-white rounded-lg shadow-lg flex items-center p-2">
          <!-- 麦克风按钮 -->
          <button
            @click="toggleMicrophone"
            :class="['button mic-button', { 'mic-open': microphoneOpen }]"
          >
            <!-- 根据状态切换图标 -->
            <font-awesome-icon
              :icon="microphoneOpen ? 'fa-solid fa-microphone-slash' : 'fa-solid fa-microphone'"
              class="mic-icon"
            />
            <!-- style="font-size: 18px;" -->
          </button>

          <!-- 输入框 -->
          <input
            v-model="input"
            type="text"
            placeholder="请输入消息"
            @keyup.enter="sendMessage"
            class="flex-grow bg-gray-100 rounded-full px-4 py-2 mx-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <!-- 发送按钮 -->
          <button
            @click="sendMessage"
            class="button send-button"
          >
            <font-awesome-icon icon="fa-solid fa-paper-plane" />
          </button>
        </div>
      </div>
    </div>

    <!-- 录音提示浮层，右下角 -->
    <div v-if="microphoneOpen" class="voice-overlay">
      <div class="voice-indicator">麦克风已打开，请讲话...</div>
    </div>
  </div>
</template>

<script>
import {
  createConversation,
  saveMessage,
  sendChatMessage,
  getChatHistory,
} from '../api/chat'; // 导入 chat.js 中的 API 函数
import LoadingSpinner from '../components/LoadingSpinner.vue';
import Swal from 'sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import { fetchPatientInfo } from '../api/patient'; // 假设您已有的 API 调用
import { useAuthStore } from '../store'; // 引入认证 store

export default {
  components: {
    LoadingSpinner,
  },
  data() {
    return {
      input: '',
      messages: [], // 初始化为空数组
      patient: {
        id: null, // 确保患者对象包含 id
        name: '',
        age: '',
        department: '',
      },
      sid: null,
      conversation_id: null,
      selectedRecommendations: [],
      currentRecommendations: [],
      displayedRecommendations: [],
      lastAssistantMessageIndex: null,
      sessionId: null,

      // 新增字段
      pendingAssistantMessage: null,
      pendingRecommendations: [],

      // 是否开启麦克风
      microphoneOpen: false,
    };
  },
  methods: {
    /**
     * 发送消息到后端
     */
    async sendMessage() {
      if (this.input.trim()) {
        const timestamp = Date.now();
        const userMessage = { id: timestamp, sender: 'user', text: this.input };
        this.messages.push(userMessage);
        this.smoothScrollToBottom();

        this.currentRecommendations = [];
        this.displayedRecommendations = [];
        this.lastAssistantMessageIndex = null;

        const userInput = this.input;
        this.input = '';
        const loadingMessage = { id: timestamp + 1, sender: 'loading', text: '' };
        this.messages.push(loadingMessage);
        this.smoothScrollToBottom();

        try {
              // 打印即将发送的消息内容
              console.log('即将发送的消息:', {
                  content: userInput,
                  conversation_id: this.conversation_id,
                  sid: this.sid
              });

              // 发送聊天消息并获取助手回复
              const response = await sendChatMessage(
                  userInput,
                  this.conversation_id,
                  this.sid,
              );

              console.log('response:', response);

              const data = response.data;

              console.log('response.data:', response.data);

              // 如果需要更新 conversation_id
              if (data.conversation_id) {
                console.log('更新 conversation_id:', data.conversation_id);
                this.conversation_id = data.conversation_id;
                await createConversation(this.patient.id, this.conversation_id);
              }

              // 如果 chat_type 为 end，则关闭数字人并返回主页
              if (data.chat_type === 'end') {
                if (
                  window.Android &&
                  typeof window.Android.closeDigitalPerson === 'function'
                ) {
                  window.Android.closeDigitalPerson();
                }
                this.$router.push('/');
                return;
              }

              // 缓存后端返回的数据，等待 App 调用再显示
              this.pendingAssistantMessage = {
                id: timestamp + 2,
                sender: 'assistant',
                text: data.doctor_question,
              };
              this.pendingRecommendations = data.recommendation_texts || [];

              console.log('pendingAssistantMessage:', this.pendingAssistantMessage);
              console.log('pendingRecommendations:', this.pendingRecommendations);

              this.smoothScrollToBottom();

              // 保存用户消息和加载状态消息到后端
              console.log('即将保存的消息:', {
                  conversation_id: this.conversation_id,
                  role: 'user',
                  text: userMessage.text,
              });
              await saveMessage(this.conversation_id, 'user', userMessage.text);
              // await saveMessage(this.conversation_id, 'loading', loadingMessage.text);
        } catch (error) {
          console.error('Error:', error);
          const errorMessage = {
            id: timestamp + 3,
            sender: 'assistant',
            text: '抱歉，发生了错误。请稍后再试。',
          };
          const loadingIndex = this.messages.findIndex(
            (msg) => msg.id === timestamp + 1
          );
          if (loadingIndex !== -1) {
            this.messages.splice(loadingIndex, 1, errorMessage);
          }
          this.smoothScrollToBottom();
        }
      }
    },

    /**
     * 显示待处理的助手消息和推荐回答
     */
    async showPendingAssistantMessage() {
      if (!this.pendingAssistantMessage) return;

      // 查找是否有 'loading' 消息
      const loadingIndex = this.messages.findIndex(
        (msg) => msg.sender === 'loading'
      );

      if (loadingIndex !== -1) {
        this.messages.splice(loadingIndex, 1, this.pendingAssistantMessage);
        this.lastAssistantMessageIndex = loadingIndex;
      } else {
        this.messages.push(this.pendingAssistantMessage);
        this.lastAssistantMessageIndex = this.messages.length - 1;
      }

      this.currentRecommendations = this.pendingRecommendations;

      console.log('即将保存的消息:', {
                  conversation_id: this.conversation_id,
                  role: 'assistant',
                  text: this.pendingAssistantMessage.text,
              });

      // 保存助手消息到后端
      await saveMessage(this.conversation_id, 'assistant', this.pendingAssistantMessage.text);

      
      this.displayedRecommendations = [];
      this.showRecommendationsOneByOne();

      this.pendingAssistantMessage = null;
      this.pendingRecommendations = [];

      this.smoothScrollToBottom();
    },

    /**
     * 切换推荐回答的选择状态
     */
    toggleRecommendation(rec) {
      const index = this.selectedRecommendations.indexOf(rec);
      if (index > -1) {
        this.selectedRecommendations.splice(index, 1);
        const regex = new RegExp(`\\b${this.escapeRegExp(rec)}\\b`, 'g');
        this.input = this.input.replace(regex, '').replace(/\s\s+/g, ' ').trim();
      } else {
        this.selectedRecommendations.push(rec);
        if (!this.input.includes(rec)) {
          this.input += (this.input ? ' ' : '') + rec;
        }
      }
    },

    /**
     * 一次性显示推荐回答（逐个显现）
     */
    showRecommendationsOneByOne() {
      const recs = this.currentRecommendations.slice();
      const displayNext = () => {
        if (recs.length > 0) {
          this.displayedRecommendations.push(recs.shift());
          this.smoothScrollToBottom();
          setTimeout(displayNext, 300);
        }
      };
      displayNext();
    },

    /**
     * 平滑滚动到底部
     */
    smoothScrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.chatContainer;
        if (container) {
          requestAnimationFrame(() => {
            container.scrollTo({
              top: container.scrollHeight,
              behavior: 'smooth',
            });
          });
        }
      });
    },

    /**
     * 转义正则中的特殊字符
     */
    escapeRegExp(string) {
      return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    },

    /**
     * 点击麦克风按钮，切换麦克风开关
     */
    toggleMicrophone() {
      if (!this.microphoneOpen) {
        // 打开麦克风
        if (
          window.Android &&
          typeof window.Android.openMicrophone === 'function'
        ) {
          window.Android.openMicrophone();
        } else {
          Swal.fire({
            title: '错误',
            text: '无效麦克风打开方法',
            icon: 'error',
            confirmButtonText: '确定',
            width: 400, // 直接设置宽度像素值或百分比
          });
        }
        this.microphoneOpen = true;
      } else {
        // 关闭麦克风
        if (
          window.Android &&
          typeof window.Android.closeMicrophone === 'function'
        ) {
          window.Android.closeMicrophone();
        } else {
          Swal.fire({
            title: '错误',
            text: '无效麦克风关闭方法',
            icon: 'error',
            confirmButtonText: '确定',
            width: 400, // 直接设置宽度像素值或百分比
          });
        }
        this.microphoneOpen = false;
      }
    },

    /**
     * 加载聊天历史
     */
    async loadChatHistory() {
      if (!this.conversation_id) return;

      try {
        const response = await getChatHistory(this.conversation_id);
        this.messages = response.data.messages.map(msg => ({
          id: msg.id,
          sender: msg.sender,
          text: msg.text,
          timestamp: msg.timestamp,
        }));
        this.smoothScrollToBottom();
      } catch (error) {
        console.error('加载聊天历史失败:', error);
        Swal.fire({
          title: '加载失败',
          text: '无法加载聊天历史，请稍后再试。',
          icon: 'error',
          confirmButtonText: '确定',
          width: 400,
        });
      }
    },
  },

  async mounted() {
    const authStore = useAuthStore(); // 引入认证 store

    // 绑定全局函数
    window.receiveSessionId = (param) => {
      try {
        if (typeof param === 'string') {
          param = JSON.parse(param);
        }
        if (param && param.sessionId) {
          this.sid = param.sessionId;
          // 使用 SweetAlert2：
          Swal.fire({
            title: '数字人已成功打开',
            text: 'Session ID: ' + this.sid,
            icon: 'success',
            confirmButtonText: '确定',
            width: 400, // 直接设置宽度像素值或百分比
          });
        } else {
          console.error('无效的参数，缺少 sessionId');
          Swal.fire({
            title: '错误',
            text: '无效的参数，缺少 sessionId',
            icon: 'error',
            confirmButtonText: '确定',
            width: 400, // 直接设置宽度像素值或百分比
          });
        }
      } catch (error) {
        console.error('解析 param 为 JSON 时发生错误:', error);
        Swal.fire({
          title: '解析错误',
          text: '解析参数时发生错误',
          icon: 'error',
          confirmButtonText: '确定',
          width: 400, // 直接设置宽度像素值或百分比
        });
      }
    };

    window.receiveDigitalPersonBroadcastData = () => {
      this.showPendingAssistantMessage();
    };

    window.receiveDigitalPersonIdentifyData = (param) => {
      try {
        if (typeof param === 'string') {
          param = JSON.parse(param);
        }
        if (param && param.identifyText) {
          // 使用 SweetAlert2 替换原生 alert
          Swal.fire({
            title: '检测到文本',
            text: `是否将以下文本插入输入框？\n\n${param.identifyText}`,
            icon: 'info',
            showCancelButton: true, // 显示取消按钮
            confirmButtonText: '确定', // 确定按钮文字
            cancelButtonText: '取消', // 取消按钮文字
            reverseButtons: true, // 交换确定、取消按钮的位置（可选）
            width: 400, // 直接设置宽度像素值或百分比
          }).then((result) => {
            if (result.isConfirmed) {
              // 用户点击“确定”时才将文本放入输入框
              this.input = param.identifyText;
              // 如需可再弹一个提示“插入成功”
              // Swal.fire('已插入', '', 'success');
            } else {
              // 用户点击“取消”或关闭弹窗则不做任何处理
              console.log('用户取消了插入文本');
            }
          });
        } else {
          console.error('无效的参数，缺少 identifyText');
          // 这里也可以用 Swal 弹窗提示
          Swal.fire({
            title: '错误',
            text: '无效的参数，缺少 identifyText',
            icon: 'error',
            confirmButtonText: '确定',
            width: 400, // 直接设置宽度像素值或百分比
          });
        }
      } catch (error) {
        console.error('解析 param 为 JSON 时发生错误:', error);
        Swal.fire({
          title: '解析错误',
          text: '解析参数时发生错误',
          icon: 'error',
          confirmButtonText: '确定',
          width: 400, // 直接设置宽度像素值或百分比
        });
      }
    };

    // 调用数字人接口
    if (window.Android && typeof window.Android.openDigitalPerson === 'function') {
      const digitalPersonConfig = {
        digitalperson: {
          id: '2894645415315454',
          width: '400',
          height: '600',
          x: '0',
          y: '280',
        },
      };
      try {
        window.Android.openDigitalPerson(JSON.stringify(digitalPersonConfig));
      } catch (e) {
        Swal.fire({
          title: '调用 openDigitalPerson 时发生错误',
          text: e.message,
          icon: 'error',
          confirmButtonText: '确定',
          width: 400, // 直接设置宽度像素值或百分比
        });
      }
    } else {
      Swal.fire({
        title: '错误',
        text: 'window.Android.openDigitalPerson 方法不可用。',
        icon: 'error',
        confirmButtonText: '确定',
        width: 400, // 直接设置宽度像素值或百分比
      });
    }

    // 获取患者信息
    try {
      const patientData = await fetchPatientInfo();
      this.patient = patientData;
      // 如果已存在 conversation_id，则加载聊天历史
      if (this.conversation_id) {
        this.conversation_id = this.patient.conversation_id;
        this.loadChatHistory();
      }
    } catch (error) {
      Swal.fire({
        title: '加载失败',
        text: '获取患者信息时出现问题，请稍后重试。',
        icon: 'error',
        confirmButtonText: '确定',
        width: 400,
      });
    }

    // 如果 conversation_id 已存在（例如通过 URL 参数传递），加载聊天历史
    if (this.conversation_id) {
      this.loadChatHistory();
    }
  },

  beforeDestroy() {
    // 清理全局函数
    delete window.receiveSessionId;
    delete window.receiveDigitalPersonBroadcastData;
    delete window.receiveDigitalPersonIdentifyData;
  },
};
</script>
  
<style scoped>
  /* Page fade-in animation */
  .fade-in {
    animation: fadeIn 0.6s ease-in-out forwards;
    opacity: 0;
  }
  @keyframes fadeIn {
    to {
      opacity: 1;
    }
  }
  
  /* 全局布局 */
  .layout {
    position: relative;
    width: 100vw;
    height: 100vh;
    margin: 0;
    padding: 0;
    overflow: hidden;
    box-sizing: border-box;
  }
  
  /* 第一个区域样式 */
  .top-area {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 34.9vh;
    background: url('../assets/问诊页面最上方背景图.png') no-repeat top center;
    background-size: cover;
    display: flex;
    align-items: flex-start;
    padding-top: 1.2vh;
    padding-left: 2.2vh;
    gap: 5vw;
  }
  
  /* Logo 样式 */
  .logo {
    position: relative;
    width: 11vh;
    height: 8.3vh;
    top: 1.2vh;
    left: 1.6vh;
  }
  
  /* 描述文本样式 */
  .description {
    font-family: SourceHanSansSCVF-Bold, sans-serif;
    font-size: 3vh;
    color: #333333;
    letter-spacing: 0;
    line-height: 5vh;
    font-weight: 700;
    margin-right: 10vw;
    top: 2.4vh;
  }
  
  /* 第二个区域样式 */
  .middle-area {
    position: absolute;
    top: 14.1vh;
    left: 0;
    width: 100%;
    height: 10.5vh;
    background-color: rgba(255, 255, 255, 0.5);
  }
  
  /* 第三个区域样式 */
  .bottom-area {
    position: absolute;
    top: 20.4vh;
    left: 0;
    width: 100%;
    height: 79.6vh;
    background: #E9EDF7;
    border-radius: 24px 24px 0px 0px;
  }
  
  /* 消息列表的进入和离开动画 */
  .message-enter-active,
  .message-leave-active {
    transition: all 0.6s;
  }
  .message-enter-from {
    opacity: 0;
    transform: translateY(10px);
  }
  .message-enter-to {
    opacity: 1;
    transform: translateY(0);
  }
  
  .ai-message-bubble {
    box-shadow: 0 0 12px 0 rgba(0, 0, 0, 0.1);
    border-radius: 0px 12px 12px 12px;
  }
  
  .user-message-bubble {
    box-shadow: 0 0 12px 0 rgba(0, 0, 0, 0.1);
    border-radius: 12px 0px 12px 12px;
  }
  
  /* 防止医生头像被压缩 */
  .ai-avatar {
    width: 40px;
    height: 40px;
    flex-shrink: 0;
  }
  
/* 通用按钮样式 */
.button {
  width: 40px; /* 固定宽度，确保为正方形 */
  height: 40px; /* 固定高度 */
  border-radius: 50%; /* 圆角设置为50%实现圆形 */
  display: flex;
  align-items: center;
  justify-content: center; /* 确保内容居中 */
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease; /* 增加动态效果 */
  border: none; /* 去除边框 */
}

/* 麦克风按钮 */
.mic-button {
  background: linear-gradient(to right, #007bff, #82d5ff);
  color: white; /* 图标颜色 */
}

.mic-button:hover {
  transform: scale(1.1); /* 悬停时放大效果 */
}

.mic-button.mic-open {
  background: linear-gradient(to right, #e53e3e, #f6c7c7);; /* 录音状态下的红色背景 */
}

.mic-icon {
  font-size: 18px; /* 设置图标大小 */
}

/* 发送按钮 */
.send-button {
  background: linear-gradient(to right, #007bff, #82d5ff); /* 渐变背景 */
  color: white; /* 图标颜色 */
}

.send-button:hover {
  transform: scale(1.1); /* 悬停时放大效果 */
}

  
  /* 自定义滚动条样式（仅适用于Webkit内核浏览器） */
  ::-webkit-scrollbar {
    width: 6px;
  }
  ::-webkit-scrollbar-track {
    background: #f1f1f1;
  }
  ::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 1px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
  }
  
  /* 推荐回答气泡 */
  .recommendation-bubble {
    cursor: pointer;
    border-radius: 16px;
    padding: 8px 16px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin: 4px;
    transition: all 0.3s ease-in-out;
    background-color: #f9f9f9;
    font-size: 14px;
    font-weight: 500;
  }
  .recommendation-bubble:hover {
    background-color: #eaeaea;
  }
  .recommendation-bubble.selected {
    background-color: #007bff;
    color: white;
    font-weight: bold;
    box-shadow: 0 0 10px rgba(0, 123, 255, 0.5);
    transform: scale(1.05);
  }
  .recommendation-enter-active {
    transition: opacity 0.3s;
  }
  .recommendation-enter-from {
    opacity: 0;
  }
  .recommendation-enter-to {
    opacity: 1;
  }
  
  /* 录音提示浮层：右下角，避免遮挡主要内容，带呼吸波动 */
  .voice-overlay {
    position: fixed;
    right: 20vw;
    bottom: 80px;
    display: flex;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.55);
    color: #fff;
    border-radius: 16px;
    padding: 10px 16px;
    z-index: 9999;
    animation: fadeInUp 0.3s ease-in-out;
  }
  @keyframes fadeInUp {
    0% {
      opacity: 0;
      transform: translateY(10px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }
  .voice-indicator {
    position: relative;
    padding-left: 24px;
    font-size: 14px;
  }
  .voice-indicator::before {
    content: '';
    position: absolute;
    left: 0;
    top: 4px;
    width: 8px;
    height: 8px;
    background-color: #fff;
    border-radius: 50%;
    animation: micWave 1.2s infinite;
  }
  @keyframes micWave {
    0% {
      transform: scale(1);
      opacity: 1;
    }
    50% {
      transform: scale(2.2);
      opacity: 0;
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }
</style>
  