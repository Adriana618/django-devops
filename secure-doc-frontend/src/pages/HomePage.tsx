import React from "react";
import { Container, Typography } from "@mui/material";
import DocumentUploader from "../components/DocumentUploader";
import DocumentList from "../components/DocumentList";

const HomePage: React.FC = () => {
  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Document Dashboard</Typography>
      <DocumentUploader />
      <DocumentList />
    </Container>
  );
};

export default HomePage;