# SNP-Allele-Frequency-Scraper-for-European-Population

# Project Overview:
This project scrapes SNP alternate allele frequency data specifically for the European population from NCBI's database. The tool parses the scraped data and updates an existing Excel file with the most relevant frequency for each SNP based on user-defined preferences for alleles. This is useful for researchers working with SNP data who need allele frequency information.

# Features:
Fetches SNP data from NCBI for the European population.
Handles multiple allele frequency entries and filters based on user preferences.
Automatically updates the Excel file with the selected alternate allele frequency.
Includes error handling and a delay mechanism to avoid overloading servers.
# Requirements:
Python 3.x
Pandas: pip install pandas
Requests: pip install requests
BeautifulSoup: pip install beautifulsoup4
LXML (optional for better performance with BeautifulSoup): pip install lxml
# How to Use:
Ensure your Excel file contains a list of SNPs, and the relevant columns for effect and other alleles.
Adjust the file paths for your Excel input and output.
Run the script, and it will fetch the allele frequencies and update the file.


