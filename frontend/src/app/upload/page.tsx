"use client";

import { useState } from "react";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);
    if (selectedFile) {
      setStatus(`📄 Selected: ${selectedFile.name}`);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setStatus("❌ No file selected.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setStatus("⏳ Uploading...");

    try {
      const res = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errorText = await res.text();
        console.error("Upload error response:", errorText);
        throw new Error("Upload failed");
      }

      const data = await res.json();
      setStatus(`✅ Uploaded: ${data.filename}\n\nSummary:\n${data.summary}`);

    } catch (err) {
      console.error("Upload error:", err);
      setStatus("❌ Upload failed");
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto space-y-4 bg-white rounded shadow">
      <h2 className="text-2xl font-bold">Upload Research Paper</h2>

      <input
        type="file"
        onChange={handleFileChange}
        className="block w-full text-sm text-gray-600"
      />

      <button
        onClick={handleUpload}
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
      >
        Upload
      </button>

      <p className="text-gray-800 mt-2">{status}</p>
    </div>
  );
}
