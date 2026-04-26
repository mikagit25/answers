'use client';

import React, { useState } from 'react';
import { Button } from './ui/Button';

interface QuestionInputProps {
  onSubmit: (question: string) => void;
  isLoading?: boolean;
}

const QuestionInput: React.FC<QuestionInputProps> = ({ onSubmit, isLoading = false }) => {
  const [question, setQuestion] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (question.trim().length < 10) {
      setError('Вопрос должен содержать минимум 10 символов');
      return;
    }
    
    if (question.trim().length > 500) {
      setError('Вопрос не должен превышать 500 символов');
      return;
    }
    
    setError(null);
    onSubmit(question.trim());
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Задайте ваш вопрос о жизни, этике или духовности..."
          disabled={isLoading}
          rows={3}
          className={`
            w-full px-4 py-3 rounded-xl border-2 resize-none
            transition-all duration-200
            focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
            disabled:opacity-50 disabled:cursor-not-allowed
            ${error 
              ? 'border-red-500 dark:border-red-400' 
              : 'border-gray-300 dark:border-gray-600'
            }
            bg-white dark:bg-gray-800
            text-gray-900 dark:text-gray-100
            placeholder-gray-500 dark:placeholder-gray-400
          `}
        />
        
        <div className="mt-2 flex justify-between items-center">
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {question.length}/500
          </span>
          
          <Button 
            type="submit" 
            disabled={isLoading || question.trim().length < 10}
            size="lg"
          >
            {isLoading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Думаю...
              </span>
            ) : (
              'Получить ответ'
            )}
          </Button>
        </div>
        
        {error && (
          <p className="mt-2 text-sm text-red-600 dark:text-red-400">
            {error}
          </p>
        )}
      </div>
    </form>
  );
};

export default QuestionInput;
