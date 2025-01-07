<template>
    <div class="medical-record">
        <!-- 页首固定 -->
        <header class="header">
            <div>
                logo
            </div>
            <div class="header-center">
                <div class="title">白泽晓大模型</div>
            </div>
            <div class="header-right">
                <div class="date-time">{{ currentDateTime }}</div>
                <router-link to="/dashboard" class="admin-info">{{ user.username }}</router-link>
                <button @click="logout" class="logout-btn">退出</button>
            </div>
        </header>

        <!-- 滚动区域 -->
        <div class="content">
            <section 
                v-for="section in filteredReportSections" 
                :key="section.id" 
                :class="['report-section', section.layout === 'horizontal' ? 'horizontal-layout' : 'vertical-layout']"
            >
                <h2 class="section-title">{{ section.title }}</h2>
                <div class="info-container">
                    <p v-for="(item, index) in section.fields" :key="index">
                        <strong>{{ item.label }}：</strong>{{ item.value }}
                    </p>
                </div>
            </section>
        </div>

        <!-- 打印按钮固定在右下角 -->
        <div class="actions">
            <button @click="print">打印</button>
        </div>
    </div>
</template>

<script>
import { useAuthStore } from '../store/index.js'; // 导入 Pinia Store
import { computed, onMounted, ref } from 'vue'; // 确保导入了 ref
import { useRouter } from 'vue-router';

export default {
    name: "MedicalRecord",
    props: {
        // 通过 props 接收数据
        reportData: {
            type: Object,
            default: () => ({})
        }
    },
    setup(props) {
        const authStore = useAuthStore();
        const router = useRouter();

        // 计算属性获取当前用户
        const user = computed(() => authStore.user);

        // 计算属性获取就诊类型
        const visitType = computed(() => props.reportData.visitType || '复诊');

        // 定义报告部分
        const reportSections = computed(() => [
            {
                id: 1,
                title: "基本信息",
                layout: "horizontal",
                fields: [
                    { label: "就诊科室", value: props.reportData.department || "皮肤科" },
                    { label: "就诊医生", value: props.reportData.doctor || "陈宁刚" },
                    { label: "就诊日期", value: props.reportData.visitDate || "2025-1-14 9:30" },
                    { label: "就诊类型", value: visitType.value } // 动态值
                ],
            },
            {
                id: 2,
                title: "一般状况",
                layout: "horizontal",
                fields: [
                    { label: "过敏史", value: props.reportData.allergyHistory || "海鲜过敏；青霉素过敏；" },
                    { label: "身高", value: props.reportData.height || "178cm" },
                    { label: "体重", value: props.reportData.weight || "75kg" },
                    { label: "BMI", value: props.reportData.bmi || "23.6（正常）" },
                    { label: "体温", value: props.reportData.temperature || "36.8℃（体温正常）" },
                    { label: "收缩压", value: props.reportData.systolicBP || "135mmHg" },
                    { label: "舒张压", value: props.reportData.diastolicBP || "76mmHg（血压正常）" },
                ],
            },
            {
                id: 3,
                title: "中医四诊信息",
                layout: "horizontal",
                fields: [
                    { label: "舌相", value: props.reportData.tongue || "舌淡红" },
                    { label: "苔", value: props.reportData.coating || "黄苔，厚苔、腻苔" },
                    { label: "唇色", value: props.reportData.lipColor || "黯淡" },
                    { label: "面色", value: props.reportData.faceColor || "红黄隐隐，明润含蓄" },
                    { label: "脉", value: props.reportData.pulse || "滑脉" },
                ],
            },
            {
                id: 4,
                title: "本次就诊问题摘要",
                layout: "vertical",
                fields: [
                    { label: "症状", value: props.reportData.symptoms || "皮肤起红疹3天；部位：胳膊、胸前、背部；" },
                    { label: "用药情况", value: props.reportData.medication || "已自行服用氯雷他定，效果不佳；" },
                    { label: "病史", value: props.reportData.medicalHistory || "患有高血压、糖尿病；曾于2021-1-1日进行阑尾炎手术；" },
                    { label: "婚育情况", value: props.reportData.maritalStatus || "已婚已育；" },
                ],
            },
            {
                id: 5,
                title: "既往就诊情况摘要",
                layout: "vertical",
                fields: [
                    { label: "初次就诊", value: props.reportData.firstVisit || "您于2024-4-1日初次就诊，开立XXX药品，疗效良好；" },
                    { label: "第二次就诊", value: props.reportData.secondVisit || "于2024-4-8日第二次就诊，开立XXX药品，疗效良好；" },
                ],
            },
            {
                id: 6,
                title: "下次复诊提醒",
                layout: "vertical",
                fields: [
                    { label: "复诊时间", value: props.reportData.nextVisitReminder || "预计2024-4-22日前往医院进行复诊，请及时挂号就诊。" },
                ],
            },
        ]);

        // 根据 visitType 过滤报告部分
        const filteredReportSections = computed(() => {
            if (visitType.value === '初诊') {
                // 过滤掉 "既往就诊情况摘要" 部分
                return reportSections.value.filter(section => section.title !== "既往就诊情况摘要");
            }
            return reportSections.value;
        });

        // 当前日期时间
        const currentDateTime = ref(new Date().toLocaleString('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }));

        // 动态更新时间
        const updateDateTime = () => {
            setInterval(() => {
                currentDateTime.value = new Date().toLocaleString('zh-CN', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                });
            }, 60000); // 每分钟更新一次
        };

        // 退出登录
        const logout = () => {
            authStore.logout();
            router.push('/login');
        };

        // 打印功能
        const print = () => {
            window.print();
        };

        onMounted(() => {
            // 启动动态更新时间
            updateDateTime();
        });

        return {
            currentDateTime,
            filteredReportSections,
            user,
            logout,
            print
        };
    }
};
</script>

<style scoped>
/* 引入更现代的字体 */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

.medical-record {
    font-family: 'Roboto', sans-serif;
    display: flex;
    flex-direction: column;
    height: 100vh;
    background: #f5f7fa; /* 更柔和的背景色 */
}

/* 页首样式 */
.header {
    display: flex;
    align-items: center;
    background-color: #ffffff;
    padding: 15px 30px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 1000;
    box-sizing: border-box;
}

.header-center {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
}

.title {
    font-size: 20px;
    font-weight: 600;
    color: #333;
}

.date-time {
    font-size: 14px;
    color: #888;
    margin-right: 5px;
}

.header-right {
    display: flex;
    align-items: center;
    margin-left: auto;
}

.admin-info {
    font-size: 14px;
    color: #555;
    margin-right: 15px;
    cursor: pointer;
    text-decoration: underline;
}

.admin-info:hover {
    color: #007bff;
}

/* 退出按钮样式 */
.logout-btn {
    background-color: #ff4d4f;
    color: #fff;
    border: none;
    padding: 8px 16px;
    cursor: pointer;
    border-radius: 4px;
    font-size: 14px;
    transition: background-color 0.2s ease;
}

.logout-btn:hover {
    background-color: #d9363e;
}

/* 内容区域 */
.content {
    flex: 1;
    margin-top: 80px; /* 调整固定头部的空间 */
    padding: 20px 40px;
    overflow-y: auto;
    box-sizing: border-box;
}

.report-section {
    background: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

.section-title {
    font-size: 18px;
    margin-bottom: 12px;
    color: #333;
    border-bottom: 2px solid #007bff;
    padding-bottom: 6px;
}

.info-container {
    display: flex;
    flex-wrap: wrap;
}

.horizontal-layout .info-container p {
    width: 45%;
    margin: 6px 0;
    font-size: 15px;
    color: #555;
}

.vertical-layout .info-container p {
    width: 100%;
    margin: 6px 0;
    font-size: 15px;
    color: #555;
}

/* 打印按钮样式 */
.actions {
    position: fixed;
    bottom: 20px;
    right: 30px;
}

.actions button {
    background: #28a745;
    color: white;
    border: none;
    padding: 12px 24px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 50px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    transition: background-color 0.2s ease, transform 0.2s ease;
}

.actions button:hover {
    background: #218838;
    transform: translateY(-2px);
}

/* 响应式设计调整 */
@media (max-width: 768px) {
    .header {
        flex-direction: column;
        align-items: flex-start;
        padding: 10px 20px;
    }

    .header-center {
        position: relative;
        left: 0;
        transform: none;
        margin-bottom: 10px;
        width: 100%;
        text-align: center;
    }

    .title {
        font-size: 18px;
    }

    .date-time {
        font-size: 12px;
    }

    .header-right {
        width: 100%;
        justify-content: flex-start;
    }

    .admin-info {
        margin-right: 10px;
    }

    .logout-btn {
        padding: 6px 12px;
        font-size: 13px;
    }

    .content {
        padding: 15px 20px;
    }

    .report-section {
        padding: 15px;
    }

    .section-title {
        font-size: 16px;
    }

    .horizontal-layout .info-container p {
        width: 100%;
    }

    .actions {
        bottom: 15px;
        right: 20px;
    }

    .actions button {
        padding: 10px 20px;
        font-size: 14px;
    }
}

/* 打印样式 */
@media print {
    .header,
    .actions {
        display: none; /* 隐藏页首和打印按钮 */
    }

    .content {
        margin: 0;
        padding: 0;
        overflow: visible;
        height: auto;
    }

    .report-section {
        page-break-inside: avoid;
    }

    body {
        -webkit-print-color-adjust: exact;
    }
}
</style>
