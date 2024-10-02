import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Load the Excel file
file_path = 'C:\\Danial\\VitaminD\\2-ebi-a-GCST010144\\3.ebi-a-GCST000612\\snp3.xlsx'  # Replace with your Excel file path
df = pd.read_excel(file_path)

# Function to parse Alt Allele frequencies
def parse_alt_allele_frequencies(alt_allele_text):
    alt_allele_values = []
    try:
        # Handle multiple entries separated by commas
        entries = alt_allele_text.split(',')
        for entry in entries:
            allele, frequency = entry.split('=', 1)
            if frequency != '0':  # Skip zero values
                alt_allele_values.append((allele.strip(), float(frequency.strip())))
    except ValueError as e:
        print(f"Error parsing Alt Allele value '{alt_allele_text}': {e}")
    return alt_allele_values

# Function to scrape the Alt Allele frequency for European population
def get_european_alt_allele_frequency(snp):
    url = f"https://www.ncbi.nlm.nih.gov/snp/{snp}/"
    print(f"Opening URL: {url}")  # For debugging to see if the link is being opened
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all table rows in the page
        rows = soup.find_all('tr')
        alt_allele_values = []
        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 1:
                population = columns[0].get_text(strip=True)
                if population == 'European':
                    alt_allele_text = columns[-1].get_text(strip=True)  # The last column typically contains the Alt Allele
                    alt_allele_values.extend(parse_alt_allele_frequencies(alt_allele_text))
        return alt_allele_values
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    return []

# Iterate through each SNP and update the DataFrame
for index, row in df.iterrows():
    test_snp = row['SNP']
    effect_allele = row['effect_allele.outcome']
    other_allele = row['other_allele.outcome']
    
    print(f"Processing SNP {test_snp}...")
    alt_allele_values = get_european_alt_allele_frequency(test_snp)

    if alt_allele_values:
        # Define preferred alleles based on effect_allele and other_allele
        preferred_alleles = [effect_allele, other_allele]
        
        # Filter values to remove zero values and find preferred allele
        selected_value = None
        filtered_values = [value for value in alt_allele_values if value[0] in ['A', 'T', 'C', 'G']]
        preferred_values = [value for value in filtered_values if value[0] in preferred_alleles]
        
        if preferred_values:
            # If there's a match, use that value
            selected_value = preferred_values[0][1]
        else:
            # If no preferred allele found, use the remaining values
            if filtered_values:
                selected_value = max(filtered_values, key=lambda x: x[1])[1]
        
        if selected_value is not None:
            df.at[index, 'eaf.outcome'] = selected_value
            print(f"Alt Allele Frequency for SNP {test_snp}: {selected_value}")
        else:
            print(f"Could not find a valid Alt Allele Frequency for SNP {test_snp}")
    else:
        print(f"Could not find Alt Allele Frequency for SNP {test_snp}")
    
    # Wait for 2 seconds before the next request to avoid overloading the server
    time.sleep(10)

# Save the updated DataFrame back to the Excel file
try:
    # Save to a different location if permission is denied
    save_path = 'C:\\Danial\\VitaminD\\2-ebi-a-GCST010144\\3.ebi-a-GCST000612\\snp3.updated.xlsx'  # Change path if needed
    df.to_excel(save_path, index=False)
    print(f"Update complete and saved to Excel at {save_path}.")
except PermissionError:
    print(f"Permission denied: Unable to save the file at {file_path}. Try closing the file if it's open.")
