import json
import time
import os

from config import OUTPUT_DIR, MAX_WORKERS, BATCH_SIZE
from data_utils import assign_unique_ids
from property_matcher import process_batches

def main():
    start_time = time.time()
    
    # Create output foler if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")
    
    try:
        # Load data.json fle
        data_file = "data.json"
        if not os.path.exists(data_file):
            print(f"Data file '{data_file}' not found. Please provide the correct filename.")
        
        with open(data_file, "r") as f:
            data = json.load(f)
        
        # Prepare and separate portfolios | assign unique id's for each property
        portfolio1 = assign_unique_ids(data["portfolio1"]["properties"])
        portfolio2 = assign_unique_ids(data["portfolio2"]["properties"])
        
        print(f"Processing {len(portfolio2)} properties from portfolio2 against {len(portfolio1)} properties from portfolio1")
        
        # Process batches)
        all_results = process_batches(
            portfolio1, 
            portfolio2,
            worker_count=MAX_WORKERS,
            batch_size=BATCH_SIZE
        )
        
        # Save processed results
        final_output_file = os.path.join(OUTPUT_DIR, "reconciled_properties.json")
        with open(final_output_file, "w") as f:
            json.dump(all_results, f, indent=4)
        
        # Calculate and print total process time (dev purposes)
        end_time = time.time()
        execution_time = end_time - start_time
        hours, remainder = divmod(execution_time, 3600)
        minutes, seconds = divmod(remainder, 60)

        total_time = f"{int(hours):02d}:{int(minutes):02d}:{seconds:.2f}"
        
        print("=== Execution Summary ===")
        print(f"Processed {len(all_results)} results in {total_time}, saved to {final_output_file}")
        
    except Exception as e:
        print(f"Error at run: {e}")

if __name__ == "__main__":
    main()