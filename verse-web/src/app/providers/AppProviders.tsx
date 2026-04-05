import type { PropsWithChildren} from 'react';
import { useState } from 'react';
import { QueryClientProvider } from '@tanstack/react-query';

import { createAppQueryClient } from '@/services/query/queryClient';

export function AppProviders({ children }: PropsWithChildren) {
  const [queryClient] = useState(() => createAppQueryClient());

  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}
