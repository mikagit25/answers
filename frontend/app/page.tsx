'use client';

import React, { useState, useEffect } from 'react';
import TraditionSelector from '@/components/TraditionSelector';
import QuestionInput from '@/components/QuestionInput';
import AnswerCard from '@/components/AnswerCard';
import { askQuestion, loadTraditions, type Tradition, type AskResponse } from '@/lib/api';

export default function Home() {
  const [traditions, setTraditions] = useState<Tradition[]>([]);
  const [selectedTradition, setSelectedTradition] = useState<string | null>(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState<AskResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load traditions on mount
  useEffect(() => {
    const fetchTraditions = async () => {
      try {
        const data = await loadTraditions();
        setTraditions(data);
      } catch (err) {
        console.error('Failed to load traditions:', err);
        setError('Не удалось загрузить список традиций');
      }
    };
    
    fetchTraditions();
  }, []);

  const handleAskQuestion = async (userQuestion: string) => {
    if (!selectedTradition) {
      setError('Пожалуйста, выберите традицию');
      return;
    }

    setIsLoading(true);
    setError(null);
    setQuestion(userQuestion);

    try {
      const response = await askQuestion({
        question: userQuestion,
        tradition_id: selectedTradition,
        depth: 'basic',
      });
      
      setAnswer(response);
    } catch (err: any) {
      console.error('Error asking question:', err);
      setError(err.message || 'Произошла ошибка при получении ответа');
    } finally {
      setIsLoading(false);
    }
  };

  const handleShare = () => {
    if (answer?.share_url) {
      const url = `${window.location.origin}${answer.share_url}`;
      navigator.clipboard.writeText(url);
      alert('Ссылка скопирована в буфер обмена!');
    }
  };

  const handleFeedback = (type: 'accurate' | 'clarify_source' | 'suggest_tradition') => {
    console.log('Feedback:', type);
    // TODO: Implement feedback submission
    alert('Спасибо за обратную связь!');
  };

  const getTraditionName = (id: string) => {
    return traditions.find(t => t.id === id)?.name || id;
  };

  return (
    <main className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {/* Header */}
        <header className="text-center space-y-4">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-gray-100">
            Answers
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Платформа ответов на жизненные, этические и духовные вопросы 
            в рамках различных философских и религиозных традиций
          </p>
        </header>

        {/* Tradition Selector */}
        <section>
          <TraditionSelector
            traditions={traditions}
            selectedTradition={selectedTradition}
            onSelect={setSelectedTradition}
          />
        </section>

        {/* Question Input */}
        <section>
          <QuestionInput
            onSubmit={handleAskQuestion}
            isLoading={isLoading}
          />
        </section>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-4 rounded">
            <p className="text-red-700 dark:text-red-400">{error}</p>
          </div>
        )}

        {/* Answer Card */}
        {answer && (
          <section>
            <AnswerCard
              answer={answer.answer}
              sources={answer.sources}
              traditionName={getTraditionName(answer.tradition_id)}
              onShare={handleShare}
              onFeedback={handleFeedback}
            />
          </section>
        )}

        {/* Footer */}
        <footer className="text-center text-sm text-gray-500 dark:text-gray-500 pt-8 pb-4">
          <p>© 2026 Answers Platform. Все ответы основаны на открытых источниках.</p>
        </footer>
      </div>
    </main>
  );
}
