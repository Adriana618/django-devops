import React, { useEffect, useState, forwardRef, useImperativeHandle } from "react";
import { List, ListItem, ListItemText, Typography, Button } from "@mui/material";
import apiClient from "../api/axiosConfig";

interface DocumentType {
  id: number;
  file_name: string;
  status: string;
  extracted_text?: string | null;
}

export interface DocumentListRef {
  refreshDocuments: () => void;
}

const DocumentList = forwardRef<DocumentListRef>((props, ref) => {
  const [documents, setDocuments] = useState<DocumentType[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get<DocumentType[]>("/api/documents/");
      setDocuments(response.data);
    } catch (error) {
      console.error("Error fetching documents:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  useImperativeHandle(ref, () => ({
    refreshDocuments: () => {
      fetchDocuments();
    }
  }));

  return (
    <div>
      <Typography variant="h6" gutterBottom>Your Documents</Typography>
      <Button variant="outlined" onClick={fetchDocuments} disabled={loading}>
        {loading ? "Refreshing..." : "Refresh"}
      </Button>
      <List>
        {documents.map((doc) => (
          <ListItem key={doc.id} sx={{ flexDirection: "column", alignItems: "start" }}>
            <ListItemText
              primary={`File: ${doc.file_name}`}
              secondary={`Status: ${doc.status}`}
            />
            {doc.status === "DONE" && doc.extracted_text && (
              <Typography
                variant="body2"
                sx={{ backgroundColor: "#f4f4f4", padding: 1 }}
              >
                {doc.extracted_text}
              </Typography>
            )}
          </ListItem>
        ))}
      </List>
    </div>
  );
});

export default DocumentList;