#!/usr/bin/env python3
"""
Test script for SmartTree .treeignore functionality
"""

import os
import tempfile
import shutil
from smarttree import should_ignore

def test_patterns():
    """Test various ignore patterns"""
    test_cases = [
        # (item_name, is_dir, patterns, expected_ignored)
        # Basic file matching
        ("test.pyc", False, ["*.pyc"], True),
        ("test.py", False, ["*.pyc"], False),
        ("test.log", False, ["*.log"], True),
        
        # Directory matching with trailing slash
        (".venv", True, [".venv/"], True),
        (".venv", False, [".venv/"], False),  # File named .venv should not match
        ("venv", True, ["venv/"], True),
        ("venv", True, ["venv"], True),  # Also matches without slash
        
        # Wildcard patterns
        ("__pycache__", True, ["__pycache__/"], True),
        ("build", True, ["build*/"], True),
        ("build123", True, ["build*/"], True),
        ("buildstuff", True, ["build*/"], True),
        
        # Multiple character wildcards
        ("test.egg-info", True, ["*.egg-info/"], True),
        ("myproject.egg-info", True, ["*.egg-info/"], True),
        
        # Question mark single character
        ("test1.txt", False, ["test?.txt"], True),
        ("test22.txt", False, ["test?.txt"], False),
        
        # Character sequences
        ("test1.txt", False, ["test[0-9].txt"], True),
        ("testa.txt", False, ["test[0-9].txt"], False),
        
        # Hidden files/folders
        (".DS_Store", False, [".DS_Store"], True),
        (".git", True, [".git/"], True),
        (".gitignore", False, [".git/"], False),  # Should not match
        
        # Case sensitivity
        ("README.md", False, ["readme.md"], False),  # fnmatch is case-sensitive
        
        # Multiple patterns
        ("test.pyc", False, ["*.log", "*.pyc", "*.tmp"], True),
        ("test.txt", False, ["*.log", "*.pyc", "*.tmp"], False),
    ]
    
    print("🧪 Testing .treeignore patterns...\n")
    
    passed = 0
    failed = 0
    
    for item_name, is_dir, patterns, expected in test_cases:
        result = should_ignore(item_name, is_dir, patterns)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
            
        item_type = "dir" if is_dir else "file"
        print(f"{status} | {item_name} ({item_type}) | patterns: {patterns} | "
              f"expected: {expected}, got: {result}")
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    return failed == 0

def test_real_directory():
    """Test with a real directory structure"""
    print("\n🏗️  Testing with real directory structure...\n")
    
    # Create temporary test directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test structure
        os.makedirs(os.path.join(tmpdir, ".venv", "lib"))
        os.makedirs(os.path.join(tmpdir, "__pycache__"))
        os.makedirs(os.path.join(tmpdir, "src"))
        os.makedirs(os.path.join(tmpdir, "node_modules", "package"))
        os.makedirs(os.path.join(tmpdir, "build"))
        os.makedirs(os.path.join(tmpdir, "my.egg-info"))
        
        # Create test files
        open(os.path.join(tmpdir, "main.py"), "w").close()
        open(os.path.join(tmpdir, "test.pyc"), "w").close()
        open(os.path.join(tmpdir, ".DS_Store"), "w").close()
        open(os.path.join(tmpdir, "debug.log"), "w").close()
        open(os.path.join(tmpdir, "README.md"), "w").close()
        
        # Create .treeignore
        treeignore_content = """# Test .treeignore
.venv/
__pycache__/
*.pyc
*.log
.DS_Store
node_modules/
build*/
*.egg-info/
"""
        with open(os.path.join(tmpdir, ".treeignore"), "w") as f:
            f.write(treeignore_content)
        
        print(f"📁 Created test directory: {tmpdir}")
        print("\n📄 .treeignore contents:")
        print(treeignore_content)
        
        print("\n🌳 Running smarttree...")
        os.system(f"python smarttree.py {tmpdir}")
        
        print("\n✅ Files/folders that should be visible:")
        print("  - main.py")
        print("  - src/")
        print("  - README.md")
        print("  - .treeignore")
        
        print("\n❌ Files/folders that should be ignored:")
        print("  - .venv/")
        print("  - __pycache__/")
        print("  - test.pyc")
        print("  - .DS_Store")
        print("  - debug.log")
        print("  - node_modules/")
        print("  - build/")
        print("  - my.egg-info/")

if __name__ == "__main__":
    # Run pattern tests
    success = test_patterns()
    
    # Run real directory test
    test_real_directory()
    
    if success:
        print("\n✅ All pattern tests passed!")
    else:
        print("\n❌ Some pattern tests failed!")