import { useQuery } from '@tanstack/react-query';

import type { FoundationModule } from '@/types/runtime';

const foundationModules: FoundationModule[] = [
  {
    id: 'routing',
    label: 'Routing',
    status: 'ready',
    description: 'Central route definitions with lazy page imports and a guarded 404 path.',
  },
  {
    id: 'state',
    label: 'State',
    status: 'ready',
    description: 'A small Zustand store with a stable pattern for future slice extraction.',
  },
  {
    id: 'forms',
    label: 'Forms',
    status: 'ready',
    description: 'React Hook Form wiring and validation patterns for future feature forms.',
  },
  {
    id: 'http',
    label: 'Data Layer',
    status: 'extension',
    description: 'A generic request client and React Query provider ready for API modules.',
  },
];

async function loadFoundationModules() {
  return Promise.resolve(foundationModules);
}

export function useFoundationModules() {
  return useQuery({
    queryKey: ['foundation-modules'],
    queryFn: loadFoundationModules,
    staleTime: 5 * 60 * 1000,
  });
}
