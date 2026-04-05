import { initialAppStoreState, useAppStore } from '@/store/appStore';

afterEach(() => {
  useAppStore.setState({
    ...initialAppStoreState,
    setAccentTone: useAppStore.getState().setAccentTone,
    toggleSidebar: useAppStore.getState().toggleSidebar,
  });
});

it('toggles the sidebar state and updates the accent tone', () => {
  useAppStore.getState().toggleSidebar();
  useAppStore.getState().setAccentTone('ember');

  expect(useAppStore.getState().sidebarCollapsed).toBe(true);
  expect(useAppStore.getState().accentTone).toBe('ember');
});
