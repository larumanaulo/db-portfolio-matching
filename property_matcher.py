from concurrent.futures import ThreadPoolExecutor

from config import CHUNK_SIZE, MATCH_THRESHOLD
from data_utils import chunk_portfolio, parse_monetary_value, format_value, are_values_similar
from api_client import call_matching_api


def find_best_match(portfolio1, prop2):
    chunks = chunk_portfolio(portfolio1, CHUNK_SIZE)

    best_match = None
    best_score = -1
    
    # Process chunks one by one
    for i, chunk in enumerate(chunks):
        try:
            # Call matching API. Open AI API
            matched_data = call_matching_api(prop2, chunk)

            if matched_data:
                score = matched_data.get("portfolio1_match", {}).get("match_score", 0)
                
                if score > best_score:
                    best_score = score
                    best_match = matched_data
        except Exception as e:
            print(f"Error processing chunk: {e}")
        
    return best_match


def create_result(p2=None, p1=None, match_data=None):
    # print(f"p1 >> {parse_monetary_value(p1.get("limit"))}")
    # print(f"p1 >> {parse_monetary_value(p1.get("mortgageAmount"))}")
    # print(f"p2 >> {parse_monetary_value(p2.get("limit"))}")
    # print(f"p2 >> {parse_monetary_value(p21.get("mortgageAmount"))}")

    # Set as mismatch if properties from the matching process are missing
    if not p1 or not p2 or not match_data:
        return {
            "list2": p2["description"] if p2 else "-",
            "list1": p1["description"] if p1 else "-",
            "status": "Mismatch",
            "details": {
                "limit1": format_value(parse_monetary_value(p1.get("limit"))) if p1 else "-",
                "limit2": format_value(parse_monetary_value(p2.get("limit"))) if p2 else "-",
                "mortgage1": format_value(parse_monetary_value(p1.get("mortgageAmount"))) if p1 else "-",
                "mortgage2": format_value(parse_monetary_value(p2.get("mortgageAmount"))) if p2 else "-",
                "score": 0
            }
        }
    
    # For matched properties, extract the data we need
    match_score = match_data.get("portfolio1_match", {}).get("match_score", 0)
    
    # Parse and format the financial details
    limit1 = parse_monetary_value(p1.get("limit"))
    limit2 = parse_monetary_value(p2.get("limit"))
    mortgage1 = parse_monetary_value(p1.get("mortgageAmount"))
    mortgage2 = parse_monetary_value(p2.get("mortgageAmount"))
    
    # heck if financials match and determine the status
    amounts_similar = are_values_similar(limit1, limit2) and are_values_similar(mortgage1, mortgage2)
    match_status = "Match" if amounts_similar else "Similar Match"
    
    # Return the formatted result
    return {
        "list2": p2["description"],
        "list1": p1["description"],
        "status": match_status,
        "details": {
            "limit1": format_value(limit1),
            "limit2": format_value(limit2),
            "mortgage1": format_value(mortgage1),
            "mortgage2": format_value(mortgage2),
            "score": match_score
        }
    }


def process_batches(portfolio1, portfolio2, worker_count, batch_size):
    all_results = []
    
    # Check list for duplicate properties
    processed_ids = set()
    
    # Process each batcg individually
    def process_batch(batch_props):
        batch_results = []
        
        for prop2 in batch_props:
            # Try to find the best matching property in portfolio1
            match_data = find_best_match(portfolio1, prop2)
            
            # Skip if no match data was returned (e.g., API error)
            if not match_data:
                continue
                
            portfolio1_match = match_data.get("portfolio1_match", {})
            is_mismatch = portfolio1_match.get("match_score", 0) < MATCH_THRESHOLD or not portfolio1_match.get("id")

            
            # Create the appropriate result based on whether it's a match or mismatch
            if is_mismatch:
                # Create mismatch result. No matching prop1
                result = create_result(p2=prop2)
            else:
                # get portfolio1 matching property using assigned id
                match_id = portfolio1_match.get("id")
                prop1 = next((p for p in portfolio1 if p["id"] == match_id), None)
                
                # Crete result with matching property info
                if prop1:
                    result = create_result(p2=prop2, p1=prop1, match_data=match_data)
            
            batch_results.append(result)
                
        return batch_results
    
    # split portfolio2 into batches
    batches = []

    for i in range(0, len(portfolio2), batch_size):
        batch = []

        for j in range(i, min(i + batch_size, len(portfolio2))):
            prop = portfolio2[j]
            
            # Only include properties that have not been processed yet
            if prop["id"] not in processed_ids:
                batch.append(prop)
                # add property to processed id's for tracking
                processed_ids.add(prop["id"])

        if batch:
            batches.append(batch)

    # Process batches in parallel
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_results = list(executor.map(process_batch, batches))
    
    # Merge Results
    for batch_result in future_results:
        if batch_result:
            all_results.extend(batch_result)

    # Get matching descriptions
    matched_descriptions = {r["list1"] for r in all_results if r["list1"] != "-"}
    
    # Get properties with no matches
    unmatched_props = [p for p in portfolio1 if p["description"] not in matched_descriptions]
    
    # Add properties with no match to the results
    for prop in unmatched_props:
        all_results.append(create_result(p1=prop))
    
    return all_results