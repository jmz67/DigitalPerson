
<template>
<div class="auth-container">
    <h2>登录</h2>
    <form @submit.prevent="handleLogin">
    <div class="form-group">
        <label for="username">用户名：</label>
        <input v-model="username" id="username" type="text" required />
    </div>
    <div class="form-group">
        <label for="password">密码：</label>
        <input v-model="password" id="password" type="password" required />
    </div>
    <button type="submit">登录</button>
    </form>
    <p>
    没有账号？
    <router-link to="/register">注册</router-link>
    </p>
    <div v-if="errorMessage" class="error-message">
    {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="success-message">
    {{ successMessage }}
    </div>
</div>
</template>

<script>
import api from '../axios';
import { useAuthStore } from '../store';
import { useRouter } from 'vue-router';

export default {
name: 'Login',
data() {
    return {
    username: '',
    password: '',
    errorMessage: '',
    successMessage: '',
    };
},
methods: {
    async handleLogin() {
    this.errorMessage = '';
    this.successMessage = '';
    try {
        // 使用 OAuth2PasswordRequestForm 格式
        const params = new URLSearchParams();
        params.append('username', this.username);
        params.append('password', this.password);
        // params.append('grant_type', 'password'); // 根据 FastAPI 的 OAuth2 配置

        const response = await api.post('/login', params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });

        const { access_token } = response.data;
        const authStore = useAuthStore();
        authStore.setToken(access_token);

        // 获取用户信息
        const userResponse = await api.get('/users/me');
        authStore.setUser(userResponse.data);

        this.successMessage = '登录成功！';
        this.$router.push('/report');
    } catch (error) {
        console.error(error);
        this.errorMessage = error.response?.data?.detail || '登录失败，请重试。';
    }
    },
},
};
</script>

<style scoped>
.auth-container {
max-width: 400px;
margin: 100px auto;
padding: 20px;
background: #ffffff;
border-radius: 8px;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.auth-container h2 {
text-align: center;
margin-bottom: 20px;
}

.auth-container form .form-group {
margin-bottom: 15px;
}

.auth-container label {
display: block;
margin-bottom: 5px;
}

.auth-container input {
width: 100%;
padding: 8px;
box-sizing: border-box;
}

.auth-container button {
width: 100%;
padding: 10px;
background-color: #007bff;
border: none;
color: #fff;
border-radius: 4px;
cursor: pointer;
}

.auth-container button:hover {
background-color: #0056b3;
}

.auth-container p {
text-align: center;
margin-top: 10px;
}

.error-message {
margin-top: 15px;
color: #ff4d4f;
text-align: center;
}

.success-message {
margin-top: 15px;
color: #28a745;
text-align: center;
}
</style>
  