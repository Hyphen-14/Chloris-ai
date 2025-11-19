import React, { useState } from 'react';
import { Settings as SettingsIcon, Bell, Camera, Moon, Sun, Globe, Shield } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Switch } from './ui/switch';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { toast } from 'sonner';

export default function Settings() {
  const [notifications, setNotifications] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [autoScan, setAutoScan] = useState(true);
  const [language, setLanguage] = useState('en');

  const handleToggle = (setting, value, label) => {
    switch (setting) {
      case 'notifications':
        setNotifications(value);
        break;
      case 'darkMode':
        setDarkMode(value);
        break;
      case 'autoScan':
        setAutoScan(value);
        break;
      default:
        break;
    }
    toast.success(`${label} ${value ? 'enabled' : 'disabled'}`);
  };

  return (
    <div className="min-h-screen p-8">
      {/* Header */}
      <div className="mb-8 animate-fade-in">
        <h1 className="text-4xl font-bold mb-2" style={{ color: 'hsl(var(--primary))' }}>
          Settings
        </h1>
        <p className="text-lg" style={{ color: 'hsl(var(--muted-foreground))' }}>
          Customize your Chloris experience
        </p>
      </div>

      <div className="max-w-3xl space-y-6">
        {/* General Settings */}
        <Card className="glass-card border-0 animate-fade-in" style={{ animationDelay: '0.1s' }}>
          <CardHeader>
            <CardTitle className="text-2xl flex items-center gap-3" style={{ color: 'hsl(var(--primary))' }}>
              <SettingsIcon className="w-6 h-6" />
              General
            </CardTitle>
            <CardDescription>Manage your general preferences</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Language */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Globe className="w-5 h-5" style={{ color: 'hsl(var(--primary))' }} />
                <div>
                  <Label className="text-base font-medium" style={{ color: 'hsl(var(--foreground))' }}>Language</Label>
                  <p className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>Select your preferred language</p>
                </div>
              </div>
              <Select value={language} onValueChange={setLanguage}>
                <SelectTrigger className="w-[180px] glass-button border-0">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="en">English</SelectItem>
                  <SelectItem value="es">Español</SelectItem>
                  <SelectItem value="fr">Français</SelectItem>
                  <SelectItem value="id">Bahasa Indonesia</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Dark Mode */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                {darkMode ? (
                  <Moon className="w-5 h-5" style={{ color: 'hsl(var(--primary))' }} />
                ) : (
                  <Sun className="w-5 h-5" style={{ color: 'hsl(var(--primary))' }} />
                )}
                <div>
                  <Label className="text-base font-medium" style={{ color: 'hsl(var(--foreground))' }}>Dark Mode</Label>
                  <p className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>Enable dark theme</p>
                </div>
              </div>
              <Switch
                checked={darkMode}
                onCheckedChange={(value) => handleToggle('darkMode', value, 'Dark mode')}
              />
            </div>
          </CardContent>
        </Card>

        {/* Notifications */}
        <Card className="glass-card border-0 animate-fade-in" style={{ animationDelay: '0.2s' }}>
          <CardHeader>
            <CardTitle className="text-2xl flex items-center gap-3" style={{ color: 'hsl(var(--primary))' }}>
              <Bell className="w-6 h-6" />
              Notifications
            </CardTitle>
            <CardDescription>Configure notification preferences</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Bell className="w-5 h-5" style={{ color: 'hsl(var(--primary))' }} />
                <div>
                  <Label className="text-base font-medium" style={{ color: 'hsl(var(--foreground))' }}>Push Notifications</Label>
                  <p className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>Receive detection alerts</p>
                </div>
              </div>
              <Switch
                checked={notifications}
                onCheckedChange={(value) => handleToggle('notifications', value, 'Notifications')}
              />
            </div>
          </CardContent>
        </Card>

        {/* Camera Settings */}
        <Card className="glass-card border-0 animate-fade-in" style={{ animationDelay: '0.3s' }}>
          <CardHeader>
            <CardTitle className="text-2xl flex items-center gap-3" style={{ color: 'hsl(var(--primary))' }}>
              <Camera className="w-6 h-6" />
              Camera
            </CardTitle>
            <CardDescription>Configure camera and scanning options</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Camera className="w-5 h-5" style={{ color: 'hsl(var(--primary))' }} />
                <div>
                  <Label className="text-base font-medium" style={{ color: 'hsl(var(--foreground))' }}>Auto-Scan</Label>
                  <p className="text-sm" style={{ color: 'hsl(var(--muted-foreground))' }}>Automatically detect plants</p>
                </div>
              </div>
              <Switch
                checked={autoScan}
                onCheckedChange={(value) => handleToggle('autoScan', value, 'Auto-scan')}
              />
            </div>
          </CardContent>
        </Card>

        {/* Privacy & Security */}
        <Card className="glass-card border-0 animate-fade-in" style={{ animationDelay: '0.4s' }}>
          <CardHeader>
            <CardTitle className="text-2xl flex items-center gap-3" style={{ color: 'hsl(var(--primary))' }}>
              <Shield className="w-6 h-6" />
              Privacy & Security
            </CardTitle>
            <CardDescription>Manage your data and privacy</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-4 rounded-lg" style={{ background: 'hsl(var(--muted))' }}>
                <h4 className="font-semibold mb-2" style={{ color: 'hsl(var(--foreground))' }}>Data Collection</h4>
                <p className="text-sm leading-relaxed" style={{ color: 'hsl(var(--muted-foreground))' }}>
                  We collect scan data to improve our AI models. All data is anonymized and encrypted.
                </p>
              </div>
              <div className="p-4 rounded-lg" style={{ background: 'hsl(var(--muted))' }}>
                <h4 className="font-semibold mb-2" style={{ color: 'hsl(var(--foreground))' }}>Camera Access</h4>
                <p className="text-sm leading-relaxed" style={{ color: 'hsl(var(--muted-foreground))' }}>
                  Camera access is required for plant scanning. Images are processed locally and not stored on our servers.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* About */}
        <Card className="glass-card border-0 animate-fade-in" style={{ animationDelay: '0.5s' }}>
          <CardHeader>
            <CardTitle className="text-2xl" style={{ color: 'hsl(var(--primary))' }}>About Chloris</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span style={{ color: 'hsl(var(--muted-foreground))' }}>Version</span>
                <span className="font-medium" style={{ color: 'hsl(var(--foreground))' }}>1.0.0</span>
              </div>
              <div className="flex justify-between items-center">
                <span style={{ color: 'hsl(var(--muted-foreground))' }}>Model</span>
                <span className="font-medium" style={{ color: 'hsl(var(--foreground))' }}>YOLO v8</span>
              </div>
              <div className="flex justify-between items-center">
                <span style={{ color: 'hsl(var(--muted-foreground))' }}>Accuracy</span>
                <span className="font-bold" style={{ color: 'hsl(var(--success))' }}>98.2%</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}