import subprocess
import sys
import os
SCRIPTS = [
    'train_crop_model.py',
    'train_yield_model.py',
    'train_fertilizer_model.py',
    'train_price_model.py',
    'train_disease_model.py',
    'train_pest_model.py',
    'train_faq_model.py',
]

def run_script(script: str):
    cmd = [sys.executable, os.path.join(os.path.dirname(__file__), script)]
    print(f"\n=== Running {script} ===")
    subprocess.check_call(cmd)

def main():
    for s in SCRIPTS:
        run_script(s)
    print("\nAll training jobs finished.")

if __name__ == '__main__':
    main()






