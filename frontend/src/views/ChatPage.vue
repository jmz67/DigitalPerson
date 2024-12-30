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
                    <div class="container px-4 sm:px-6 lg:px-8 flex flex-col flex-grow overflow-y-auto" ref="chatContainer">
                        
                        <transition-group name="message" tag="div">
                            <!-- 遍历消息列表，渲染每条消息 -->
                            <div
                                v-for="(msg, index) in messages"
                                :key="msg.id"
                                class="flex mb-2"
                                :class="msg.sender === 'user' ? 'justify-end' : 'justify-start'"
                            >
                                <!-- Assistant Message -->
                                <div v-if="msg.sender === 'assistant' || msg.sender === 'loading'">
                                    <img
                                        v-if="msg.sender === 'assistant'"
                                        src="../assets/doctor.svg"
                                        alt="AI Avatar"
                                        class="w-10 h-10 rounded-full mr-2"
                                    />
                                </div>

                                <!-- Message Bubble -->
                                <div>
                                    <transition name="fade">
                                        <div
                                            v-if="msg.sender !== 'loading'"
                                            :class="[msg.sender === 'user' ? 'bg-gradient-to-r from-sky-400 to-blue-400 text-white user-message-bubble' : 'bg-white text-gray-800', 'px-4 py-2 shadow-md ai-message-bubble']"
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
                                        v-if="msg.sender === 'assistant' && index === lastAssistantMessageIndex && displayedRecommendations.length > 0"
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
                                                :class="['recommendation-bubble', selectedRecommendations.includes(rec) ? 'selected' : '']"
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
                    <input
                        v-model="input"
                        type="text"
                        placeholder="请输入消息"
                        @keyup.enter="sendMessage"
                        class="flex-grow bg-gray-100 rounded-full px-4 py-2 mx-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                        @click="sendMessage"
                        class="send-button rounded-full bg-gradient-to-r from-blue-600 to-sky-400 text-white px-4 py-2 focus:outline-none hover:opacity-90 transition"
                    >
                        <font-awesome-icon icon="fa-solid fa-paper-plane" />
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import LoadingSpinner from '../components/LoadingSpinner.vue';

export default {
    components: {
        LoadingSpinner,
    },
    data() {
        return {
            input: '',
            messages: [
                { id: 1, sender: 'assistant', text: '你好，请问有什么可以帮助您？' },
            ],
            patient: {
                name: '张伟',
                age: 38,
                department: '皮肤科',
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
            pendingRecommendations: []
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
                const loadingMessage = { id: timestamp + 1, sender: 'loading' };
                this.messages.push(loadingMessage);
                this.smoothScrollToBottom();

                try {
                    const response = await axios.post('/api/chatMessage', {
                        message: userInput,
                        conversation_id: this.conversation_id,
                        sid: this.sid,
                    });

                    console.log('response:', response);

                    const data = response.data;

                    console.log('response.data:', response.data);

                    if (data.conversation_id) {
                        this.conversation_id = data.conversation_id;
                    }

                    // 检查是否存在 chat_type 字段
                    if (data.chat_type == "end") {
                        // 调用关闭数字人方法
                        if (window.Android && typeof window.Android.closeDigitalPerson === 'function') {
                            window.Android.closeDigitalPerson();
                        }
                        // 跳转到首页 "/"
                        this.$router.push('/');
                        return; // 提前结束，不再处理后续逻辑
                    }

                    // 将后端返回的数据缓存起来，等待App调用JS方法后再显示
                    this.pendingAssistantMessage = {
                        id: timestamp + 2,
                        sender: 'assistant',
                        text: data.doctor_question,
                        // text: data.question
                    };
                    this.pendingRecommendations = data.recommendation_texts || [];
                    // this.pendingRecommendations = data.recommendAnswers || [];

                    console.log("pendingAssistantMessage:", this.pendingAssistantMessage);
                    console.log("pendingRecommendations:", this.pendingRecommendations);

                    // 此时不直接替换loading消息为assistant消息，而是等待App调用
                    this.smoothScrollToBottom();
                } catch (error) {
                    console.error('Error:', error);
                    const errorMessage = {
                        id: timestamp + 3,
                        sender: 'assistant',
                        text: '抱歉，发生了错误，请稍后重试。',
                    };
                    const loadingIndex = this.messages.findIndex((msg) => msg.id === (timestamp + 1));
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
        showPendingAssistantMessage() {
            // 如果没有待回复的 AI 消息，则不处理
            if (!this.pendingAssistantMessage) return;
            
            // 查找消息列表中是否有标记为 'loading' 的消息，获取其索引
            const loadingIndex = this.messages.findIndex((msg) => msg.sender === 'loading');
            
            if (loadingIndex !== -1) {
                
                this.messages.splice(loadingIndex, 1, this.pendingAssistantMessage);
                this.lastAssistantMessageIndex = loadingIndex;
            } else {
                this.messages.push(this.pendingAssistantMessage);
                this.lastAssistantMessageIndex = this.messages.length - 1;
            }

            this.currentRecommendations = this.pendingRecommendations;
            this.displayedRecommendations = [];
            this.showRecommendationsOneByOne();

            // 清空pending数据
            this.pendingAssistantMessage = null;
            this.pendingRecommendations = [];

            this.smoothScrollToBottom();
        },

        /**
         * 切换推荐回答的选择状态
         * @param {string} rec - 推荐回答内容
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
         * 一次性显示推荐回答
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
         * 平滑滚动到聊天容器底部
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
         * 转义正则表达式中的特殊字符
         * @param {string} string - 需要转义的字符串
         * @returns {string} - 转义后的字符串
         */
        escapeRegExp(string) {
            return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        },
    },
    mounted() {
        
        // 绑定全局函数，并使用箭头函数保留this上下文
        
        window.receiveSessionId = (param) => {
            try {
                // 如果 param 是一个 JSON 字符串，我们先将它解析为对象
                if (typeof param === 'string') {
                    param = JSON.parse(param);
                }

                // 现在 param 已经是一个对象，可以安全地访问 sessionId
                if (param && param.sessionId) {
                    // 将 sessionId 赋值给 sid
                    this.sid = param.sessionId;
                    alert("数字人已成功打开，Session ID: " + this.sid);
                } else {
                    console.error("无效的参数，缺少 sessionId");
                    alert("无效的参数，缺少 sessionId");
                }

            } catch (error) {
                console.error("解析 param 为 JSON 时发生错误:", error);
                alert("解析参数时发生错误");
            }
        };


        window.receiveDigitalPersonBroadcastData = () => {
            this.showPendingAssistantMessage();
        };

        window.receiveDigitalPersonIdentifyData = ( param ) => {
            try {
                // 如果 param 是一个 JSON 字符串，我们先将它解析为对象
                if (typeof param === 'string') {
                    param = JSON.parse(param);
                }

                // 现在 param 已经是一个对象，可以安全地访问 identifyText
                if (param && param.identifyText) {
                    this.input = param.identifyText;
                    alert("接收文本内容成功: " + this.input);
                } else {
                    console.error("无效的参数，缺少 identifyText");
                    alert("无效的参数，缺少 identifyText");
                }

            } catch (error) {
                console.error("解析 param 为 JSON 时发生错误:", error);
                alert("解析参数时发生错误");
            }
        };

        // 调用数字人接口
        if (window.Android && typeof window.Android.openDigitalPerson === 'function') {
            const digitalPersonConfig = {
                digitalperson: {
                    id: "2894645415315454",
                    width: "400",
                    height: "600",
                    x: "0",
                    y: "280"
                }
            };
            try {
                window.Android.openDigitalPerson(JSON.stringify(digitalPersonConfig));
            } catch (e) {
                alert(`调用 openDigitalPerson 时发生错误: ${e.message}`);
            }
        } else {
            alert('window.Android.openDigitalPerson 方法不可用。');
        }
    },

    beforeDestroy() {
        // 清理全局函数绑定
        delete window.receiveSessionId;
    }
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
    height: 100vh; /* 使用视口高度 */
    margin: 0;
    padding: 0;
    overflow: hidden;
    box-sizing: border-box;
}

/* 第一个区域样式 */
.top-area {
    position: absolute;
    top: 0; /* 紧贴网页顶部 */
    left: 0;
    width: 100%; /* 全宽 */
    height: 34.9vh; /* 占视口高度的 34.9% */
    background: url('../assets/问诊页面最上方背景图.png') no-repeat top center; /* 背景图片对齐顶部和居中 */
    background-size: cover; /* 确保图片覆盖整个区域 */
    display: flex;
    align-items: flex-start;
    padding-top: 1.2vh; /* 顶部内边距 */
    padding-left: 2.2vh; /* 左侧内边距 */
    gap: 5vw; /* Logo 和文本之间的间距 */
}

/* Logo 样式 */
.logo {
    position: relative;
    width: 11vh;
    height: 8.3vh;
    top: 1.2vh; /* 距离顶部 */
    left: 1.6vh; /* 距离左侧 */
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
    top: 14.1vh; /* 默认距离网页顶部 14.1% */
    left: 0;
    width: 100%;
    height: 10.5vh; /* 默认占视口高度 10.5% */
    background-color: rgba(255, 255, 255, 0.5); /* 50% 透明的浅红色 */
}

/* 第三个区域样式 */
.bottom-area {
    position: absolute;
    top: 20.4vh; /* 默认距离网页顶部 20.4% */
    left: 0;
    width: 100%;
    height: 79.6vh; /* 默认占视口高度 79.6% */
    background-image: linear-gradient(233deg, #F2F2F5 0%, #E9EDF7 100%); /* 渐变背景 */
    border-radius: 24px 24px 0px 0px; /* 仅顶部圆角 */
}

/* 消息列表的进入和离开动画 */
.message-enter-active,
.message-leave-active {
    transition: all 0.6s; /* 过渡时间为0.6秒 */
}
.message-enter-from {
    opacity: 0; /* 初始透明度 */
    transform: translateY(10px); /* 初始位置向下偏移 */
}
.message-enter-to {
    opacity: 1; /* 结束时的透明度 */
    transform: translateY(0); /* 结束时的位置 */
}

.ai-message-bubble {
    box-shadow: 0 0 12px 0 rgba(0,0,0,0.10);
    border-radius: 0px 12px 12px 12px;
}

.user-message-bubble {
    box-shadow: 0 0 12px 0 rgba(0,0,0,0.10);
    border-radius: 12px 0px 12px 12px;
}

.send-button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 50%; /* 圆形按钮 */
    cursor: pointer;
    transition: background-color 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* 自定义滚动条样式（仅适用于Webkit内核浏览器） */
::-webkit-scrollbar {
    width: 6px; /* 滚动条宽度 */
}

::-webkit-scrollbar-track {
background: #f1f1f1; /* 滚动条轨道背景色 */
}

::-webkit-scrollbar-thumb {
background: #c1c1c1; /* 滚动条滑块颜色 */
border-radius: 1px; /* 滚动条滑块圆角 */
}

::-webkit-scrollbar-thumb:hover {
background: #a8a8a8; /* 滚动条滑块悬停颜色 */
}

.recommendation-bubble {
    cursor: pointer;
    border-radius: 16px; /* Rounded edges */
    padding: 8px 16px; /* Adequate padding */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    margin: 4px; /* Margin between recommendations */
    transition: all 0.3s ease-in-out; /* Smooth transition */
    background-color: #f9f9f9; /* Light background */
    font-size: 14px;
    font-weight: 500; /* Slightly bolder font */
}

.recommendation-bubble:hover {
    background-color: #eaeaea; /* Hover state background */
}

.recommendation-bubble.selected {
    background-color: #007bff; /* Highlight selected */
    color: white; /* White text for selected */
    font-weight: bold; /* Bold font */
    box-shadow: 0 0 10px rgba(0, 123, 255, 0.5); /* Glow effect */
    transform: scale(1.05); /* Slight enlargement */
}

/* 推荐回答列表的进入动画 */
.recommendation-enter-active {
    transition: opacity 0.3s; /* 透明度过渡时间为0.3秒 */
}
.recommendation-enter-from {
    opacity: 0; /* 初始透明度 */
}
.recommendation-enter-to {
    opacity: 1; /* 结束时的透明度 */
}

</style>
