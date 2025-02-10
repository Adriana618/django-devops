import React, { useState, ChangeEvent } from "react";
import { Button, CircularProgress, Box } from "@mui/material";
import apiClient from "../api/axiosConfig";

interface Props {
  onUploadSuccess?: () => void;
}

const DocumentUploader: React.FC<Props> = ({ onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

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
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await apiClient.post("/api/documents/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      alert("File uploaded successfully!");
      if (onUploadSuccess) {
        onUploadSuccess();
      }
    } catch (error) {
      console.error("Upload error:", error);
      alert("Upload failed. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box mb={2}>
      <input type="file" onChange={handleFileChange} />
      <Button variant="contained" onClick={handleUpload} sx={{ ml: 2 }} disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </Button>
      {loading && <CircularProgress size={24} sx={{ ml: 2 }} />}
    </Box>
  );
};

export default DocumentUploader;