<template>
    <div class="center-container">
      <input ref="inputRef" class="centered-input" />
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  
  const inputRef = ref(null)
  
  onMounted(() => {
    inputRef.value.focus()
  })
  </script>
  
  <style scoped>
  .center-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* 视口高度 */
    margin: 0;
  }
  
  .centered-input {
    /* 可选：为输入框添加一些样式 */
    padding: 10px;
    font-size: 16px;
  }
  </style>