import * as React from "react";
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

// Button + modal flow for importing a .bag recording and registering it via the API.
// The user first picks a file, then chooses the logical type (e.g. RGB-D vs Depth) before upload.
interface UploadBagButtonProps {
  onUploadSuccess?: () => void;
  disabled?: boolean;
}

export function UploadBagButton({ onUploadSuccess, disabled }: UploadBagButtonProps) {
  // UI state for the inline modal and the current upload.
  const [showTypeModal, setShowTypeModal] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileType, setFileType] = useState<BagFileType>("RGB-D");
  const [uploading, setUploading] = useState(false);

  // Tracks whether we're currently in the process of opening a file picker (reserved for future use).
  const isSelectingFile = useRef(false);
  const handleButtonClick = () => {
    console.log("Button clicked, opening file dialog...");

  // Create a temporary file input instead of keeping one in the JSX tree.
  // This avoids layout concerns and lets us fully control its lifecycle.
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.bag';
  input.style.display = 'none';

  // Handle the file the user picked in the native file dialog.
  input.onchange = (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    console.log("File selected via temp input:", file?.name);

    if (!file) {
      document.body.removeChild(input)
      return;
    }

    // Guard against wrong extensions early; backend expects a .bag recording.
    if (!file.name.toLowerCase().endsWith('.bag')) {
      toast.error("Please select a .bag file.");
      document.body.removeChild(input)
      return;
    }

    // Persist the chosen file and show the type-selection modal.
    setSelectedFile(file);
    setFileType("RGB-D");
    setShowTypeModal(true);

    document.body.removeChild(input)
  };

  document.body.appendChild(input);
  input.click();
};

  // Called when the user confirms the import from the modal.
  const handleImport = async () => {
    if (!selectedFile) {
      console.log("ERROR: No file selected for import!");
      toast.error("No file selected for import.");
      return;
    }

    // Mark UI as busy while the upload is in flight.
    setUploading(true);
    try {
        const result = await uploadBagFile(selectedFile, fileType);
        toast.success("Bag file imported successfully.");

        // Close dialog and reset state after a successful upload.
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


  // Reset local state when the user backs out of the modal.
  const handleCancel = () => {
    setShowTypeModal(false);
    setSelectedFile(null);
  };

  return (
    <>
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

      {/* Inline modal rendered in-place (no portal) so it works in more environments, e.g. Storybook. */}
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