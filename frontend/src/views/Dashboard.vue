<!-- src/views/Dashboard.vue -->
<template>
<div class="dashboard-container">
    <header class="dashboard-header">
    <h1>仪表盘</h1>
    <div class="user-info">
        <span>当前用户: {{ user.username }}</span>
        <button @click="logout" class="logout-button">退出登录</button>
    </div>
    </header>
    <nav class="dashboard-nav">
    <router-link to="/report">报告</router-link>
    <router-link to="/chat">聊天</router-link>
    <router-link to="/pro-test">测试</router-link>
    <!-- 添加更多链接根据需要 -->
    </nav>
    <main class="dashboard-main">
    <div v-if="loading" class="loading">
        加载中...
    </div>
    <div v-else>
        <p>欢迎来到您的仪表盘！</p>
        <!-- 更多内容 -->
    </div>
    </main>
</div>
</template>

<script>
import { useAuthStore } from '../store/index.js';
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import api from '../axios';

export default {
name: 'Dashboard',
setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const loading = ref(true);
    const reportData = ref(null);

    const logout = () => {
    authStore.logout();
    router.push('/login');
    };

    const fetchReport = async () => {
    try {
        const response = await api.get('/report');
        reportData.value = response.data;
    } catch (error) {
        console.error('无法获取报告数据。');
    } finally {
        loading.value = false;
    }
    };

    onMounted(() => {
    fetchReport();
    });

    return {
    user: authStore.user,
    logout,
    loading,
    reportData,
    };
},
};
</script>

<style scoped>
.dashboard-container {
display: flex;
flex-direction: column;
height: 100vh;
}

.dashboard-header {
display: flex;
justify-content: space-between;
align-items: center;
background-color: #007bff;
color: white;
padding: 15px 30px;
}

.user-info {
display: flex;
align-items: center;
}

.logout-button {
margin-left: 20px;
padding: 8px 16px;
background-color: #dc3545;
border: none;
color: white;
border-radius: 4px;
cursor: pointer;
}

.logout-button:hover {
background-color: #c82333;
}

.dashboard-nav {
background-color: #f1f1f1;
padding: 10px 30px;
display: flex;
gap: 15px;
}

.dashboard-nav a {
text-decoration: none;
color: #007bff;
}

.dashboard-nav a:hover {
text-decoration: underline;
}

.dashboard-main {
flex: 1;
padding: 20px 30px;
background-color: #f8f9fa;
}

.loading {
font-size: 18px;
color: #555;
}
</style>
  