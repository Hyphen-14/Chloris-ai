import React, { useState, useRef, useEffect } from 'react';
import { Camera, CameraOff, Activity, Leaf, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Badge } from './ui/badge';
import { toast } from 'sonner';

export default function Scanner() {
  const [isScanning, setIsScanning] = useState(false);
  const [detectionData, setDetectionData] = useState(null);
  const [cameraStream, setCameraStream] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  // Mock detection simulation
  const simulateDetection = () => {
    const diseases = [
      { name: 'Leaf Rust', confidence: 88, severity: 'high', color: '#ef4444' },
      { name: 'Powdery Mildew', confidence: 92, severity: 'medium', color: '#f59e0b' },
      { name: 'Healthy Leaf', confidence: 95, severity: 'none', color: '#10b981' },
      { name: 'Leaf Spot', confidence: 85, severity: 'high', color: '#ef4444' },
      { name: 'Bacterial Blight', confidence: 78, severity: 'critical', color: '#dc2626' },
    ];
    
    const randomDisease = diseases[Math.floor(Math.random() * diseases.length)];
    
    setDetectionData({
      disease: randomDisease.name,
      confidence: randomDisease.confidence,
      severity: randomDisease.severity,
      timestamp: new Date().toLocaleTimeString(),
      recommendations: getRecommendations(randomDisease.name),
      color: randomDisease.color
    });
  };

  const getRecommendations = (disease) => {
    const recommendations = {
      'Leaf Rust': ['Remove infected leaves', 'Apply fungicide spray', 'Improve air circulation'],
      'Powdery Mildew': ['Reduce humidity', 'Apply neem oil', 'Prune affected areas'],
      'Healthy Leaf': ['Maintain current care routine', 'Monitor regularly', 'Ensure proper watering'],
      'Leaf Spot': ['Remove affected leaves', 'Avoid overhead watering', 'Apply copper fungicide'],
      'Bacterial Blight': ['Isolate plant immediately', 'Remove infected parts', 'Apply bactericide']
    };
    return recommendations[disease] || ['Consult plant expert', 'Monitor closely'];
  };

  // Start camera
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 1280, height: 720 } 
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setCameraStream(stream);
        setIsScanning(true);
        toast.success('Camera activated', {
          description: 'Point at a plant leaf for detection'
        });
        
        // Start detection simulation
        const interval = setInterval(() => {
          simulateDetection();
          drawFloralCorners();
        }, 3000);
        
        return () => clearInterval(interval);
      }
    } catch (error) {
      console.error('Camera error:', error);
      toast.error('Camera access denied', {
        description: 'Please allow camera permissions'
      });
    }
  };

  // Stop camera
  const stopCamera = () => {
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
      setCameraStream(null);
      setIsScanning(false);
      setDetectionData(null);
      toast.info('Camera stopped');
    }
  };

  // Draw floral corner decorations on canvas
  const drawFloralCorners = () => {
    if (!canvasRef.current || !videoRef.current) return;
    
    const canvas = canvasRef.current;
    const video = videoRef.current;
    const ctx = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (detectionData) {
      // Draw floral-styled corners (elegant tech aesthetic)
      const cornerLength = 60;
      const cornerWidth = 4;
      const offset = 100;
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const boxWidth = 400;
      const boxHeight = 300;
      
      ctx.strokeStyle = detectionData.color || 'hsl(150, 25%, 55%)';
      ctx.lineWidth = cornerWidth;
      ctx.lineCap = 'round';
      
      // Top-left corner
      ctx.beginPath();
      ctx.moveTo(centerX - boxWidth/2, centerY - boxHeight/2 + cornerLength);
      ctx.lineTo(centerX - boxWidth/2, centerY - boxHeight/2);
      ctx.lineTo(centerX - boxWidth/2 + cornerLength, centerY - boxHeight/2);
      ctx.stroke();
      
      // Top-right corner
      ctx.beginPath();
      ctx.moveTo(centerX + boxWidth/2 - cornerLength, centerY - boxHeight/2);
      ctx.lineTo(centerX + boxWidth/2, centerY - boxHeight/2);
      ctx.lineTo(centerX + boxWidth/2, centerY - boxHeight/2 + cornerLength);
      ctx.stroke();
      
      // Bottom-left corner
      ctx.beginPath();
      ctx.moveTo(centerX - boxWidth/2, centerY + boxHeight/2 - cornerLength);
      ctx.lineTo(centerX - boxWidth/2, centerY + boxHeight/2);
      ctx.lineTo(centerX - boxWidth/2 + cornerLength, centerY + boxHeight/2);
      ctx.stroke();
      
      // Bottom-right corner
      ctx.beginPath();
      ctx.moveTo(centerX + boxWidth/2 - cornerLength, centerY + boxHeight/2);
      ctx.lineTo(centerX + boxWidth/2, centerY + boxHeight/2);
      ctx.lineTo(centerX + boxWidth/2, centerY + boxHeight/2 - cornerLength);
      ctx.stroke();
      
      // Draw detection label
      ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
      ctx.fillRect(centerX - boxWidth/2, centerY - boxHeight/2 - 50, 250, 40);
      ctx.fillStyle = detectionData.color;
      ctx.font = 'bold 20px Montserrat';
      ctx.fillText(detectionData.disease, centerX - boxWidth/2 + 15, centerY - boxHeight/2 - 22);
    }
  };

  useEffect(() => {
    return () => {
      if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
      }
    };
  }, [cameraStream]);

  return (
    <div className="min-h-screen p-8">
      {/* Header */}
      <div className="mb-8 animate-fade-in">
        <h1 className="text-4xl font-bold mb-2" style={{ color: 'hsl(var(--primary))' }}>
          Plant Scanner
        </h1>
        <p className="text-lg" style={{ color: 'hsl(var(--muted-foreground))' }}>
          Real-time disease detection powered by AI vision
        </p>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Camera Feed - 2/3 width */}
        <div className="lg:col-span-2 animate-fade-in" style={{ animationDelay: '0.1s' }}>
          <Card className="glass-card border-0 overflow-hidden" style={{ minHeight: '600px' }}>
            <CardContent className="p-0 relative">
              {!isScanning ? (
                <div className="flex flex-col items-center justify-center" style={{ minHeight: '600px' }}>
                  <div className="w-32 h-32 rounded-full glass-card flex items-center justify-center mb-6 animate-float">
                    <Camera className="w-16 h-16" style={{ color: 'hsl(var(--primary))' }} />
                  </div>
                  <h3 className="text-2xl font-semibold mb-4" style={{ color: 'hsl(var(--foreground))' }}>
                    Start Camera Scanning
                  </h3>
                  <p className="text-center mb-8 max-w-md" style={{ color: 'hsl(var(--muted-foreground))' }}>
                    Point your camera at a plant leaf to detect diseases and receive instant analysis
                  </p>
                  <Button 
                    onClick={startCamera}
                    className="px-8 py-6 text-lg rounded-xl"
                    style={{
                      background: 'var(--gradient-primary)',
                      color: 'hsl(var(--primary-foreground))'
                    }}
                  >
                    <Camera className="w-5 h-5 mr-2" />
                    Activate Camera
                  </Button>
                </div>
              ) : (
                <div className="relative" style={{ minHeight: '600px' }}>
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    className="w-full h-full object-cover"
                    style={{ minHeight: '600px' }}
                  />
                  <canvas
                    ref={canvasRef}
                    className="absolute top-0 left-0 w-full h-full pointer-events-none"
                  />
                  
                  {/* Stop Button */}
                  <div className="absolute top-6 right-6">
                    <Button
                      onClick={stopCamera}
                      variant="destructive"
                      className="rounded-xl glass-card border-0"
                      style={{
                        background: 'rgba(239, 68, 68, 0.9)',
                        backdropFilter: 'blur(10px)'
                      }}
                    >
                      <CameraOff className="w-4 h-4 mr-2" />
                      Stop
                    </Button>
                  </div>
                  
                  {/* Scanning Indicator */}
                  <div className="absolute bottom-6 left-6">
                    <div className="glass-card px-4 py-2 rounded-xl flex items-center gap-2">
                      <Activity className="w-4 h-4 animate-pulse" style={{ color: 'hsl(var(--success))' }} />
                      <span className="text-sm font-medium" style={{ color: 'hsl(var(--foreground))' }}>
                        Scanning Active
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Analysis Results - 1/3 width */}
        <div className="lg:col-span-1 space-y-6 animate-fade-in" style={{ animationDelay: '0.2s' }}>
          {/* Detection Card */}
          <Card className="glass-card border-0">
            <CardHeader>
              <CardTitle className="text-xl flex items-center gap-2" style={{ color: 'hsl(var(--primary))' }}>
                <Leaf className="w-5 h-5" />
                Detection Results
              </CardTitle>
              <CardDescription>Real-time analysis</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {detectionData ? (
                <>
                  <div className="space-y-3">
                    <div>
                      <p className="text-sm font-medium mb-2" style={{ color: 'hsl(var(--muted-foreground))' }}>
                        Detected Condition
                      </p>
                      <div className="flex items-center justify-between">
                        <h3 className="text-2xl font-bold" style={{ color: 'hsl(var(--foreground))' }}>
                          {detectionData.disease}
                        </h3>
                        <Badge
                          variant="secondary"
                          className="text-xs"
                          style={{
                            background: detectionData.severity === 'none' ? 'hsl(var(--success))' : 
                                       detectionData.severity === 'medium' ? 'hsl(var(--warning))' : 
                                       'hsl(var(--destructive))',
                            color: 'white'
                          }}
                        >
                          {detectionData.severity}
                        </Badge>
                      </div>
                    </div>
                    
                    <div>
                      <p className="text-sm font-medium mb-2" style={{ color: 'hsl(var(--muted-foreground))' }}>
                        Confidence Level
                      </p>
                      <div className="flex items-center gap-3">
                        <div className="flex-1 h-3 rounded-full" style={{ background: 'hsl(var(--muted))' }}>
                          <div 
                            className="h-full rounded-full transition-all duration-500"
                            style={{ 
                              width: `${detectionData.confidence}%`,
                              background: detectionData.color
                            }}
                          />
                        </div>
                        <span className="text-lg font-bold" style={{ color: 'hsl(var(--foreground))' }}>
                          {detectionData.confidence}%
                        </span>
                      </div>
                    </div>
                    
                    <div>
                      <p className="text-xs" style={{ color: 'hsl(var(--muted-foreground))' }}>
                        Last detected: {detectionData.timestamp}
                      </p>
                    </div>
                  </div>
                </>
              ) : (
                <div className="text-center py-8">
                  <div className="w-16 h-16 rounded-full glass-card flex items-center justify-center mx-auto mb-4 animate-pulse">
                    <Leaf className="w-8 h-8" style={{ color: 'hsl(var(--muted-foreground))' }} />
                  </div>
                  <p className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>
                    No detection yet. Start scanning to see results.
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Recommendations Card */}
          {detectionData && (
            <Card className="glass-card border-0">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2" style={{ color: 'hsl(var(--primary))' }}>
                  <CheckCircle2 className="w-5 h-5" />
                  Recommendations
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {detectionData.recommendations.map((rec, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <div className="w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5"
                           style={{ background: 'hsl(var(--primary))', color: 'hsl(var(--primary-foreground))' }}>
                        <span className="text-xs font-bold">{index + 1}</span>
                      </div>
                      <p className="text-sm leading-relaxed" style={{ color: 'hsl(var(--foreground))' }}>
                        {rec}
                      </p>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {/* Quick Stats */}
          <Card className="glass-card border-0">
            <CardHeader>
              <CardTitle className="text-lg" style={{ color: 'hsl(var(--primary))' }}>Session Stats</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>Scans</span>
                <span className="text-lg font-bold" style={{ color: 'hsl(var(--foreground))' }}>0</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>Detections</span>
                <span className="text-lg font-bold" style={{ color: 'hsl(var(--foreground))' }}>0</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>Accuracy</span>
                <span className="text-lg font-bold" style={{ color: 'hsl(var(--success))' }}>98%</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}