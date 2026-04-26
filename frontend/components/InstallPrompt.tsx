'use client';

import React, { useState, useEffect } from 'react';
import { Button } from './ui/Button';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

const InstallPrompt: React.FC = () => {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [showPrompt, setShowPrompt] = useState(false);

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
      
      // Show prompt after 2 visits or scroll > 60%
      const visitCount = parseInt(localStorage.getItem('visitCount') || '0', 10);
      if (visitCount >= 2) {
        setShowPrompt(true);
      }
      localStorage.setItem('visitCount', String(visitCount + 1));
    };

    window.addEventListener('beforeinstallprompt', handler);

    return () => {
      window.removeEventListener('beforeinstallprompt', handler);
    };
  }, []);

  const handleInstall = async () => {
    if (!deferredPrompt) return;

    await deferredPrompt.prompt();
    const choiceResult = await deferredPrompt.userChoice;

    if (choiceResult.outcome === 'accepted') {
      console.log('User accepted the install prompt');
    }
    
    setDeferredPrompt(null);
    setShowPrompt(false);
  };

  const handleDismiss = () => {
    setShowPrompt(false);
    localStorage.setItem('installPromptDismissed', 'true');
  };

  if (!showPrompt || !deferredPrompt) return null;

  return (
    <div className="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:w-96 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-4 z-50">
      <div className="flex items-start gap-3">
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-1">
            Установить Answers
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Добавьте приложение на главный экран для быстрого доступа и офлайн-режима
          </p>
        </div>
        <button
          onClick={handleDismiss}
          className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          aria-label="Закрыть"
        >
          ✕
        </button>
      </div>
      <div className="mt-3 flex gap-2 justify-end">
        <Button variant="secondary" size="sm" onClick={handleDismiss}>
          Позже
        </Button>
        <Button variant="primary" size="sm" onClick={handleInstall}>
          Установить
        </Button>
      </div>
    </div>
  );
};

export default InstallPrompt;
