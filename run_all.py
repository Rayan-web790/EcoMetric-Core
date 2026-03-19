import subprocess
import os
import sys

def run_script(script_path, interpreter="py"):
    print(f"\n--- Running {script_path} ---")
    try:
        # Use the provided interpreter for better compatibility (e.g. 'py' on Windows)
        result = subprocess.run([interpreter, script_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")
        return False
    except FileNotFoundError:
        print(f"Error: Interpreter '{interpreter}' not found. Trying 'python'...")
        try:
             subprocess.run(["python", script_path], check=True)
             return True
        except Exception as e2:
             print(f"Failed with 'python' too: {e2}")
             return False

def main():
    scripts = [
        "scripts/data_cleaning.py",
        "scripts/eda_analysis.py",
        "scripts/rfm_analysis.py",
        "scripts/behavior_analysis.py",
        "data_exporter.py"
    ]
    
    # Check if cleaned data already exists to avoid lengthy re-cleaning
    cleaned_data = "data/events_oct_cleaned.csv"
    if os.path.exists(cleaned_data):
        print(f"Cleaned data found at {cleaned_data}. Skipping data cleaning step.")
        scripts.pop(0) # Skip data_cleaning.py
    else:
        print(f"Cleaned data NOT found. Starting full pipeline...")

    # Ensure directories exist
    for d in ["data", "visuals", "reports"]:
        if not os.path.exists(d):
            os.makedirs(d)

    # Execute each script
    success_count = 0
    for script in scripts:
        if run_script(script):
            success_count += 1
        else:
            print(f"Aborting pipeline due to error in {script}.")
            break
            
    if success_count == len(scripts):
        print("\n" + "="*40)
        print("PIPELINE COMPLETED SUCCESSFULLY!")
        
        # --- NEW: Sync to Dashboard ---
        if os.path.exists("dashboard/public"):
            print("Syncing data to web dashboard...")
            try:
                # Use simple os/shutil calls for portability
                import shutil
                shutil.copy("data/dashboard_data.json", "dashboard/public/data/")
                # Copy all visuals
                for f in os.listdir("visuals"):
                    if f.endswith(".png"):
                        shutil.copy(os.path.join("visuals", f), "dashboard/public/visuals/")
                print("Dashboard sync complete.")
            except Exception as e:
                print(f"Warning: Could not sync to dashboard: {e}")

        print("Visuals are available in 'visuals/' and 'dashboard/public/visuals/'.")
        print("="*40)
    else:
        print("\nPIPELINE FAILED.")

if __name__ == "__main__":
    main()
