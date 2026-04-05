import type { PropsWithChildren } from 'react';

import { cn } from '@/utils/cn';

type PanelProps = PropsWithChildren<{
  className?: string;
  eyebrow?: string;
  title: string;
  description?: string;
}>;

export function Panel({ children, className, eyebrow, title, description }: PanelProps) {
  return (
    <section className={cn('rounded-shell border border-ink/10 bg-cloud/90 p-6 shadow-panel', className)}>
      <div className="space-y-2">
        {eyebrow ? <p className="text-xs uppercase tracking-[0.3em] text-lagoon">{eyebrow}</p> : null}
        <h2 className="font-display text-2xl text-ink">{title}</h2>
        {description ? <p className="max-w-2xl text-sm leading-6 text-ink/70">{description}</p> : null}
      </div>
      <div className="mt-6">{children}</div>
    </section>
  );
}
