import React, { useContext, useRef } from "react";
import { Container, Typography, Button } from "@mui/material";
import { AuthContext } from "../context/AuthContext";
import DocumentUploader from "../components/DocumentUploader";
import DocumentList, { DocumentListRef } from "../components/DocumentList";
import { useNavigate } from "react-router-dom";

const HomePage: React.FC = () => {
  const { isLoggedIn } = useContext(AuthContext);
  const navigate = useNavigate();

  const documentListRef = useRef<DocumentListRef>(null);

  if (!isLoggedIn) {
    return (
      <Container>
        <Typography variant="h5" mt={4}>
          You are not logged in!
        </Typography>
        <Button variant="contained" onClick={() => navigate("/login")} sx={{ mt: 2 }}>
          Go to Login!
        </Button>
      </Container>
    );
  }

  const handleUploadSuccess = () => {
    if (documentListRef.current) {
      documentListRef.current.refreshDocuments();
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Document Dashboard</Typography>
      <DocumentUploader onUploadSuccess={handleUploadSuccess} />
      <DocumentList ref={documentListRef} />
    </Container>
  );
};

export default HomePage;