import { create } from 'zustand';

export type AccentTone = 'lagoon' | 'ember';

export type AppStoreState = {
  accentTone: AccentTone;
  sidebarCollapsed: boolean;
  setAccentTone: (tone: AccentTone) => void;
  toggleSidebar: () => void;
};

export const initialAppStoreState: Pick<AppStoreState, 'accentTone' | 'sidebarCollapsed'> = {
  accentTone: 'lagoon',
  sidebarCollapsed: false,
};

export const useAppStore = create<AppStoreState>((set) => ({
  ...initialAppStoreState,
  setAccentTone: (tone) => set({ accentTone: tone }),
  toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
}));
