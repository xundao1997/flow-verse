import type { ButtonHTMLAttributes, PropsWithChildren } from 'react';

import { cn } from '@/utils/cn';

type ButtonProps = PropsWithChildren<ButtonHTMLAttributes<HTMLButtonElement>> & {
  variant?: 'primary' | 'secondary';
};

export function Button({ children, className, variant = 'primary', ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-full px-5 py-3 text-sm font-semibold transition focus:outline-none focus:ring-2 focus:ring-offset-2',
        variant === 'primary'
          ? 'bg-ink text-cloud hover:bg-ink/90 focus:ring-ink/30'
          : 'border border-ink/15 bg-white/80 text-ink hover:border-ink/30 focus:ring-ink/20',
        className,
      )}
      {...props}
    >
      {children}
    </button>
  );
}
