import os
sync_command = f"aws s3 sync <src-bucket> <dest-bucket>"
os.system(sync_command)
