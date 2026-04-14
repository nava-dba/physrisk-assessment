# 🚀 Quick Start Guide - PhysRisk Pipeline

## Get Started in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

```bash
# Install required packages
pip install pandas openpyxl requests numpy

# Optional: Install PhysRisk library for real API access
pip install physrisk
```

### Step 2: Prepare Your Data (1 minute)

Ensure your input file is named:
```
List of assests for physical risk assessment- BDO.xlsx
```

And contains a sheet named `List assets` with these columns:
- IGS Office Name
- IGS Office Address
- City
- State
- Zip

### Step 3: Run the Pipeline (2 minutes)

```bash
# Run the enhanced version (recommended)
python physrisk_pipeline_v2.py
```

The pipeline will:
1. ✅ Geocode all addresses (takes ~1 second per address)
2. ✅ Fetch risk data for 6 scenarios (2 climate paths × 3 time periods)
3. ✅ Generate comprehensive Excel report

### Step 4: Review Outputs

**Generated Files:**
1. `Scenario_analysis_PhysRisk_Output.xlsx` - Main results
2. `List of assests for physical risk assessment- BDO_geocoded.xlsx` - Coordinates reference
3. `physrisk_pipeline.log` - Detailed execution log

## 📊 Understanding Your Results

### Excel File Structure

Your output file contains multiple sheets:

#### Scenario Sheets
- **SSP1-2.6 2030** - Low emissions, near-term
- **SSP1-2.6 2040** - Low emissions, mid-term
- **SSP1-2.6 2050** - Low emissions, long-term
- **SSP5-8.5 2030** - High emissions, near-term
- **SSP5-8.5 2040** - High emissions, mid-term
- **SSP5-8.5 2050** - High emissions, long-term

#### Key Columns in Each Sheet
- **Asset Information**: Name, Address, City, State
- **Coordinates**: Latitude, Longitude
- **Raw Risk Indicators**: Precipitation, Flood, Heat, Water, Wind, Fire
- **Normalized Scores**: Each indicator scaled 0-1
- **Composite Scores**:
  - PPT_Risk (Precipitation + Flood)
  - Water Stress Risk
  - Temperature Risk
  - Climate Hazards Risk
  - **Overall Climate Impact Score** ⭐ (Main metric)
- **Rankings**: Overall Climate Impact rank

### Summary Sheet
- Aggregated statistics for each asset
- Average, Max, Min risk scores across all scenarios
- **Sorted by highest average risk** (most vulnerable assets first)

## 🎯 Quick Analysis Tips

### Find Your Top 10 Riskiest Assets
1. Open the **Summary** sheet
2. Look at the top 10 rows (already sorted)
3. Note the `Avg_Risk_Score` column

### Compare Climate Scenarios
1. Open **SSP1-2.6 2050** sheet
2. Open **SSP5-8.5 2050** sheet
3. Compare `Overall Climate Impact Score` for same assets
4. Higher difference = more sensitive to emissions pathway

### Identify Risk Drivers
For each high-risk asset, check which normalized scores are highest:
- High `PPT_Risk` → Flooding concerns
- High `Water Stress Risk` → Water scarcity issues
- High `Temperature Risk` → Heat-related impacts
- High `Climate Hazards Risk` → Wind/fire exposure

## 🔧 Troubleshooting

### Issue: Geocoding Fails
**Solution**: Check address formatting in input file
```bash
# View the geocoded file to see which addresses failed
# Manually add coordinates for failed addresses
# Re-run pipeline
```

### Issue: Pipeline Runs Slowly
**Reason**: Geocoding takes ~1 second per address (API rate limit)
**Solution**: 
- For 25 assets, expect ~25 seconds for geocoding
- Subsequent runs can use cached coordinates

### Issue: Mock Data Warning
**Message**: "PhysRisk library not available. Using mock data mode."
**Solution**: 
```bash
pip install physrisk
```
Or continue with mock data for testing

## 📈 Next Steps

### For Client Presentation
1. Review the [PPT_PREPARATION_GUIDE.md](PPT_PREPARATION_GUIDE.md)
2. Extract key metrics from Summary sheet
3. Create visualizations using the data
4. Focus on top 10 highest-risk assets

### For Detailed Analysis
1. Review full [README.md](README.md)
2. Customize scenarios and years if needed
3. Add additional risk indicators
4. Integrate with GIS tools for mapping

## 💡 Pro Tips

1. **Save the geocoded file**: Speeds up future runs
2. **Check the log file**: Detailed information about each step
3. **Start with mock data**: Test the pipeline before using real API
4. **Backup your results**: Keep copies of output files with dates

## 🆘 Need Help?

1. Check `physrisk_pipeline.log` for error details
2. Review the full [README.md](README.md)
3. Consult [PhysRisk documentation](https://physrisk.readthedocs.io/)

---

**Estimated Total Time**: 5-10 minutes (depending on number of assets)

**Ready to go?** Run: `python physrisk_pipeline_v2.py`