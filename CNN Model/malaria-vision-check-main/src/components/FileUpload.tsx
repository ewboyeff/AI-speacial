
import React, { useCallback } from 'react';
import { Upload, FileImage, X } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  onRemoveFile: () => void;
  isLoading: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ 
  onFileSelect, 
  selectedFile, 
  onRemoveFile, 
  isLoading 
}) => {
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.type.startsWith('image/')) {
        onFileSelect(file);
      }
    }
  }, [onFileSelect]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      onFileSelect(files[0]);
    }
  }, [onFileSelect]);

  return (
    <div className="w-full max-w-md mx-auto">
      {!selectedFile ? (
        <div
          className="border-2 border-dashed border-medical-blue/30 rounded-xl p-8 text-center bg-medical-lightBlue/30 hover:bg-medical-lightBlue/50 transition-colors cursor-pointer"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-input')?.click()}
        >
          <div className="flex flex-col items-center space-y-4">
            <div className="p-4 bg-medical-blue/10 rounded-full">
              <Upload className="h-8 w-8 text-medical-blue" />
            </div>
            <div>
              <p className="text-lg font-medium text-gray-900 mb-2">
                Rasm yuklash
              </p>
              <p className="text-sm text-gray-600 mb-4">
                Qon namunasi rasmini yuklang yoki bu yerga sudrab olib keling
              </p>
              <p className="text-xs text-gray-500">
                PNG, JPG, JPEG (maksimal 10MB)
              </p>
            </div>
            <Button
              type="button"
              className="bg-medical-blue hover:bg-medical-blue/90"
              disabled={isLoading}
            >
              <FileImage className="h-4 w-4 mr-2" />
              Fayl tanlash
            </Button>
          </div>
          <input
            id="file-input"
            type="file"
            accept="image/*"
            onChange={handleFileInput}
            className="hidden"
            disabled={isLoading}
          />
        </div>
      ) : (
        <div className="border rounded-xl p-4 bg-white shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-3">
              <FileImage className="h-5 w-5 text-medical-blue" />
              <div>
                <p className="font-medium text-gray-900 truncate max-w-48">
                  {selectedFile.name}
                </p>
                <p className="text-sm text-gray-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={onRemoveFile}
              disabled={isLoading}
              className="text-gray-500 hover:text-red-500"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
          {selectedFile && (
            <div className="mt-3">
              <img
                src={URL.createObjectURL(selectedFile)}
                alt="Yuklangan rasm"
                className="w-full h-48 object-cover rounded-lg border"
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
