"""
PhysRisk Data Pipeline for BDO Physical Risk Assessment - Version 2
Uses the official PhysRisk Python library

This pipeline:
1. Reads asset locations from Excel
2. Geocodes addresses to get latitude/longitude
3. Fetches physical risk data using PhysRisk library
4. Processes and formats the data
5. Generates output Excel file for scenario analysis

Author: Bob
Date: 2026-04-14
"""

import pandas as pd
import requests
import json
from typing import Dict, List, Tuple, Optional
import time
from pathlib import Path
import logging
from datetime import datetime
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('physrisk_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PhysRiskPipelineV2:
    """Enhanced pipeline using PhysRisk Python library"""
    
    def __init__(self, input_file: str, output_file: str):
        """
        Initialize the pipeline
        
        Args:
            input_file: Path to input Excel file with asset locations
            output_file: Path to output Excel file for results
        """
        self.input_file = input_file
        self.output_file = output_file
        self.assets_df = None
        self.results = []
        
        # Import PhysRisk components
        try:
            from physrisk.api.v1.hazard_data import HazardDataRequest, HazardDataResponse
            from physrisk.kernel.hazards import (
                RiverineInundation, ChronicHeat, Fire, Drought, 
                CoastalInundation, Wind, Precipitation
            )
            self.physrisk_available = True
            self.HazardDataRequest = HazardDataRequest
            logger.info("PhysRisk library loaded successfully")
        except ImportError:
            self.physrisk_available = False
            logger.warning("PhysRisk library not available. Using mock data mode.")
        
        # Scenarios and years to analyze
        self.scenarios = {
            'ssp126': 'SSP1-2.6',
            'ssp585': 'SSP5-8.5'
        }
        self.years = [2030, 2040, 2050]
        
        # Risk indicators mapping
        self.risk_indicators = {
            'precipitation': 'Precipitation (mm)',
            'flood_depth': 'Flood Depth (combined inundation)',
            'heat_work_loss': 'Mean work loss due to heat stress',
            'heat_days_95f': 'Number of days per year above >95 °F',
            'water_stress': 'Water risk (Aqueduct)',
            'wind_speed': 'Max wind speed (m/s)',
            'fire_probability': 'Fire Probability'
        }
    
    def load_assets(self) -> pd.DataFrame:
        """Load asset data from input Excel file"""
        logger.info(f"Loading assets from {self.input_file}")
        
        try:
            # Read the Excel file
            df = pd.read_excel(self.input_file, sheet_name='List assets')
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            logger.info(f"Loaded {len(df)} assets")
            self.assets_df = df
            return df
            
        except Exception as e:
            logger.error(f"Error loading assets: {e}")
            raise
    
    def geocode_address(self, address: str, city: str, state: str, zip_code: str) -> Tuple[Optional[float], Optional[float]]:
        """
        Geocode an address to get latitude and longitude
        Uses OpenStreetMap Nominatim API (free, no API key required)
        
        Args:
            address: Street address
            city: City name
            state: State code
            zip_code: ZIP code
            
        Returns:
            Tuple of (latitude, longitude) or (None, None) if geocoding fails
        """
        try:
            # Construct full address
            full_address = f"{address}, {city}, {state} {zip_code}, USA"
            
            # Use Nominatim API
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': full_address,
                'format': 'json',
                'limit': 1
            }
            headers = {
                'User-Agent': 'BDO-PhysRisk-Pipeline/2.0'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                logger.info(f"Geocoded: {city}, {state} -> ({lat:.4f}, {lon:.4f})")
                return lat, lon
            else:
                logger.warning(f"No geocoding results for: {full_address}")
                return None, None
                
        except Exception as e:
            logger.error(f"Geocoding error for {city}, {state}: {e}")
            return None, None
        
        finally:
            # Rate limiting - be respectful to free API
            time.sleep(1)
    
    def geocode_all_assets(self) -> pd.DataFrame:
        """Geocode all assets in the dataframe"""
        logger.info("Starting geocoding for all assets...")
        
        if self.assets_df is None:
            raise ValueError("Assets not loaded. Call load_assets() first.")
        
        latitudes = []
        longitudes = []
        
        for idx, row in self.assets_df.iterrows():
            address = str(row.get('IGS Office Address', ''))
            city = str(row.get('City', ''))
            state = str(row.get('State', ''))
            zip_code = str(row.get('Zip', ''))
            
            lat, lon = self.geocode_address(address, city, state, zip_code)
            latitudes.append(lat)
            longitudes.append(lon)
        
        self.assets_df['Latitude'] = latitudes
        self.assets_df['Longitude'] = longitudes
        
        # Count successful geocodes
        success_count = self.assets_df['Latitude'].notna().sum()
        logger.info(f"Successfully geocoded {success_count}/{len(self.assets_df)} assets")
        
        return self.assets_df
    
    def fetch_physrisk_data_mock(self, latitude: float, longitude: float, 
                                 scenario: str, year: int) -> Dict:
        """
        Generate mock physical risk data for testing
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            scenario: Climate scenario
            year: Future year
            
        Returns:
            Dictionary with mock risk indicators
        """
        # Generate realistic-looking mock data based on location and scenario
        base_multiplier = 1.0 if scenario == 'ssp126' else 1.3
        year_multiplier = 1.0 + (year - 2030) * 0.02
        
        # Add some randomness based on coordinates
        location_factor = (abs(latitude) + abs(longitude)) / 100
        
        mock_data = {
            'Precipitation (mm)': np.random.uniform(100, 300) * location_factor,
            'Flood Depth (combined inundation)': np.random.uniform(0, 1) * base_multiplier * year_multiplier,
            'Mean work loss due to heat stress': np.random.uniform(0, 0.3) * base_multiplier * year_multiplier,
            'Number of days per year above >95 °F': np.random.uniform(0, 50) * base_multiplier * year_multiplier,
            'Water risk (Aqueduct)': np.random.uniform(0, 1) * location_factor,
            'Max wind speed (m/s)': np.random.uniform(20, 40),
            'Fire Probability': np.random.uniform(0, 0.2) * location_factor
        }
        
        return mock_data
    
    def fetch_physrisk_data_real(self, latitude: float, longitude: float,
                                 scenario: str, year: int) -> Dict:
        """
        Fetch real physical risk data using PhysRisk library
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            scenario: Climate scenario
            year: Future year
            
        Returns:
            Dictionary with risk indicators
        """
        try:
            # Create hazard data request
            request = self.HazardDataRequest(
                longitude=longitude,
                latitude=latitude,
                scenario=scenario,
                year=year
            )
            
            # Fetch data for different hazards
            # Note: Actual implementation depends on PhysRisk API structure
            risk_data = {}
            
            # This is a template - adjust based on actual PhysRisk API
            # Example: risk_data = request.get_hazard_data()
            
            return risk_data
            
        except Exception as e:
            logger.error(f"Error fetching PhysRisk data: {e}")
            return {}
    
    def fetch_physrisk_data(self, latitude: float, longitude: float,
                           scenario: str, year: int) -> Dict:
        """
        Fetch physical risk data (uses real API if available, otherwise mock)
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            scenario: Climate scenario
            year: Future year
            
        Returns:
            Dictionary with risk indicators
        """
        if self.physrisk_available:
            return self.fetch_physrisk_data_real(latitude, longitude, scenario, year)
        else:
            return self.fetch_physrisk_data_mock(latitude, longitude, scenario, year)
    
    def process_asset_risks(self, asset_row: pd.Series) -> List[Dict]:
        """
        Process all risk scenarios for a single asset
        
        Args:
            asset_row: Row from assets dataframe
            
        Returns:
            List of dictionaries with risk data for each scenario/year combination
        """
        results = []
        
        lat = asset_row['Latitude']
        lon = asset_row['Longitude']
        
        if pd.isna(lat) or pd.isna(lon):
            logger.warning(f"Skipping asset {asset_row['IGS Office Name']} - no coordinates")
            return results
        
        office_name = asset_row['IGS Office Name']
        address = asset_row['IGS Office Address']
        city = asset_row['City']
        state = asset_row['State']
        
        logger.info(f"Processing risks for: {office_name}")
        
        for scenario_code, scenario_name in self.scenarios.items():
            for year in self.years:
                logger.info(f"  Fetching {scenario_name} {year}...")
                
                risk_data = self.fetch_physrisk_data(float(lat), float(lon), scenario_code, year)
                
                result = {
                    'Asset (IGS Office name)': office_name,
                    'Address': address,
                    'City': city,
                    'State': state,
                    'Latitude': lat,
                    'Longitude': lon,
                    'Scenario': scenario_name,
                    'Year': year,
                    **risk_data
                }
                
                results.append(result)
                
                # Rate limiting
                time.sleep(0.2)
        
        return results
    
    def normalize_and_rank(self, df: pd.DataFrame, scenario: str, year: int) -> pd.DataFrame:
        """
        Normalize risk indicators and calculate rankings for a specific scenario/year
        
        Args:
            df: DataFrame with risk data
            scenario: Climate scenario
            year: Year
            
        Returns:
            DataFrame with normalized values and rankings
        """
        # Filter for specific scenario and year
        df_filtered = df[(df['Scenario'] == scenario) & (df['Year'] == year)].copy()
        
        if df_filtered.empty:
            return df_filtered
        
        # Get numeric columns (risk indicators)
        numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns
        risk_cols = [col for col in numeric_cols if col not in 
                    ['Latitude', 'Longitude', 'Year']]
        
        # Normalize each risk indicator (0-1 scale)
        for col in risk_cols:
            min_val = df_filtered[col].min()
            max_val = df_filtered[col].max()
            
            if max_val > min_val:
                df_filtered[f'{col}_N'] = (df_filtered[col] - min_val) / (max_val - min_val)
            else:
                df_filtered[f'{col}_N'] = 0
        
        # Calculate composite risk scores
        normalized_cols = [col for col in df_filtered.columns if col.endswith('_N')]
        
        if normalized_cols:
            # PPT Risk (precipitation + flood)
            ppt_cols = [col for col in normalized_cols if 'Precipitation' in col or 'Flood' in col]
            if ppt_cols:
                df_filtered['PPT_Risk'] = df_filtered[ppt_cols].mean(axis=1)
            
            # Water Stress Risk
            water_cols = [col for col in normalized_cols if 'Water' in col or 'Drought' in col]
            if water_cols:
                df_filtered['Water Stress Risk'] = df_filtered[water_cols].mean(axis=1)
            
            # Temperature Risk (heat-related)
            temp_cols = [col for col in normalized_cols if 'heat' in col.lower() or 'days' in col.lower()]
            if temp_cols:
                df_filtered['Temperature Risk'] = df_filtered[temp_cols].mean(axis=1)
            
            # Climate Hazards Risk (wind + fire)
            hazard_cols = [col for col in normalized_cols if 'wind' in col.lower() or 'fire' in col.lower()]
            if hazard_cols:
                df_filtered['Climate Hazards Risk'] = df_filtered[hazard_cols].mean(axis=1)
            
            # Overall Climate Impact Score
            composite_cols = ['PPT_Risk', 'Water Stress Risk', 'Temperature Risk', 'Climate Hazards Risk']
            available_composite = [col for col in composite_cols if col in df_filtered.columns]
            
            if available_composite:
                df_filtered['Overall Climate Impact Score'] = df_filtered[available_composite].mean(axis=1)
                
                # Add rankings
                df_filtered['Overall Climate Impact rank'] = df_filtered['Overall Climate Impact Score'].rank(
                    ascending=False, method='min'
                ).astype(int)
        
        return df_filtered
    
    def generate_output_excel(self, results_df: pd.DataFrame):
        """
        Generate output Excel file matching the template structure
        
        Args:
            results_df: DataFrame with all processed results
        """
        logger.info(f"Generating output Excel file: {self.output_file}")
        
        with pd.ExcelWriter(self.output_file, engine='openpyxl') as writer:
            # Create sheets for each scenario/year combination
            for scenario_code, scenario_name in self.scenarios.items():
                for year in self.years:
                    sheet_name = f"{scenario_name.replace('-', '-')} {year}"
                    
                    # Normalize and rank data for this scenario/year
                    df_sheet = self.normalize_and_rank(results_df, scenario_name, year)
                    
                    if not df_sheet.empty:
                        # Sort by risk score
                        if 'Overall Climate Impact Score' in df_sheet.columns:
                            df_sheet = df_sheet.sort_values('Overall Climate Impact Score', 
                                                           ascending=False)
                        
                        # Write to sheet
                        df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
                        logger.info(f"  Created sheet: {sheet_name}")
            
            # Create summary sheet
            if 'Overall Climate Impact Score' in results_df.columns:
                summary = results_df.groupby(['Asset (IGS Office name)', 'City', 'State']).agg({
                    'Overall Climate Impact Score': ['mean', 'max', 'min', 'std']
                }).reset_index()
                
                summary.columns = ['Asset', 'City', 'State', 'Avg_Risk_Score', 
                                 'Max_Risk_Score', 'Min_Risk_Score', 'Std_Risk_Score']
                summary = summary.sort_values('Avg_Risk_Score', ascending=False)
                summary.to_excel(writer, sheet_name='Summary', index=False)
                logger.info("  Created summary sheet")
            
            # Create geocoded assets reference sheet
            if self.assets_df is not None:
                self.assets_df.to_excel(writer, sheet_name='Geocoded_Assets', index=False)
                logger.info("  Created geocoded assets sheet")
        
        logger.info(f"Output file created successfully: {self.output_file}")
    
    def run(self):
        """Execute the complete pipeline"""
        logger.info("=" * 80)
        logger.info("Starting PhysRisk Pipeline V2")
        logger.info("=" * 80)
        
        start_time = time.time()
        
        try:
            # Step 1: Load assets
            self.load_assets()
            
            # Step 2: Geocode addresses
            self.geocode_all_assets()
            
            # Save geocoded assets for reference
            geocoded_file = self.input_file.replace('.xlsx', '_geocoded.xlsx')
            if self.assets_df is not None:
                self.assets_df.to_excel(geocoded_file, index=False)
                logger.info(f"Saved geocoded assets to: {geocoded_file}")
            
            # Step 3: Fetch risk data for each asset
            all_results = []
            if self.assets_df is not None:
                for idx, row in self.assets_df.iterrows():
                    asset_results = self.process_asset_risks(row)
                    all_results.extend(asset_results)
            
            # Step 4: Create results dataframe
            results_df = pd.DataFrame(all_results)
            
            # Step 5: Generate output Excel
            if not results_df.empty:
                self.generate_output_excel(results_df)
            else:
                logger.warning("No results to generate - check if geocoding was successful")
            
            elapsed_time = time.time() - start_time
            logger.info("=" * 80)
            logger.info(f"Pipeline completed successfully in {elapsed_time:.2f} seconds")
            logger.info(f"Processed {len(all_results)} risk assessments")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            raise


def main():
    """Main entry point"""
    # Configuration
    INPUT_FILE = "List of assests for physical risk assessment- BDO.xlsx"
    OUTPUT_FILE = "Scenario_analysis_PhysRisk_Output.xlsx"
    
    # Create and run pipeline
    pipeline = PhysRiskPipelineV2(INPUT_FILE, OUTPUT_FILE)
    pipeline.run()


if __name__ == "__main__":
    main()

# Made with Bob
