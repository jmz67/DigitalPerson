import axios from 'axios';

/**
 * 获取患者基本信息
 * @returns {Promise<Object>} 患者信息对象
 */
export async function fetchPatientInfo() {
    try {
      const response = await axios.get('http://127.0.0.1:5000/v2/patientInfo');
      return response.data;
    } catch (error) {
      console.error('Error fetching patient info:', error);
      throw error;
    }
}

export async function fetchPatientDetail(opcId) {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/v2/patientDetail/${opcId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching patient detail:', error);
    throw error;
  }
}