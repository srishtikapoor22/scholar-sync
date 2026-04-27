'use client';

import * as React from 'react';
import { cn } from '../../lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
}

export function Button({ className, variant = 'primary', ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-full px-4 py-2 text-sm font-semibold transition focus:outline-none focus:ring-2 focus:ring-sky-400 disabled:cursor-not-allowed disabled:opacity-60',
        variant === 'primary' && 'bg-sky-500 text-white hover:bg-sky-400',
        variant === 'secondary' && 'bg-slate-800 text-slate-100 hover:bg-slate-700',
        variant === 'ghost' && 'bg-transparent text-slate-200 hover:bg-slate-900/30',
        className,
      )}
      {...props}
    />
  );
}
