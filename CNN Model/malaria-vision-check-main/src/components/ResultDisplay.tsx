
import React from 'react';
import { AlertTriangle, CheckCircle, BarChart3, Calendar, Download } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface ResultDisplayProps {
  result: {
    prediction: string;
    confidence: number;
  } | null;
  onNewAnalysis: () => void;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, onNewAnalysis }) => {
  if (!result) return null;

  const isInfected = result.prediction === 'Infected';
  const confidencePercentage = (result.confidence * 100).toFixed(1);

  const getResultColor = () => {
    if (isInfected) return 'medical-red';
    return 'medical-green';
  };

  const getResultIcon = () => {
    if (isInfected) {
      return <AlertTriangle className="h-8 w-8 text-medical-red" />;
    }
    return <CheckCircle className="h-8 w-8 text-medical-green" />;
  };

  const getResultMessage = () => {
    if (isInfected) {
      return {
        title: "Malaria aniqlandi",
        description: "Tahlil natijasiga ko'ra, namunada malaria parazitlari belgilari topildi.",
        recommendation: "Zudlik bilan shifokor bilan maslahatlashing va qo'shimcha tekshiruvlar o'tkazing."
      };
    }
    return {
      title: "Malaria aniqlanmadi",
      description: "Tahlil natijasiga ko'ra, namunada malaria parazitlari belgilari topilmadi.",
      recommendation: "Natija ijobiy, lekin shubhali alomatlar bo'lsa shifokor bilan maslahatlashing."
    };
  };

  const resultInfo = getResultMessage();

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6">
      {/* Main Result Card */}
      <Card className="border-0 shadow-lg">
        <CardHeader className="text-center pb-4">
          <div className="flex justify-center mb-4">
            {getResultIcon()}
          </div>
          <CardTitle className={`text-2xl font-bold ${isInfected ? 'text-medical-red' : 'text-medical-green'}`}>
            {resultInfo.title}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="text-center">
            <p className="text-gray-600 mb-4">{resultInfo.description}</p>
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center justify-center space-x-2 mb-2">
                <BarChart3 className="h-5 w-5 text-gray-600" />
                <span className="font-medium text-gray-900">Ishonch darajasi</span>
              </div>
              <div className="text-3xl font-bold text-gray-900">{confidencePercentage}%</div>
              <div className="w-full bg-gray-200 rounded-full h-3 mt-3">
                <div 
                  className={`h-3 rounded-full ${isInfected ? 'bg-medical-red' : 'bg-medical-green'}`}
                  style={{ width: `${confidencePercentage}%` }}
                ></div>
              </div>
            </div>
          </div>

          {/* Recommendation */}
          <div className={`border-l-4 ${isInfected ? 'border-medical-red bg-medical-lightRed' : 'border-medical-green bg-medical-lightGreen'} p-4 rounded`}>
            <h4 className="font-semibold text-gray-900 mb-2">Tavsiya</h4>
            <p className="text-gray-700 text-sm">{resultInfo.recommendation}</p>
          </div>

          {/* Additional Info */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4">
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Calendar className="h-4 w-4" />
              <span>Tahlil sanasi: {new Date().toLocaleDateString('uz-UZ')}</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <BarChart3 className="h-4 w-4" />
              <span>AI Model: CNN v2.1</span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 pt-4">
            <Button 
              onClick={onNewAnalysis}
              className="flex-1 bg-medical-blue hover:bg-medical-blue/90"
            >
              Yangi tahlil
            </Button>
            <Button 
              variant="outline" 
              className="flex-1"
            >
              <Download className="h-4 w-4 mr-2" />
              Natijani saqlash
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Disclaimer */}
      <Card className="bg-yellow-50 border-yellow-200">
        <CardContent className="p-4">
          <p className="text-sm text-yellow-800">
            <strong>Ogohlantirish:</strong> Bu natija faqat dastlabki ko'rsatma uchun. 
            Aniq diagnoz uchun malakali shifokor bilan maslahatlashing va laboratoriya tekshiruvlarini o'tkazing.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default ResultDisplay;
