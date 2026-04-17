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
import { uploadBagFile, type BagFileType, type UploadResponse } from "../services/api";

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
        toast.success(`Bag file imported successfully. Predicted mass: ${result.mass_prediction.toFixed(2)}kg`);

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
        className="gap-2 border-green-200/60 hover:border-green-200/70"
      >
        <Upload className="size-4" />
        Import .bag file
      </Button>

      {/* Inline modal rendered in-place (no portal) so it works in more environments, e.g. Storybook. */}
      {showTypeModal && (
          <div
            className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-sm animate-fade-in"
            style={{ animationDuration: '0.2s' }}
            onClick={() => { if (!uploading) handleCancel(); }}
          >
            <div
              className="rounded-xl p-6 max-w-[500px] w-[90%] bg-card border-2 border-green-200/60 shadow-2xl transition-smooth animate-slide-up"
              style={{ animationDuration: '0.3s', boxShadow: '0 25px 50px -12px rgba(45, 90, 39, 0.25)' }}
              onClick={(e) => e.stopPropagation()}
            >
              <h2 className="text-xl font-semibold mb-2 text-card-foreground">
                Import .bag file
              </h2>
              <p className="mb-6 text-muted-foreground">
                Choose the file type for this recording. The file will be saved and registered in the database.
              </p>

              <div className="mb-4">
                <Label className="text-muted-foreground">File</Label>
                <p className="mt-1 py-2 px-3 rounded-md border border-border bg-muted/50 text-sm text-foreground">
                  {selectedFile?.name ?? "—"}
                </p>
              </div>

              <div className="mb-6">
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

              <div className="flex justify-end gap-3">
                <Button
                  variant="outline"
                  onClick={handleCancel}
                  disabled={uploading}
                  className="border-green-200/60 hover:border-green-200/70"
                >
                  Cancel
                </Button>
                <Button
                  onClick={handleImport}
                  disabled={uploading || !selectedFile}
                  className="bg-green-600 hover:bg-green-700"
                >
                  {uploading ? "Importing…" : "Import"}
                </Button>
              </div>
            </div>
          </div>
)}
    </>
  );
}