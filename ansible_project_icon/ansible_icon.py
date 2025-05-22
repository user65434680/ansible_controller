import os
import shutil

source_file = "/opt/ansible_icon/start.sh"
home_root = "/home"

for username in os.listdir(home_root):
    user_home = os.path.join(home_root, username)
    
    if os.path.isdir(user_home):
        dest_file = os.path.join(user_home, "start.sh")
        try:
            shutil.copy(source_file, dest_file)
            os.chmod(dest_file, 0o755)
            shutil.chown(dest_file, user=username, group=username)
            print(f"Copied to {dest_file}")
        except Exception as e:
            print(f"Failed to copy to {user_home}: {e}")

root_home = "/root"
if os.path.isdir(root_home):
    dest_file = os.path.join(root_home, "start.sh")
    try:
        shutil.copy(source_file, dest_file)
        os.chmod(dest_file, 0o755)
        print(f"Copied to {dest_file}")
    except Exception as e:
        print(f"Failed to copy to root home: {e}")