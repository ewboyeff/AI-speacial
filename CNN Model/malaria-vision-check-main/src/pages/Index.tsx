
import React, { useState } from 'react';
import { toast } from '@/hooks/use-toast';
import Header from '@/components/Header';
import FileUpload from '@/components/FileUpload';
import AnalysisProgress from '@/components/AnalysisProgress';
import ResultDisplay from '@/components/ResultDisplay';
import { predictMalaria, PredictionResult } from '@/services/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Activity, Shield, Zap, Users } from 'lucide-react';

const Index = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);

  const handleFileSelect = (file: File) => {
    console.log('File selected:', file.name, file.size, file.type);
    setSelectedFile(file);
    setResult(null);
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setResult(null);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      toast({
        title: "Xatolik",
        description: "Iltimos, avval rasm yuklang.",
        variant: "destructive",
      });
      return;
    }

    setIsAnalyzing(true);
    try {
      console.log('Starting analysis...');
      const analysisResult = await predictMalaria(selectedFile);
      console.log('Analysis completed:', analysisResult);
      
      setResult(analysisResult);
      toast({
        title: "Tahlil tugallandi",
        description: "Natijalar tayyor!",
      });
    } catch (error) {
      console.error('Analysis failed:', error);
      toast({
        title: "Xatolik yuz berdi",
        description: error instanceof Error ? error.message : "Noma'lum xatolik",
        variant: "destructive",
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleNewAnalysis = () => {
    setSelectedFile(null);
    setResult(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-medical-lightBlue via-white to-medical-lightGreen">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!result ? (
          <>
            {/* Hero Section */}
            <div className="text-center mb-12">
              <div className="inline-flex items-center justify-center p-3 bg-medical-blue/10 rounded-full mb-6">
                <Activity className="h-8 w-8 text-medical-blue" />
              </div>
              <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                Malaria AI Diagnostika
              </h1>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
                Sun'iy intellekt yordamida qon namunalaridan malaria kasalligini 
                aniqlash uchun ilg'or tibbiy diagnostika tizimi
              </p>
              
              {/* Stats */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto mb-12">
                <div className="bg-white rounded-lg p-6 shadow-sm border">
                  <div className="flex items-center justify-center mb-3">
                    <Zap className="h-6 w-6 text-medical-blue" />
                  </div>
                  <div className="text-2xl font-bold text-gray-900">95.7%</div>
                  <div className="text-sm text-gray-600">Aniqlik darajasi</div>
                </div>
                <div className="bg-white rounded-lg p-6 shadow-sm border">
                  <div className="flex items-center justify-center mb-3">
                    <Shield className="h-6 w-6 text-medical-green" />
                  </div>
                  <div className="text-2xl font-bold text-gray-900">2-5s</div>
                  <div className="text-sm text-gray-600">Tahlil vaqti</div>
                </div>
                <div className="bg-white rounded-lg p-6 shadow-sm border">
                  <div className="flex items-center justify-center mb-3">
                    <Users className="h-6 w-6 text-medical-blue" />
                  </div>
                  <div className="text-2xl font-bold text-gray-900">10K+</div>
                  <div className="text-sm text-gray-600">Tahlil qilingan</div>
                </div>
              </div>
            </div>

            {/* Main Interface */}
            <div className="max-w-4xl mx-auto">
              <Card className="border-0 shadow-xl bg-white/80 backdrop-blur-sm">
                <CardHeader className="text-center">
                  <CardTitle className="text-2xl font-bold text-gray-900">
                    Rasm yuklash va tahlil qilish
                  </CardTitle>
                  <p className="text-gray-600">
                    Qon namunasi rasmini yuklang va AI tahlilini boshlang
                  </p>
                </CardHeader>
                <CardContent className="space-y-8">
                  {isAnalyzing ? (
                    <AnalysisProgress isAnalyzing={isAnalyzing} />
                  ) : (
                    <>
                      <FileUpload
                        onFileSelect={handleFileSelect}
                        selectedFile={selectedFile}
                        onRemoveFile={handleRemoveFile}
                        isLoading={isAnalyzing}
                      />
                      
                      {selectedFile && (
                        <div className="text-center">
                          <Button
                            onClick={handleAnalyze}
                            disabled={isAnalyzing}
                            size="lg"
                            className="bg-medical-blue hover:bg-medical-blue/90 px-8 py-3 text-lg font-semibold"
                          >
                            <Activity className="h-5 w-5 mr-2" />
                            Tahlilni boshlash
                          </Button>
                        </div>
                      )}
                    </>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Features Section */}
            <div className="mt-16">
              <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
                Nima uchun MalariaVision?
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                <div className="text-center">
                  <div className="bg-medical-lightBlue rounded-lg p-6 mb-4">
                    <Zap className="h-8 w-8 text-medical-blue mx-auto" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Tez va Aniq</h3>
                  <p className="text-gray-600">
                    Ilg'or CNN modeli yordamida bir necha soniyada yuqori aniqlikda natija
                  </p>
                </div>
                <div className="text-center">
                  <div className="bg-medical-lightGreen rounded-lg p-6 mb-4">
                    <Shield className="h-8 w-8 text-medical-green mx-auto" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Xavfsiz</h3>
                  <p className="text-gray-600">
                    Barcha ma'lumotlar shifrlangan va maxfiy saqlanadi
                  </p>
                </div>
                <div className="text-center">
                  <div className="bg-medical-lightBlue rounded-lg p-6 mb-4">
                    <Users className="h-8 w-8 text-medical-blue mx-auto" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Ishonchli</h3>
                  <p className="text-gray-600">
                    Minglab test va tibbiy mutaxassislar tomonidan tasdiqlangan
                  </p>
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="pt-8">
            <ResultDisplay result={result} onNewAnalysis={handleNewAnalysis} />
          </div>
        )}
      </main>
    </div>
  );
};

export default Index;
