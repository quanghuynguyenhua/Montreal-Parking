import pandas as pd
import requests
import time
import os
import glob
import config

def reverse_geocode(lat, lng):
    """
    Perform reverse geocoding to get the JSON response and extract the street number and street name
    from latitude and longitude values.
    """
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {'latlng': f"{lat},{lng}", 'key': config.API_KEY}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        json_response = response.json()
        if json_response['results']:
            address_components = json_response['results'][0]['address_components']
            street_number, street_name = None, None
            for component in address_components:
                if 'street_number' in component['types']:
                    street_number = component['long_name']
                elif 'route' in component['types']:
                    street_name = component['long_name']
            return street_number, street_name
        else:
            return None, None
    else:
        return None, None

def find_latest_backup():
    '''
    Checking for latest Backups
    '''
    folder_name = 'src/Reverse-Geocoding/assets'
    search_path = os.path.join(folder_name, 'backup_*.csv')  # Create the full path for glob
    list_of_files = glob.glob(search_path)  # List all backup files with the pattern in 'assets' folder
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def main():
    df = pd.read_csv(config.CSV_FILE)

    # Filter columns early to reduce processing load
    df = df[['POTEAU_ID_POT', 'Longitude', 'Latitude', 'NOM_ARROND']]


    chunk_size = 3000
    total_rows = len(df)

    start_index = 0
    latest_backup = find_latest_backup()
    folder_name = 'src/Reverse-Geocoding/assets'

    if latest_backup:
        start_index = int(latest_backup.split('_')[1])
        df = pd.read_csv(latest_backup)  # Load the latest backup file
        print(f"Resuming from backup {latest_backup}, starting at row {start_index}")

    for start_row in range(start_index, total_rows, chunk_size):
        end_row = min(start_row + chunk_size, total_rows)
        df_chunk = df.iloc[start_row:end_row]

        street_numbers = []
        street_names = []

        for index, row in df_chunk.iterrows():
            lat = row['Latitude']
            lng = row['Longitude']
            street_number, street_name = reverse_geocode(lat, lng)
            street_numbers.append(street_number)
            street_names.append(street_name)

        df.loc[start_row:end_row-1, 'street_number'] = street_numbers
        df.loc[start_row:end_row-1, 'street_name'] = street_names

        
        backup_filename = f'{folder_name}/backup_{start_row}_{end_row-1}.csv'
        df.to_csv(backup_filename, index=False)
        print(f"Backup saved as {backup_filename}. Processed rows {start_row} to {end_row-1}.")

        if end_row != total_rows:
            print("Waiting for 60 seconds before processing the next chunk...")
            time.sleep(60)

    df = df.drop_duplicates(subset=['POTEAU_ID_POT'])
    save_file = f'{folder_name}/pot_address.csv'
    df.to_csv(save_file, index=False)
    print("All data processed and saved successfully.")

if __name__ == "__main__":
    main()