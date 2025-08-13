#!/usr/bin/env python
# apply_optimizations.py - Script to apply all performance optimizations to SNAIKS game
import os
import shutil
import time
import sys


def backup_file(filepath):
    """Create a backup of a file"""
    backup_path = filepath + ".bak"
    try:
        shutil.copy2(filepath, backup_path)
        print(f"✓ Created backup: {backup_path}")
        return True
    except Exception as e:
        print(f"✗ Backup failed for {filepath}: {e}")
        return False


def apply_optimizations():
    """Apply all performance optimizations to the game files"""
    print("🚀 SNAIKS Performance Optimization")
    print("==================================")

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Create backups first
    files_to_backup = ["basic_behavior.py", "resource_manager.py", "game_manager.py"]

    print("\nCreating backups...")
    for file in files_to_backup:
        filepath = os.path.join(base_dir, file)
        if not os.path.exists(filepath):
            print(f"✗ File not found: {filepath}")
            continue

        backup_file(filepath)

    # 1. Replace basic_behavior.py with optimized version
    print("\nApplying optimizations to basic_behavior.py...")
    try:
        optimized_file = os.path.join(base_dir, "basic_behavior_optimized.py")
        target_file = os.path.join(base_dir, "basic_behavior.py")

        if os.path.exists(optimized_file):
            shutil.copy2(optimized_file, target_file)
            print("✓ Applied optimized behavior system")
        else:
            print(f"✗ Optimized file not found: {optimized_file}")
    except Exception as e:
        print(f"✗ Failed to apply behavior optimizations: {e}")

    # 2. Apply TextCache and NumPy particle system optimizations
    print("\nUpdating resource_manager.py with optimized classes...")
    try:
        # Import the optimized classes
        patch_successful = False

        with open(os.path.join(base_dir, "resource_manager.py"), "r") as f:
            resource_manager_code = f.read()

        # Add import for OrderedDict and numpy
        if "from collections import deque" in resource_manager_code:
            resource_manager_code = resource_manager_code.replace(
                "from collections import deque",
                "from collections import deque, OrderedDict",
            )
            patch_successful = True

        # Replace TextCache implementation with LRU Cache version
        if "class TextCache:" in resource_manager_code and patch_successful:
            # Read optimized TextCache implementation
            with open(os.path.join(base_dir, "optimized_classes.py"), "r") as opt_file:
                optimized_code = opt_file.read()

                # Extract OptimizedTextCache class
                start = optimized_code.find("class OptimizedTextCache:")
                end = optimized_code.find("class NumpyParticleSystem:")
                if start != -1 and end != -1:
                    optimized_text_cache = optimized_code[start:end].strip()
                    optimized_text_cache = optimized_text_cache.replace(
                        "class OptimizedTextCache:", "class TextCache:"
                    )

                    # Replace existing TextCache in resource_manager.py
                    start = resource_manager_code.find("class TextCache:")
                    end = resource_manager_code.find("class ObjectPool:")
                    if start != -1 and end != -1:
                        resource_manager_code = (
                            resource_manager_code[:start]
                            + optimized_text_cache
                            + "\n\n"
                            + resource_manager_code[end:]
                        )
                        print("✓ Applied optimized LRU TextCache")
                    else:
                        print("✗ Failed to locate TextCache class")
                else:
                    print(
                        "✗ Failed to extract OptimizedTextCache from optimized_classes.py"
                    )

            # Write modified code back to file
            with open(os.path.join(base_dir, "resource_manager.py"), "w") as f:
                f.write(resource_manager_code)
                print("✓ Updated resource_manager.py successfully")
        else:
            print("✗ Failed to update import statements")

    except Exception as e:
        print(f"✗ Failed to update resource_manager.py: {e}")

    # 3. Clean up __pycache__ to ensure fresh compilation
    print("\nCleaning __pycache__ directory...")
    try:
        pycache_dir = os.path.join(base_dir, "__pycache__")
        if os.path.exists(pycache_dir):
            for cached_file in os.listdir(pycache_dir):
                if cached_file.endswith(".pyc"):
                    try:
                        os.remove(os.path.join(pycache_dir, cached_file))
                        print(f"✓ Removed {cached_file}")
                    except:
                        print(f"✗ Failed to remove {cached_file}")
        else:
            print("✓ No __pycache__ directory found")
    except Exception as e:
        print(f"✗ Failed to clean __pycache__: {e}")

    print("\n🎮 Optimization complete! Run the game to see performance improvements.")
    print(
        "Backup files have been created with .bak extension in case you need to restore."
    )


if __name__ == "__main__":
    apply_optimizations()
