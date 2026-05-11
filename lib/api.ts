export type PredictionResult = {
  food: string;
  serving: string;
  calories: number;
  confidence: number;
  model_type: string;
  bmi: number;
  bmi_category: string;
  recommendation: string;
  action_items: string[];
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export async function scanFood(params: {
  image: File;
  heightCm: string;
  weightKg: string;
}): Promise<PredictionResult> {
  const formData = new FormData();
  formData.append("image", params.image);
  formData.append("height_cm", params.heightCm);
  formData.append("weight_kg", params.weightKg);

  const response = await fetch(`${API_URL}/predict`, {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(error?.detail ?? "Food scan failed. Please try another image.");
  }

  return response.json();
}
