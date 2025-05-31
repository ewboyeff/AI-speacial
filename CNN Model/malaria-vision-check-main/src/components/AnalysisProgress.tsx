
import React from 'react';
import { Brain, Zap, CheckCircle } from 'lucide-react';

interface AnalysisProgressProps {
  isAnalyzing: boolean;
}

const AnalysisProgress: React.FC<AnalysisProgressProps> = ({ isAnalyzing }) => {
  if (!isAnalyzing) return null;

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-6 border">
        <div className="text-center mb-6">
          <div className="relative">
            <div className="w-16 h-16 mx-auto bg-medical-blue/10 rounded-full flex items-center justify-center mb-4">
              <Brain className="h-8 w-8 text-medical-blue animate-pulse" />
              <div className="absolute inset-0 border-2 border-medical-blue rounded-full animate-pulse-ring"></div>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Tahlil jarayoni
            </h3>
            <p className="text-sm text-gray-600">
              AI model rasmni tahlil qilmoqda...
            </p>
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex items-center space-x-3">
            <CheckCircle className="h-5 w-5 text-medical-green" />
            <span className="text-sm text-gray-700">Rasm yuklandi</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-5 h-5 border-2 border-medical-blue border-t-transparent rounded-full animate-spin"></div>
            <span className="text-sm text-gray-700">Rasm qayta ishlanmoqda</span>
          </div>
          <div className="flex items-center space-x-3 opacity-50">
            <Zap className="h-5 w-5 text-gray-400" />
            <span className="text-sm text-gray-500">AI model bashorati</span>
          </div>
        </div>

        <div className="mt-6">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-medical-blue h-2 rounded-full animate-pulse" style={{ width: '60%' }}></div>
          </div>
          <p className="text-xs text-gray-500 mt-2 text-center">
            Kutilgan vaqt: 2-5 soniya
          </p>
        </div>
      </div>
    </div>
  );
};

export default AnalysisProgress;
