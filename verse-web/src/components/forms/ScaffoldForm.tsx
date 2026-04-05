import { useState } from 'react';
import type { SubmitHandler} from 'react-hook-form';
import { useForm } from 'react-hook-form';

import { Button } from '@/components/common/Button';
import { Panel } from '@/components/common/Panel';
import { env } from '@/config/env';
import type { ScaffoldFormValues } from '@/types/runtime';

export function ScaffoldForm() {
  const [preview, setPreview] = useState<ScaffoldFormValues | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ScaffoldFormValues>({
    mode: 'onBlur',
    defaultValues: {
      workspaceLabel: 'verse-web',
      apiBaseUrl: env.apiBaseUrl,
      releaseChannel: 'stable',
    },
  });

  const onSubmit: SubmitHandler<ScaffoldFormValues> = async (values) => {
    setPreview(values);
  };

  return (
    <Panel
      eyebrow="Form Setup"
      title="React Hook Form baseline"
      description="A neutral example for validation and submission state handling that future feature forms can follow."
    >
      <form className="grid gap-5" onSubmit={handleSubmit(onSubmit)} noValidate>
        <label className="grid gap-2 text-sm">
          <span className="font-medium text-ink">Workspace label</span>
          <input
            className="h-12 rounded-2xl border border-ink/10 bg-white px-4 outline-none transition focus:border-lagoon"
            {...register('workspaceLabel', {
              required: 'Workspace label is required.',
              minLength: {
                value: 3,
                message: 'Use at least 3 characters.',
              },
            })}
          />
          {errors.workspaceLabel ? <span className="text-xs text-ember">{errors.workspaceLabel.message}</span> : null}
        </label>

        <label className="grid gap-2 text-sm">
          <span className="font-medium text-ink">API base URL</span>
          <input
            className="h-12 rounded-2xl border border-ink/10 bg-white px-4 outline-none transition focus:border-lagoon"
            {...register('apiBaseUrl', {
              required: 'API base URL is required.',
              pattern: {
                value: /^https?:\/\/.+/i,
                message: 'Use an absolute http(s) URL.',
              },
            })}
          />
          {errors.apiBaseUrl ? <span className="text-xs text-ember">{errors.apiBaseUrl.message}</span> : null}
        </label>

        <label className="grid gap-2 text-sm">
          <span className="font-medium text-ink">Release channel</span>
          <select
            className="h-12 rounded-2xl border border-ink/10 bg-white px-4 outline-none transition focus:border-lagoon"
            {...register('releaseChannel', {
              required: 'Release channel is required.',
            })}
          >
            <option value="stable">stable</option>
            <option value="preview">preview</option>
            <option value="canary">canary</option>
          </select>
        </label>

        <div className="flex flex-wrap gap-3">
          <Button type="submit" disabled={isSubmitting}>
            Save Scaffold Defaults
          </Button>
          <Button type="button" variant="secondary" onClick={() => setPreview(null)}>
            Clear Preview
          </Button>
        </div>
      </form>

      <div className="mt-6 rounded-3xl bg-ink px-5 py-4 text-sm text-cloud">
        <p className="text-xs uppercase tracking-[0.25em] text-cloud/50">Submission Preview</p>
        <pre className="mt-3 overflow-x-auto font-mono text-xs leading-6 text-cloud/85">{JSON.stringify(preview, null, 2) || 'Submit the form to inspect sanitized values.'}</pre>
      </div>
    </Panel>
  );
}
