import os
import re
from datetime import datetime

# Function to add cost entries interactively
def add_cost_entry(costs):
    while True:
        item = input("Enter the item name (or type 'done' to finish): ")
        if item.lower() == 'done':
            break
        try:
            price = float(input(f"Enter the price for '{item}': $"))
            costs.append((item, price))
            print("Cost added successfully!")
        except ValueError:
            print("Invalid price, please enter a valid number.")

# Function to get current date with time in the required format
def get_current_date():
    return datetime.now().strftime("%d/%m/%Y %H:%M")

# Function to get clean date without time
def get_clean_date():
    return datetime.now().strftime("%d/%m/%Y")

# Function to append the new costs and progress to README.md
def append_to_readme(costs, progress_text=None):
    # Get current date with time
    progress_date = get_current_date()
    
    # Determine the file path (use current directory)
    readme_path = os.path.join(os.getcwd(), "README.md")
    
    # Read the current README content or create a new one if it doesn't exist
    try:
        with open(readme_path, "r") as f:
            readme_content = f.read().strip()
    except FileNotFoundError:
        readme_content = "# Project: Morphex Rotating Arm\n\n## TODO\n1. Remodel brackets and servo.\n2. Think about materials more.\n3. Cost analysis.\n\n## Costs\n\n## Progress\n"
    
    # Prepare new cost section (if costs exist)
    new_cost_section = ""
    new_total_cost = 0
    if costs:
        new_cost_section = f"\n**{progress_date}:**\n"
        for item, cost in costs:
            new_cost_section += f"- ${cost:.2f} for {item}\n"
        new_total_cost = sum(price for _, price in costs)
    
    # Extract existing structure
    project_title_match = re.match(r'(#\s*Project:.*?)(?=\n\n|\n#|\Z)', readme_content, re.DOTALL)
    project_title = project_title_match.group(1) if project_title_match else "# Project: Morphex Rotating Arm"
    
    todo_match = re.search(r'(## TODO\n.*?)(?=\n\n|\n#|\n##|\Z)', readme_content, re.DOTALL)
    todo_section = todo_match.group(1) if todo_match else "## TODO\n1. Remodel brackets and servo.\n2. Think about materials more.\n3. Cost analysis."
    
    # Extract existing costs and total
    existing_costs_match = re.search(r'(## Costs\n.*?)(?=\n\n|\n#|\n##|\Z)', readme_content, re.DOTALL | re.MULTILINE)
    existing_costs = existing_costs_match.group(1) if existing_costs_match else "## Costs"
    
    # Extract existing total
    total_match = re.search(r'\*\*Total:\*\* \$(\d+\.\d{2})', existing_costs)
    existing_total = float(total_match.group(1)) if total_match else 0.0
    
    # Calculate new total cost
    total_cost = existing_total + new_total_cost
    
    # Reconstruct the Costs section
    updated_costs_section = "## Costs"
    if new_cost_section:
        updated_costs_section += new_cost_section
    
    # Append existing cost entries (if they exist and are different from the new entries)
    if existing_costs_match and existing_costs_match.group(1).strip() != "## Costs":
        updated_costs_section += re.sub(r'\*\*Total:\*\* \$\d+\.\d{2}', '', existing_costs_match.group(1)).strip() + "\n"
    
    # Add total cost line
    updated_costs_section += f"**Total:** ${total_cost:.2f}\n"
    
    # Extract existing progress section
    progress_match = re.search(r'(## Progress\n.*?)(?=\n\n|\n#|\n##|\Z)', readme_content, re.DOTALL)
    progress_section = "## Progress" if not progress_match else progress_match.group(1)
    
    # Prepare new progress section if text is provided
    new_progress_section = ""
    if progress_text:
        new_progress_section = f"\n**{progress_date}:**\n- {progress_text}"
    
    # Construct the final README content
    final_content = f"{project_title}\n\n{todo_section}\n\n{updated_costs_section}\n\n{progress_section}{new_progress_section}"
    
    # Save updated content back to README.md
    with open(readme_path, "w") as f:
        f.write(final_content)
    
    print(f"README.md file updated successfully at {get_current_date()}")

# Main execution
def main():
    # Initialize costs list
    costs = []
    
    # Optional: Prompt for cost entries
    print("Enter cost entries (optional):")
    add_cost_entry(costs)
    
    # Optional: Prompt for progress text
    progress_text = input("What did you do today? (Press Enter to skip): ").strip()
    
    # Append to the README file with the current data
    append_to_readme(costs, progress_text if progress_text else None)

# Run the script
if __name__ == "__main__":
    main()