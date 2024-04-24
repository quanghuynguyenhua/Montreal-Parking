### README.md

# Montreal Parking Data Geocoding

This Python script performs geocoding for parking data in Montreal by using Google's Geocoding API. It reads parking signage pole location (longtitue and latitude), performs reverse geocoding to fetch street names and numbers, and saves the enhanced data back as a CSV file.

## Prerequisites

- Python 3.x
- pandas
- requests
- time
- os
- glob

Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/quanghuynguyenhua/Montreal-Parking.git
   cd Montreal-Parking
   ```

2. **Install Required Libraries:**

   Use pip to install the required Python packages:

   ```bash
   pip install pandas requests time os glob
   ```

3. **API Key Configuration:**

   You will need a Google Geocoding API key to perform reverse geocoding. Create a file named `config.py` locally in the project directory (src\Reverse-Geocoding) with the following content:
    
   ```python
   API_KEY = "<Your_Google_Geocoding_API_key_here>"
   CSV_FILE = 'https://raw.githubusercontent.com/quanghuynguyenhua/Montreal-Parking/main/assets/signalisation_stationnement.csv'
   ```

   Replace `<Your_Google_Geocoding_API_key_here>` with your actual Google Geocoding API key.

## Running the Script

To run the script, execute the following command from the project directory:

```bash
python rev_geo_v1.py 
```

The script will process each chunk of parking data and perform geocoding. Results will be saved in a file named `pot_address.csv` in the same directory.

## Backup and Continuation
The script includes functionality to save a backup of the processed data after each chunk. If the process is interrupted for any reason, you can restart the script and it will continue from the last successfully processed chunk, preventing the need to start over from the beginning. This ensures data is not lost and reduces redundancy in API usage and processing time.

Each backup is saved under the name 'backup_{start_row}_{end_row-1}.csv', where '{start_row}' and '{end_row-1}' denote the indices of the first and last rows of the data chunk respectively. When restarting, the script checks for the latest available backup and continues from the next chunk.

## Output

The output CSV file will contain the following columns:

- `POTEAU_ID_POT`
- `Longitude`
- `Latitude`
- `NOM_ARROND`
- `street_number`
- `street_name`

Each row represents parking data enriched with geocoded street information.

## Note

The script includes a break of 60 seconds between processing each data chunk to comply with API rate limits and to prevent overloading the server.
```
