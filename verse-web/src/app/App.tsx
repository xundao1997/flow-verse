import { AppProviders } from '@/app/providers/AppProviders';
import { AppRouter } from '@/router/AppRouter';

export function App() {
  return (
    <AppProviders>
      <AppRouter />
    </AppProviders>
  );
}
