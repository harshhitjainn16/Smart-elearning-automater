"""
Show Machine Info and Data Files
Helps identify which files belong to this device
"""
import platform
import getpass
import os

print("=" * 60)
print("🖥️  MACHINE INFORMATION")
print("=" * 60)

machine_id = f"{platform.node()}_{getpass.getuser()}".replace(" ", "_")

print(f"\nComputer Name: {platform.node()}")
print(f"Username: {getpass.getuser()}")
print(f"\n🆔 Unique Machine ID: {machine_id}")

print("\n" + "=" * 60)
print("📁 YOUR DATA FILES")
print("=" * 60)

data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
db_file = f'learning_progress_{machine_id}.db'
log_file = f'automation_{machine_id}.log'

print(f"\nDatabase: {db_file}")
db_path = os.path.join(data_dir, db_file)
if os.path.exists(db_path):
    size = os.path.getsize(db_path) / 1024
    print(f"  ✅ Exists ({size:.2f} KB)")
else:
    print(f"  ⚠️  Not created yet (will be created on first use)")

print(f"\nLog File: {log_file}")
log_path = os.path.join(data_dir, log_file)
if os.path.exists(log_path):
    size = os.path.getsize(log_path) / 1024
    print(f"  ✅ Exists ({size:.2f} KB)")
else:
    print(f"  ⚠️  Not created yet (will be created on first use)")

# Check for old shared database
old_db = os.path.join(data_dir, 'learning_progress.db')
if os.path.exists(old_db):
    print("\n" + "⚠️ " * 20)
    print("FOUND OLD SHARED DATABASE: learning_progress.db")
    print("This was used before the multi-device fix.")
    print("\nOptions:")
    print(f"1. Rename to your machine: ren learning_progress.db {db_file}")
    print("2. Delete it: del learning_progress.db")
    print("3. Keep as backup (won't be used)")

print("\n" + "=" * 60)
print("🌐 BROWSER PROFILE LOCATION")
print("=" * 60)

import tempfile
profile_dir = os.path.join(tempfile.gettempdir(), f'selenium_profile_{machine_id}')
print(f"\n{profile_dir}")
if os.path.exists(profile_dir):
    print("  ✅ Profile exists")
else:
    print("  ⚠️  Will be created on first browser launch")

print("\n" + "=" * 60)
print("✅ All set! Each device has its own data.")
print("=" * 60 + "\n")
