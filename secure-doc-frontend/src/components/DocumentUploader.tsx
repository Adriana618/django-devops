import React, { useState, ChangeEvent } from "react";
import { Button } from "@mui/material";
import apiClient from "../api/axiosConfig";

const DocumentUploader: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await apiClient.post("/api/documents/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("File uploaded successfully!");
      console.log(response.data);
    } catch (error) {
      console.error("Upload error:", error);
      alert("Upload failed. Check console for details.");
    }
  };

  return (
    <div style={{ marginBottom: "2rem" }}>
      <input type="file" onChange={handleFileChange} />
      <Button variant="contained" onClick={handleUpload} sx={{ ml: 2 }}>
        Upload
      </Button>
    </div>
  );
};

export default DocumentUploader;