'use client';

import React, { useState } from 'react';
import { Card, CardHeader, CardContent, CardFooter } from './ui/Card';
import { Button } from './ui/Button';

interface Source {
  text: string;
  reference: string;
  translation: string;
  commentary: string;
}

interface AnswerCardProps {
  answer: string;
  sources: Source[];
  traditionName: string;
  onCompare?: () => void;
  onShare?: () => void;
  onFeedback?: (type: 'accurate' | 'clarify_source' | 'suggest_tradition') => void;
}

const AnswerCard: React.FC<AnswerCardProps> = ({
  answer,
  sources,
  traditionName,
  onCompare,
  onShare,
  onFeedback,
}) => {
  const [showSources, setShowSources] = useState(false);

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100">
          Ответ согласно {traditionName}
        </h2>
      </CardHeader>
      
      <CardContent>
        <div className="prose dark:prose-invert max-w-none">
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap">
            {answer}
          </p>
        </div>
        
        {/* Sources Section */}
        {sources.length > 0 && (
          <div className="mt-6">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowSources(!showSources)}
              className="mb-3"
            >
              {showSources ? 'Скрыть источники' : `Показать источники (${sources.length})`}
            </Button>
            
            {showSources && (
              <div className="space-y-4 bg-gray-50 dark:bg-gray-900/50 p-4 rounded-lg">
                <h3 className="font-semibold text-gray-800 dark:text-gray-200 mb-3">
                  Источники:
                </h3>
                {sources.map((source, index) => (
                  <div key={index} className="border-l-4 border-primary-500 pl-4">
                    <blockquote className="italic text-gray-700 dark:text-gray-300 mb-2">
                      "{source.text}"
                    </blockquote>
                    <cite className="text-sm text-gray-600 dark:text-gray-400 not-italic">
                      — {source.reference}
                      {source.translation !== 'оригинал' && (
                        <span>, {source.translation}</span>
                      )}
                    </cite>
                    {source.commentary && (
                      <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                        {source.commentary}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </CardContent>
      
      <CardFooter className="flex flex-col sm:flex-row gap-3 justify-between">
        <div className="flex gap-2 flex-wrap">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => onFeedback?.('accurate')}
          >
            ✅ Точно
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={() => onFeedback?.('clarify_source')}
          >
            🔍 Уточнить источник
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={() => onFeedback?.('suggest_tradition')}
          >
            💡 Предложить традицию
          </Button>
        </div>
        
        <div className="flex gap-2">
          {onCompare && (
            <Button variant="outline" size="sm" onClick={onCompare}>
              🔍 Сравнить
            </Button>
          )}
          {onShare && (
            <Button variant="outline" size="sm" onClick={onShare}>
              📤 Поделиться
            </Button>
          )}
        </div>
      </CardFooter>
      
      {/* Disclaimer */}
      <div className="px-6 pb-4">
        <p className="text-xs text-gray-500 dark:text-gray-500 italic">
          Ответ сформирован на основе открытых источников выбранной традиции. 
          Не является богословским или профессиональным руководством.
        </p>
      </div>
    </Card>
  );
};

export default AnswerCard;
