// src/store/index.js
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user')) || null,
    scanCode: '', 
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    setToken(token) {
      this.token = token;
      localStorage.setItem('token', token);
    },
    setUser(user) {
      this.user = user;
      localStorage.setItem('user', JSON.stringify(user));
    },
    setScanCode(scanCode) {
      this.scanCode = scanCode; 
    },
    logout() {
      this.token = '';
      this.user = null;
      this.scanCode = ''; 
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    },
  },
});
