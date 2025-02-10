import React, { useEffect, useState } from "react";
import { List, ListItem, ListItemText, Typography } from "@mui/material";
import apiClient from "../api/axiosConfig";
import { DocumentType } from "../types/Document";

const DocumentList: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentType[]>([]);

  const fetchDocuments = async () => {
    try {
      const response = await apiClient.get<DocumentType[]>("/api/documents/");
      setDocuments(response.data);
    } catch (error) {
      console.error("Error fetching documents:", error);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  return (
    <div>
      <Typography variant="h6" gutterBottom>Your Documents</Typography>
      <List>
        {documents.map((doc) => (
          <ListItem 
            key={doc.id} 
            sx={{ flexDirection: "column", alignItems: "start" }}
          >
            <ListItemText
              primary={`File: ${doc.file_name}`}
              secondary={`Status: ${doc.status}`}
            />
            {doc.status === "DONE" && (
              <Typography 
                variant="body2" 
                sx={{ backgroundColor: "#f4f4f4", padding: 1 }}
              >
                {doc.extracted_text || "No text extracted"}
              </Typography>
            )}
          </ListItem>
        ))}
      </List>
    </div>
  );
};

export default DocumentList;