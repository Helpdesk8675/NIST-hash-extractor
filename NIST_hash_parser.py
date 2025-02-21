import sqlite3
import sys
import os
import argparse

def extract_hashes(db_path, output_file):
    """
    Extract MD5 hashes from NIST SQLite database, sort, remove duplicates,
    and save to a text file
    
    Args:
        db_path (str): Path to the SQLite database
        output_file (str): Path where to save the output text file
    """
    try:
        # Verify database exists
        if not os.path.exists(db_path):
            print(f"Error: Database file not found at {db_path}")
            return False
            
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query to get MD5 hashes from the FILE table
        cursor.execute("SELECT md5 FROM FILE")
        hashes = cursor.fetchall()
        
        if not hashes:
            print("No MD5 hashes found in the database")
            return False
            
        # Create a set of unique hashes and convert to sorted list
        unique_hashes = sorted(set(hash_value[0] for hash_value in hashes if hash_value[0]))
        
        # Write sorted, unique hashes to output file
        with open(output_file, 'w') as f:
            for hash_value in unique_hashes:
                f.write(f"{hash_value}\n")
                
        print(f"Successfully extracted {len(hashes)} total hashes")
        print(f"Wrote {len(unique_hashes)} unique hashes to {output_file}")
        return True
        
    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract MD5 hashes from NIST SQLite database')
    parser.add_argument('-i', '--input', help='Path to the input SQLite database')
    parser.add_argument('-o', '--output', help='Path for the output file')
    
    args = parser.parse_args()
    
    # If arguments not provided, prompt user
    db_path = args.input
    if not db_path:
        db_path = input("Enter the path to the NIST SQLite database: ").strip()
        
    output_file = args.output
    if not output_file:
        output_file = input("Enter the path for the output file: ").strip()
    
    # Extract hashes
    success = extract_hashes(db_path, output_file)
    
    if not success:
        print("Failed to extract hashes. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
