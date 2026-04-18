// This module sets up the base URL for API requests using environment variables.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

const buildVideoUrl = (fileId: number): string => `${API_BASE_URL}/video/${fileId}`;

/**
 * Backend from Flask API service URL
 */

export interface BackendPrediction {
  prediction_id: number;
  file_id: number;
  mass_prediction: number;
  model_version: string;
  created_at: string;
  file?: {
    file_id: number;
    file_name: string;
    file_type: 'RGB-D' | 'Depth';
    upload_date: string;
  };
}

export interface HealthCheckResponse {
  status: string;
  camera_connected: boolean;
  model_loaded: boolean;
}

export type BagFileType = 'RGB-D' | 'Depth';

export interface BagFile {
  file_id: number;
  file_name: string;
  file_type: string;
  file_path: string;
  upload_date: string | null;
}

// Response type for upload endpoint
export interface UploadResponse {
  message: string;
  file: {
    file_id: number;
    file_name: string;
    file_type: string;
    upload_date: string;
  };
  prediction: {
    prediction_id: number;
    mass_prediction: number;
    model_version: string;
    created_at: string;
  };
  pipeline_result: any;
  video_url: string;   // from backend
}

/**
 * Fetch all imported bag files from the backend.
 */
export async function getBagFiles(): Promise<BagFile[]> {
  const response = await fetch(`${API_BASE_URL}/api/files`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!response.ok) {
    throw new Error(`Error fetching bag files: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Upload a .bag file; backend saves it and inserts a record into the database.
 */
export async function uploadBagFile(file: File, fileType: BagFileType): Promise<UploadResponse> {
  console.log("=".repeat(50));
  console.log("Uploading file:", file.name, "of type:", fileType);
  console.log("File size:", file.size, "bytes");
  console.log("API URL:", `${API_BASE_URL}/api/upload`);

  const formData = new FormData();
  formData.append('file', file);
  formData.append('file_type', fileType);

  const response = await fetch(`${API_BASE_URL}/api/upload`, {
    method: 'POST',
    body: formData,
  });

  const text = await response.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch (e) {
    console.error("Failed to parse response as JSON:", e);
    throw new Error("Invalid response from server");
  }
  if (!response.ok) {
    throw new Error(data?.error || `Upload failed with status ${response.status}`);
  }

  console.log("✓ Upload successful!");
  console.log("=".repeat(50));
  return data as UploadResponse;
}

/**
 * Fetch all predictions from the backend API.
 * Adds videoUrl to each prediction using file_id.
 */
export async function getPredictions() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/predictions`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      throw new Error(`Error fetching predictions: ${response.statusText}`);
    }

    const data = await response.json();
    // Add videoUrl to each prediction using file_id from the nested file object
    return data.map((pred: any) => ({
      ...pred,
      videoUrl: pred.file?.file_id ? buildVideoUrl(pred.file.file_id) : undefined,
    }));
  } catch (error) {
    console.error('Error fetching predictions:', error);
    throw error;
  }
}

/**
 * Fetch latest prediction from the backend API.
 */
export async function getLatestPrediction() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/predictions/latest`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      throw new Error(`Error fetching latest prediction: ${response.statusText}`);
    }

    const data = await response.json();

    return data.map((pred: any) => ({
        ...pred,
        videoUrl: pred.file?.file_id ? buildVideoUrl(pred.file.file_id) : undefined,
    }));

  } catch (error) {
    console.error('Error fetching latest prediction:', error);
    throw error;
  }
}

/**
 * Check if backend is alive
 */
export async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(5000),
    });
    return response.ok;
  } catch (error) {
    console.error('Backend health check failed:', error);
    return false;
  }
}

/**
 * Get camera status
 */
export async function getCameraStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/camera/status`, {
      method: 'GET',
    });
    if (!response.ok) {
      return { camera_connected: false };
    }
    return response.json();
  } catch (error) {
    console.error('Failed to check camera status:', error);
    return { camera_connected: false };
  }
}

/**
 * Delete a single prediction
 */
export async function deletePrediction(predictionId: number) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/predictions/${predictionId}`, {
      method: 'DELETE',
    });
    return response.ok;
  } catch (error) {
    console.error('Error deleting prediction:', error);
    return false;
  }
}

/**
 * Delete all predictions
 */
export async function deleteAllPredictions() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/predictions`, {
      method: 'DELETE',
    });
    return response.ok;
  } catch (error) {
    console.error('Error deleting all predictions:', error);
    return false;
  }
}

/**
 * Export predictions as CSV
 */
export async function exportPredictionsCSV() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/predictions/export`, {
      method: 'GET',
    });
    if (!response.ok) {
      throw new Error('Failed to export predictions');
    }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `predictions_${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  } catch (error) {
    console.error('Error exporting predictions:', error);
  }
}