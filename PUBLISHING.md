# Publishing smarttree to PyPI

## 📋 Pre-publication Checklist

- [ ] Update version number in `pyproject.toml` and `smarttree.py`
- [ ] Update email address in `pyproject.toml`
- [ ] Test the package locally
- [ ] Create and push a git tag for the version
- [ ] Ensure all tests pass (if you have tests)

## 🔧 Setup (First Time Only)

1. **Install build tools**:
   ```bash
   pip install --upgrade pip
   pip install --upgrade build twine
   ```

2. **Create PyPI account**:
   - Go to https://pypi.org/account/register/
   - Verify your email
   - Enable 2FA (recommended)

3. **Create API token**:
   - Go to https://pypi.org/manage/account/token/
   - Create a token with scope "Entire account"
   - Save it securely!

## 📦 Building the Package

1. **Clean previous builds**:
   ```bash
   rm -rf dist/ build/ *.egg-info
   ```

2. **Build the package**:
   ```bash
   python -m build
   ```

   This creates:
   - `dist/smarttree-0.1.0.tar.gz` (source distribution)
   - `dist/smarttree-0.1.0-py3-none-any.whl` (wheel)

## 🧪 Test Locally

1. **Create a test virtual environment**:
   ```bash
   python -m venv test-env
   source test-env/bin/activate  # On Windows: test-env\Scripts\activate
   ```

2. **Install from local build**:
   ```bash
   pip install dist/smarttree-0.1.0-py3-none-any.whl
   ```

3. **Test the command**:
   ```bash
   smarttree --version
   smarttree --help
   smarttree --depth 2 --emoji
   ```

4. **Deactivate test environment**:
   ```bash
   deactivate
   rm -rf test-env
   ```

## 🚀 Upload to PyPI

### Option 1: Upload with token (Recommended)

```bash
python -m twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: `<your-api-token-including-pypi-prefix>`

### Option 2: Save token in .pypirc

Create `~/.pypirc`:
```ini
[pypi]
  username = __token__
  password = pypi-AgEIcHlwaS5vcmcC...your-full-token-here
```

Then upload:
```bash
python -m twine upload dist/*
```

## ✅ Post-Publication

1. **Test installation from PyPI**:
   ```bash
   pip install smarttree
   smarttree --version
   ```

2. **Create GitHub release**:
   ```bash
   git tag -a v0.1.0 -m "Initial release"
   git push origin v0.1.0
   ```

3. **Update README** if needed with the PyPI badge

## 🔄 Updating the Package

1. Bump version in `pyproject.toml` and `smarttree.py`
2. Update CHANGELOG.md (if you have one)
3. Commit changes
4. Follow build and upload steps again

## 🐛 Troubleshooting

- **"Invalid distribution file"**: Clean and rebuild
- **"Version already exists"**: Bump version number
- **Authentication failed**: Check token and use `__token__` as username
- **Module not found after install**: Check `[project.scripts]` in pyproject.toml

## 📚 Resources

- [PyPI Publishing Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [PyPI Help](https://pypi.org/help/)