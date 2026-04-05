import { StatusPill } from '@/components/common/StatusPill';
import { ScaffoldForm } from '@/components/forms/ScaffoldForm';
import { useFoundationModules } from '@/hooks/useFoundationModules';
import { useAppStore } from '@/store/appStore';

function HomePage() {
  const accentTone = useAppStore((state) => state.accentTone);
  const { data = [], isLoading } = useFoundationModules();

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-shell border border-ink/10 bg-ink px-6 py-8 text-cloud shadow-panel lg:px-8">
        <div className="grid gap-8 lg:grid-cols-[1.6fr_0.9fr]">
          <div className="space-y-5">
            <p className="text-xs uppercase tracking-[0.35em] text-cloud/60">React 19 Frontend Scaffold</p>
            <div className="space-y-4">
              <h1 className="font-display text-4xl leading-tight sm:text-5xl">Intentional foundations for long-lived frontend work.</h1>
              <p className="max-w-2xl text-sm leading-7 text-cloud/75 sm:text-base">
                Routing, state, forms, queries, request primitives, tests, and environment handling are pre-wired so feature teams can start from structure instead of boilerplate.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <StatusPill label="TypeScript Ready" tone={accentTone} />
              <StatusPill label="Tailwind Enabled" tone={accentTone === 'lagoon' ? 'ember' : 'lagoon'} />
            </div>
          </div>

          <div className="grid gap-4 rounded-3xl bg-white/8 p-5">
            <div>
              <p className="text-xs uppercase tracking-[0.25em] text-cloud/45">Included Capabilities</p>
              <p className="mt-2 text-3xl font-semibold text-cloud">{data.length || 4}</p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.25em] text-cloud/45">Query State</p>
              <p className="mt-2 text-lg font-medium text-cloud">{isLoading ? 'Loading' : 'Warm cache'}</p>
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.25em] text-cloud/45">Extensibility</p>
              <p className="mt-2 text-lg font-medium text-cloud">Modular, typed, test-backed</p>
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.25fr_0.95fr]">
        <div className="rounded-shell border border-ink/10 bg-cloud/90 p-6 shadow-panel">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-lagoon">System Map</p>
              <h2 className="mt-2 font-display text-2xl text-ink">Scaffold modules</h2>
            </div>
            <StatusPill label={isLoading ? 'Loading' : 'Live'} tone={accentTone} />
          </div>

          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            {data.map((module) => (
              <article key={module.id} className="rounded-3xl border border-ink/10 bg-white p-5">
                <div className="flex items-center justify-between gap-3">
                  <h3 className="text-lg font-semibold text-ink">{module.label}</h3>
                  <StatusPill label={module.status === 'ready' ? 'Ready' : 'Extend'} tone={module.status === 'ready' ? accentTone : 'ember'} />
                </div>
                <p className="mt-3 text-sm leading-6 text-ink/70">{module.description}</p>
              </article>
            ))}
          </div>
        </div>

        <ScaffoldForm />
      </section>
    </div>
  );
}

export default HomePage;
