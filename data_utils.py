import uuid
import re
from config import CHUNK_SIZE

def assign_unique_ids(portfolio):
    for property in portfolio:
        property["id"] = str(uuid.uuid4())
    return portfolio


def chunk_portfolio(portfolio, chunk_size=CHUNK_SIZE):
    return [portfolio[i:i + chunk_size] for i in range(0, len(portfolio), chunk_size)]


def parse_monetary_value(value_str):
    if value_str is None or value_str == "-":
        return None
    
    # If it's already a number, return it
    if isinstance(value_str, (int, float)):
        return float(value_str)
    
    # Convert string to standard format
    value_str = str(value_str).strip().lower()
    
    # Remove currency symbols and commas
    value_str = re.sub(r'[$,]', '', value_str)
    
    # Handle "K" and "M" suffixes
    if 'k' in value_str:
        value_str = value_str.replace('k', '')
        multiplier = 1000
    elif 'm' in value_str:
        value_str = value_str.replace('m', '')
        multiplier = 1000000
    else:
        multiplier = 1
    
    number_match = re.search(r'(\d+\.?\d*)', value_str)
    if number_match:
        try:
            return float(number_match.group(1)) * multiplier
        except ValueError:
            pass
    
    # Handle text numbers
    text_numbers = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'hundred': 100, 'thousand': 1000, 'million': 1000000
    }
    
    # Check for text number patterns
    for word, number in text_numbers.items():
        if word in value_str:
            # Very basic handling - just estimate
            if 'hundred' in value_str:
                return 100000
            elif 'thousand' in value_str:
                return 1000000
            elif 'million' in value_str:
                return 1000000
            else:
                return number * 100000  # Rough estimate
    
    return None


def are_values_similar(value1, value2):
    return value1 == value2


def format_value(val):
    if val is None or val == "-":
        return "N/A"
    if isinstance(val, (int, float)):
        if val >= 1000000:
            return f"${val/1000000:.2f}M"
        elif val >= 1000:
            return f"${val/1000:.1f}K"
        else:
            return f"${val:.2f}"
    return str(val)