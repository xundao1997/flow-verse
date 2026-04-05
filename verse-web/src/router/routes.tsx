import { Suspense, lazy } from 'react';
import type { RouteObject} from 'react-router-dom';
import { Outlet, useRoutes } from 'react-router-dom';

import { AppShell } from '@/layouts/AppShell';

const HomePage = lazy(() => import('@/pages/home/HomePage'));
const NotFoundPage = lazy(() => import('@/pages/not-found/NotFoundPage'));

function RouteFallback() {
  return (
    <div className="rounded-shell border border-ink/10 bg-cloud/90 p-8 text-sm text-ink/70 shadow-panel">
      Loading foundation modules...
    </div>
  );
}

function ShellLayout() {
  return (
    <AppShell>
      <Suspense fallback={<RouteFallback />}>
        <Outlet />
      </Suspense>
    </AppShell>
  );
}

export const appRoutes: RouteObject[] = [
  {
    path: '/',
    element: <ShellLayout />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: '*',
        element: <NotFoundPage />,
      },
    ],
  },
];

export function AppRoutes() {
  return useRoutes(appRoutes);
}
