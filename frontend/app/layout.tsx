import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Scholar Sync Audit',
  description: 'Streamed PDF audit UI with evidence highlighting and migration guidance.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
