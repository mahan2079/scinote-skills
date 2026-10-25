#!/usr/bin/env bash
set -euo pipefail

# setup_notes_env.sh - Initializes the shared notes environment with Jupyter and scientific packages.

DEST_DIR="${1:-.venv-notes}"
KERNEL_NAME="${2:-scinotes-kernel}"
DISPLAY_NAME="${3:-Python (Scientific Notes)}"

echo "=== Initializing Scientific Notes Shared Environment at ${DEST_DIR} ==="

if command -v uv >/dev/null 2>&1; then
    echo "Found 'uv', using high-speed installer..."
    uv venv "${DEST_DIR}" --python 3.12 2>/dev/null || uv venv "${DEST_DIR}"
    
    # Activate virtual environment
    source "${DEST_DIR}/bin/activate"
    
    echo "Installing core scientific stack and Jupyter kernel..."
    uv pip install \
        ipykernel \
        jupyter_client \
        nbconvert \
        nbformat \
        numpy \
        scipy \
        matplotlib \
        seaborn \
        pandas \
        sympy
else
    echo "Using python3 -m venv..."
    python3 -m venv "${DEST_DIR}"
    source "${DEST_DIR}/bin/activate"
    python3 -m pip install --upgrade pip
    python3 -m pip install \
        ipykernel \
        jupyter_client \
        nbconvert \
        nbformat \
        numpy \
        scipy \
        matplotlib \
        seaborn \
        pandas \
        sympy
fi

echo "Registering ipykernel '${KERNEL_NAME}'..."
python -m ipykernel install --user --name "${KERNEL_NAME}" --display-name "${DISPLAY_NAME}"

echo "=== Shared notes environment ready at ${DEST_DIR} ==="
echo "Kernel '${KERNEL_NAME}' is registered for Jupyter notebooks."
