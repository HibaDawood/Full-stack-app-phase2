// contexts/LanguageContext.tsx
import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { Language, TranslationKeys } from '../types/i18n';
import { en } from '../translations/en';
import { zh } from '../translations/zh';

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: keyof TranslationKeys) => string;
}

const translations: Record<Language, TranslationKeys> = {
  en,
  zh,
};

const getInitialLanguage = (): Language => {
  if (typeof window !== 'undefined') {
    const savedLang = localStorage.getItem('language');
    if (savedLang && (savedLang === 'en' || savedLang === 'zh')) {
      return savedLang as Language;
    }
    
    // Detect user's language preference
    const userLang = navigator.language.substring(0, 2);
    if (userLang === 'zh') {
      return 'zh';
    }
  }
  return 'en';
};

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [language, setLanguage] = useState<Language>(getInitialLanguage);

  useEffect(() => {
    localStorage.setItem('language', language);
  }, [language]);

  const t = (key: keyof TranslationKeys): string => {
    return translations[language][key] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};