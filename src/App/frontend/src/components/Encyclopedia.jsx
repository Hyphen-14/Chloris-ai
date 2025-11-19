import React, { useState } from 'react';
import { Search, Leaf, AlertCircle, Info } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Input } from './ui/input';
import { Badge } from './ui/badge';

export default function Encyclopedia() {
  const [searchQuery, setSearchQuery] = useState('');

  const diseases = [
    {
      name: 'Leaf Rust',
      scientificName: 'Puccinia spp.',
      severity: 'high',
      description: 'Fungal disease causing rusty orange spots on leaves',
      symptoms: ['Orange pustules', 'Leaf yellowing', 'Premature leaf drop'],
      treatment: ['Apply fungicide', 'Remove infected leaves', 'Improve air circulation'],
      prevention: ['Avoid overhead watering', 'Space plants properly', 'Use resistant varieties']
    },
    {
      name: 'Powdery Mildew',
      scientificName: 'Erysiphe cichoracearum',
      severity: 'medium',
      description: 'White powdery coating on leaves and stems',
      symptoms: ['White powder on leaves', 'Leaf distortion', 'Stunted growth'],
      treatment: ['Apply sulfur spray', 'Use neem oil', 'Prune affected areas'],
      prevention: ['Ensure good air flow', 'Avoid overcrowding', 'Water at base']
    },
    {
      name: 'Leaf Spot',
      scientificName: 'Cercospora spp.',
      severity: 'high',
      description: 'Dark spots with yellow halos on foliage',
      symptoms: ['Brown spots', 'Yellow halos', 'Leaf deterioration'],
      treatment: ['Remove affected leaves', 'Apply copper fungicide', 'Improve drainage'],
      prevention: ['Avoid wet foliage', 'Sanitize tools', 'Rotate crops']
    },
    {
      name: 'Bacterial Blight',
      scientificName: 'Pseudomonas syringae',
      severity: 'critical',
      description: 'Bacterial infection causing rapid tissue death',
      symptoms: ['Water-soaked lesions', 'Rapid wilting', 'Blackened stems'],
      treatment: ['Isolate plant', 'Apply bactericide', 'Remove infected tissue'],
      prevention: ['Use clean tools', 'Avoid injury to plants', 'Control insects']
    },
    {
      name: 'Downy Mildew',
      scientificName: 'Peronospora spp.',
      severity: 'high',
      description: 'Fuzzy gray growth on leaf undersides',
      symptoms: ['Gray fuzz', 'Yellow patches', 'Leaf curling'],
      treatment: ['Apply fungicide', 'Improve ventilation', 'Remove debris'],
      prevention: ['Reduce humidity', 'Water in morning', 'Space plants']
    }
  ];

  const filteredDiseases = diseases.filter(disease =>
    disease.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    disease.scientificName.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'hsl(0, 70%, 58%)';
      case 'high': return 'hsl(0, 70%, 58%)';
      case 'medium': return 'hsl(38, 92%, 60%)';
      case 'low': return 'hsl(140, 50%, 50%)';
      default: return 'hsl(var(--muted))';
    }
  };

  return (
    <div className="min-h-screen p-8">
      {/* Header */}
      <div className="mb-8 animate-fade-in">
        <h1 className="text-4xl font-bold mb-2" style={{ color: 'hsl(var(--primary))' }}>
          Disease Encyclopedia
        </h1>
        <p className="text-lg" style={{ color: 'hsl(var(--muted-foreground))' }}>
          Comprehensive database of plant diseases and treatments
        </p>
      </div>

      {/* Search Bar */}
      <div className="mb-8 animate-fade-in" style={{ animationDelay: '0.1s' }}>
        <div className="relative max-w-2xl">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5" 
                  style={{ color: 'hsl(var(--muted-foreground))' }} />
          <Input
            type="text"
            placeholder="Search diseases by name or scientific name..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-12 py-6 text-base rounded-xl glass-card border-0"
            style={{ background: 'rgba(255, 255, 255, 0.6)' }}
          />
        </div>
      </div>

      {/* Disease Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredDiseases.map((disease, index) => (
          <Card 
            key={disease.name} 
            className="glass-card border-0 animate-fade-in"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <CardHeader>
              <div className="flex items-start justify-between mb-2">
                <Leaf className="w-8 h-8" style={{ color: getSeverityColor(disease.severity) }} />
                <Badge 
                  variant="secondary"
                  style={{
                    background: getSeverityColor(disease.severity),
                    color: 'white'
                  }}
                >
                  {disease.severity}
                </Badge>
              </div>
              <CardTitle className="text-xl" style={{ color: 'hsl(var(--foreground))' }}>
                {disease.name}
              </CardTitle>
              <CardDescription className="italic">
                {disease.scientificName}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm leading-relaxed" style={{ color: 'hsl(var(--foreground))' }}>
                {disease.description}
              </p>

              {/* Symptoms */}
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <AlertCircle className="w-4 h-4" style={{ color: 'hsl(var(--primary))' }} />
                  <h4 className="text-sm font-semibold" style={{ color: 'hsl(var(--primary))' }}>
                    Symptoms
                  </h4>
                </div>
                <ul className="space-y-1 ml-6">
                  {disease.symptoms.map((symptom, idx) => (
                    <li key={idx} className="text-xs list-disc" style={{ color: 'hsl(var(--muted-foreground))' }}>
                      {symptom}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Treatment */}
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <Info className="w-4 h-4" style={{ color: 'hsl(var(--primary))' }} />
                  <h4 className="text-sm font-semibold" style={{ color: 'hsl(var(--primary))' }}>
                    Treatment
                  </h4>
                </div>
                <ul className="space-y-1 ml-6">
                  {disease.treatment.slice(0, 2).map((treatment, idx) => (
                    <li key={idx} className="text-xs list-disc" style={{ color: 'hsl(var(--muted-foreground))' }}>
                      {treatment}
                    </li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredDiseases.length === 0 && (
        <div className="text-center py-16">
          <div className="w-24 h-24 rounded-full glass-card flex items-center justify-center mx-auto mb-6">
            <Search className="w-12 h-12" style={{ color: 'hsl(var(--muted-foreground))' }} />
          </div>
          <h3 className="text-2xl font-semibold mb-2" style={{ color: 'hsl(var(--foreground))' }}>
            No Results Found
          </h3>
          <p style={{ color: 'hsl(var(--muted-foreground))' }}>
            Try adjusting your search query
          </p>
        </div>
      )}
    </div>
  );
}