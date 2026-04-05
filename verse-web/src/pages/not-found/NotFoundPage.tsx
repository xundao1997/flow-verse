import { Link } from 'react-router-dom';

import { Button } from '@/components/common/Button';
import { Panel } from '@/components/common/Panel';

function NotFoundPage() {
  return (
    <Panel
      eyebrow="404"
      title="Route not found"
      description="The requested page is not part of the foundation scaffold. Add a new route definition when the next feature slice is ready."
    >
      <div className="flex flex-wrap gap-3">
        <Link to="/">
          <Button>Return Home</Button>
        </Link>
      </div>
    </Panel>
  );
}

export default NotFoundPage;
