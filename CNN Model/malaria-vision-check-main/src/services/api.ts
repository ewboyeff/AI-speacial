
const API_BASE_URL = 'http://localhost:8000';

export interface PredictionResult {
  status: string;
  prediction: string;
  confidence: number;
}

export const predictMalaria = async (file: File): Promise<PredictionResult> => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    console.log('Sending request to API...', file.name);
    
    const response = await fetch(`${API_BASE_URL}/predict/`, {
      method: 'POST',
      body: formData,
    });

    console.log('Response status:', response.status);

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      console.error('API Error:', errorData);
      throw new Error(errorData?.detail || `Server xatosi: ${response.status}`);
    }

    const result = await response.json();
    console.log('API Response:', result);
    
    return result;
  } catch (error) {
    console.error('API call failed:', error);
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Tarmoq xatosi yuz berdi');
  }
};
