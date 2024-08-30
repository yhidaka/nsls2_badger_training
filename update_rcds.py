from pathlib import Path
import shutil

import xopt

src_path = Path.cwd() / "rcds" / "rcds.py"
dst_path = Path(xopt.__file__).parent / "generators" / "rcds" / "rcds.py"
backup_path = dst_path.parent / "rcds.py.original"

shutil.move(dst_path, backup_path)
shutil.copy(src_path, dst_path)
