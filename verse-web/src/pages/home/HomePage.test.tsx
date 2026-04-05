import { screen } from '@testing-library/react';

import HomePage from '@/pages/home/HomePage';
import { renderWithProviders } from '@/test/test-utils';

it('renders the scaffold overview and form baseline', async () => {
  renderWithProviders(<HomePage />);

  expect(screen.getByText('Intentional foundations for long-lived frontend work.')).toBeInTheDocument();
  expect(await screen.findByText('Routing')).toBeInTheDocument();
  expect(screen.getByText('React Hook Form baseline')).toBeInTheDocument();
});
