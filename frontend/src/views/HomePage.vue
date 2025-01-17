<template>
<div class="layout">
    <!-- 顶部区域 -->
    <div class="top-area">
    <div class="top-content">
        <img class="logo" src="../assets/logo@2x.png" alt="logo" />
        <img class="welcome-text01" src="../assets/标题@3x.svg" alt="welcome-text01" />
        <div class="welcome-text02">
        <p class="text-blue-800 text-[1.6vw] max-w-[47vw]">在这里我们将提前收集您的就诊信息，以协助专家诊疗，下面请您跟着我们的指令，开始吧!</p>
        </div>
        <img class="welcome-text03" src="../assets/气泡@2x.png" alt="welcome-text03" />
        <div class="mt-8 ml-4 hidden-input">
            <input 
                name="scanCode" 
                id="scanCode" 
                v-model="scanCodeValue" 
                @input="handleInput"
                @keydown.enter="handleEnterKey"
                ref="scanCodeInput"
            />
            <button @click="handleEnterKey" class="ml-2">
                <font-awesome-icon icon="fa-solid fa-paper-plane" />
            </button>
        </div>
    </div>
    </div>

    <!-- 底部区域 -->
    <div class="bottom-area">
    <div class="flex">
        <!-- STEP 1 -->
        <a href="/wzchat/#/chat" class="step-card">
        <img src="../assets/AI预问诊@2x.png" alt="AI预问诊" />
        <h3>STEP 1</h3>
        <p>AI 预问诊</p>
        </a>
        <!-- STEP 2 -->
        <div class="step-card">
        <img src="../assets/把脉@2x.png" alt="中医舌脉信息采集指引" />
        <h3>STEP 2</h3>
        <p>中医舌脉信息采集指引</p>
        </div>
        <!-- STEP 3 -->
        <div class="step-card">
        <img src="../assets/血压采集@2x.png" alt="身高体重血压信息采集指引" />
        <h3>STEP 3</h3>
        <p>身高体重血压信息采集指引</p>
        </div>
        <!-- STEP 4 -->
        <div class="step-card">
        <img src="../assets/生成报告.png" alt="生成问诊报告智能辅助诊疗" />
        <h3>STEP 4</h3>
        <p>生成问诊报告智能辅助诊疗</p>
        </div>
    </div>
    </div>
</div>
</template>

<script>
import { useAuthStore } from '../store'; // 如果使用 Pinia
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'; // 引入 FontAwesome 图标组件

export default {
components: {
    FontAwesomeIcon, // 注册 FontAwesome 图标组件
},
data() {
    return {
    scanCodeValue: '', // 输入框的值
    inputTimeout: null, // 用于延迟处理的计时器
    };
},
methods: {
    handleEnterKey() {
    alert('handleEnterKey called'); // 调试信息：handleEnterKey 被调用
    if (this.scanCodeValue) {
        alert('Scan code value: ' + this.scanCodeValue); // 显示扫码结果
        const authStore = useAuthStore();
        authStore.setScanCode(this.scanCodeValue);

        // 显示跳转提示
        alert('扫码成功！将会在 1 秒后跳转到下一个页面');

        // 使用 setTimeout 延迟 1 秒钟进行跳转
        setTimeout(() => {
            this.$router.push('/chat');
        }, 1000); // 延迟 1 秒（1000 毫秒）后跳转
    } else {
        alert('Scan code value is empty'); // 扫码值为空
    }
    },
    handleInput() {
        // 清除之前的计时器
        if (this.inputTimeout) {
            clearTimeout(this.inputTimeout);
        }

        // 设置一个新的计时器，延迟 500 毫秒后执行跳转逻辑
        this.inputTimeout = setTimeout(() => {
            this.handleEnterKey();
        }, 1000); // 延迟 500 毫秒
    }
},
mounted() {

    // 检查是否在 Android 环境中
    if (window.Android) {
        // 调用 Android 的原生方法，聚焦输入框
        alert('Android 环境，调用 Android 原生方法聚焦输入框');
        window.Android.focusInput();
    } else {
        // 如果不是 Android 环境，直接使用 JavaScript 聚焦
        alert('非 Android 环境，使用 JavaScript 聚焦输入框');
        this.$refs.scanCodeInput.focus();
    }
},
};
</script>

<style scoped>
/* 样式保持不变 */
.layout {
position: relative;
width: 100%;
height: 100vh;
margin: 0;
padding: 0;
overflow: hidden;
box-sizing: border-box;
}

.top-area {
position: absolute;
top: 0;
left: 0;
width: 100%;
height: 50vh;
background: url('../assets/问诊页面最上方背景图.png');
background-size: cover;
}

.bottom-area {
position: absolute;
bottom: 0;
left: 0;
width: 100%;
height: 50vh;
background-image: linear-gradient(180deg, rgba(249,251,255,0.40) 0%, rgba(241,246,255,0.00) 100%);
}

.top-content {
position: absolute;
top: 3.7vh;
left: 2.5vh;
right: 2.5vh;
height: 46.3vh;
border-radius: 24px 24px 0 0;
box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
overflow: hidden;
background-image: linear-gradient(124deg, rgba(250,250,255,0.25) 0%, #E9F2F7 100%);
border: 3px solid rgba(255,255,255,1);
border-radius: 24px 24px 0 0;
border-bottom: none;
}

.logo {
position: relative;
width: 7vw;
height: 9vh;
top: 2vh;
left: 2.4vh;
}

.welcome-text01 {
position: absolute;
width: 64.6vw;
height: 5vh;
left: 27.5vw;
top: 10vh;
}

.welcome-text02 {
position: absolute;
width: 64.6vw;
height: 5vh;
left: 38vw;
top: 18vh;
}

.welcome-text03 {
position: absolute;
width: 28vw;
height: 14vh;
left: 38vw;
bottom: 2vh;
}

.flex {
display: flex;
justify-content: space-between;
gap: 10px;
padding-left: 3.4vw;
padding-right: 3.4vw;
}

.step-card {
margin-top: 7.2vh;
width: 21.4vw;
height: 38vh;
background-color: white;
border-radius: 20px;
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
text-align: center;
transition: transform 0.3s ease;
}

.step-card:hover {
transform: scale(1.05);
}

.step-card img {
width: 100%;
border-radius: 10px 10px 0 0;
}

.step-card h3 {
color: #0066cc;
font-size: 1.2em;
margin-top: 10px;
}

.step-card p {
font-size: 1em;
color: #333;
margin-top: 5px;
}

.hidden-input {
opacity: 100;
height: 1;
overflow: hidden;
}

input {
caret-color: #0066cc;
border: 2px solid #ccc;
padding: 10px;
font-size: 16px;
transition: border-color 0.3s ease;
}

input:focus {
outline: none;
border-color: #0066cc;
box-shadow: 0 0 8px rgba(0, 102, 204, 0.6);
}

input:focus {
caret-width: 3px;
}

input::placeholder {
color: #888;
}
</style>