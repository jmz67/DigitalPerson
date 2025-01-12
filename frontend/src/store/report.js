// src/store/report.js
import { defineStore } from 'pinia';

export const useReportStore = defineStore('report', {
  state: () => ({
    patientBasicInfo: {},
    patientDetailedInfo: {},
    lastAIReply: '',
  }),
  actions: {
    setReportData(basicInfo, detailedInfo, lastAIReply) {
      this.patientBasicInfo = basicInfo;
      this.patientDetailedInfo = detailedInfo;
      this.lastAIReply = lastAIReply;
    },
    clearReportData() {
      this.patientBasicInfo = {};
      this.patientDetailedInfo = {};
      this.lastAIReply = '';
    },
  },
});
