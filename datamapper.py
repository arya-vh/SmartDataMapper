import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataQualityGuardian:
    def __init__(self):
        self.start_time = datetime.now()
        self.quality_report = {}
    
    def analyze_data_quality(self, raw_df, ref_df, raw_col, ref_col):
        """AI-Powered Data Quality Analysis"""
        print("🔍 Running Data Quality Guardian...")
        
        # 1. CLEANING ANALYSIS
        raw_dirty = raw_df[raw_col].astype(str).str.strip()
        ref_dirty = ref_df[ref_col].astype(str).str.strip()
        
        self.quality_report['before_clean'] = {
            'raw_nulls': raw_df[raw_col].isna().sum(),
            'raw_duplicates': raw_df[raw_col].duplicated().sum(),
            'ref_nulls': ref_df[ref_col].isna().sum()
        }
        
        # 2. SMART CLEANING
        raw_clean = raw_dirty.str.lower().str.replace(r'[^a-z0-9]', '', regex=True)
        ref_clean = ref_dirty.str.lower().str.replace(r'[^a-z0-9]', '', regex=True)
        
        # 3. FUZZY + EXACT MATCHING (Levenshtein distance)
        exact_matches = ref_df[raw_dirty.isin(ref_dirty)].copy()
        exact_matches['_match_confidence'] = 1.00
        exact_matches['_match_type'] = 'EXACT'
        
        fuzzy_matches = self.fuzzy_matching(raw_clean, ref_clean, ref_df, threshold=0.85)
        
        final_matches = pd.concat([exact_matches, fuzzy_matches], ignore_index=True)
        final_matches.drop_duplicates(subset=[ref_col], inplace=True)
        
        # 4. QUALITY METRICS
        self.quality_report['results'] = {
            'exact_matches': len(exact_matches),
            'fuzzy_matches': len(fuzzy_matches),
            'total_matches': len(final_matches),
            'match_rate': f"{len(final_matches)/len(raw_df)*100:.1f}%"
        }
        
        return final_matches
    
    def fuzzy_matching(self, raw_clean, ref_clean, ref_df, threshold=0.85):
        from rapidfuzz import fuzz
        
        fuzzy_results = []
        # FIX: Only process UNIQUE raw values (not 100x duplicates)
        unique_raw = raw_clean.drop_duplicates().dropna()
        
        for raw_val in unique_raw:
            best_score = 0
            best_match = None
            
            for ref_val in ref_clean:
                score = fuzz.ratio(raw_val, ref_val) / 100.0
                if score > best_score and score >= threshold:
                    best_score = score
                    best_match = ref_val
                    
            if best_match:
                matched_row = ref_df[ref_clean == best_match].iloc[0].copy()
                matched_row['_match_confidence'] = best_score
                matched_row['_match_type'] = 'FUZZY'
                fuzzy_results.append(matched_row)
                
        return pd.DataFrame(fuzzy_results)
    
    def generate_executive_dashboard(self, final_matches):
        """STUNNING Professional Dashboard - Fixed empty confidence + Beautiful design"""
        print("✨ Creating EXECUTIVE dashboard...")
        
        # Fix: Always create data even for exact matches
        if '_match_confidence' not in final_matches.columns:
            final_matches['_match_confidence'] = 1.00
            final_matches['_match_type'] = 'EXACT'
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('🎯 Match Success Rate', '📊 Match Types', '⭐ Confidence Distribution', '⚡ Performance Timeline'),
            specs=[[{"type": "pie"}, {"type": "bar"}], 
                   [{"type": "histogram"}, {"type": "indicator"}]],
            horizontal_spacing=0.05,
            vertical_spacing=0.1
        )
        
        # 1. GORGEOUS PIE CHART (Top Left)
        fig.add_trace(go.Pie(
            values=[self.quality_report['results']['exact_matches'], 
                    self.quality_report['results']['fuzzy_matches']],
            labels=['✅ Exact Matches', '🤖 AI Fuzzy Matches'],
            marker_colors=['#10B981', '#3B82F6'],
            textinfo='label+percent',
            textposition='inside',
            showlegend=False
        ), row=1, col=1)
        
        # 2. Match Types Bar (Top Right)  
        fig.add_trace(go.Bar(
            x=['Exact', 'Fuzzy AI'],
            y=[self.quality_report['results']['exact_matches'], 
               self.quality_report['results']['fuzzy_matches']],
            marker_color=['#10B981', '#3B82F6'],
            text=[f'{x}' for x in [self.quality_report['results']['exact_matches'], 
                                  self.quality_report['results']['fuzzy_matches']]],
            textposition='auto'
        ), row=1, col=2)
        
        # 3. FIXED Confidence Histogram (Bottom Left) - NOW HAS DATA!
        fig.add_trace(go.Histogram(
            x=final_matches['_match_confidence'],
            nbinsx=10,
            marker_color='#F59E0B',
            name="Confidence",
            opacity=0.7
        ), row=2, col=1)
        
        # 4. Performance Indicator (Bottom Right)
        match_rate = self.quality_report['results']['match_rate'].rstrip('%')
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=float(match_rate),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Match Success"},
            delta={'reference': 90, 'increasing': {'color': "RebeccaPurple"}},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#10B981"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"}, 
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': float(match_rate)
                }
            }
        ), row=2, col=2)
        
        # STUNNING THEME
        fig.update_layout(
            height=700,
            width=1200,
            title={
                'text': f"🚀 Data Quality Guardian - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                'x': 0.5,
                'font': {'size': 24, 'color': '#1F2937'}
            },
            paper_bgcolor='#F9FAFB',
            plot_bgcolor='#FFFFFF',
            font=dict(size=12, color='#374151'),
            showlegend=False
        )
        
        # Auto-open in browser
        fig.write_html("data_quality_dashboard.html")
        import webbrowser
        import os
        webbrowser.open_new_tab(f'file://{os.path.realpath("data_quality_dashboard.html")}')
        print("🌐 🎨 STUNNING dashboard opened automatically!")
    
    def run_full_pipeline(self, raw_col='lookup_key', ref_col='lookup_key'):
        print("🚀 Data Quality Guardian v2.0 Starting...")
        
        # Load data
        raw_df = pd.read_csv('raw_data.csv')
        ref_df = pd.read_excel('reference_data.xlsx')
        
        print(f"📊 Raw: {len(raw_df)} rows | Ref: {len(ref_df)} rows")
        
        # Run analysis
        final_matches = self.analyze_data_quality(raw_df, ref_df, raw_col, ref_col)
        
        # Save results
        final_matches.to_csv('mapped_output_enhanced.csv', index=False)
        pd.DataFrame([self.quality_report]).to_csv('quality_report.csv', index=False)
        
        # Generate dashboard
        self.generate_executive_dashboard(final_matches)
        
        # Final report
        print(f"\n🎉 PIPELINE COMPLETE!")
        print(f"✅ Enhanced output: mapped_output_enhanced.csv ({len(final_matches)} rows)")
        print(f"📊 Dashboard: data_quality_dashboard.html")
        print(f"📈 Match rate: {self.quality_report['results']['match_rate']}")
        print(f"⏱️  Total time: {(datetime.now() - self.start_time).total_seconds():.1f}s")

if __name__ == "__main__":
    guardian = DataQualityGuardian()
    guardian.run_full_pipeline()
