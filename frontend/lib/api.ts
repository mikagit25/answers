/**
 * API клиент для взаимодействия с backend.
 * Включает retry логику и timeout.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface ApiOptions extends RequestInit {
  timeout?: number;
  retries?: number;
}

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchWithTimeout(url: string, options: ApiOptions = {}) {
  const { timeout = 10000, ...fetchOptions } = options;
  
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);
  
  try {
    const response = await fetch(url, {
      ...fetchOptions,
      signal: controller.signal,
    });
    clearTimeout(id);
    return response;
  } catch (error) {
    clearTimeout(id);
    throw error;
  }
}

async function fetchWithRetry(
  url: string,
  options: ApiOptions = {}
): Promise<Response> {
  const { retries = 3, ...fetchOptions } = options;
  
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetchWithTimeout(url, fetchOptions);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(response.status, errorData.detail || 'Request failed');
      }
      
      return response;
    } catch (error) {
      if (i === retries - 1) throw error;
      
      // Wait before retry (exponential backoff)
      await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
    }
  }
  
  throw new Error('Max retries exceeded');
}

export interface AskRequest {
  question: string;
  tradition_id: string;
  depth?: string;
}

export interface Source {
  text: string;
  reference: string;
  translation: string;
  commentary: string;
}

export interface AskResponse {
  answer: string;
  sources: Source[];
  tradition_id: string;
  share_url?: string;
  status: string;
  metadata?: {
    model?: string;
    response_time_ms?: number;
    cache_hit?: boolean;
  };
}

export interface Tradition {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
}

export interface Comparison {
  tradition_id: string;
  tradition_name: string;
  summary: string;
  source_preview: string;
}

/**
 * Отправить вопрос и получить ответ
 */
export async function askQuestion(request: AskRequest): Promise<AskResponse> {
  const response = await fetchWithRetry(`${API_BASE_URL}/ask`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
    timeout: 15000,
    retries: 2,
  });
  
  return response.json();
}

/**
 * Получить сравнение ответов разных традиций
 */
export async function compareTraditions(
  question: string,
  exclude?: string
): Promise<Comparison[]> {
  const params = new URLSearchParams({ question });
  if (exclude) params.append('exclude', exclude);
  
  const response = await fetchWithRetry(
    `${API_BASE_URL}/compare?${params.toString()}`,
    {
      timeout: 10000,
      retries: 2,
    }
  );
  
  const data = await response.json();
  return data.comparisons;
}

/**
 * Загрузить список традиций из метаданных
 */
export async function loadTraditions(): Promise<Tradition[]> {
  // В продакшене это должно coming from API
  // Сейчас загружаем из локального файла
  const response = await fetch('/knowledge_base/metadata.json');
  if (!response.ok) {
    throw new ApiError(response.status, 'Failed to load traditions');
  }
  const data = await response.json();
  return data.traditions;
}
