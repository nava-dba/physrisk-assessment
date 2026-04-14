# 🌐 PhysRisk Web Application Guide

## Overview

A user-friendly web interface for physical climate risk assessment with:
- 📤 **File Upload**: Drag-and-drop Excel file upload
- 📊 **Interactive Dashboard**: Real-time visualizations and analytics
- 💬 **AI Chat**: Ask questions about your data in natural language
- 📥 **Export Results**: Download comprehensive reports

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- Plotly (interactive charts)
- Pandas, NumPy (data processing)
- All other required packages

### 2. Launch the Application

```bash
streamlit run app.py
```

The app will automatically open in your default web browser at `http://localhost:8501`

### 3. Use the Application

1. **Upload Data**: Go to "Upload & Process" page
2. **Upload Excel File**: Click "Browse files" and select your Excel file
3. **Run Assessment**: Click "Run Risk Assessment" button
4. **View Results**: Navigate to "Analysis Dashboard"
5. **Ask Questions**: Use "Chat with Data" for insights
6. **Download**: Export results from "Download Results" page

## 📋 Features

### 🏠 Home Page
- Welcome screen with quick start guide
- Feature overview
- Input file requirements
- Example data format

### 📤 Upload & Process
- **File Upload**: Drag-and-drop or browse for Excel files
- **Data Preview**: View uploaded data before processing
- **Statistics**: See asset count, states, and cities
- **Process Button**: Run the risk assessment pipeline
- **Progress Indicator**: Real-time processing status

### 📊 Analysis Dashboard

#### Key Metrics
- Total assets analyzed
- Average risk score
- High-risk asset count
- Maximum risk score

#### Visualizations

**Tab 1: Risk Distribution**
- Pie chart showing high/medium/low risk breakdown
- Histogram of risk score distribution

**Tab 2: Geographic View**
- Bar chart of average risk by state
- Interactive map with asset locations (color-coded by risk)

**Tab 3: Top Assets**
- Bar chart of top 10 highest-risk assets
- Detailed table with risk scores

**Tab 4: Time Evolution**
- Line chart showing risk progression (2030→2040→2050)
- Comparison between SSP1-2.6 and SSP5-8.5 scenarios

### 💬 Chat with Data

**AI-Powered Q&A Interface**

Ask questions like:
- "What are the highest-risk assets?"
- "Show me the lowest-risk locations"
- "What's the average risk score?"
- "Which states have the highest risk?"
- "What recommendations do you have?"
- "Tell me about the risk distribution"

**Features:**
- Natural language understanding
- Context-aware responses
- Data-driven insights
- Actionable recommendations
- Chat history
- Clear chat option

### 📥 Download Results

**Available Downloads:**
1. **Full Excel Report**: Complete analysis with all sheets
2. **Summary CSV**: Quick summary for data import

## 🎨 User Interface

### Color Coding
- 🔴 **Red**: High risk (score > 0.7)
- 🟡 **Yellow**: Medium risk (score 0.4-0.7)
- 🟢 **Green**: Low risk (score < 0.4)

### Navigation
- **Sidebar**: Easy page navigation
- **Tabs**: Organized content within pages
- **Responsive**: Works on desktop and tablet

## 💡 Usage Tips

### Best Practices

1. **File Preparation**
   - Ensure Excel file has "List assets" sheet
   - Include all required columns
   - Check for data quality before upload

2. **Processing**
   - Allow 1-2 minutes for processing
   - Don't close browser during processing
   - Check progress indicator

3. **Analysis**
   - Start with Key Metrics overview
   - Explore different visualization tabs
   - Use filters and sorting in tables

4. **Chat Interface**
   - Ask specific questions for better results
   - Use suggested questions as templates
   - Review chat history for insights

5. **Export**
   - Download Excel for detailed analysis
   - Use CSV for quick data import
   - Save files with descriptive names

## 🔧 Customization

### Modify Chat Responses

Edit the `analyze_data_with_ai()` function in `app.py`:

```python
def analyze_data_with_ai(question, data):
    # Add your custom logic here
    # Integrate with OpenAI, Claude, or other LLM APIs
    pass
```

### Add New Visualizations

Add new tabs in the dashboard section:

```python
with tab5:
    st.subheader("Your Custom Visualization")
    # Add your chart code here
```

### Change Color Scheme

Modify the CSS in the `st.markdown()` section:

```python
st.markdown("""
<style>
    .risk-high { color: #your-color; }
    .risk-medium { color: #your-color; }
    .risk-low { color: #your-color; }
</style>
""", unsafe_allow_html=True)
```

## 🐛 Troubleshooting

### Issue: App Won't Start

**Solution:**
```bash
# Check if Streamlit is installed
pip list | grep streamlit

# Reinstall if needed
pip install streamlit --upgrade
```

### Issue: File Upload Fails

**Possible Causes:**
- File format not supported (use .xlsx or .xls)
- Missing "List assets" sheet
- Incorrect column names

**Solution:**
- Verify file format
- Check sheet name (case-sensitive)
- Review column names against requirements

### Issue: Processing Takes Too Long

**Reasons:**
- Large number of assets (>50)
- Geocoding API rate limits
- Network connectivity

**Solutions:**
- Be patient (1-2 minutes is normal)
- Check internet connection
- Review logs for errors

### Issue: Charts Not Displaying

**Solution:**
```bash
# Reinstall Plotly
pip install plotly --upgrade

# Clear Streamlit cache
streamlit cache clear
```

### Issue: Chat Not Working

**Reason:**
- Default implementation uses rule-based responses
- No LLM API configured

**Solution:**
- Use provided question templates
- Or integrate with your preferred LLM API

## 🔐 Security Considerations

### Data Privacy
- All processing happens locally
- No data sent to external servers (except geocoding)
- Files stored temporarily during processing
- Automatic cleanup after session

### Best Practices
- Don't upload sensitive data to public deployments
- Use secure connections (HTTPS) for production
- Implement authentication for multi-user deployments
- Regular security updates

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Network Access
```bash
streamlit run app.py --server.address 0.0.0.0
```

### Production Deployment

**Option 1: Streamlit Cloud**
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy with one click

**Option 2: Docker**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

**Option 3: Cloud Platforms**
- AWS EC2
- Google Cloud Run
- Azure App Service
- Heroku

## 📊 Performance Optimization

### For Large Datasets (>100 assets)

1. **Enable Caching**
```python
@st.cache_data
def load_data(file):
    return pd.read_excel(file)
```

2. **Batch Processing**
- Process assets in batches
- Show progress bar
- Allow pause/resume

3. **Optimize Visualizations**
- Limit data points in charts
- Use sampling for large datasets
- Lazy loading for tabs

## 🔄 Updates and Maintenance

### Check for Updates
```bash
pip list --outdated
```

### Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Clear Cache
```bash
streamlit cache clear
```

## 📞 Support

### Getting Help
1. Check this guide first
2. Review error messages in terminal
3. Check Streamlit documentation: https://docs.streamlit.io
4. Review pipeline logs: `physrisk_pipeline.log`

### Common Commands
```bash
# Start app
streamlit run app.py

# Start with custom port
streamlit run app.py --server.port 8502

# Start with custom config
streamlit run app.py --server.headless true

# Clear cache
streamlit cache clear

# Check version
streamlit version
```

## 🎯 Advanced Features

### Integrate with LLM APIs

**OpenAI Integration:**
```python
import openai

def analyze_data_with_ai(question, data):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a climate risk analyst."},
            {"role": "user", "content": f"Data: {data}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content
```

**Anthropic Claude Integration:**
```python
import anthropic

def analyze_data_with_ai(question, data):
    client = anthropic.Anthropic(api_key="your-api-key")
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Data: {data}\n\nQuestion: {question}"}
        ]
    )
    return message.content
```

### Add Authentication

```python
import streamlit_authenticator as stauth

# Add to app.py
authenticator = stauth.Authenticate(
    credentials,
    'cookie_name',
    'signature_key',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show app
    main()
elif authentication_status == False:
    st.error('Username/password is incorrect')
```

### Add Database Integration

```python
import sqlite3

# Store results in database
def save_to_db(results):
    conn = sqlite3.connect('physrisk.db')
    results.to_sql('assessments', conn, if_exists='append')
    conn.close()
```

## 📈 Analytics and Monitoring

### Track Usage
```python
import logging

logging.basicConfig(
    filename='app_usage.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Log events
logging.info(f"File uploaded: {filename}")
logging.info(f"Assessment completed: {asset_count} assets")
```

### Performance Monitoring
```python
import time

start_time = time.time()
# Process data
elapsed = time.time() - start_time
st.info(f"Processing completed in {elapsed:.2f} seconds")
```

## 🎓 Learning Resources

### Streamlit
- Official Docs: https://docs.streamlit.io
- Gallery: https://streamlit.io/gallery
- Forum: https://discuss.streamlit.io

### Plotly
- Documentation: https://plotly.com/python/
- Examples: https://plotly.com/python/plotly-express/

### Best Practices
- Keep UI simple and intuitive
- Provide clear feedback
- Handle errors gracefully
- Optimize for performance
- Test with real data

---

## 🎉 You're Ready!

Start the app with:
```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

**Happy analyzing!** 🌍📊

---

**Version**: 1.0  
**Last Updated**: April 14, 2026  
**Author**: Bob