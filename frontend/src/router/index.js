// src/router/index.js

import { createRouter, createWebHashHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import ChatPage from '../views/ChatPage.vue';
import TestPage from '../views/TestPage.vue';
import ReportPage from '../views/ReportPage.vue';
import LoginPage from '../views/LoginPage.vue';
import RegisterPage from '../views/RegisterPage.vue';
import Dashboard from '../views/Dashboard.vue'; // 导入 Dashboard 组件
import { useAuthStore } from '../store/index.js'; // 正确导入 useAuthStore

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
    meta: { requiresAuth: true }, 
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
    meta: { requiresAuth: false }, 
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: RegisterPage,
    meta: { requiresAuth: false }, 
  },
  {
    path: '/chat',
    name: 'ChatPage',
    component: ChatPage,
    meta: { requiresAuth: true }, 
  },
  {
    path: '/report',
    name: 'ReportPage',
    component: ReportPage,
    meta: { requiresAuth: true }, 
  },
  {
    path: '/pro-test',
    name: 'TestPage',
    component: TestPage,
    meta: { requiresAuth: true }, 
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }, // 需要认证
  },
  // 处理未匹配的路由，重定向到主页或显示 404 页面
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes, // 提供路由规则
});

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    next('/dashboard'); // 登录后重定向到 Dashboard
  } else {
    next();
  }
});

export default router;
