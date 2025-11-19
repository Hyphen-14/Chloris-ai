import React from 'react';
import { FileText, Download, Calendar, TrendingUp, Activity } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { toast } from 'sonner';

export default function Report() {
  const mockReports = [
    {
      id: 1,
      date: '2024-01-15',
      scans: 24,
      detections: 18,
      healthyPlants: 6,
      mostCommon: 'Leaf Rust',
      status: 'completed'
    },
    {
      id: 2,
      date: '2024-01-14',
      scans: 31,
      detections: 22,
      healthyPlants: 9,
      mostCommon: 'Powdery Mildew',
      status: 'completed'
    },
    {
      id: 3,
      date: '2024-01-13',
      scans: 19,
      detections: 15,
      healthyPlants: 4,
      mostCommon: 'Leaf Spot',
      status: 'completed'
    }
  ];

  const handleDownload = (reportId) => {
    toast.success('Report downloaded', {
      description: `Report #${reportId} has been saved to your device`
    });
  };

  return (
    <div className="min-h-screen p-8">
      {/* Header */}
      <div className="mb-8 animate-fade-in">
        <h1 className="text-4xl font-bold mb-2" style={{ color: 'hsl(var(--primary))' }}>
          Analysis Reports
        </h1>
        <p className="text-lg" style={{ color: 'hsl(var(--muted-foreground))' }}>
          Historical scan data and detection analytics
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card className="glass-card border-0 animate-fade-in" style={{ animationDelay: '0.1s' }}>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-2">
              <Activity className="w-8 h-8" style={{ color: 'hsl(var(--primary))' }} />
              <Badge style={{ background: 'hsl(var(--primary))', color: 'hsl(var(--primary-foreground))' }}>
                +12%
              </Badge>
            </div>
            <h3 className="text-3xl font-bold mb-1" style={{ color: 'hsl(var(--foreground))' }}>74</h3>
            <p className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>Total Scans</p>
          </CardContent>
        </Card>

        <Card className="glass-card border-0 animate-fade-in" style={{ animationDelay: '0.2s' }}>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="w-8 h-8" style={{ color: 'hsl(var(--success))' }} />
              <Badge style={{ background: 'hsl(var(--success))', color: 'white' }}>
                +8%
              </Badge>
            </div>
            <h3 className="text-3xl font-bold mb-1" style={{ color: 'hsl(var(--foreground))' }}>55</h3>
            <p className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>Detections</p>
          </CardContent>
        </Card>

        <Card className="glass-card border-0 animate-fade-in" style={{ animationDelay: '0.3s' }}>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-2">
              <FileText className="w-8 h-8" style={{ color: 'hsl(var(--rose-deep))' }} />
              <Badge style={{ background: 'hsl(var(--rose-deep))', color: 'white' }}>
                Latest
              </Badge>
            </div>
            <h3 className="text-3xl font-bold mb-1" style={{ color: 'hsl(var(--foreground))' }}>3</h3>
            <p className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>Reports</p>
          </CardContent>
        </Card>

        <Card className="glass-card border-0 animate-fade-in" style={{ animationDelay: '0.4s' }}>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-2">
              <Calendar className="w-8 h-8" style={{ color: 'hsl(var(--primary-light))' }} />
              <Badge style={{ background: 'hsl(var(--primary-light))', color: 'white' }}>
                98%
              </Badge>
            </div>
            <h3 className="text-3xl font-bold mb-1" style={{ color: 'hsl(var(--foreground))' }}>19</h3>
            <p className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>Healthy Plants</p>
          </CardContent>
        </Card>
      </div>

      {/* Reports List */}
      <div className="space-y-4">
        <h2 className="text-2xl font-semibold mb-4" style={{ color: 'hsl(var(--foreground))' }}>
          Recent Reports
        </h2>
        
        {mockReports.map((report, index) => (
          <Card 
            key={report.id} 
            className="glass-card border-0 animate-fade-in"
            style={{ animationDelay: `${(index + 5) * 0.1}s` }}
          >
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-xl flex items-center gap-3">
                    <FileText className="w-6 h-6" style={{ color: 'hsl(var(--primary))' }} />
                    <span style={{ color: 'hsl(var(--foreground))' }}>Report #{report.id}</span>
                  </CardTitle>
                  <CardDescription className="flex items-center gap-2 mt-2">
                    <Calendar className="w-4 h-4" />
                    {new Date(report.date).toLocaleDateString('en-US', { 
                      weekday: 'long', 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })}
                  </CardDescription>
                </div>
                <Button
                  onClick={() => handleDownload(report.id)}
                  className="rounded-xl"
                  style={{
                    background: 'var(--gradient-primary)',
                    color: 'hsl(var(--primary-foreground))'
                  }}
                >
                  <Download className="w-4 h-4 mr-2" />
                  Download
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-6">
                <div>
                  <p className="text-sm mb-1" style={{ color: 'hsl(var(--muted-foreground))' }}>Total Scans</p>
                  <p className="text-2xl font-bold" style={{ color: 'hsl(var(--foreground))' }}>{report.scans}</p>
                </div>
                <div>
                  <p className="text-sm mb-1" style={{ color: 'hsl(var(--muted-foreground))' }}>Detections</p>
                  <p className="text-2xl font-bold" style={{ color: 'hsl(var(--destructive))' }}>{report.detections}</p>
                </div>
                <div>
                  <p className="text-sm mb-1" style={{ color: 'hsl(var(--muted-foreground))' }}>Healthy</p>
                  <p className="text-2xl font-bold" style={{ color: 'hsl(var(--success))' }}>{report.healthyPlants}</p>
                </div>
                <div>
                  <p className="text-sm mb-1" style={{ color: 'hsl(var(--muted-foreground))' }}>Most Common</p>
                  <p className="text-base font-semibold" style={{ color: 'hsl(var(--foreground))' }}>{report.mostCommon}</p>
                </div>
                <div>
                  <p className="text-sm mb-1" style={{ color: 'hsl(var(--muted-foreground))' }}>Status</p>
                  <Badge style={{ background: 'hsl(var(--success))', color: 'white' }}>
                    {report.status}
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}