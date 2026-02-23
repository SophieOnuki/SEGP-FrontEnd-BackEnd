import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { UploadBagButton } from "./UploadBagButton";
import { FileArchive, Clock } from "lucide-react";
import type { BagFile } from "../services/api";

interface ImportedBagFilesProps {
  bagFiles: BagFile[];
  onUploadSuccess?: () => void;
}

export function ImportedBagFiles({ bagFiles, onUploadSuccess }: ImportedBagFilesProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Imported .bag files</CardTitle>
          <UploadBagButton onUploadSuccess={onUploadSuccess} />
        </div>
      </CardHeader>
      <CardContent>
        {bagFiles.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            No imported files yet. Use the button above to import a .bag file.
          </div>
        ) : (
          <div className="space-y-3">
            {bagFiles.map((file) => (
              <div
                key={file.file_id}
                className="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-green-300 hover:bg-green-50/30 transition-colors"
              >
                <div className="flex gap-4">
                  <div className="w-12 h-12 rounded-lg bg-gray-200 flex items-center justify-center flex-shrink-0">
                    <FileArchive className="size-6 text-gray-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4">
                      <div className="space-y-2">
                        <p className="font-medium text-gray-900 truncate" title={file.file_name}>
                          {file.file_name}
                        </p>
                        <div className="flex items-center gap-3 flex-wrap">
                          <span className="text-sm text-gray-600">{file.file_type}</span>
                          {file.upload_date && (
                            <div className="flex items-center gap-1.5 text-sm text-gray-600">
                              <Clock className="w-3.5 h-3.5" />
                              {new Date(file.upload_date).toLocaleString()}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
