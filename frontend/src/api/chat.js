// src/api/chat.js
import axios from 'axios';
// import { useAuthStore } from '../store'; // 假设您使用 Pinia 或 Vuex
// import router from '../router';

// 创建一个 Axios 实例，基础 URL 指向 FastAPI 的 /api 路径
const chatApi = axios.create({
  baseURL: '/api/v2', // 请根据您的实际 FastAPI 服务器地址进行调整
  headers: {
    'Content-Type': 'application/json',
  },
});

// // 请求拦截器，添加认证头
// chatApi.interceptors.request.use(
//   (config) => {
//     const authStore = useAuthStore();
//     if (authStore.token) {
//       config.headers.Authorization = `Bearer ${authStore.token}`;
//     }
//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );

// // 响应拦截器，处理错误
// chatApi.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     if (error.response && error.response.status === 401) {
//       const authStore = useAuthStore();
//       authStore.logout();
//       router.push('/login');
//       alert('身份验证失败，请重新登录。');
//     }
//     return Promise.reject(error);
//   }
// );

// API 调用函数

/**
 * 创建新的对话
 * @param {number} patientId - 患者的ID
 * @returns {Promise} - Axios响应
 */
export const createConversation = (patient_id, conversation_id) => {
  return chatApi.post('/createConversation', { patient_id, conversation_id });
};

/**
 * 保存消息到对话
 * @param {number} conversationId - 对话的ID
 * @param {string} sender - 发送者（'user' 或 'assistant'）
 * @param {string} text - 消息内容
 * @returns {Promise} - Axios响应
 */
export const saveMessage = (conversation_id, sender, text) => {
  return chatApi.post('/saveMessage', {
    conversation_id,
    sender,
    text,
  });
};

/**
 * 发送聊天消息并获取助手回复
 * @param {string} text - 消息内容
 * @param {number} conversation_id - 对话的ID
 * @param {string} sid - 会话ID（可选，根据需要）
 * @returns {Promise} - Axios响应
 */
export const sendChatMessage = (message, conversation_id, sid) => {
  return chatApi.post('/chatMessage', {
    message: message,
    conversation_id: conversation_id,
    sid: sid,
  });
};

/**
 * 获取对话的聊天历史
 * @param {number} conversationId - 对话的ID
 * @returns {Promise} - Axios响应
 */
export const getChatHistory = (conversationId) => {
  return chatApi.get(`/chatHistory/${conversationId}`);
};

// 导出 Axios 实例（如果需要）
export default chatApi;
