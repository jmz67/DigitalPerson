<template>

    <div class="layout">
        
        <!-- 顶部区域 -->
        <div class="top-area">

            <!-- 顶部内容 -->
            <div class="top-content">
                
                <img class="logo" src="../assets/logo@2x.png" alt="logo">

                <img class="welcome-text01" src="../assets/标题@3x.svg" alt="welcome-text01">

                <div class="welcome-text02">
                    <p class="text-blue-800 text-[1.6vw] max-w-[47vw]">在这里我们将提前收集您的就诊信息，以协助专家诊疗，下面请您跟着我们的指令，开始吧!</p>
                </div>

                <img class="welcome-text03" src="../assets/气泡@2x.png" alt="welcome-text03">
            </div>

        </div>

        <!-- 底部区域 -->
        <div class="bottom-area">

            <div class="flex">
                
                <!-- STEP 1 -->
                <a href="/wzchat/#/chat" class="step-card">
                    <img src="../assets/AI预问诊@2x.png" alt="AI预问诊">
                    <h3>STEP 1</h3>
                    <p>AI 预问诊</p>
                </a>

                <!-- STEP 2 -->
                <div class="step-card">
                    <img src="../assets/把脉@2x.png" alt="中医舌脉信息采集指引">
                    <h3>STEP 2</h3>
                    <p>中医舌脉信息采集指引</p>
                </div>

                <!-- STEP 3 -->
                <div class="step-card">
                    <img src="../assets/血压采集@2x.png" alt="身高体重血压信息采集指引">
                    <h3>STEP 3</h3>
                    <p>身高体重血压信息采集指引</p>
                </div>

                <!-- STEP 4 -->
                <div class="step-card">
                    <img src="../assets/生成报告.png" alt="生成问诊报告智能辅助诊疗">
                    <h3>STEP 4</h3>
                    <p>生成问诊报告智能辅助诊疗</p>
                </div>


            </div>

        </div>


    </div>


</template>


<script setup>



</script>


<style scoped>  

/* 全局布局 */
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
    background-image: 
    linear-gradient(180deg, rgba(249,251,255,0.40) 0%, rgba(241,246,255,0.00) 100%);
}

/* 顶部内容样式 */
.top-content {
    position: absolute;
    top: 3.7vh; /* 距离顶部 3.7vh */
    left: 2.5vh; /* 距离左侧 2.5vh */
    right: 2.5vh; /* 距离右侧 2.5vh */
    height: 46.3vh; /* 自动计算内容高度 */
    border-radius: 24px 24px 0 0; /* 左上和右上角圆角 */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 可选，增加阴影效果 */
    overflow: hidden; /* 防止内容溢出 */
    background-image: linear-gradient(124deg, rgba(250,250,255,0.25) 0%, #E9F2F7 100%);
    border: 3px solid rgba(255,255,255,1);
    border-radius: 24px 24px 0 0;
    border-bottom: none;
}

.logo {
    position: relative;
    width: 7vw;
    height: 9vh;
    top: 2vh; /* 距离顶部 */
    left: 2.4vh; /* 距离左侧 */
}

.welcome-text01 {
    position: absolute;
    width: 64.6vw;
    height: 5vh;
    left: 27.5vw; /* 距离左侧 */
    top: 10vh; /* 距离顶部 */
}

.welcome-text02 {
    position: absolute;
    width: 64.6vw;
    height: 5vh;
    left: 38vw; /* 距离左侧 */
    top: 18vh; /* 距离顶部 */
}

.welcome-text03 {
    position: absolute;
    width: 28vw;
    height: 14vh;
    left: 38vw; /* 距离左侧 */
    bottom: 2vh; /* 距离底部 */
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

</style>