# PhysRisk Physical Risk Assessment Pipeline for BDO

This pipeline automates the process of fetching physical climate risk data from the PhysRisk API for BDO's asset portfolio and generates scenario analysis reports.

## 📋 Overview

The pipeline performs the following steps:
1. **Loads** asset locations from Excel file
2. **Geocodes** addresses to obtain latitude/longitude coordinates
3. **Fetches** physical risk data from PhysRisk API for multiple scenarios and years
4. **Processes** and normalizes risk indicators
5. **Generates** comprehensive Excel reports for client presentations

## 🎯 Features

- **Automated Geocoding**: Converts addresses to coordinates using OpenStreetMap Nominatim API
- **Multi-Scenario Analysis**: Supports SSP1-2.6 and SSP5-8.5 climate scenarios
- **Time Horizons**: Analyzes risks for 2030, 2040, and 2050
- **Comprehensive Risk Indicators**:
  - Precipitation risk
  - Flood depth (combined inundation)
  - Heat stress (work loss)
  - Extreme heat days (>95°F)
  - Water stress
  - Wind speed
  - Fire probability
- **Risk Scoring**: Normalized scores and rankings for easy comparison
- **Excel Output**: Multiple sheets organized by scenario and year

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download** this repository to your local machine

2. **Install required packages**:
```bash
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python -c "import pandas, requests, openpyxl; print('All packages installed successfully!')"
```

## 🚀 Usage

### Basic Usage

1. **Ensure your input file is in the correct location**:
   - File name: `List of assests for physical risk assessment- BDO.xlsx`
   - Must contain a sheet named `List assets` with columns:
     - IGS Office Name
     - IGS Office Address
     - City
     - State
     - Zip

2. **Run the pipeline**:
```bash
python physrisk_pipeline.py
```

3. **Monitor progress**:
   - Watch console output for real-time progress
   - Check `physrisk_pipeline.log` for detailed logs

4. **Review outputs**:
   - `Scenario_analysis_PhysRisk_Output.xlsx` - Main results file
   - `List of assests for physical risk assessment- BDO_geocoded.xlsx` - Geocoded coordinates reference

### Advanced Usage

#### Custom Configuration

Edit the `main()` function in `physrisk_pipeline.py` to customize:

```python
def main():
    # Custom input/output files
    INPUT_FILE = "your_custom_input.xlsx"
    OUTPUT_FILE = "your_custom_output.xlsx"
    
    pipeline = PhysRiskPipeline(INPUT_FILE, OUTPUT_FILE)
    pipeline.run()
```

#### Modify Scenarios and Years

Edit the `__init__` method in the `PhysRiskPipeline` class:

```python
# Add or remove scenarios
self.scenarios = ['ssp126', 'ssp245', 'ssp585']

# Add or remove years
self.years = [2030, 2040, 2050, 2070, 2100]
```

## 📊 Output File Structure

The generated Excel file contains multiple sheets:

### Scenario Sheets (e.g., SSP126_2030, SSP585_2050)
Each sheet contains:
- Asset information (name, address, city, state)
- Geographic coordinates (latitude, longitude)
- Raw risk indicator values
- Normalized risk scores (0-1 scale)
- Overall climate impact score
- Risk ranking

### Summary Sheet
- Aggregated statistics for each asset
- Average, maximum, and minimum risk scores across all scenarios
- Sorted by average risk score (highest to lowest)

### Geocoded_Assets Sheet
- Reference sheet with all assets and their coordinates
- Useful for verification and mapping

## 🔧 Troubleshooting

### Common Issues

#### 1. Geocoding Failures
**Problem**: Some addresses cannot be geocoded

**Solutions**:
- Check address formatting in input file
- Verify ZIP codes are correct
- Manually add coordinates for failed addresses in the geocoded file
- Re-run pipeline with updated coordinates

#### 2. API Rate Limiting
**Problem**: Too many requests to geocoding or PhysRisk API

**Solutions**:
- Pipeline includes built-in rate limiting (1 second between geocoding requests)
- For large datasets, consider running in batches
- Use cached geocoded coordinates file to skip geocoding step

#### 3. Missing Data
**Problem**: Some risk indicators return null values

**Solutions**:
- Check PhysRisk API documentation for data availability
- Verify coordinates are within supported regions
- Review API response logs in `physrisk_pipeline.log`

### Debug Mode

Enable detailed logging by modifying the logging level:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    ...
)
```

## 📈 Using Results for Client Presentations

### Step 1: Review Risk Rankings
1. Open the Summary sheet
2. Identify top 10 highest-risk assets
3. Note key risk drivers for each asset

### Step 2: Scenario Comparison
1. Compare SSP1-2.6 (low emissions) vs SSP5-8.5 (high emissions)
2. Analyze risk progression across time horizons (2030, 2040, 2050)
3. Identify assets with accelerating risk trends

### Step 3: Create Visualizations
Use the data to create:
- **Heat maps**: Geographic distribution of risks
- **Bar charts**: Top 10 highest-risk assets
- **Line charts**: Risk progression over time
- **Scatter plots**: Risk correlation analysis

### Step 4: Key Metrics for PPT
Extract these metrics for your presentation:
- Total number of assets analyzed
- Percentage of assets in high-risk category
- Top 3 risk drivers across portfolio
- Assets requiring immediate attention
- Comparison between scenarios

### Recommended PPT Structure
1. **Executive Summary**
   - Portfolio overview
   - Key findings
   - Critical assets

2. **Methodology**
   - Data sources (PhysRisk API)
   - Scenarios analyzed
   - Risk indicators

3. **Results by Scenario**
   - SSP1-2.6 analysis
   - SSP5-8.5 analysis
   - Comparative insights

4. **Asset-Level Analysis**
   - Top 10 highest-risk assets
   - Geographic clustering
   - Risk drivers

5. **Recommendations**
   - Prioritization framework
   - Mitigation strategies
   - Monitoring plan

## 🔗 PhysRisk API Documentation

For detailed information about the PhysRisk API:
- Documentation: https://physrisk.readthedocs.io/en/stable/api/physrisk.html
- GitHub: https://github.com/os-climate/physrisk

### Important Notes about PhysRisk API

⚠️ **API Configuration Required**: The current pipeline includes a template for PhysRisk API calls. You may need to:

1. **Install PhysRisk Python package**:
```bash
pip install physrisk
```

2. **Update API endpoints**: The actual PhysRisk API may use different endpoints than shown in the template. Refer to the official documentation.

3. **Authentication**: Check if API key or authentication is required.

4. **Alternative: Use PhysRisk Python Library Directly**:
```python
from physrisk.api.v1.hazard_data import HazardDataRequest
from physrisk.kernel.hazards import RiverineInundation, ChronicHeat

# Example usage
request = HazardDataRequest(
    longitude=longitude,
    latitude=latitude,
    scenario="ssp585",
    year=2050
)
```

## 📝 Data Dictionary

### Risk Indicators

| Indicator | Description | Unit | Source |
|-----------|-------------|------|--------|
| Precipitation | Annual precipitation | mm | OS Climate |
| Flood Depth | Combined inundation depth | meters | OS Climate |
| Heat Work Loss | Mean work loss due to heat stress | % | OS Climate |
| Heat Days >95°F | Days per year above 95°F | days | OS Climate |
| Water Stress | Water stress index | 0-1 | Aqueduct |
| Wind Speed | Max 1-minute sustained wind | m/s | OS Climate |
| Fire Probability | Wildfire probability | 0-1 | OS Climate |

### Climate Scenarios

- **SSP1-2.6**: Low emissions scenario (Paris Agreement aligned)
- **SSP5-8.5**: High emissions scenario (business as usual)

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review `physrisk_pipeline.log` for detailed error messages
3. Consult PhysRisk documentation
4. Contact the development team

## 📄 License

This pipeline is provided for BDO's internal use for physical risk assessment.

## 🔄 Version History

- **v1.0.0** (2026-04-14): Initial release
  - Automated geocoding
  - Multi-scenario analysis
  - Excel report generation
  - Comprehensive logging

---

**Last Updated**: April 14, 2026  
**Author**: Bob  
**Purpose**: BDO Physical Risk Assessment Automation