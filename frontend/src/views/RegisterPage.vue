
<template>
<div class="auth-container">
    <h2>注册</h2>
    <form @submit.prevent="handleRegister">
    <div class="form-group">
        <label for="username">用户名：</label>
        <input v-model="username" id="username" type="text" required />
    </div>
    <div class="form-group">
        <label for="password">密码：</label>
        <input v-model="password" id="password" type="password" required />
    </div>
    <button type="submit">注册</button>
    </form>
    <p>
    已有账号？
    <router-link to="/login">登录</router-link>
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

export default {
name: 'Register',
data() {
    return {
    username: '',
    password: '',
    errorMessage: '',
    successMessage: '',
    };
},
methods: {
    async handleRegister() {
    this.errorMessage = '';
    this.successMessage = '';
    try {
        await api.post('/register', {
        username: this.username,
        password: this.password,
        });
        this.successMessage = '注册成功！请登录。';
        // 延迟几秒后跳转，或立即跳转
        setTimeout(() => {
        this.$router.push('/login');
        }, 1500);
    } catch (error) {
        this.errorMessage = error.response?.data?.detail || '注册失败，请重试。';
    }
    },
},
};
</script>

<style scoped>
/* 与 Login.vue 相同的样式 */
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
background-color: #28a745;
border: none;
color: #fff;
border-radius: 4px;
cursor: pointer;
}

.auth-container button:hover {
background-color: #218838;
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
  