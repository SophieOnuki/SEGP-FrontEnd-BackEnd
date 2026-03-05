import { useRef, useState } from "react";
import { Button } from "./ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "./ui/dialog";
import { Label } from "./ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import { Upload } from "lucide-react";
import { toast } from "sonner";
import { uploadBagFile, type BagFileType } from "../services/api";

interface UploadBagButtonProps {
  onUploadSuccess?: () => void;
  disabled?: boolean;
}

export function UploadBagButton({ onUploadSuccess, disabled }: UploadBagButtonProps) {
  const [showTypeModal, setShowTypeModal] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileType, setFileType] = useState<BagFileType>("RGB-D");
  const [uploading, setUploading] = useState(false);

  // Add a ref to track if we're in the process of selecting a file
  const isSelectingFile = useRef(false);
  const handleButtonClick = () => {
    console.log("Button clicked, opening file dialog...");

  // Create a temporary file input
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.bag';
  input.style.display = 'none';

  input.onchange = (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    console.log("File selected via temp input:", file?.name);

    if (!file) {
      document.body.removeChild(input)
      return;
    }

    if (!file.name.toLowerCase().endsWith('.bag')) {
      toast.error("Please select a .bag file.");
      document.body.removeChild(input)
      return;
    }

    setSelectedFile(file);
    setFileType("RGB-D");
    setShowTypeModal(true);

    document.body.removeChild(input)
  };

  document.body.appendChild(input);
  input.click();
};

  const handleImport = async () => {
    console.log("=== HANDLE IMPORT CALLED ===");
    console.log("selectedFile:", selectedFile);
    console.log("fileType:", fileType);
    const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';
    console.log("API_BASE_URL:", apiUrl);

    if (!selectedFile) {
      console.log("ERROR: No file selected for import!");
      toast.error("No file selected for import.");
      return;
    }

    setUploading(true);
    console.log("Calling uploadBagFile with:", selectedFile.name, selectedFile.size);

    try {
        console.log("File details:", {
            name: selectedFile.name,
            size: selectedFile.size,
            type: selectedFile.type,
            lastModified: new Date(selectedFile.lastModified).toLocaleString(),
        });

        const result = await uploadBagFile(selectedFile, fileType);
        console.log("Upload result:", result);
        toast.success("Bag file imported successfully.");
        console.log("Import successful, closing dialog and resetting state.");

        // Close dialog and reset state
        setShowTypeModal(false);
        setSelectedFile(null);
        onUploadSuccess?.();
    } catch (err) {
      console.error("Error during import:", err);
      toast.error(err instanceof Error ? err.message : "Failed to import .bag file.");
    } finally {
      setUploading(false);
    }
  };


  const handleCancel = () => {
    console.log("Cancel button clicked");
    setShowTypeModal(false);
    setSelectedFile(null);
  };

  return (
    <>
      <input
        type="file"
        accept=".bag"
        hidden
        // onChange={handleFileChange}
        onClick={(e) => {
          // Stop propagation to prevent any parent handlers from interfering
          e.stopPropagation();
        }}
        aria-label="Select .bag file"
      />
      <Button
        type="button"
        variant="outline"
        size="sm"
        onClick={handleButtonClick}
        disabled={disabled|| uploading}
        className="gap-2"
      >
        <Upload className="size-4" />
        Import .bag file
      </Button>

      {showTypeModal && (
          <div
            style={{
              position: 'fixed',
              top: 0, left: 0, right: 0, bottom: 0,
              backgroundColor: 'rgba(0,0,0,0.5)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 9999,
            }}
            onClick={() => { if (!uploading) handleCancel(); }}
          >
            <div
              style={{
                backgroundColor: 'white',
                borderRadius: '8px',
                padding: '24px',
                maxWidth: '500px',
                width: '90%',
              }}
              onClick={(e) => e.stopPropagation()}
            >
              <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '8px' }}>
                Import .bag file
              </h2>
              <p style={{ marginBottom: '24px', color: '#666' }}>
                Choose the file type for this recording. The file will be saved and registered in the database.
              </p>

              <div style={{ marginBottom: '16px' }}>
                <Label className="text-muted-foreground">File</Label>
                <p style={{
                  padding: '8px 12px',
                  border: '1px solid #e2e8f0',
                  borderRadius: '6px',
                  backgroundColor: '#f8fafc',
                  fontSize: '0.875rem',
                  marginTop: '4px',
                }}>
                  {selectedFile?.name ?? "—"}
                </p>
              </div>

              <div style={{ marginBottom: '24px' }}>
                <Label htmlFor="file-type-modal">File type</Label>
                <Select
                  value={fileType}
                  onValueChange={(v) => setFileType(v as BagFileType)}
                >
                  <SelectTrigger id="file-type-modal">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="RGB-D">RGB-D</SelectItem>
                    <SelectItem value="Depth">Depth</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
                <Button variant="outline" onClick={handleCancel} disabled={uploading}>
                  Cancel
                </Button>
                <Button onClick={handleImport} disabled={uploading || !selectedFile}>
                  {uploading ? "Importing…" : "Import"}
                </Button>
              </div>
            </div>
          </div>
)}
    </>
  );
}