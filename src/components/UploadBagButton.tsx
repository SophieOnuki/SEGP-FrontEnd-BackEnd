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
  const inputRef = useRef<HTMLInputElement>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileType, setFileType] = useState<BagFileType>("RGB-D");
  const [uploading, setUploading] = useState(false);

  const handleButtonClick = () => {
    inputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".bag")) {
      toast.error("Please select a .bag file.");
      return;
    }
    setSelectedFile(file);
    setFileType("RGB-D");
    setDialogOpen(true);
    e.target.value = "";
  };

  const handleImport = async () => {
    if (!selectedFile) return;
    setUploading(true);
    try {
      await uploadBagFile(selectedFile, fileType);
      toast.success("Bag file imported successfully.");
      setDialogOpen(false);
      setSelectedFile(null);
      onUploadSuccess?.();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to import .bag file.");
    } finally {
      setUploading(false);
    }
  };

  const handleDialogOpenChange = (open: boolean) => {
    if (!open && !uploading) {
      setDialogOpen(false);
      setSelectedFile(null);
    }
  };

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        accept=".bag"
        hidden
        onChange={handleFileChange}
        aria-label="Select .bag file"
      />
      <Button
        type="button"
        variant="outline"
        size="sm"
        onClick={handleButtonClick}
        disabled={disabled}
        className="gap-2"
      >
        <Upload className="size-4" />
        Import .bag file
      </Button>

      <Dialog open={dialogOpen} onOpenChange={handleDialogOpenChange}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Import .bag file</DialogTitle>
            <DialogDescription>
              Choose the file type for this recording. The file will be saved and registered in the database.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label className="text-muted-foreground">File</Label>
              <p className="rounded-md border bg-muted/50 px-3 py-2 text-sm font-medium">
                {selectedFile?.name ?? "—"}
              </p>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="file-type">File type</Label>
              <Select
                value={fileType}
                onValueChange={(v) => setFileType(v as BagFileType)}
              >
                <SelectTrigger id="file-type">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="RGB-D">RGB-D</SelectItem>
                  <SelectItem value="Depth">Depth</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => handleDialogOpenChange(false)}
              disabled={uploading}
            >
              Cancel
            </Button>
            <Button onClick={handleImport} disabled={uploading}>
              {uploading ? "Importing…" : "Import"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
