// app/layout-content.tsx
'use client';

import { useLanguage } from '@/contexts/LanguageContext';
import { Providers } from '@/providers';
import '@/app/globals.css';
import { Inter } from 'next/font/google';
import { ReactNode } from 'react';

const inter = Inter({ subsets: ['latin'] });

interface LayoutContentProps {
  children: ReactNode;
}

export default function LayoutContent({ children }: LayoutContentProps) {
  const { t } = useLanguage();
  
  return (
    <html lang={useLanguage().language}>
      <head>
        <title>{t('appTitle')}</title>
        <meta name="description" content={t('welcomeBack')} />
      </head>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}