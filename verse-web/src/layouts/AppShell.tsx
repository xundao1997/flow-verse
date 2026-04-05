import type { PropsWithChildren } from 'react';
import { Link } from 'react-router-dom';

import { StatusPill } from '@/components/common/StatusPill';
import { env } from '@/config/env';
import { useAppStore } from '@/store/appStore';
import { cn } from '@/utils/cn';

export function AppShell({ children }: PropsWithChildren) {
  const accentTone = useAppStore((state) => state.accentTone);
  const sidebarCollapsed = useAppStore((state) => state.sidebarCollapsed);
  const toggleSidebar = useAppStore((state) => state.toggleSidebar);
  const setAccentTone = useAppStore((state) => state.setAccentTone);

  return (
    <div className="min-h-screen bg-canvas px-4 py-6 text-ink sm:px-6 lg:px-10">
      <div className="mx-auto flex min-h-[calc(100vh-3rem)] max-w-7xl flex-col gap-6 lg:flex-row">
        <aside
          className={cn(
            'rounded-shell border border-ink/10 bg-cloud/90 p-6 shadow-panel transition-all duration-300',
            sidebarCollapsed ? 'lg:w-24' : 'lg:w-80',
          )}
        >
          <div className="flex items-start justify-between gap-4">
            <Link to="/" className="space-y-2">
              <p className="font-display text-xs uppercase tracking-[0.35em] text-lagoon">Verse Web</p>
              {!sidebarCollapsed && (
                <h1 className="font-display text-3xl leading-none text-ink">Frontend Foundation</h1>
              )}
            </Link>
            <button
              type="button"
              onClick={toggleSidebar}
              className="rounded-full border border-ink/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-ink/70 transition hover:border-ink/30 hover:text-ink"
            >
              {sidebarCollapsed ? 'Open' : 'Fold'}
            </button>
          </div>

          {!sidebarCollapsed && (
            <>
              <p className="mt-6 text-sm leading-6 text-ink/70">
                A reusable shell for routing, forms, state, queries, and request primitives without introducing domain code.
              </p>

              <div className="mt-6 grid gap-3 rounded-3xl bg-haze p-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs uppercase tracking-[0.25em] text-ink/50">Runtime</span>
                  <StatusPill label="Scaffold Ready" tone={accentTone} />
                </div>
                <dl className="space-y-3 text-sm">
                  <div>
                    <dt className="text-ink/45">App name</dt>
                    <dd className="font-medium text-ink">{env.appName}</dd>
                  </div>
                  <div>
                    <dt className="text-ink/45">API base URL</dt>
                    <dd className="break-all font-medium text-ink">{env.apiBaseUrl}</dd>
                  </div>
                </dl>
              </div>

              <div className="mt-6 space-y-3">
                <p className="text-xs uppercase tracking-[0.25em] text-ink/45">Accent Tone</p>
                <div className="flex gap-3">
                  <button
                    type="button"
                    onClick={() => setAccentTone('lagoon')}
                    className="h-10 flex-1 rounded-full bg-lagoon text-xs font-semibold uppercase tracking-[0.2em] text-white"
                  >
                    Lagoon
                  </button>
                  <button
                    type="button"
                    onClick={() => setAccentTone('ember')}
                    className="h-10 flex-1 rounded-full bg-ember text-xs font-semibold uppercase tracking-[0.2em] text-white"
                  >
                    Ember
                  </button>
                </div>
              </div>
            </>
          )}
        </aside>

        <main className="flex-1">{children}</main>
      </div>
    </div>
  );
}
