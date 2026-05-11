"use client";

import { ChangeEvent, FormEvent, useMemo, useState } from "react";
import { Activity, Camera, Gauge, Loader2, Scale, Sparkles, Utensils } from "lucide-react";
import { PredictionResult, scanFood } from "@/lib/api";

export default function Home() {
  const [image, setImage] = useState<File | null>(null);
  const [heightCm, setHeightCm] = useState("165");
  const [weightKg, setWeightKg] = useState("60");
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const previewUrl = useMemo(() => {
    if (!image) return "";
    return URL.createObjectURL(image);
  }, [image]);

  function handleImageChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0] ?? null;
    setImage(file);
    setResult(null);
    setError("");
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!image) {
      setError("Upload a food image first.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const prediction = await scanFood({ image, heightCm, weightKg });
      setResult(prediction);
    } catch (scanError) {
      setError(scanError instanceof Error ? scanError.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <section className="workspace" aria-label="Food calorie scanner">
        <div className="scanner-panel">
          <div className="brand-row">
            <div className="brand-mark">
              <Utensils size={24} />
            </div>
            <div>
              <h1>Food Calorie Scanner</h1>
              <p>Image based food detection with BMI guidance</p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="form-stack">
            <label className="upload-zone">
              <input type="file" accept="image/*" onChange={handleImageChange} />
              {previewUrl ? (
                <img src={previewUrl} alt="Uploaded food preview" />
              ) : (
                <span className="upload-empty">
                  <Camera size={34} />
                  <strong>Upload food image</strong>
                  <small>JPG, PNG, or WebP</small>
                </span>
              )}
            </label>

            <div className="input-grid">
              <label>
                <span>Height</span>
                <div className="input-with-unit">
                  <input
                    type="number"
                    min="80"
                    max="230"
                    value={heightCm}
                    onChange={(event) => setHeightCm(event.target.value)}
                  />
                  <b>cm</b>
                </div>
              </label>
              <label>
                <span>Weight</span>
                <div className="input-with-unit">
                  <input
                    type="number"
                    min="20"
                    max="220"
                    value={weightKg}
                    onChange={(event) => setWeightKg(event.target.value)}
                  />
                  <b>kg</b>
                </div>
              </label>
            </div>

            <button type="submit" disabled={loading}>
              {loading ? <Loader2 className="spin" size={20} /> : <Sparkles size={20} />}
              {loading ? "Scanning" : "Scan calories"}
            </button>
          </form>

          {error ? <p className="error">{error}</p> : null}
        </div>

        <div className="results-panel">
          <div className="panel-heading">
            <h2>Scan Result</h2>
            <span>{result ? result.model_type : "Ready"}</span>
          </div>

          {result ? (
            <>
              <div className="primary-result">
                <span>{result.food.replace("_", " ")}</span>
                <strong>{result.calories} kcal</strong>
                <small>{result.serving}</small>
              </div>

              <div className="metric-grid">
                <Metric icon={<Gauge size={20} />} label="Confidence" value={`${Math.round(result.confidence * 100)}%`} />
                <Metric icon={<Scale size={20} />} label="BMI" value={`${result.bmi}`} />
                <Metric icon={<Activity size={20} />} label="Category" value={result.bmi_category} />
              </div>

              <div className="recommendation">
                <h3>Recommendation</h3>
                <p>{result.recommendation}</p>
                <ul>
                  {result.action_items.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            </>
          ) : (
            <div className="empty-result">
              <Utensils size={42} />
              <p>Your calorie estimate and BMI recommendation will appear here after scanning.</p>
            </div>
          )}
        </div>
      </section>
    </main>
  );
}

function Metric({
  icon,
  label,
  value
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="metric">
      {icon}
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
