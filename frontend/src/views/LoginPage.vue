<template>
    <div class="auth-container">
      <div class="auth-header">
        <div class="mb-2">
            logo
        </div>
        <h2>数字人预问诊系统</h2>
        <p>登录进行数字人问诊，管理病人问诊记录</p>
      </div>
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <input
            v-model="username"
            id="username"
            type="text"
            placeholder="用户名"
            required
          />
        </div>
        <div class="form-group">
          <input
            v-model="password"
            id="password"
            type="password"
            placeholder="密码"
            required
          />
        </div>
        <div class="form-footer mb-4">
          <a href="#" class="forgot-password">忘记密码了？</a>
        </div>
        <button type="submit" class="btn-login">登录</button>
      </form>
      <p class="sign-up-text">
            没有账户吗？
        <router-link 
        to="/register" 
        class="text-blue-500 hover:text-blue-700 font-medium"
        >
            注册
        </router-link>
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
  import api from "../api/auth";
  import { useAuthStore } from "../store";
  import { useRouter } from "vue-router";
  
  export default {
    name: "Login",
    data() {
      return {
        username: "",
        password: "",
        errorMessage: "",
        successMessage: "",
      };
    },
    methods: {
      async handleLogin() {
        this.errorMessage = "";
        this.successMessage = "";
        try {
          const params = new URLSearchParams();
          params.append("username", this.username);
          params.append("password", this.password);
  
          const response = await api.post("/login", params, {
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
          });
  
          const { access_token } = response.data;
          const authStore = useAuthStore();
          authStore.setToken(access_token);
  
          const userResponse = await api.get("/users/me");
          authStore.setUser(userResponse.data);
  
          this.successMessage = "登录成功！";
          this.$router.push("/dashboard");
        } catch (error) {
          console.error(error);
          this.errorMessage =
            error.response?.data?.detail || "登录失败，请重试。";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* 背景整体样式 */
  body {
    background-color: #f9f9fc;
    font-family: "Inter", sans-serif;
  }
  
  /* 登录容器样式 */
  .auth-container {
    max-width: 360px;
    margin: 120px auto;
    padding: 20px;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  /* Header 样式 */
  .auth-header {
    margin-bottom: 20px;
  }
  
  .auth-header .logo {
    width: 60px;
    margin-bottom: 10px;
  }
  
  .auth-header h2 {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 8px;
  }
  
  .auth-header p {
    font-size: 14px;
    color: #666;
  }
  
  /* 表单样式 */
  .auth-form {
    text-align: left;
  }
  
  .auth-form .form-group {
    margin-bottom: 15px;
  }
  
  .auth-form input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    box-sizing: border-box;
  }
  
  .auth-form input:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 4px rgba(0, 123, 255, 0.4);
  }
  
  /* 按钮样式 */
  .btn-login {
    width: 100%;
    padding: 12px;
    background-color: #007bff;
    border: none;
    color: white;
    font-size: 16px;
    font-weight: bold;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .btn-login:hover {
    background-color: #0056b3;
  }
  
  /* 链接样式 */
  .forgot-password {
    font-size: 12px;
    color: #007bff;
    text-decoration: none;
  }
  
  .forgot-password:hover {
    text-decoration: underline;
  }
  
  /* 注册文本样式 */
  .sign-up-text {
    margin-top: 15px;
    font-size: 14px;
    color: #666;
  }
  
  /* 错误和成功消息样式 */
  .error-message {
    margin-top: 15px;
    color: #ff4d4f;
    font-size: 14px;
    text-align: center;
  }
  
  .success-message {
    margin-top: 15px;
    color: #28a745;
    font-size: 14px;
    text-align: center;
  }
  </style>
  