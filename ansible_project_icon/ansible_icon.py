import os
import shutil

source_file = "/opt/ansible_icon/start.sh"

home_root = "/home"

for username in os.listdir(home_root):
    user_desktop = os.path.join(home_root, username, "Desktop")
    
    if os.path.isdir(user_desktop):
        dest_file = os.path.join(user_desktop, "start.sh")
        try:
            shutil.copy(source_file, dest_file)
            os.chmod(dest_file, 0o755)
            print(f"Copied to {dest_file}")
        except Exception as e:
            print(f"Failed to copy to {user_desktop}: {e}")

root_desktop = "/root/Desktop"
if os.path.isdir(root_desktop):
    dest_file = os.path.join(root_desktop, "start.sh")
    try:
        shutil.copy(source_file, dest_file)
        os.chmod(dest_file, 0o755)
        print(f"Copied to {dest_file}")
    except Exception as e:
        print(f"Failed to copy to root Desktop: {e}")