import { type HTMLAttributes } from 'react';
import { cn } from '../../lib/utils';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  asChild?: boolean;
}

export function Card({ className, ...props }: CardProps) {
  return <div className={cn('rounded-3xl border border-slate-800 bg-slate-900/90 shadow-xl shadow-slate-950/25', className)} {...props} />;
}
