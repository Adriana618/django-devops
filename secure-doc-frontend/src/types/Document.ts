export interface DocumentType {
    id: number;
    file_name: string;
    status: string;
    extracted_text: string | null;
    created_at?: string; 
  }