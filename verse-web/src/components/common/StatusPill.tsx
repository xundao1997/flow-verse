import type { AccentTone } from '@/store/appStore';
import { cn } from '@/utils/cn';

type StatusPillProps = {
  label: string;
  tone?: AccentTone;
};

export function StatusPill({ label, tone = 'lagoon' }: StatusPillProps) {
  return (
    <span
      className={cn(
        'inline-flex rounded-full px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.22em]',
        tone === 'lagoon' ? 'bg-lagoon/10 text-lagoon' : 'bg-ember/10 text-ember',
      )}
    >
      {label}
    </span>
  );
}
