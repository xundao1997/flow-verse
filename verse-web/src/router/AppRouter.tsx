import { BrowserRouter } from 'react-router-dom';

import { AppRoutes } from '@/router/routes';

export function AppRouter() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <AppRoutes />
    </BrowserRouter>
  );
}
