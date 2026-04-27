import { type HTMLAttributes } from 'react';
import { cn } from '../../lib/utils';

interface BadgeProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'secondary' | 'outline';
}

export function Badge({ className, variant = 'default', ...props }: BadgeProps) {
  return (
    <div
      className={cn(
        'inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.22em] text-slate-300',
        variant === 'default' && 'bg-slate-800 text-slate-100',
        variant === 'secondary' && 'bg-slate-900 text-slate-300',
        variant === 'outline' && 'border border-slate-700 bg-transparent text-slate-300',
        className,
      )}
      {...props}
    />
  );
}
