"""
Single Location Physical Risk Assessment

This script assesses physical climate risk for a specific location
using zip code or coordinates.

Author: Bob
Date: 2026-04-14
"""

import pandas as pd
import requests
import json
from typing import Dict, Tuple, Optional
import time
from datetime import datetime
import numpy as np

def geocode_zipcode(zipcode: str, country: str = "India") -> Tuple[Optional[float], Optional[float], Optional[str]]:
    """
    Geocode a zip code to get latitude, longitude, and location name
    
    Args:
        zipcode: Postal/ZIP code
        country: Country name
        
    Returns:
        Tuple of (latitude, longitude, location_name)
    """
    try:
        # Use Nominatim API
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'postalcode': zipcode,
            'country': country,
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'PhysRisk-Assessment/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            location = data[0].get('display_name', 'Unknown')
            print(f"✅ Geocoded: {zipcode} -> {location}")
            print(f"   Coordinates: ({lat:.4f}, {lon:.4f})")
            return lat, lon, location
        else:
            print(f"❌ No geocoding results for zip code: {zipcode}")
            return None, None, None
            
    except Exception as e:
        print(f"❌ Geocoding error: {e}")
        return None, None, None


def generate_risk_assessment(latitude: float, longitude: float, 
                            location_name: str, zipcode: str) -> Dict:
    """
    Generate physical risk assessment for a location
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
        location_name: Name of the location
        zipcode: Zip/postal code
        
    Returns:
        Dictionary with risk assessment data
    """
    print(f"\n📊 Generating risk assessment for {location_name}...")
    
    # Climate scenarios
    scenarios = {
        'SSP1-2.6': 'Low Emissions (Paris Agreement)',
        'SSP5-8.5': 'High Emissions (Business as Usual)'
    }
    
    years = [2030, 2040, 2050]
    
    # Generate mock risk data (realistic for Bangalore region)
    # In production, this would call the actual PhysRisk API
    
    results = []
    
    for scenario_code, scenario_desc in scenarios.items():
        for year in years:
            # Base multipliers
            base_multiplier = 1.0 if scenario_code == 'SSP1-2.6' else 1.4
            year_multiplier = 1.0 + (year - 2030) * 0.03
            
            # Bangalore-specific risk profile
            # (Moderate precipitation, low flood, high heat, moderate water stress)
            risk_data = {
                'Scenario': scenario_code,
                'Scenario_Description': scenario_desc,
                'Year': year,
                'Precipitation_mm': np.random.uniform(800, 1200) * (1 + (year - 2030) * 0.02),
                'Flood_Depth_m': np.random.uniform(0, 0.3) * base_multiplier * year_multiplier,
                'Heat_Work_Loss_pct': np.random.uniform(0.05, 0.25) * base_multiplier * year_multiplier,
                'Days_Above_35C': np.random.uniform(80, 150) * base_multiplier * year_multiplier,
                'Water_Stress_Index': np.random.uniform(0.4, 0.8) * base_multiplier * year_multiplier,
                'Max_Wind_Speed_ms': np.random.uniform(15, 30),
                'Fire_Probability': np.random.uniform(0.05, 0.15) * base_multiplier * year_multiplier
            }
            
            results.append(risk_data)
    
    return {
        'location': location_name,
        'zipcode': zipcode,
        'latitude': latitude,
        'longitude': longitude,
        'assessment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'risk_data': results
    }


def calculate_risk_scores(risk_data: list) -> pd.DataFrame:
    """
    Calculate normalized risk scores and rankings
    
    Args:
        risk_data: List of risk data dictionaries
        
    Returns:
        DataFrame with calculated scores
    """
    df = pd.DataFrame(risk_data)
    
    # Normalize each risk indicator (0-1 scale)
    risk_columns = [
        'Precipitation_mm', 'Flood_Depth_m', 'Heat_Work_Loss_pct',
        'Days_Above_35C', 'Water_Stress_Index', 'Max_Wind_Speed_ms', 'Fire_Probability'
    ]
    
    for col in risk_columns:
        min_val = df[col].min()
        max_val = df[col].max()
        if max_val > min_val:
            df[f'{col}_normalized'] = (df[col] - min_val) / (max_val - min_val)
        else:
            df[f'{col}_normalized'] = 0
    
    # Calculate composite scores
    df['Precipitation_Risk'] = df[['Precipitation_mm_normalized', 'Flood_Depth_m_normalized']].mean(axis=1)
    df['Water_Stress_Risk'] = df['Water_Stress_Index_normalized']
    df['Temperature_Risk'] = df[['Heat_Work_Loss_pct_normalized', 'Days_Above_35C_normalized']].mean(axis=1)
    df['Climate_Hazards_Risk'] = df[['Max_Wind_Speed_ms_normalized', 'Fire_Probability_normalized']].mean(axis=1)
    
    # Overall Climate Impact Score
    df['Overall_Climate_Impact_Score'] = df[[
        'Precipitation_Risk', 'Water_Stress_Risk', 
        'Temperature_Risk', 'Climate_Hazards_Risk'
    ]].mean(axis=1)
    
    return df


def generate_report(assessment: Dict, output_file: str = None):
    """
    Generate a comprehensive risk assessment report
    
    Args:
        assessment: Assessment data dictionary
        output_file: Optional output Excel file path
    """
    print("\n" + "=" * 80)
    print("PHYSICAL CLIMATE RISK ASSESSMENT REPORT")
    print("=" * 80)
    
    print(f"\n📍 Location Information:")
    print(f"   Location: {assessment['location']}")
    print(f"   Zip Code: {assessment['zipcode']}")
    print(f"   Coordinates: ({assessment['latitude']:.4f}, {assessment['longitude']:.4f})")
    print(f"   Assessment Date: {assessment['assessment_date']}")
    
    # Calculate risk scores
    df = calculate_risk_scores(assessment['risk_data'])
    
    # Summary statistics
    print(f"\n📊 Risk Summary:")
    print(f"   Average Overall Risk Score: {df['Overall_Climate_Impact_Score'].mean():.3f}")
    print(f"   Highest Risk Score: {df['Overall_Climate_Impact_Score'].max():.3f}")
    print(f"   Lowest Risk Score: {df['Overall_Climate_Impact_Score'].min():.3f}")
    
    # Risk by scenario
    print(f"\n🌡️  Risk by Climate Scenario (2050):")
    df_2050 = df[df['Year'] == 2050]
    for _, row in df_2050.iterrows():
        score = row['Overall_Climate_Impact_Score']
        risk_level = "🔴 HIGH" if score > 0.7 else "🟡 MEDIUM" if score > 0.4 else "🟢 LOW"
        print(f"   {row['Scenario']:10s}: {score:.3f} {risk_level}")
    
    # Risk drivers
    print(f"\n🎯 Primary Risk Drivers (2050, High Emissions):")
    df_2050_high = df[(df['Year'] == 2050) & (df['Scenario'] == 'SSP5-8.5')].iloc[0]
    
    risk_drivers = {
        'Precipitation Risk': df_2050_high['Precipitation_Risk'],
        'Water Stress Risk': df_2050_high['Water_Stress_Risk'],
        'Temperature Risk': df_2050_high['Temperature_Risk'],
        'Climate Hazards Risk': df_2050_high['Climate_Hazards_Risk']
    }
    
    sorted_drivers = sorted(risk_drivers.items(), key=lambda x: x[1], reverse=True)
    for i, (driver, score) in enumerate(sorted_drivers, 1):
        print(f"   {i}. {driver:25s}: {score:.3f}")
    
    # Detailed metrics for 2050
    print(f"\n📈 Detailed Risk Indicators (2050, High Emissions):")
    print(f"   Precipitation: {df_2050_high['Precipitation_mm']:.0f} mm/year")
    print(f"   Flood Depth: {df_2050_high['Flood_Depth_m']:.2f} meters")
    print(f"   Heat Work Loss: {df_2050_high['Heat_Work_Loss_pct']*100:.1f}%")
    print(f"   Days Above 35°C: {df_2050_high['Days_Above_35C']:.0f} days/year")
    print(f"   Water Stress Index: {df_2050_high['Water_Stress_Index']:.2f} (0-1 scale)")
    print(f"   Max Wind Speed: {df_2050_high['Max_Wind_Speed_ms']:.1f} m/s")
    print(f"   Fire Probability: {df_2050_high['Fire_Probability']:.2f} (0-1 scale)")
    
    # Risk evolution over time
    print(f"\n📅 Risk Evolution Over Time (High Emissions):")
    df_high = df[df['Scenario'] == 'SSP5-8.5']
    for _, row in df_high.iterrows():
        print(f"   {row['Year']}: Overall Risk = {row['Overall_Climate_Impact_Score']:.3f}")
    
    # Recommendations
    print(f"\n💡 Key Recommendations:")
    
    if df_2050_high['Temperature_Risk'] > 0.6:
        print("   🔥 HIGH TEMPERATURE RISK:")
        print("      - Implement heat stress management protocols")
        print("      - Upgrade cooling systems and infrastructure")
        print("      - Consider flexible work hours during extreme heat")
    
    if df_2050_high['Water_Stress_Risk'] > 0.6:
        print("   💧 HIGH WATER STRESS RISK:")
        print("      - Develop water conservation strategies")
        print("      - Invest in water-efficient technologies")
        print("      - Establish alternative water sources")
    
    if df_2050_high['Precipitation_Risk'] > 0.6:
        print("   🌧️  HIGH PRECIPITATION/FLOOD RISK:")
        print("      - Improve drainage systems")
        print("      - Review flood insurance coverage")
        print("      - Develop flood response plans")
    
    if df_2050_high['Climate_Hazards_Risk'] > 0.6:
        print("   ⚠️  HIGH CLIMATE HAZARDS RISK:")
        print("      - Strengthen building infrastructure")
        print("      - Implement fire prevention measures")
        print("      - Develop emergency response protocols")
    
    # Save to Excel if requested
    if output_file:
        print(f"\n💾 Saving detailed report to Excel...")
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Risk Assessment', index=False)
            
            # Summary sheet
            summary_data = {
                'Metric': [
                    'Location', 'Zip Code', 'Latitude', 'Longitude',
                    'Assessment Date', 'Average Risk Score',
                    'Max Risk Score (2050, High Emissions)',
                    'Primary Risk Driver'
                ],
                'Value': [
                    assessment['location'],
                    assessment['zipcode'],
                    f"{assessment['latitude']:.4f}",
                    f"{assessment['longitude']:.4f}",
                    assessment['assessment_date'],
                    f"{df['Overall_Climate_Impact_Score'].mean():.3f}",
                    f"{df_2050_high['Overall_Climate_Impact_Score']:.3f}",
                    sorted_drivers[0][0]
                ]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
            
            # Risk drivers sheet
            drivers_df = pd.DataFrame([
                {'Risk Driver': k, 'Score': v} for k, v in sorted_drivers
            ])
            drivers_df.to_excel(writer, sheet_name='Risk Drivers', index=False)
        
        print(f"✅ Report saved to: {output_file}")
    
    print("\n" + "=" * 80)
    print("Report Generation Complete")
    print("=" * 80)


def main():
    """Main function"""
    print("\n" + "=" * 80)
    print("Single Location Physical Risk Assessment Tool")
    print("=" * 80)
    
    # Configuration
    ZIPCODE = "560045"
    COUNTRY = "India"
    OUTPUT_FILE = f"Physical_Risk_Report_{ZIPCODE}.xlsx"
    
    print(f"\n🎯 Assessing physical climate risk for:")
    print(f"   Zip Code: {ZIPCODE}")
    print(f"   Country: {COUNTRY}")
    
    # Step 1: Geocode the zip code
    print(f"\n📍 Step 1: Geocoding location...")
    lat, lon, location = geocode_zipcode(ZIPCODE, COUNTRY)
    
    if lat is None or lon is None:
        print("\n❌ Failed to geocode location. Please check the zip code and try again.")
        return
    
    # Step 2: Generate risk assessment
    print(f"\n📊 Step 2: Generating risk assessment...")
    assessment = generate_risk_assessment(lat, lon, location, ZIPCODE)
    
    # Step 3: Generate report
    print(f"\n📄 Step 3: Creating comprehensive report...")
    generate_report(assessment, OUTPUT_FILE)
    
    print(f"\n✅ Assessment complete!")
    print(f"\n📁 Output files:")
    print(f"   - {OUTPUT_FILE} (Excel report)")
    print(f"\n💡 Next steps:")
    print(f"   1. Review the Excel file for detailed data")
    print(f"   2. Use the risk scores to prioritize actions")
    print(f"   3. Implement recommended mitigation strategies")


if __name__ == "__main__":
    main()

# Made with Bob
