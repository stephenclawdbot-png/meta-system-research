#!/usr/bin/env python3
"""
JLCPCB Order Automation Script for SILENT-001
Generates JLCPCB-compatible order JSON and validates BOM/CPL files.
"""

import csv
import json
import zipfile
import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class JLCPCBOrderGenerator:
    """Generates JLCPCB order files and validates manufacturing data."""
    
    # JLCPCB Part Categories and LCSC Part Number patterns
    JLCPCB_BASIC_PARTS_URL = "https://jlcpcb.com/partdetail/"
    
    # Components excluded from JLCPCB assembly (through-hole, user-supplied)
    NON_SMT_COMPONENTS = ['J1', 'J2', 'J3', 'J4', 'J5', 'TP1', 'TP2']
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.production_path = self.project_path / "production"
        self.bom_data: List[Dict] = []
        self.cpl_data: List[Dict] = []
        self.digikey_parts: List[Dict] = []
        
    def load_bom(self) -> bool:
        """Load and validate the JLCPCB BOM file."""
        bom_path = self.production_path / "SILENT-001_BOM_JLCPCB.csv"
        
        if not bom_path.exists():
            print(f"❌ Error: BOM file not found at {bom_path}")
            return False
            
        try:
            with open(bom_path, 'r') as f:
                reader = csv.DictReader(f)
                self.bom_data = list(reader)
            
            print(f"✅ Loaded BOM: {len(self.bom_data)} components")
            
            # Validate LCSC part numbers
            missing_lcsc = [row for row in self.bom_data if not row.get('LCSC')]
            if missing_lcsc:
                print(f"⚠️  Warning: {len(missing_lcsc)} components missing LCSC part numbers")
                for comp in missing_lcsc[:5]:
                    print(f"   - {comp.get('Designator', 'Unknown')}: {comp.get('Val', 'N/A')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading BOM: {e}")
            return False
    
    def load_cpl(self) -> bool:
        """Load and validate the Component Placement List (CPL)."""
        cpl_path = self.production_path / "SILENT-001_CPL_JLCPCB.csv"
        
        if not cpl_path.exists():
            print(f"❌ Error: CPL file not found at {cpl_path}")
            return False
            
        try:
            with open(cpl_path, 'r') as f:
                reader = csv.DictReader(f)
                self.cpl_data = list(reader)
            
            print(f"✅ Loaded CPL: {len(self.cpl_data)} placements")
            
            # Validate placements
            top_count = sum(1 for row in self.cpl_data if row.get('Layer') == 'Top')
            bottom_count = sum(1 for row in self.cpl_data if row.get('Layer') == 'Bottom')
            print(f"   - Top side: {top_count} placements")
            print(f"   - Bottom side: {bottom_count} placements")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading CPL: {e}")
            return False
    
    def load_full_bom(self) -> bool:
        """Load the full BOM with Digi-Key part numbers."""
        bom_path = self.production_path / "SILENT-001_BOM_Full.csv"
        
        if not bom_path.exists():
            print(f"⚠️  Full BOM not found, skipping Digi-Key sourcing")
            return False
            
        try:
            with open(bom_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            # Filter for Digi-Key only parts (non-SMT connectors)
            self.digikey_parts = [
                row for row in rows 
                if row.get('Digi-Key Part Number') and 
                any(ref in row.get('Reference Designator', '') for ref in self.NON_SMT_COMPONENTS)
            ]
            
            print(f"✅ Loaded Digi-Key sourcing list: {len(self.digikey_parts)} parts")
            return True
            
        except Exception as e:
            print(f"⚠️  Error loading full BOM: {e}")
            return False
    
    def verify_gerbers(self) -> Tuple[bool, Dict]:
        """Verify Gerber archive integrity and contents."""
        gerber_zip = self.production_path / "gerbers" / "SILENT-001_Gerbers.zip"
        
        if not gerber_zip.exists():
            print(f"❌ Error: Gerber ZIP not found at {gerber_zip}")
            return False, {}
        
        # Required Gerber layers for 4-layer PCB
        required_layers = [
            ('GTL', 'Top Copper'),
            ('G1', 'Internal Layer 1'),
            ('G2', 'Internal Layer 2'),
            ('GBL', 'Bottom Copper'),
            ('GTS', 'Top Soldermask'),
            ('GBS', 'Bottom Soldermask'),
            ('GTO', 'Top Silkscreen'),
            ('GBO', 'Bottom Silkscreen'),
            ('GTP', 'Top Paste'),
            ('GM1', 'Edge Cuts'),
            ('drl', 'Drill file')
        ]
        
        try:
            with zipfile.ZipFile(gerber_zip, 'r') as zf:
                files = zf.namelist()
                found_layers = []
                missing_layers = []
                
                for ext, desc in required_layers:
                    matching = [f for f in files if ext.lower() in f.lower()]
                    if matching:
                        found_layers.append((ext, desc, matching[0]))
                    else:
                        missing_layers.append((ext, desc))
                
                # Calculate file hash for integrity
                with open(gerber_zip, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()[:16]
                
                result = {
                    'filename': gerber_zip.name,
                    'path': str(gerber_zip),
                    'size_kb': round(os.path.getsize(gerber_zip) / 1024, 2),
                    'found_layers': found_layers,
                    'missing_layers': missing_layers,
                    'hash': file_hash,
                    'file_count': len(files)
                }
                
                if missing_layers:
                    print(f"⚠️  Missing layers: {[m[0] for m in missing_layers]}")
                    return False, result
                
                print(f"✅ Gerber archive verified: {len(found_layers)} layers")
                return True, result
                
        except Exception as e:
            print(f"❌ Error verifying gerbers: {e}")
            return False, {}
    
    def generate_order_json(self, quantity: int = 10) -> Dict:
        """Generate JLCPCB-compatible order JSON."""
        order_data = {
            "order_info": {
                "project_name": "SILENT-001 Subvocalization Interface",
                "project_id": "SILENT-001",
                "revision": "1.0",
                "created_at": datetime.now().isoformat(),
                "quantity": quantity,
                "customer_reference": f"SILENT-001-{datetime.now().strftime('%Y%m%d')}"
            },
            "pcb_specifications": {
                "board_name": "SILENT-001",
                "dimensions": "50mm x 35mm",
                "layer_count": 4,
                "thickness_mm": 1.6,
                "surface_finish": "ENIG",
                "copper_weight_oz": 1,
                "solder_mask_color": "Green",
                "silkscreen_color": "White",
                "material": "FR-4 TG155-160",
                "min_trace_mils": 6,
                "min_via_mils": 12,
                "impedance_control": False,
                "via_covering": "Tented"
            },
            "assembly_specifications": {
                "assembly_service": True,
                "assembly_side": "Top",
                "unique_component_count": len(self.bom_data),
                "total_placement_count": len(self.cpl_data),
                "supply_parts": "JLCPCB SMT Parts Library (Basic + Extended)"
            },
            "files": {
                "gerber_zip": "production/gerbers/SILENT-001_Gerbers.zip",
                "bom_csv": "production/SILENT-001_BOM_JLCPCB.csv",
                "cpl_csv": "production/SILENT-001_CPL_JLCPCB.csv"
            },
            "component_summary": {
                "total_components": len(self.bom_data),
                "jlcpcb_smt": len(self.bom_data) - len([c for c in self.bom_data 
                    if any(ns in c.get('Designator', '') for ns in self.NON_SMT_COMPONENTS)]),
                "user_assembly": len([c for c in self.bom_data 
                    if any(ns in c.get('Designator', '') for ns in self.NON_SMT_COMPONENTS)]),
                "digikey_required": len(self.digikey_parts)
            },
            "cost_estimate": {
                "pcb_fabrication_usd": round(quantity * 2.00, 2),  # ~$2/pc for qty 10
                "assembly_usd": round(quantity * 5.50, 2),  # ~$5.50/pc
                "components_usd": 32.00,  # Approximate component cost
                "shipping_usd": 20.00,  # DHL estimate
                "total_estimate_usd": round(quantity * 7.50 + 52.00, 2)
            },
            "digikey_supplement": {
                "note": "Through-hole connectors and test points for user assembly",
                "parts": [
                    {
                        "designator": row.get('Reference Designator', ''),
                        "part_number": row.get('Digi-Key Part Number', ''),
                        "manufacturer": row.get('Manufacturer', ''),
                        "description": row.get('Description', ''),
                        "quantity": int(row.get('Qty', 1)) if row.get('Qty') else 1
                    }
                    for row in self.digikey_parts
                ]
            },
            "assembly_notes": [
                "USB-C Connector (U13): Mid-mount SMD, verify orientation",
                "Crystal (U15): Placed on bottom layer, verify placement",
                "Headers (J1-J5): Through-hole, user assembly required",
                "Test Points (TP1-TP2): SMD test points, user assembly required",
                "Clean PCB with IPA before assembly",
                "Recommended: Order 10-20% extra for testing/rework"
            ]
        }
        
        return order_data
    
    def save_order_json(self, order_data: Dict, output_path: Optional[str] = None):
        """Save order JSON to file."""
        if output_path is None:
            output_path = self.project_path / "procurement" / "jlcpcb_order.json"
        else:
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(order_data, f, indent=2)
        
        print(f"✅ Order JSON saved: {output_path}")
        return output_path
    
    def validate_order(self) -> bool:
        """Run full validation on order package."""
        print("\n" + "="*60)
        print("SILENT-001 JLCPCB Order Validation")
        print("="*60)
        
        all_valid = True
        
        # Check BOM
        if not self.load_bom():
            all_valid = False
        
        # Check CPL
        if not self.load_cpl():
            all_valid = False
        
        # Check Digi-Key parts
        self.load_full_bom()
        
        # Check Gerbers
        gerber_ok, _ = self.verify_gerbers()
        if not gerber_ok:
            all_valid = False
        
        # Cross-reference BOM and CPL
        bom_designators = {row['Designator'] for row in self.bom_data}
        cpl_designators = {row['Designator'] for row in self.cpl_data}
        
        missing_in_cpl = bom_designators - cpl_designators
        extra_in_cpl = cpl_designators - bom_designators
        
        if missing_in_cpl:
            print(f"⚠️  Designators in BOM but not in CPL: {missing_in_cpl}")
        
        if extra_in_cpl:
            print(f"⚠️  Designators in CPL but not in BOM: {extra_in_cpl}")
        
        if not missing_in_cpl and not extra_in_cpl:
            print("✅ BOM/CPL cross-reference: MATCHED")
        
        print("\n" + "="*60)
        if all_valid:
            print("✅ Order package validation: PASSED")
        else:
            print("❌ Order package validation: FAILED")
        print("="*60)
        
        return all_valid
    
    def generate_html_summary(self, output_path: Optional[str] = None):
        """Generate HTML summary for easy viewing."""
        if output_path is None:
            output_path = self.project_path / "procurement" / "order_summary.html"
        else:
            output_path = Path(output_path)
        
        order_data = self.generate_order_json()
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>SILENT-001 JLCPCB Order Summary</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; background: #f5f5f5; }}
        .card {{ background: white; border-radius: 8px; padding: 24px; margin: 16px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a1a1a; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #333; margin-top: 24px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
        th {{ background: #4CAF50; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f9f9f9; }}
        .status-ok {{ color: #4CAF50; font-weight: bold; }}
        .status-warn {{ color: #FF9800; font-weight: bold; }}
        .cost {{ font-size: 1.3em; color: #2196F3; font-weight: bold; }}
        .note {{ background: #fff3cd; padding: 12px; border-radius: 4px; margin: 8px 0; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🔇 SILENT-001 Subvocalization Interface</h1>
        <p><strong>JLCPCB Order Package</strong> | Generated: {order_data['order_info']['created_at']}</p>
    </div>
    
    <div class="card">
        <h2>📋 PCB Specifications</h2>
        <table>
            <tr><td>Dimensions</td><td>{order_data['pcb_specifications']['dimensions']}</td></tr>
            <tr><td>Layer Count</td><td>{order_data['pcb_specifications']['layer_count']}-layer</td></tr>
            <tr><td>Thickness</td><td>{order_data['pcb_specifications']['thickness_mm']}mm</td></tr>
            <tr><td>Surface Finish</td><td>{order_data['pcb_specifications']['surface_finish']}</td></tr>
            <tr><td>Solder Mask</td><td>{order_data['pcb_specifications']['solder_mask_color']}</td></tr>
        </table>
    </div>
    
    <div class="card">
        <h2>🔧 Assembly Summary</h2>
        <table>
            <tr><td>Unique Components</td><td>{order_data['component_summary']['total_components']}</td></tr>
            <tr><td>JLCPCB SMT</td><td>{order_data['component_summary']['jlcpcb_smt']}</td></tr>
            <tr><td>User Assembly Required</td><td>{order_data['component_summary']['user_assembly']}</td></tr>
            <tr><td>Digi-Key Supplement</td><td>{order_data['component_summary']['digikey_required']} parts</td></tr>
        </table>
    </div>
    
    <div class="card">
        <h2>💰 Cost Estimate (Qty {order_data['order_info']['quantity']})</h2>
        <table>
            <tr><td>PCB Fabrication</td><td>${order_data['cost_estimate']['pcb_fabrication_usd']}</td></tr>
            <tr><td>Assembly Labor</td><td>${order_data['cost_estimate']['assembly_usd']}</td></tr>
            <tr><td>Component Cost</td><td>${order_data['cost_estimate']['components_usd']}</td></tr>
            <tr><td>Shipping (DHL)</td><td>${order_data['cost_estimate']['shipping_usd']}</td></tr>
            <tr style="font-weight: bold; background: #e3f2fd;">
                <td>Total Estimate</td><td class="cost">${order_data['cost_estimate']['total_estimate_usd']}</td>
            </tr>
        </table>
    </div>
    
    <div class="card">
        <h2>⚠️ Assembly Notes</h2>
        {''.join(f'<div class="note">{note}</div>' for note in order_data['assembly_notes'])}
    </div>
    
    <div class="card">
        <h2>📦 Order Files</h2>
        <table>
            <tr><th>File</th><th>Path</th></tr>
            <tr><td>Gerber Archive</td><td><code>{order_data['files']['gerber_zip']}</code></td></tr>
            <tr><td>BOM</td><td><code>{order_data['files']['bom_csv']}</code></td></tr>
            <tr><td>CPL</td><td><code>{order_data['files']['cpl_csv']}</code></td></tr>
        </table>
    </div>
    
    <div class="card" style="text-align: center; color: #666;">
        <p>SILENT-001 Hardware Prototype | OpenClaw Labs</p>
    </div>
</body>
</html>"""
        
        with open(output_path, 'w') as f:
            f.write(html)
        
        print(f"✅ HTML summary saved: {output_path}")
        return output_path


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='JLCPCB Order Generator for SILENT-001')
    parser.add_argument('--project-path', default='.', help='Path to SILENT-001 project')
    parser.add_argument('--quantity', type=int, default=10, help='Order quantity')
    parser.add_argument('--validate', action='store_true', help='Run validation only')
    parser.add_argument('--generate', action='store_true', help='Generate order files')
    parser.add_argument('--output-dir', default='procurement', help='Output directory')
    
    args = parser.parse_args()
    
    # Resolve project path
    project_path = Path(args.project_path).resolve()
    
    if not project_path.exists():
        print(f"❌ Project path not found: {project_path}")
        return 1
    
    generator = JLCPCBOrderGenerator(project_path)
    
    if args.validate or not args.generate:
        # Run validation
        if not generator.validate_order():
            print("\n❌ Validation failed. Please fix issues before ordering.")
            return 1
    
    if args.generate:
        # Generate order JSON
        order_data = generator.generate_order_json(quantity=args.quantity)
        json_path = generator.save_order_json(
            order_data, 
            output_path=project_path / args.output_dir / "jlcpcb_order.json"
        )
        
        # Generate HTML summary
        html_path = generator.generate_html_summary(
            output_path=project_path / args.output_dir / "order_summary.html"
        )
        
        print(f"\n📦 Order package generated:")
        print(f"   JSON: {json_path}")
        print(f"   HTML: {html_path}")
        print(f"\n🚀 Ready to order at https://jlcpcb.com")
    
    return 0


if __name__ == "__main__":
    exit(main())
