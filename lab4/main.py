import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import os
from pymongo import MongoClient

def load_mock_data(db):
    """
    Checks MongoDB for existing data. If not found, it creates mock data
    and inserts it into the 'raw_taxi_data' collection.
    """
    collection = db['raw_taxi_data']
    
    # Check if data already exists
    try:
        count = collection.count_documents({})
        if count > 0:
            print(f"Loading {count} records from MongoDB collection 'raw_taxi_data'...")
            cursor = collection.find()
            df = pd.DataFrame(list(cursor))
            # Remove the MongoDB-specific _id column
            df.drop('_id', axis=1, inplace=True)
            
            # Ensure correct data types after loading from BSON
            df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
            df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
            
            print("Data loaded successfully from MongoDB.")
            
        else:
            print("No data in MongoDB. Creating and inserting mock data...")
            data = {
                'VendorID': [1, 2, 1, 1, 2, 1, 2, 1, 2, 1],
                'tpep_pickup_datetime': pd.to_datetime([
                    '2021-01-01 00:30:10', '2021-01-01 00:45:15', '2021-01-01 00:12:30',
                    '2021-01-01 00:15:20', '2021-01-01 00:25:30', '2021-01-01 01:30:10',
                    '2021-01-01 01:45:15', '2021-01-01 01:12:30', '2021-01-01 01:15:20',
                    '2021-01-01 02:25:30'
                ]),
                'tpep_dropoff_datetime': pd.to_datetime([
                    '2021-01-01 00:45:20', '2021-01-01 00:55:30', '2021-01-01 00:22:45',
                    '2021-01-01 00:30:40', '2021-01-01 00:40:50', '2021-01-01 01:45:20',
                    '2021-01-01 01:55:30', '2021-01-01 01:22:45', '2021-01-01 01:30:40',
                    '2021-01-01 02:40:50'
                ]),
                'passenger_count': [1.0, 2.0, 1.0, 0.0, 1.0, 1.0, 2.0, 1.0, np.nan, 1.0],
                'trip_distance': [3.1, 2.5, 2.8, 1.2, 3.5, 3.1, 2.5, 2.8, 2.2, 3.5],
                'RatecodeID': [1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, np.nan],
                'store_and_fwd_flag': ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'Y', 'N'],
                'PULocationID': [138, 238, 239, 148, 231, 138, 238, 239, 148, 231],
                'DOLocationID': [141, 42, 74, 87, 246, 141, 42, 74, 87, 246],
                'payment_type': [1, 2, 1, 1, 1, 1, 2, 1, 1, 1],
                'fare_amount': [12.5, 10.0, 9.5, 7.0, 15.0, 12.5, 10.0, 9.5, 8.0, 15.0],
                'extra': [3.0, 0.5, 3.0, 3.0, 0.5, 3.0, 0.5, 3.0, 3.0, 0.5],
                'mta_tax': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                'tip_amount': [2.5, 0.0, 2.0, 2.05, 3.0, 2.5, 0.0, 2.0, 2.5, 3.0],
                'tolls_amount': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                'improvement_surcharge': [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
                'total_amount': [18.8, 13.8, 15.3, 12.85, 19.3, 18.8, 13.8, 15.3, 14.3, 19.3],
                'congestion_surcharge': [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, np.nan],
                'airport_fee': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, np.nan]
            }
            df = pd.DataFrame(data)
            
            # Fill in missing airport_fee for mock data consistency
            df['airport_fee'] = df['airport_fee'].fillna(0.0)
            
            # Insert into MongoDB
            # We use to_dict('records') to convert the DataFrame to a list of dicts
            # pandas handles np.nan -> None conversion automatically
            print("Inserting data into 'raw_taxi_data' collection...")
            collection.insert_many(df.to_dict('records'))
            print("Mock data inserted.")
            
    except Exception as e:
        print(f"Error connecting to or reading from MongoDB: {e}")
        print("Falling back to in-memory mock data for this run.")
        # Re-run the mock data creation if connection failed
        # This is simplified; in production, you might want to handle this differently
        data = {
            'VendorID': [1, 2, 1, 1, 2, 1, 2, 1, 2, 1],
            'tpep_pickup_datetime': pd.to_datetime([
                '2021-01-01 00:30:10', '2021-01-01 00:45:15', '2021-01-01 00:12:30',
                '2021-01-01 00:15:20', '2021-01-01 00:25:30', '2021-01-01 01:30:10',
                '2021-01-01 01:45:15', '2021-01-01 01:12:30', '2021-01-01 01:15:20',
                '2021-01-01 02:25:30'
            ]),
            'tpep_dropoff_datetime': pd.to_datetime([
                '2021-01-01 00:45:20', '2021-01-01 00:55:30', '2021-01-01 00:22:45',
                '2021-01-01 00:30:40', '2021-01-01 00:40:50', '2021-01-01 01:45:20',
                '2021-01-01 01:55:30', '2021-01-01 01:22:45', '2021-01-01 01:30:40',
                '2021-01-01 02:40:50'
            ]),
            'passenger_count': [1.0, 2.0, 1.0, 0.0, 1.0, 1.0, 2.0, 1.0, np.nan, 1.0],
            'trip_distance': [3.1, 2.5, 2.8, 1.2, 3.5, 3.1, 2.5, 2.8, 2.2, 3.5],
            'RatecodeID': [1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, np.nan],
            'store_and_fwd_flag': ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'Y', 'N'],
            'PULocationID': [138, 238, 239, 148, 231, 138, 238, 239, 148, 231],
            'DOLocationID': [141, 42, 74, 87, 246, 141, 42, 74, 87, 246],
            'payment_type': [1, 2, 1, 1, 1, 1, 2, 1, 1, 1],
            'fare_amount': [12.5, 10.0, 9.5, 7.0, 15.0, 12.5, 10.0, 9.5, 8.0, 15.0],
            'extra': [3.0, 0.5, 3.0, 3.0, 0.5, 3.0, 0.5, 3.0, 3.0, 0.5],
            'mta_tax': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            'tip_amount': [2.5, 0.0, 2.0, 2.05, 3.0, 2.5, 0.0, 2.0, 2.5, 3.0],
            'tolls_amount': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            'improvement_surcharge': [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
            'total_amount': [18.8, 13.8, 15.3, 12.85, 19.3, 18.8, 13.8, 15.3, 14.3, 19.3],
            'congestion_surcharge': [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, np.nan],
            'airport_fee': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, np.nan]
        }
        df = pd.DataFrame(data)
        df['airport_fee'] = df['airport_fee'].fillna(0.0)

    print("\n--- Combined Data Info ---")
    df.info()
    print("\n--- Combined Data Head ---")
    print(df.head())
    return df

def feature_engineering(data):
    """
    Engineers new features from the existing data.
    """
    print("\nStarting feature engineering...")
    
    # 3.1 Calculate Trip Duration
    data['trip_duration'] = (data['tpep_dropoff_datetime'] - data['tpep_pickup_datetime']).dt.total_seconds() / 60
    
    # 3.4 Extract Time Features
    data['pickup_hour'] = data['tpep_pickup_datetime'].dt.hour
    data['pickup_day_of_week'] = data['tpep_pickup_datetime'].dt.day_name()
    
    print("Feature engineering complete.")
    print(data.head())
    return data

def clean_data(data):
    """
    Cleans the DataFrame by handling missing values and outliers.
    """
    print("\nStarting data cleaning...")
    
    # 3.2 Handle Missing Values
    print("Missing values before drop:")
    print(data.isnull().sum())
    
    # Drop rows based on nulls in critical columns
    data.dropna(subset=['passenger_count', 'RatecodeID', 'store_and_fwd_flag', 'congestion_surcharge'], inplace=True)
    
    print(f"\nOriginal data shape: {data.shape}")

    # 3.3 Handle Outliers and Impossible Values
    data = data[(data['trip_duration'] > 1) & (data['trip_duration'] < 600)]
    data = data[data['trip_distance'] > 0]
    data = data[data['passenger_count'] > 0]
    data = data[data['fare_amount'] > 0]
    
    print(f"Cleaned data shape: {data.shape}")
    return data

def run_regression(data):
    """
    Performs a linear regression on standard trips to predict fare based on distance.
    """
    print("\nStarting advanced analysis (Linear Regression)...")
    
    # 5.1 Prepare data
    standard_trips = data[data['RatecodeID'] == 1].copy()
    
    # Filter for reasonable distances and fares
    model_data = standard_trips[
        (standard_trips['trip_distance'] < 100) & 
        (standard_trips['fare_amount'] < 500)
    ]
    
    if model_data.empty or len(model_data) < 2:
        print("Not enough data to run regression after filtering.")
        return

    # 5.2 Define Features (X) and Target (y)
    X = model_data[['trip_distance']]
    y = model_data['fare_amount']

    # 5.3 Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples.")
    
    if len(X_train) == 0 or len(X_test) == 0:
        print("Train or test split resulted in empty data. Skipping regression.")
        return

    # 5.4 Create and Train the Model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 5.5 Print Coefficients
    print(f"\nModel Coefficient (m): {model.coef_[0]:.2f}")
    print(f"Model Intercept (b): {model.intercept_:.2f}")
    print(f"Formula: fare_amount = {model.coef_[0]:.2f} * trip_distance + {model.intercept_:.2f}")
    
    # 5.6 Evaluate the Model
    y_pred = model.predict(X_test)
    r2 = metrics.r2_score(y_test, y_pred)
    print(f"\nModel R-squared: {r2:.4f}")
    print("Regression analysis complete.")

def export_aggregates(db, data):
    """
    Aggregates data and saves it to MongoDB collections.
    """
    print("\nAggregating and exporting data to MongoDB...")
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Helper function to insert data
    def insert_to_collection(collection_name, dataframe):
        try:
            collection = db[collection_name]
            # Clear the collection before inserting new data
            collection.delete_many({})
            # Reset index so the index (e.g., 'pickup_hour') becomes a column
            dataframe_reset = dataframe.reset_index()
            collection.insert_many(dataframe_reset.to_dict('records'))
            print(f"Successfully exported data to collection: {collection_name}")
        except Exception as e:
            print(f"Error exporting to {collection_name}: {e}")

    # 1. Aggregate: Trips by Hour
    hourly_data = data.groupby('pickup_hour').size().to_frame(name='trip_count')
    insert_to_collection('hourly_trips', hourly_data)

    # 2. Aggregate: Trips by Day
    daily_data = data.groupby('pickup_day_of_week').size().to_frame(name='trip_count')
    daily_data = daily_data.reindex(day_order)
    insert_to_collection('daily_trips', daily_data)

    # 3. Aggregate: Top Pickup Locations
    top_pickups = data.groupby('PULocationID').size().to_frame(name='trip_count')
    top_pickups = top_pickups.sort_values(by='trip_count', ascending=False).head(20)
    insert_to_collection('top_pickups', top_pickups)

    # 4. Aggregate: Financial Averages by Day
    financial_by_day = data.groupby('pickup_day_of_week')[[
        'fare_amount', 'tip_amount', 'total_amount', 'trip_duration'
    ]].mean()
    financial_by_day = financial_by_day.reindex(day_order)
    insert_to_collection('financial_by_day', financial_by_day)

    # 5. Sample: Data for Scatter Plot
    sample_size = min(10000, len(data)) # Keep sample small
    map_data = data.sample(sample_size)
    map_data_cleaned = map_data[['tpep_pickup_datetime', 'PULocationID', 'DOLocationID', 
                                 'trip_distance', 'fare_amount', 'tip_amount']]
    
    # This one doesn't need index reset as it's not a groupby
    try:
        collection = db['map_sample_data']
        collection.delete_many({})
        collection.insert_many(map_data_cleaned.to_dict('records'))
        print(f"Successfully exported data to collection: map_sample_data")
    except Exception as e:
        print(f"Error exporting to map_sample_data: {e}")

    print(f"\nAll aggregates have been saved to the '{db.name}' database in MongoDB!")


def main():
    """
    Main function to run the analysis pipeline.
    """
    # 1. Connect to MongoDB
    # Get connection details from environment variables set in docker-compose.yml
    # Provide defaults for local testing outside of Docker
    MONGO_URL = os.environ.get("MONGO_CONN_STRING", "mongodb://localhost:27017/")
    DB_NAME = os.environ.get("DB_NAME", "taxi_analysis")
    
    client = None
    try:
        client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000) # 5-second timeout
        # Force a connection test
        client.server_info() 
        print(f"Successfully connected to MongoDB at {MONGO_URL}")
        db = client[DB_NAME]
        
        # 2. Data Collection (from MongoDB or Mock)
        data = load_mock_data(db)
        
        # 3. Feature Engineering & Cleaning
        data = feature_engineering(data)
        data = clean_data(data)
        
        # 5. Advanced Analysis
        run_regression(data)
        
        # 6. Export
        export_aggregates(db, data)
        
    except Exception as e:
        print(f"CRITICAL ERROR: Could not connect to MongoDB or run pipeline.")
        print(e)
    finally:
        if client:
            client.close()
            print("MongoDB connection closed.")


if __name__ == "__main__":
    main()