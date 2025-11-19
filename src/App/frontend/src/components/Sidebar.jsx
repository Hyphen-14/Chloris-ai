import React from 'react';
import { Camera, BookOpen, FileText, Settings, Flower2 } from 'lucide-react';
import { cn } from '../lib/utils';

export default function Sidebar({ currentPage, setCurrentPage }) {
  const menuItems = [
    { id: 'scanner', label: 'Scanner', icon: Camera },
    { id: 'encyclopedia', label: 'Encyclopedia', icon: BookOpen },
    { id: 'report', label: 'Report', icon: FileText },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="glass-sidebar w-72 h-screen flex flex-col p-6">
      {/* Logo Section */}
      <div className="mb-12 animate-fade-in">
        <div className="flex items-center justify-center mb-4">
          <div className="w-24 h-24 rounded-full glass-card flex items-center justify-center animate-pulse-glow">
            <Flower2 className="w-12 h-12" style={{ color: 'hsl(var(--primary))' }} />
          </div>
        </div>
        <h1 className="text-3xl font-bold text-center" style={{ color: 'hsl(var(--primary))' }}>
          Chloris
        </h1>
        <p className="text-center text-sm mt-2" style={{ color: 'hsl(var(--muted-foreground))' }}>
          Goddess of Flowers
        </p>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1">
        <ul className="space-y-3">
          {menuItems.map((item, index) => {
            const Icon = item.icon;
            const isActive = currentPage === item.id;
            
            return (
              <li key={item.id} style={{ animationDelay: `${index * 0.1}s` }} className="animate-fade-in">
                <button
                  onClick={() => setCurrentPage(item.id)}
                  className={cn(
                    'w-full flex items-center gap-4 px-5 py-4 rounded-xl transition-all duration-300',
                    isActive
                      ? 'glass-card text-primary shadow-md'
                      : 'hover:glass-button text-muted-foreground hover:text-primary'
                  )}
                  style={{
                    color: isActive ? 'hsl(var(--primary))' : undefined,
                  }}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium text-base">{item.label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer */}
      <div className="mt-auto pt-6 border-t" style={{ borderColor: 'hsl(var(--border))' }}>
        <p className="text-xs text-center" style={{ color: 'hsl(var(--muted-foreground))' }}>
          Plant Disease Detection
        </p>
        <p className="text-xs text-center mt-1 font-medium" style={{ color: 'hsl(var(--primary))' }}>
          Powered by AI Vision
        </p>
      </div>
    </aside>
  );
}