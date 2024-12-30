// 从 'vue-router' 库中导入 createRouter 和 createWebHashHistory 函数。
import { createRouter, createWebHashHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import ChatPage from '../views/ChatPage.vue';
import TestPage from '../views/TestPage.vue'

// 定义路由数组，每个对象代表一个路由规则。
const routes = [
  
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/chat',
    name: 'ChatPage',
    component: ChatPage,
  },
  {
    path: '/pro-test',
    name: 'TestPage',
    component: TestPage,
  }

];

// 创建路由器实例，并传入配置选项：
// 使用 createWebHashHistory 方法来创建历史管理器，这将使得 URL 中包含一个井号（#）以确保兼容性。
// 设置模式为 "hash"，虽然这里设置 mode 已经是默认行为，因此可以省略此属性。
// 将上面定义的路由规则传递给路由器。
const router = createRouter({
  history: createWebHashHistory(),
  // 注意：mode: "hash" 这一行是多余的，因为 createWebHashHistory() 默认就是 hash 模式。
  routes // 提供路由规则
});

// 导出路由器实例，以便可以在其他地方引入并使用。
export default router;