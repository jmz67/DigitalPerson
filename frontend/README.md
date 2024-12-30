# 数字人前端页面

## 开发指南

### 和 APP 交互

为了能够和 APP 进行交互，我们做出了如下的修改：

1. 新增数据字段

我们将在 data() 中新增字段，用户缓存发送用户消息给后端之后返回的回答和推荐回答，暂不显示，等待 APP 调用 `receiveDigitalPersonBroadcastData` 方法后显示它们。

`pendingAssistantMessage` : 用于暂存从后端获取但尚未显示的医生问句。

`pendingRecommendations` : 用于暂存从后端获取但尚未显示的推荐回答列表。

`showAssistantMessage` : 布尔值，表示是否已收到 App 的回调来显示消息和推荐回答，初始为 false。


2. 修改消息的显示逻辑

- 当发送消息给后端并收到回应之后，我们不再直接将回应（用户问句和推荐回答）显示到 `messages` 数组中，而是存入 `pendingAssistantMessage` 和 `pendingRecommendations` 。`messages` 中先用一个 `loading` 类型消息占位。

- 一旦 App 调用 `receiveDigitalPersonBroadcastData` 方法，才替换该 `loading` 消息为实际的医生消息并显示推荐回答。

3. 新增全局方法

在 `mounted()` 或是 `created()` 中为 window 对象添加两个全局方法，供 APP 调用：

- `window.receiveDigitalPersonBroadcastData = (param) => {...}` ：
App 调用此方法表示数字人开始播报，这时前端从 `pendingAssistantMessage` 和 `pendingRecommendations` 中取出数据，更新 messages 的内容和显示推荐回答。更新 `showAssistantMessage` 为 true 并执行原有显示逻辑。

- `window.receiveDigitalPersonIdentifyData = (param) => {...}` ：
当 App 调用此方法并传回已识别的文本内容时，将此内容填入输入框 input 中，方便用户编辑后发送。

我们这里暂时定义的方法参数为：

```js
/**
         * 处理来自App的数字人广播数据
         * @param {Object} param - 接收到的参数对象
         * @param {string} param.action - 操作类型，固定为 "BROADCAST_START"
         * @param {string} param.sessionId - 会话唯一标识
         * @param {string} param.timestamp - ISO 8601 格式的时间戳
         * @param {string} param.messageId - 消息唯一标识
         * @param {string} param.speaker - 发言者，例如 "DoctorAI"
         * @param {number} [param.confidenceScore] - 可选：置信度分数（0到1之间）
         * @returns {Object} - 响应对象
         */
        window.receiveDigitalPersonBroadcastData = ({ action, sessionId, timestamp, messageId, speaker, confidenceScore }) => {
            if (action !== "BROADCAST_START") {
                return {
                    status: "ERROR",
                    code: 400,
                    timestamp: new Date().toISOString(),
                    message: "Invalid action type"
                };
            }

            if (!this.showAssistantMessage) {
                this.showPendingAssistantMessage();
            }

            return {
                status: "SUCCESS",
                code: 200,
                timestamp: new Date().toISOString(),
                message: "Assistant message displayed successfully",
                displayedMessageId: messageId || null
            };
        };

        /**
         * 处理来自App的语音识别数据
         * @param {Object} param - 接收到的参数对象
         * @param {string} param.action - 操作类型，固定为 "IDENTIFY_TEXT"
         * @param {string} param.sessionId - 会话唯一标识
         * @param {string} param.timestamp - ISO 8601 格式的时间戳
         * @param {string} param.content - 语音转文本内容
         * @param {string} param.language - 语言代码，例如 "zh-CN"
         * @param {number} [param.confidenceScore] - 可选：识别置信度分数（0到1之间）
         * @returns {Object} - 响应对象
         */
        window.receiveDigitalPersonIdentifyData = ({ action, sessionId, timestamp, content, language, confidenceScore }) => {
            if (action !== "IDENTIFY_TEXT") {
                return {
                    status: "ERROR",
                    code: 400,
                    timestamp: new Date().toISOString(),
                    message: "Invalid action type"
                };
            }

            if (content) {
                this.input = content;
            }

            return {
                status: "SUCCESS",
                code: 200,
                timestamp: new Date().toISOString(),
                message: "Input field updated successfully",
                recognizedContent: content || ""
            };
        };
```

4. 交互流程：

- 用户在输入框输入问题并发送后端，后端返回数据后，前端仅将数据缓存（`pendingAssistantMessage` 、`pendingRecommendations`），不显示。

- 等待 App 调用 `receiveDigitalPersonBroadcastData()` 时，才将缓存的消息渲染到界面。

- 当 App 调用 `receiveDigitalPersonIdentifyData()` 时，将识别到的文本填入输入框。

我们可以打开后端服务，然后进行测试：

```js
const broadcastParams = {
    action: "BROADCAST_START",
    sessionId: "unique-session-id-123",
    timestamp: new Date().toISOString(),
    messageId: "msg-id-456",
    speaker: "DoctorAI",
    confidenceScore: 0.9 // 可选
};

// 调用 receiveDigitalPersonBroadcastData 方法
const broadcastResponse = window.receiveDigitalPersonBroadcastData(broadcastParams);
console.log(broadcastResponse);
```

```js
const identifyParams = {
    action: "IDENTIFY_TEXT",
    sessionId: "unique-session-id-123",
    timestamp: new Date().toISOString(),
    content: "这是语音识别的内容。",
    language: "zh-CN",
    confidenceScore: 0.85 // 可选
};

// 调用 receiveDigitalPersonIdentifyData 方法
const identifyResponse = window.receiveDigitalPersonIdentifyData(identifyParams);
console.log(identifyResponse);
```