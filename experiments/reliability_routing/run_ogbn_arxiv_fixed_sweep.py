from __future__ import annotations

import sys

from run_fixed_param_sweep import main


if __name__ == "__main__":
    if "--datasets" not in sys.argv:
        sys.argv.extend(["--datasets", "OGBN-Arxiv"])
    main()
