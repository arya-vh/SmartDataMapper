import pandas as pd
import re
from datetime import datetime

def generate_unmatched_report():
    """DETAILED Unmatched Analysis + INTERACTIVE AUTO-FIX"""
    print("Unmatched Analysis Report")
    print("=" * 70)
    
    # Load data
    raw_df = pd.read_csv('raw_data.csv')
    ref_df = pd.read_excel('reference_data.xlsx')
    
    raw_keys = raw_df['lookup_key'].drop_duplicates()
    ref_keys = ref_df['lookup_key'].drop_duplicates()
    unmatched = raw_keys[~raw_keys.isin(ref_keys)]
    
    print(f"Summary:")
    print(f"   Raw keys: {len(raw_keys)}")
    print(f"   Ref keys: {len(ref_keys)}")
    print(f"   Unmatched: {len(unmatched)} ({len(unmatched)/len(raw_keys)*100:.1f}%)")
    
    # Pattern detection
    print(f"\nPattern Analysis:")
    patterns = {}
    for key in unmatched:
        # Extract prefix + numbers (MN130 → MN + 130)
        match = re.match(r'([A-Z]+)(\d+)', str(key))
        if match:
            prefix = match.group(1)
            patterns[prefix] = patterns.get(prefix, 0) + 1
    
    for prefix, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
        print(f"  '{prefix}###': {count} keys")
    
    # Auto fix options
    if len(unmatched) > 0:
        print(f"\nAuto-Fix Options:")
        print(f"   Add top {min(10, len(patterns))} patterns to reference?")
        choice = input("   Generate auto-fixed reference? (y/n): ").lower().strip()
        
        if choice in ['y', 'yes']:
            auto_fix_reference(unmatched, patterns)
        else:
            print("   Skipped auto-fix")
    
    print(f"\nSaving Detailed Report...")
    
    # Detailed CSV
    report = pd.DataFrame({
        'unmatched_key': unmatched,
        'length': unmatched.str.len(),
        'has_numbers': unmatched.str.contains(r'\d', regex=True),
        'pattern': [re.match(r'([A-Z]+)', str(x)).group(1) if re.match(r'([A-Z]+)', str(x)) else 'OTHER' for x in unmatched],
        'suggestion': 'ADD_TO_REFERENCE'
    })
    
    report.to_csv('unmatched_analysis.csv', index=False)
    
    coverage = pd.DataFrame({
        'total_raw_keys': [len(raw_keys)],
        'reference_coverage': [f"{len(ref_keys)/len(raw_keys)*100:.1f}%"],
        'missing_keys': [len(unmatched)],
        'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M')]
    })
    coverage.to_csv('reference_coverage.csv', index=False)
    
    print("Saved Files:")
    print("   • unmatched_analysis.csv")
    print("   • reference_coverage.csv")
    print(f"   • {len(unmatched)} unmatched keys documented!")

def auto_fix_reference(unmatched, patterns):
    """ Generate AUTO-FIXED reference file"""
    print("Creating AUTO-FIXED reference...")
    
    # Create template rows for top patterns
    fix_rows = []
    top_prefixes = sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for prefix, count in top_prefixes:
        sample_keys = unmatched[unmatched.str.match(f'^{prefix}')].head(3)
        for key in sample_keys:
            fix_rows.append({
                'lookup_key': key,
                'description': f'AUTO-ADDED: {prefix} pattern ({patterns[prefix]} total)',
                'status': 'PENDING_REVIEW'
            })
    
    fix_df = pd.DataFrame(fix_rows)
    
    # Save new reference
    fix_df.to_excel('reference_data_auto_fixed.xlsx', index=False)
    print(f"AUTO-FIXED reference created:")
    print(f"   • reference_data_auto_fixed.xlsx ({len(fix_rows)} rows)")
    print(f"   • Top patterns: {', '.join([f'{p[0]} ({p[1]})' for p in top_prefixes])}")
    
    # Show preview
    print("\nPreview (first 5 auto-fixed rows):")
    print(fix_df[['lookup_key', 'description', 'status']].head())

if __name__ == "__main__":
    generate_unmatched_report()

