export type FoundationModule = {
  id: string;
  label: string;
  status: 'ready' | 'extension';
  description: string;
};

export type ScaffoldFormValues = {
  workspaceLabel: string;
  apiBaseUrl: string;
  releaseChannel: string;
};
