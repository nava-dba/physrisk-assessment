"""
PhysRisk Assessment Web Application

A Streamlit-based web interface for physical climate risk assessment
with file upload, data analysis, and AI chat capabilities.

Author: Bob
Date: 2026-04-14
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import json
from pathlib import Path
import sys

# Import our pipeline modules
from physrisk_pipeline_v2 import PhysRiskPipelineV2

# Page configuration
st.set_page_config(
    page_title="PhysRisk Assessment Tool",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .risk-high {
        color: #d32f2f;
        font-weight: bold;
    }
    .risk-medium {
        color: #ffa726;
        font-weight: bold;
    }
    .risk-low {
        color: #66bb6a;
        font-weight: bold;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'processed_results' not in st.session_state:
    st.session_state.processed_results = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False


def get_risk_color(score):
    """Return color based on risk score"""
    if score > 0.7:
        return "🔴", "risk-high"
    elif score > 0.4:
        return "🟡", "risk-medium"
    else:
        return "🟢", "risk-low"


def analyze_data_with_ai(question, data):
    """
    Analyze data and answer questions using AI
    This is a template - integrate with your preferred LLM API
    """
    # Simple rule-based responses for demonstration
    question_lower = question.lower()
    
    if not data:
        return "Please upload and process data first before asking questions."
    
    # Get summary statistics
    if 'summary' in st.session_state.processed_results:
        summary_df = st.session_state.processed_results['summary']
        
        if 'highest' in question_lower or 'top' in question_lower or 'most risk' in question_lower:
            top_assets = summary_df.nlargest(5, 'Avg_Risk_Score')
            response = "**Top 5 Highest-Risk Assets:**\n\n"
            for idx, row in top_assets.iterrows():
                emoji, _ = get_risk_color(row['Avg_Risk_Score'])
                response += f"{emoji} **{row['Asset']}** ({row['City']}, {row['State']}): Risk Score = {row['Avg_Risk_Score']:.3f}\n\n"
            return response
        
        elif 'lowest' in question_lower or 'safest' in question_lower or 'least risk' in question_lower:
            bottom_assets = summary_df.nsmallest(5, 'Avg_Risk_Score')
            response = "**Top 5 Lowest-Risk Assets:**\n\n"
            for idx, row in bottom_assets.iterrows():
                emoji, _ = get_risk_color(row['Avg_Risk_Score'])
                response += f"{emoji} **{row['Asset']}** ({row['City']}, {row['State']}): Risk Score = {row['Avg_Risk_Score']:.3f}\n\n"
            return response
        
        elif 'average' in question_lower or 'mean' in question_lower:
            avg_risk = summary_df['Avg_Risk_Score'].mean()
            high_count = len(summary_df[summary_df['Avg_Risk_Score'] > 0.7])
            medium_count = len(summary_df[(summary_df['Avg_Risk_Score'] >= 0.4) & (summary_df['Avg_Risk_Score'] <= 0.7)])
            low_count = len(summary_df[summary_df['Avg_Risk_Score'] < 0.4])
            
            response = f"""**Portfolio Risk Summary:**

📊 **Average Risk Score**: {avg_risk:.3f}

**Risk Distribution:**
- 🔴 High Risk (>0.7): {high_count} assets ({high_count/len(summary_df)*100:.1f}%)
- 🟡 Medium Risk (0.4-0.7): {medium_count} assets ({medium_count/len(summary_df)*100:.1f}%)
- 🟢 Low Risk (<0.4): {low_count} assets ({low_count/len(summary_df)*100:.1f}%)

Total Assets Analyzed: {len(summary_df)}
"""
            return response
        
        elif 'state' in question_lower:
            state_risk = summary_df.groupby('State')['Avg_Risk_Score'].agg(['mean', 'count']).sort_values('mean', ascending=False)
            response = "**Risk by State:**\n\n"
            for state, row in state_risk.head(10).iterrows():
                emoji, _ = get_risk_color(row['mean'])
                response += f"{emoji} **{state}**: Avg Risk = {row['mean']:.3f} | Assets = {int(row['count'])}\n\n"
            return response
        
        elif 'recommend' in question_lower or 'action' in question_lower or 'what should' in question_lower:
            high_risk_assets = summary_df[summary_df['Avg_Risk_Score'] > 0.7]
            response = f"""**Recommendations Based on Risk Analysis:**

🎯 **Immediate Actions Required:**

1. **High-Priority Assets** ({len(high_risk_assets)} locations):
   - Conduct detailed on-site assessments
   - Review and update insurance coverage
   - Develop site-specific mitigation plans

2. **Risk Mitigation Strategies:**
   - Infrastructure hardening for high-risk locations
   - Water management systems for water-stressed areas
   - Heat adaptation measures for temperature-vulnerable sites
   - Flood protection for precipitation-risk areas

3. **Monitoring & Reporting:**
   - Establish quarterly risk monitoring
   - Integrate into enterprise risk management
   - Track mitigation effectiveness

4. **Business Continuity:**
   - Update emergency response plans
   - Ensure backup systems for critical operations
   - Train staff on climate risk protocols

**Next Steps:**
- Prioritize top 10 highest-risk assets
- Allocate budget for mitigation measures
- Schedule follow-up assessments
"""
            return response
    
    # Default response
    return f"""I can help you analyze your climate risk data! Here are some questions you can ask:

📊 **Data Analysis:**
- "What are the highest-risk assets?"
- "Show me the lowest-risk locations"
- "What's the average risk score?"
- "Which states have the highest risk?"

💡 **Insights:**
- "What recommendations do you have?"
- "What actions should we take?"
- "Tell me about the risk distribution"

🔍 **Specific Queries:**
- "Show me assets in [state]"
- "What's the risk for [asset name]?"
- "Compare scenarios"

Try asking one of these questions!"""


def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-header">🌍 PhysRisk Climate Risk Assessment Tool</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Navigation")
        page = st.radio(
            "Select Page",
            ["🏠 Home", "📤 Upload & Process", "📊 Analysis Dashboard", "💬 Chat with Data", "📥 Download Results"]
        )
        
        st.markdown("---")
        st.header("ℹ️ About")
        st.info("""
        **PhysRisk Assessment Tool**
        
        Upload your asset data and get comprehensive climate risk assessments with:
        - Multi-scenario analysis
        - Risk scoring & ranking
        - Interactive visualizations
        - AI-powered chat interface
        
        Version 1.0
        """)
    
    # Main content based on selected page
    if page == "🏠 Home":
        show_home_page()
    elif page == "📤 Upload & Process":
        show_upload_page()
    elif page == "📊 Analysis Dashboard":
        show_dashboard_page()
    elif page == "💬 Chat with Data":
        show_chat_page()
    elif page == "📥 Download Results":
        show_download_page()


def show_home_page():
    """Home page"""
    st.header("Welcome to PhysRisk Assessment Tool")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📤 Upload Data
        Upload your Excel file with asset locations and get started with climate risk assessment.
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Analyze
        View comprehensive dashboards with risk scores, rankings, and visualizations.
        """)
    
    with col3:
        st.markdown("""
        ### 💬 Chat
        Ask questions about your data using our AI-powered chat interface.
        """)
    
    st.markdown("---")
    
    st.subheader("🚀 Quick Start Guide")
    st.markdown("""
    1. **Upload Your Data**: Go to "Upload & Process" and upload your Excel file
    2. **Process Assets**: Click "Run Risk Assessment" to analyze your locations
    3. **View Results**: Explore the Analysis Dashboard for insights
    4. **Ask Questions**: Use the Chat interface to interact with your data
    5. **Download**: Export your results in Excel format
    """)
    
    st.markdown("---")
    
    st.subheader("📋 Input File Requirements")
    st.markdown("""
    Your Excel file should contain a sheet named **"List assets"** with these columns:
    - IGS Office Name
    - IGS Office Address
    - City
    - State
    - Zip
    """)
    
    # Show example
    with st.expander("📄 View Example Input Format"):
        example_data = {
            'IGS Office Name': ['Office A', 'Office B', 'Office C'],
            'IGS Office Address': ['123 Main St', '456 Oak Ave', '789 Pine Rd'],
            'City': ['New York', 'Los Angeles', 'Chicago'],
            'State': ['NY', 'CA', 'IL'],
            'Zip': ['10001', '90001', '60601']
        }
        st.dataframe(pd.DataFrame(example_data))


def show_upload_page():
    """Upload and process page"""
    st.header("📤 Upload & Process Data")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload your Excel file",
        type=['xlsx', 'xls'],
        help="Upload an Excel file with asset locations"
    )
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            df = pd.read_excel(uploaded_file, sheet_name='List assets')
            st.session_state.uploaded_data = df
            
            st.success(f"✅ File uploaded successfully! Found {len(df)} assets.")
            
            # Show preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10))
            
            # Show statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Assets", len(df))
            with col2:
                st.metric("States", df['State'].nunique())
            with col3:
                st.metric("Cities", df['City'].nunique())
            
            st.markdown("---")
            
            # Process button
            if st.button("🚀 Run Risk Assessment", type="primary"):
                with st.spinner("Processing... This may take a few minutes..."):
                    # Save uploaded file temporarily
                    temp_input = "temp_input.xlsx"
                    temp_output = "temp_output.xlsx"
                    
                    df.to_excel(temp_input, sheet_name='List assets', index=False)
                    
                    # Run pipeline
                    try:
                        pipeline = PhysRiskPipelineV2(temp_input, temp_output)
                        pipeline.run()
                        
                        # Load results
                        results = {}
                        
                        # Get all sheet names
                        xl_file = pd.ExcelFile(temp_output)
                        available_sheets = xl_file.sheet_names
                        
                        # Load available sheets
                        for sheet_name in available_sheets:
                            try:
                                results[sheet_name] = pd.read_excel(temp_output, sheet_name=sheet_name)
                            except Exception as e:
                                st.warning(f"Could not load sheet '{sheet_name}': {e}")
                        
                        # Create summary if it doesn't exist
                        if 'Summary' not in results and 'Geocoded_Assets' in results:
                            # Create summary from scenario data
                            summary_data = []
                            for sheet_name in available_sheets:
                                if any(year in sheet_name for year in ['2030', '2040', '2050']):
                                    df_sheet = results[sheet_name]
                                    if 'Asset (IGS Office name)' in df_sheet.columns:
                                        for _, row in df_sheet.iterrows():
                                            summary_data.append({
                                                'Asset': row.get('Asset (IGS Office name)', ''),
                                                'City': row.get('City', ''),
                                                'State': row.get('State', ''),
                                                'Avg_Risk_Score': row.get('Overall Climate Impact Score', 0),
                                                'Max_Risk_Score': row.get('Overall Climate Impact Score', 0),
                                                'Min_Risk_Score': row.get('Overall Climate Impact Score', 0)
                                            })
                            
                            if summary_data:
                                summary_df = pd.DataFrame(summary_data)
                                # Aggregate by asset
                                results['summary'] = summary_df.groupby(['Asset', 'City', 'State']).agg({
                                    'Avg_Risk_Score': 'mean',
                                    'Max_Risk_Score': 'max',
                                    'Min_Risk_Score': 'min'
                                }).reset_index()
                        
                        # Ensure we have geocoded data
                        if 'geocoded' not in results and 'Geocoded_Assets' in results:
                            results['geocoded'] = results['Geocoded_Assets']
                        
                        st.session_state.processed_results = results
                        st.session_state.analysis_complete = True
                        
                        st.success("✅ Risk assessment completed successfully!")
                        st.balloons()
                        
                        # Clean up temp files
                        Path(temp_input).unlink(missing_ok=True)
                        
                    except Exception as e:
                        st.error(f"❌ Error during processing: {str(e)}")
                        st.info("Check the logs for more details.")
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.info("Please ensure your file has a sheet named 'List assets' with the required columns.")
    
    else:
        st.info("👆 Please upload an Excel file to get started.")


def show_dashboard_page():
    """Analysis dashboard page"""
    st.header("📊 Analysis Dashboard")
    
    if not st.session_state.analysis_complete:
        st.warning("⚠️ Please upload and process data first!")
        return
    
    results = st.session_state.processed_results
    
    # Check if summary exists
    if 'summary' not in results or results['summary'] is None:
        st.error("❌ Summary data not available. Please re-run the assessment.")
        return
    
    summary_df = results['summary']
    
    # Validate summary data
    if len(summary_df) == 0:
        st.warning("⚠️ No data available in summary. Please check your input file.")
        return
    
    # Key metrics
    st.subheader("🎯 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Assets", len(summary_df))
    
    with col2:
        avg_risk = summary_df['Avg_Risk_Score'].mean()
        emoji, css_class = get_risk_color(avg_risk)
        st.metric("Avg Risk Score", f"{avg_risk:.3f} {emoji}")
    
    with col3:
        high_risk_count = len(summary_df[summary_df['Avg_Risk_Score'] > 0.7])
        st.metric("High Risk Assets", high_risk_count)
    
    with col4:
        max_risk = summary_df['Max_Risk_Score'].max()
        st.metric("Max Risk Score", f"{max_risk:.3f}")
    
    st.markdown("---")
    
    # Visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Risk Distribution", "🗺️ Geographic View", "📈 Top Assets", "⏱️ Time Evolution"])
    
    with tab1:
        st.subheader("Risk Distribution")
        
        # Pie chart
        high_risk = len(summary_df[summary_df['Avg_Risk_Score'] > 0.7])
        medium_risk = len(summary_df[(summary_df['Avg_Risk_Score'] >= 0.4) & (summary_df['Avg_Risk_Score'] <= 0.7)])
        low_risk = len(summary_df[summary_df['Avg_Risk_Score'] < 0.4])
        
        fig = go.Figure(data=[go.Pie(
            labels=['High Risk', 'Medium Risk', 'Low Risk'],
            values=[high_risk, medium_risk, low_risk],
            marker=dict(colors=['#d32f2f', '#ffa726', '#66bb6a']),
            hole=0.3
        )])
        fig.update_layout(title="Portfolio Risk Distribution")
        st.plotly_chart(fig, width='stretch')
        
        # Histogram
        fig2 = px.histogram(summary_df, x='Avg_Risk_Score', nbins=20,
                           title="Risk Score Distribution",
                           labels={'Avg_Risk_Score': 'Average Risk Score'})
        st.plotly_chart(fig2, width='stretch')
    
    with tab2:
        st.subheader("Geographic Distribution")
        
        # State-level analysis
        state_risk = summary_df.groupby('State')['Avg_Risk_Score'].mean().sort_values(ascending=False)
        
        fig = px.bar(x=state_risk.index, y=state_risk.values,
                    title="Average Risk by State",
                    labels={'x': 'State', 'y': 'Average Risk Score'},
                    color=state_risk.values,
                    color_continuous_scale=['green', 'yellow', 'red'])
        st.plotly_chart(fig, width='stretch')
        
        # Map (if geocoded data available)
        if 'geocoded' in results:
            geocoded_df = results['geocoded']
            if 'Latitude' in geocoded_df.columns and 'Longitude' in geocoded_df.columns:
                # Merge with summary for risk scores
                map_df = geocoded_df.merge(summary_df, left_on='IGS Office Name', right_on='Asset', how='left', suffixes=('', '_summary'))
                map_df = map_df.dropna(subset=['Latitude', 'Longitude'])
                
                # Clean up column names for hover data
                hover_cols = []
                if 'City' in map_df.columns:
                    hover_cols.append('City')
                elif 'City_summary' in map_df.columns:
                    map_df['City'] = map_df['City_summary']
                    hover_cols.append('City')
                
                if 'State' in map_df.columns:
                    hover_cols.append('State')
                elif 'State_summary' in map_df.columns:
                    map_df['State'] = map_df['State_summary']
                    hover_cols.append('State')
                
                if 'Avg_Risk_Score' in map_df.columns:
                    hover_cols.append('Avg_Risk_Score')
                
                if len(map_df) > 0 and 'Avg_Risk_Score' in map_df.columns:
                    fig = px.scatter_map(
                        map_df,
                        lat='Latitude',
                        lon='Longitude',
                        hover_name='IGS Office Name',
                        hover_data=hover_cols if hover_cols else None,
                        color='Avg_Risk_Score',
                        size='Avg_Risk_Score',
                        color_continuous_scale=['green', 'yellow', 'red'],
                        zoom=3,
                        height=500
                    )
                    st.plotly_chart(fig, width='stretch')
    
    with tab3:
        st.subheader("Top 10 Highest-Risk Assets")
        
        top10 = summary_df.nlargest(10, 'Avg_Risk_Score')
        
        fig = px.bar(top10, x='Avg_Risk_Score', y='Asset',
                    orientation='h',
                    title="Top 10 Highest-Risk Assets",
                    color='Avg_Risk_Score',
                    color_continuous_scale=['yellow', 'red'])
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, width='stretch')
        
        # Table
        st.dataframe(
            top10[['Asset', 'City', 'State', 'Avg_Risk_Score', 'Max_Risk_Score']],
            width='stretch'
        )
    
    with tab4:
        st.subheader("Risk Evolution Over Time")
        
        # Get data for different years
        evolution_data = []
        for scenario in ['SSP1-2.6', 'SSP5-8.5']:
            for year in [2030, 2040, 2050]:
                sheet_name = f"{scenario} {year}"
                if sheet_name in results:
                    df_year = results[sheet_name]
                    if 'Overall Climate Impact Score' in df_year.columns:
                        avg_score = df_year['Overall Climate Impact Score'].mean()
                        evolution_data.append({
                            'Scenario': scenario,
                            'Year': year,
                            'Average Risk Score': avg_score
                        })
        
        if evolution_data:
            evolution_df = pd.DataFrame(evolution_data)
            fig = px.line(evolution_df, x='Year', y='Average Risk Score',
                         color='Scenario',
                         title="Portfolio Risk Evolution Over Time",
                         markers=True)
            st.plotly_chart(fig, width='stretch')


def show_chat_page():
    """Chat interface page"""
    st.header("💬 Chat with Your Data")
    
    if not st.session_state.analysis_complete:
        st.warning("⚠️ Please upload and process data first!")
        return
    
    st.markdown("""
    Ask questions about your climate risk data! Examples:
    - "What are the highest-risk assets?"
    - "Show me the average risk score"
    - "Which states have the most risk?"
    - "What recommendations do you have?"
    """)
    
    # Chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="chat-message user-message">👤 **You:** {message["content"]}</div>', 
                          unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message">🤖 **Assistant:** {message["content"]}</div>', 
                          unsafe_allow_html=True)
    
    # Chat input
    user_question = st.text_input("Ask a question:", key="chat_input")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Send", type="primary"):
            if user_question:
                # Add user message
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_question
                })
                
                # Get AI response
                response = analyze_data_with_ai(user_question, st.session_state.processed_results)
                
                # Add assistant message
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
                
                st.rerun()
    
    with col2:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()


def show_download_page():
    """Download results page"""
    st.header("📥 Download Results")
    
    if not st.session_state.analysis_complete:
        st.warning("⚠️ Please upload and process data first!")
        return
    
    st.subheader("Available Downloads")
    
    # Excel report
    if Path("temp_output.xlsx").exists():
        with open("temp_output.xlsx", "rb") as file:
            st.download_button(
                label="📊 Download Full Excel Report",
                data=file,
                file_name=f"PhysRisk_Assessment_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    # Summary CSV
    if st.session_state.processed_results and 'summary' in st.session_state.processed_results:
        summary_df = st.session_state.processed_results['summary']
        csv = summary_df.to_csv(index=False)
        st.download_button(
            label="📄 Download Summary (CSV)",
            data=csv,
            file_name=f"Risk_Summary_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    st.markdown("---")
    st.info("💡 Tip: Use the Excel report for detailed analysis and the CSV for quick data import into other tools.")


if __name__ == "__main__":
    main()

# Made with Bob
