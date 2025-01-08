// src/auth.js
import axios from 'axios';
import { useAuthStore } from '../store';
import router from '../router';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/v2/auth',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器，添加认证头
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器，处理错误
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore();
      authStore.logout();
      router.push('/login');
      // 这里可以使用组件内的状态来显示错误消息
      // 例如，通过事件总线或状态管理来触发
      alert('身份验证失败，请重新登录。');
    }
    return Promise.reject(error);
  }
);

export default api;
