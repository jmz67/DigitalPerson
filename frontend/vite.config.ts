import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],

  base: './',

  server: {
    port: 5178, 
    host: "localhost",
    open: true,
    proxy: {
        // '/api' 可以理解为 请求目标地址的标识符，也可以使用其他命名代替
        "/api": {
            target: "http://127.0.0.1:5000/v1",
            changeOrigin: true, //是否跨域
            ws: true, //是否代理 websockets
            secure: false, //是否https接口
            rewrite: (path) => path.replace(/^\/api/, ""),
        },
    },
},
  
  css: {
    postcss: './postcss.config.js', // 指定 PostCSS 配置文件
  },

});
