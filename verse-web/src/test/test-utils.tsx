import type { PropsWithChildren } from 'react';

import { render } from '@testing-library/react';
import { QueryClientProvider } from '@tanstack/react-query';

import { createAppQueryClient } from '@/services/query/queryClient';

function TestProviders({ children }: PropsWithChildren) {
  const queryClient = createAppQueryClient();
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}

export function renderWithProviders(ui: React.ReactElement) {
  return render(ui, { wrapper: TestProviders });
}
