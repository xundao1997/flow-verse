import { render, screen } from '@testing-library/react';

import { App } from '@/app/App';

it('renders the not found route for unknown paths', async () => {
  window.history.pushState({}, 'Test route', '/missing-route');
  render(<App />);

  expect(await screen.findByText('Route not found')).toBeInTheDocument();
});
