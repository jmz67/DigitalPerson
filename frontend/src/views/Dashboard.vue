<template>
<div :class="['dashboard-container', { 'sidebar-collapsed': isCollapsed }]">
    <!-- 侧边栏 -->
    <aside
    class="dashboard-sidebar"
    :style="sidebarStyle"
    ref="sidebarRef"
    >
    <!-- 收起/展开按钮 -->
    <div class="sidebar-toggle" @click="toggleSidebar">
        <font-awesome-icon
        :icon="isCollapsed ? 'fa-solid fa-chevron-right' : 'fa-solid fa-chevron-left'"
        />
    </div>

    <!-- 拖拽把手：仅在展开状态下显示，且在拖拽中禁用 transition -->
    <div
        v-if="!isCollapsed"
        class="resize-handle"
        @mousedown.stop.prevent="startResize"
        :style="{ transition: isResizing ? 'none' : '' }"
    ></div>

    <div class="sidebar-content">
        <div class="sidebar-logo">
            <div v-if="!isCollapsed" class="logo-content">
                <!-- 替换为你的 LOGO -->
                <div>Logo</div>
            </div>
            <div v-else class="logo-placeholder">
                <!-- 可选：收起时的 Logo 缩略图或保持空白 -->
                <div></div>
            </div>
        </div>

        <router-link to="/" class="sidebar-item">   
            <font-awesome-icon icon="fa-solid fa-house" class="sidebar-icon" />
            <span class="sidebar-text">问诊系统首页</span>
        </router-link>


        <!-- 导航示例：报告 -->
        <router-link to="/report" class="sidebar-item">
            <font-awesome-icon icon="fa-solid fa-chart-bar" class="sidebar-icon" />
            <span class="sidebar-text">患者报告</span>
        </router-link>

        <!-- 导航示例：聊天 -->
        <router-link to="/chat" class="sidebar-item">
            <font-awesome-icon icon="fa-solid fa-comments" class="sidebar-icon" />
            <span class="sidebar-text">预问诊对话</span>
        </router-link>

        <!-- 导航示例：设置 -->
        <!-- <router-link to="/settings" class="sidebar-item">
            <font-awesome-icon icon="fa-solid fa-cog" class="sidebar-icon" />
            <span class="sidebar-text">设置</span>
        </router-link> -->
    </div>
    </aside>

    <!-- 主体内容区域 -->
    <div class="main-content">
        <header class="dashboard-header">
            <h1>控制面板</h1>
            <div class="user-info">
                <span>当前用户：{{ user.username }}</span>
                <button 
                    @click="logout" 
                    class="ml-5 px-4 py-2 bg-gradient-to-r from-red-500 to-red-600 border-none text-white rounded-md 
                    hover:bg-gradient-to-r hover:from-red-600 hover:to-red-600 transition duration-200 focus:outline-none">
                    退出登录
                </button>
            </div>
        </header>

        <main class="dashboard-main">
            <!-- 欢迎 Banner 示例 -->
            <section class="bg-gradient-to-r from-blue-400 to-blue-500 text-white rounded-lg p-5 mb-5 flex items-center">
                <div class="flex flex-col justify-center">
                    <h2 class="text-xl font-semibold">欢迎回来，{{ user.username }}！</h2>
                    <p class="mt-2 text-base">这里是您的控制中心，可在此查看实时统计和进行管理</p>
                </div>
            </section>

        </main>
    </div>
</div>
</template>
  

<script>
import { useAuthStore } from '../store/index.js';
import { useRouter } from 'vue-router';
import { ref, onMounted, computed } from 'vue';
import api from '../api/auth.js';

export default {
  name: 'Dashboard',
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    
    const loading = ref(true);
    const reportData = ref(null);

    // 是否收起
    const isCollapsed = ref(false);

    // 控制侧边栏展开时的自由宽度
    const sidebarExpandedWidth = ref(280); // 默认展开时 280px
    const minWidth = 140;
    const maxWidth = 600;

    // 拖拽中标志
    const isResizing = ref(false);

    // DOM 引用
    const sidebarRef = ref(null);

    // 拉取报告数据（例）
    const fetchReport = async () => {
      try {
        const response = await api.get('/report');
        reportData.value = response.data;
      } catch (error) {
        console.error('无法获取报告数据。', error);
      } finally {
        loading.value = false;
      }
    };

    // 退出登录
    const logout = () => {
      authStore.logout();
      router.push('/login');
    };

    // 切换收起/展开
    const toggleSidebar = () => {
      isCollapsed.value = !isCollapsed.value;
      if (isCollapsed.value) {
        // 收起时保存当前宽度
        savedWidth.value = sidebarExpandedWidth.value;
        sidebarExpandedWidth.value = 60; // 收起时宽度
      } else {
        // 展开时恢复之前的宽度
        sidebarExpandedWidth.value = savedWidth.value || 280;
      }
    };

    // 保存收起前的宽度
    const savedWidth = ref(sidebarExpandedWidth.value);

    // 拖拽
    let startX = 0;
    let startWidth = 0;

    const startResize = (e) => {
      if (isCollapsed.value) return; // 收起状态不允许拖拽

      isResizing.value = true;
      startX = e.clientX;
      startWidth = sidebarExpandedWidth.value;

      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', stopResize);
    };

    const handleMouseMove = (e) => {
      const dx = e.clientX - startX;
      let newWidth = startWidth + dx;
      if (newWidth < minWidth) newWidth = minWidth;
      if (newWidth > maxWidth) newWidth = maxWidth;
      sidebarExpandedWidth.value = newWidth;
    };

    const stopResize = () => {
      isResizing.value = false;
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', stopResize);
    };

    // 动态计算侧边栏的宽度 & 过渡
    const sidebarStyle = computed(() => {
      const widthValue = isCollapsed.value ? 60 : sidebarExpandedWidth.value;
      return {
        width: widthValue + 'px',
        transition: isResizing.value ? 'none' : 'width 0.3s cubic-bezier(0.4,0.0,0.2,1)',
      };
    });

    onMounted(() => {
      fetchReport();
    });

    return {
      user: authStore.user,
      loading,
      reportData,
      isCollapsed,
      toggleSidebar,
      sidebarStyle,
      sidebarRef,
      isResizing,
      startResize,
      logout,
    };
  },
};
</script>


<style scoped>
/* 
* 关键思路：
* 1) 用 isCollapsed + sidebarExpandedWidth 实现 收起(60px)/展开(自定义宽度) 
* 2) 当 !isCollapsed 时，可拖拽 .resize-handle 改变 sidebarExpandedWidth
* 3) 拖拽时 isResizing=true -> transition: none，保证拖拽顺畅
* 4) 收起/展开时的动画用 transition: width 0.3s
* 5) 固定 .sidebar-item 的高度 & line-height，避免视觉跳动
*/

/* 基础 */
html, body {
  margin: 0;
  padding: 0;
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f5f5;
}

.dashboard-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background-color: #ffffff;
  position: relative;
}

/* 侧边栏 */
.dashboard-sidebar {
  position: relative;
  background-color: #f9f9f9;
  border-right: 1px solid #dee2e6;
  box-sizing: border-box;
  user-select: none;
  overflow: hidden;
  /* 微弱阴影 */
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* 收起时 80px 宽 */
.dashboard-container.sidebar-collapsed .dashboard-sidebar {
  width: 80px !important;
}

/* 收起/展开按钮 */
.sidebar-toggle {
  position: absolute;
  top: 16px;
  right: 12px;
  width: 24px;
  height: 24px;
  cursor: pointer;
  color: #666;
  text-align: center;
  line-height: 24px;
  z-index: 2;
}

/* 拖拽把手 */
.resize-handle {
  position: absolute;
  top: 0;
  right: 0;
  width: 6px;
  height: 100%;
  cursor: ew-resize;
  z-index: 999; /* 确保优先捕获鼠标事件 */
  background-color: transparent; /* 可选：添加背景颜色以更易于拖拽 */
}

/* 侧边栏内容区域 */
.sidebar-content {
  padding-top: 60px; /* 与 .sidebar-logo 的高度相同 */
  padding: 10px; 
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1; /* 确保内容区域填满侧边栏 */
}


/* LOGO 示例 */
.sidebar-logo {
  text-align: center;
  height: 60px; /* 固定高度，确保布局一致 */
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-content, .logo-placeholder {
  transition: opacity 0.3s;
}

.logo-placeholder {
  /* 可选：样式调整 */
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
  opacity: 0; /* 初始隐藏 */
}

.dashboard-container.sidebar-collapsed .logo-content {
  opacity: 0;
}

.dashboard-container.sidebar-collapsed .logo-placeholder {
  opacity: 1;
}

/* 导航项：固定高度48px，避免收起/展开时的高度跳动 */
.sidebar-item {
  display: flex;
  align-items: center;
  height: 48px;
  line-height: 48px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  border-radius: 6px;
  color: #333;
  text-decoration: none;
  transition: background-color 0.2s;
  padding: 0 16px;
  font-size: 0.95rem;
}

.sidebar-item:hover {
  background-color: #e2e6ea;
}

/* 图标与文字的间距 */
.sidebar-icon {
  margin-right: 12px;
  min-width: 20px;
  text-align: center;
}

/* 可选：收起状态时隐藏文字 */
.dashboard-container.sidebar-collapsed .sidebar-text {
  display: none;
}

/* 主体区域 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

/* 顶部 */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  border-bottom: 1px solid #dee2e6;
  padding: 15px 30px;
  box-sizing: border-box;
}

.dashboard-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.user-info {
  display: flex;
  align-items: center;
}

/* 主区域 */
.dashboard-main {
  flex: 1;
  padding: 20px 30px;
  overflow-y: auto;
  box-sizing: border-box;
  background-color: #fafafa;
}

/* 加载提示 */
.loading {
  font-size: 18px;
  color: #555;
  text-align: center;
  margin-top: 40px;
}

/* 网格布局 */
.dashboard-content-layout {
  display: grid;
  grid-template-columns: 2fr 1fr; 
  grid-auto-rows: min-content;
  gap: 20px;
}

/* 卡片示例 */
.info-card {
  background-color: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.06);
  transition: box-shadow 0.2s;
}

.info-card:hover {
  box-shadow: 0 6px 12px rgba(0,0,0,0.08);
}

.info-card h2 {
  margin-top: 0;
  font-size: 1.1rem;
  margin-bottom: 12px;
}

/* 占据两列 */
.large-card {
  grid-column: 1 / span 2;
}

/* 统计 */
.statistics {
  display: flex;
  gap: 30px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 120px;
}

.stat-title {
  color: #666;
  font-size: 0.85rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  margin-top: 8px;
}

/* 快捷操作 */
.quick-actions {
  display: flex;
  gap: 10px;
}

.quick-button {
  padding: 6px 12px;
  background-color: #007bff;
  border-radius: 4px;
  border: none;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.2s;
}

.quick-button:hover {
  background-color: #0056b3;
}

/* 最新消息列表 */
.news-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.news-list li {
  margin-bottom: 6px;
}

/* 通用按钮 */
.action-button {
  padding: 8px 12px;
  background-color: #007bff;
  border-radius: 4px;
  border: none;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.2s;
}

.action-button:hover {
  background-color: #0056b3;
}
</style>

  