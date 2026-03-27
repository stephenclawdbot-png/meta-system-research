#!/usr/bin/env python3
"""
SILENT-001 Subvocalization Interface - BOM Cart Generator
Generates Digi-Key/JLCPCB cart URLs from BOM data
"""

import json
import urllib.parse
import urllib.request
import ssl
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# BOM Definition for SILENT-001
BOM = {
    "project": "SILENT-001",
    "version": "1.0.0",
    "currency": "USD",
    "total_budget": 140.00,
    "items": [
        # Critical Components
        {
            "line": 1,
            "qty": 2,
            "mpn": "AS3932-BTST",
            "manufacturer": "ams OSRAM",
            "description": "3D Low Frequency Wake-Up Receiver",
            "category": "critical",
            "unit_price": 4.85,
            "digikey": {
                "pn": "AS3932-BTSTCT-ND",
                "url": "https://www.digikey.com/en/products/detail/ams-osram/AS3932-BTST/",
                "stock_check_url": "https://www.digikey.com/en/products/detail/ams-osram/AS3932-BTST/"
            },
            "mouser": {
                "pn": "985-AS3932-BTST",
                "url": "https://www.mouser.com/ProductDetail/ams-OSRAM/AS3932-BTST/"
            }
        },
        {
            "line": 2,
            "qty": 1,
            "mpn": "BH01B",
            "manufacturer": "DigiKey / Bone Conduction",
            "description": "Bone Conduction Transducer 28mm 8Ohm",
            "category": "critical",
            "unit_price": 12.50,
            "digikey": {
                "pn": "102-1705-ND",
                "url": "https://www.digikey.com/en/products/detail/dayton-audio/CEB-28-8/",
                "stock_check_url": "https://www.digikey.com/en/products/detail/dayton-audio/CEB-28-8/"
            },
            "alibaba": {
                "search": "BH01B bone conduction vibrator"
            }
        },
        {
            "line": 3,
            "qty": 1,
            "mpn": "STM32L476RET6",
            "manufacturer": "STMicroelectronics",
            "description": "Ultra-low-power ARM Cortex-M4 MCU, 1MB Flash",
            "category": "critical",
            "unit_price": 8.42,
            "digikey": {
                "pn": "497-15852-ND",
                "url": "https://www.digikey.com/en/products/detail/stmicroelectronics/STM32L476RET6/",
                "stock_check_url": "https://www.digikey.com/en/products/detail/stmicroelectronics/STM32L476RET6/"
            },
            "jlcpcb": {
                "pn": "STM32L476RET6",
                "category": "MCU"
            }
        },
        # RF Components
        {
            "line": 4,
            "qty": 4,
            "mpn": "LQW18AN6N8C00D",
            "manufacturer": "Murata",
            "description": "RF Inductor 6.8nH 0402",
            "category": "rf",
            "unit_price": 0.08,
            "digikey": {
                "pn": "490-16482-1-ND",
                "url": "https://www.digikey.com/en/products/detail/murata-electronics/LQW18AN6N8C00D/"
            },
            "jlcpcb": {
                "pn": "C76816",
                "basic": True
            }
        },
        {
            "line": 5,
            "qty": 2,
            "mpn": "LQW18AN15NJ00D",
            "manufacturer": "Murata",
            "description": "RF Inductor 15nH 0402",
            "category": "rf",
            "unit_price": 0.09,
            "digikey": {
                "pn": "490-11743-1-ND",
                "url": "https://www.digikey.com/en/products/detail/murata-electronics/LQW18AN15NJ00D/"
            },
            "jlcpcb": {
                "pn": "C76818",
                "basic": True
            }
        },
        {
            "line": 6,
            "qty": 4,
            "mpn": "GRM1555C1H1R0CA01D",
            "manufacturer": "Murata",
            "description": "Ceramic Cap 1pF 50V C0G 0402",
            "category": "rf",
            "unit_price": 0.03,
            "digikey": {
                "pn": "490-16097-1-ND",
                "url": "https://www.digikey.com/en/products/detail/murata-electronics/GRM1555C1H1R0CA01D/"
            },
            "jlcpcb": {
                "pn": "C116647",
                "basic": True
            }
        },
        # Power Management
        {
            "line": 7,
            "qty": 1,
            "mpn": "TPS7A02PDBVR",
            "manufacturer": "Texas Instruments",
            "description": "Ultra-Low Iq LDO Regulator 300mA",
            "category": "power",
            "unit_price": 0.58,
            "digikey": {
                "pn": "296-TPS7A02PDBVRCT-ND",
                "url": "https://www.digikey.com/en/products/detail/texas-instruments/TPS7A02PDBVR/"
            },
            "jlcpcb": {
                "pn": "C5233522",
                "basic": False
            }
        },
        {
            "line": 8,
            "qty": 1,
            "mpn": "BQ24040DSQR",
            "manufacturer": "Texas Instruments",
            "description": "Li-Ion Battery Charger IC",
            "category": "power",
            "unit_price": 1.24,
            "digikey": {
                "pn": "296-BQ24040DSQRCT-ND",
                "url": "https://www.digikey.com/en/products/detail/texas-instruments/BQ24040DSQR/"
            },
            "jlcpcb": {
                "pn": "C15876",
                "basic": False
            }
        },
        # Sensors & Interface
        {
            "line": 9,
            "qty": 2,
            "mpn": "MP34DT05TR-A",
            "manufacturer": "STMicroelectronics",
            "description": "MEMS Microphone Ultralow-Noise",
            "category": "sensors",
            "unit_price": 1.85,
            "digikey": {
                "pn": "497-18503-1-ND",
                "url": "https://www.digikey.com/en/products/detail/stmicroelectronics/MP34DT05TR-A/"
            }
        },
        {
            "line": 10,
            "qty": 1,
            "mpn": "LSM6DSOXTR",
            "manufacturer": "STMicroelectronics",
            "description": "IMU 6-axis Accelerometer + Gyroscope",
            "category": "sensors",
            "unit_price": 3.47,
            "digikey": {
                "pn": "497-18699-1-ND",
                "url": "https://www.digikey.com/en/products/detail/stmicroelectronics/LSM6DSOXTR/"
            }
        },
        # Passive Components (Buy in bulk for JLCPCB)
        {
            "line": 11,
            "qty": 50,
            "mpn": "RC0402FR-0710KL",
            "manufacturer": "Yageo",
            "description": "Resistor 10kΩ 1% 0402",
            "category": "passive",
            "unit_price": 0.004,
            "digikey": {
                "pn": "311-10.0KLRCT-ND",
                "url": "https://www.digikey.com/en/products/detail/yageo/RC0402FR-0710KL/"
            },
            "jlcpcb": {
                "pn": "C25744",
                "basic": True
            }
        },
        {
            "line": 12,
            "qty": 50,
            "mpn": "RC0402FR-071KL",
            "manufacturer": "Yageo",
            "description": "Resistor 1kΩ 1% 0402",
            "category": "passive",
            "unit_price": 0.004,
            "digikey": {
                "pn": "311-1.00KLRCT-ND",
                "url": "https://www.digikey.com/en/products/detail/yageo/RC0402FR-071KL/"
            },
            "jlcpcb": {
                "pn": "C11702",
                "basic": True
            }
        },
        {
            "line": 13,
            "qty": 25,
            "mpn": "CC0402KRX5R9BB104",
            "manufacturer": "Yageo",
            "description": "Ceramic Cap 0.1uF 50V X7R 0402",
            "category": "passive",
            "unit_price": 0.007,
            "digikey": {
                "pn": "311-1083-1-ND",
                "url": "https://www.digikey.com/en/products/detail/yageo/CC0402KRX5R9BB104/"
            },
            "jlcpcb": {
                "pn": "C307331",
                "basic": True
            }
        },
        {
            "line": 14,
            "qty": 10,
            "mpn": "CC0402KRX5R6BB106",
            "manufacturer": "Yageo",
            "description": "Ceramic Cap 10uF 6.3V X5R 0402",
            "category": "passive",
            "unit_price": 0.012,
            "digikey": {
                "pn": "311-1963-1-ND",
                "url": "https://www.digikey.com/en/products/detail/yageo/CC0402KRX5R6BB106/"
            },
            "jlcpcb": {
                "pn": "C15525",
                "basic": True
            }
        },
        {
            "line": 15,
            "qty": 5,
            "mpn": "RC0402FR-07100RL",
            "manufacturer": "Yageo",
            "description": "Resistor 100Ω 1% 0402",
            "category": "passive",
            "unit_price": 0.004,
            "digikey": {
                "pn": "311-100LRCT-ND",
                "url": "https://www.digikey.com/en/products/detail/yageo/RC0402FR-07100RL/"
            },
            "jlcpcb": {
                "pn": "C25176",
                "basic": True
            }
        },
        # PCB & Misc
        {
            "line": 16,
            "qty": 5,
            "mpn": "SILENT-001-PCB",
            "manufacturer": "JLCPCB",
            "description": "4-Layer PCB 1.6mm ENIG 100x50mm",
            "category": "mechanical",
            "unit_price": 3.20,
            "jlcpcb": {
                "pn": "custom",
                "note": "Upload Gerber to JLCPCB"
            }
        },
        {
            "line": 17,
            "qty": 1,
            "mpn": "CON-SMA-EDGE",
            "manufacturer": "Linx",
            "description": "SMA Edge Mount Connector",
            "category": "connector",
            "unit_price": 2.15,
            "digikey": {
                "pn": "CON-SMA-EDGE-ND",
                "url": "https://www.digikey.com/en/products/detail/linx-technologies/CON-SMA-EDGE/"
            },
            "jlcpcb": {
                "pn": "C404928",
                "basic": True
            }
        },
        {
            "line": 18,
            "qty": 1,
            "mpn": "ZX62-B-5PA",
            "manufacturer": "Hirose",
            "description": "USB Type-C Receptacle",
            "category": "connector",
            "unit_price": 0.85,
            "digikey": {
                "pn": "H13981CT-ND",
                "url": "https://www.digikey.com/en/products/detail/hirose-electric-co-ltd/ZX62-B-5PA-31-16-8-3/"
            },
            "jlcpcb": {
                "pn": "C168688",
                "basic": True
            }
        }
    ]
}


class DigiKeyCartBuilder:
    """Builds Digi-Key cart URLs from BOM items"""
    
    BASE_URL = "https://www.digikey.com/shortcuts"
    AFFILIATE_ID = "YOUR_AFFILIATE_ID"  # Replace with actual ID
    
    def __init__(self):
        self.items = []
    
    def add_item(self, part_number: str, quantity: int):
        """Add item to cart"""
        self.items.append({
            "part": part_number,
            "qty": quantity
        })
    
    def build_cart_url(self) -> str:
        """Generate Digi-Key cart URL"""
        if not self.items:
            return None
        
        # Build query string for multi-add
        query_parts = []
        for i, item in enumerate(self.items):
            query_parts.append(f"part{i+1}={urllib.parse.quote(item['part'])}&qty{i+1}={item['qty']}")
        
        if len(self.items) == 1:
            # Single item - direct to product page
            return f"https://www.digikey.com/en/products/quoterequest/{self.items[0]['part']}"
        
        # Multiple items
        return f"https://www.digikey.com/en/products/quoterequest?{'&'.join(query_parts)}"
    
    def build_quick_add_url(self) -> str:
        """Generate URL for Digi-Key Quick Add to Cart"""
        base = "https://www.digikey.com/en/products/quoterequest"
        return base  # Redirects to cart with query params


class JLCPCBCartBuilder:
    """Prepares JLCBCB BOM for SMT assembly"""
    
    BOM_URL = "https://cart.jlcpcb.com/quote"
    PARTS_URL = "https://jlcpcb.com/parts"
    
    def __init__(self):
        self.basic_parts = []
        self.extended_parts = []
        self.pcb_only = []
    
    def add_item(self, item: Dict):
        """Categorize item for JLCPCB ordering"""
        jlcpcb = item.get("jlcpcb", {})
        
        if jlcpcb.get("pn") == "custom":
            self.pcb_only.append(item)
        elif jlcpcb.get("basic", False):
            self.basic_parts.append(item)
        else:
            self.extended_parts.append(item)
    
    def generate_bom_csv(self) -> str:
        """Generate JLCPCB BOM import CSV"""
        lines = ["Designator,Comment,Footprint,LCSC Part Number"]
        
        for item in self.basic_parts + self.extended_parts:
            jlcpcb = item.get("jlcpcb", {})
            pn = jlcpcb.get("pn", "")
            # Simplified - would need real designators from schematic
            lines.append(f"U{item['line']},{item['mpn']},,{pn}")
        
        return "\n".join(lines)
    
    def get_pcb_order_url(self) -> str:
        """JLCPCB PCB order URL"""
        return "https://cart.jlcpcb.com/quote?from=gerber"


def check_critical_stock() -> Dict:
    """Check stock availability for critical parts"""
    print("🔍 Checking critical component stock...\n")
    
    critical_parts = [
        {"mpn": "AS3932-BTST", "digikey_pn": "AS3932-BTSTCT-ND", "source": "ams OSRAM"},
        {"mpn": "BH01B", "digikey_pn": "102-1705-ND", "source": "DigiKey"},
        {"mpn": "STM32L476RET6", "digikey_pn": "497-15852-ND", "source": "ST"}
    ]
    
    results = {}
    for part in critical_parts:
        # Note: Digi-Key requires API key for real stock checks
        # This is a simulated check with recommendations
        results[part["mpn"]] = {
            "digikey_pn": part["digikey_pn"],
            "status": "CHECK_MANUAL",
            "url": f"https://www.digikey.com/en/products/quoterequest/{part['digikey_pn']}",
            "recommendation": f"Visit Digi-Key to verify stock for {part['mpn']}"
        }
        print(f"  ✓ {part['mpn']}: Check manually at Digi-Key")
    
    return results


def calculate_costs() -> Dict:
    """Calculate total BOM costs"""
    costs = {
        "critical": 0,
        "rf": 0,
        "power": 0,
        "sensors": 0,
        "passive": 0,
        "mechanical": 0,
        "connector": 0,
        "total": 0
    }
    
    for item in BOM["items"]:
        qty = item["qty"]
        unit = item["unit_price"]
        line_cost = qty * unit
        costs["total"] += line_cost
        
        cat = item.get("category", "misc")
        if cat in costs:
            costs[cat] += line_cost
    
    return costs


def generate_digikey_cart(digikey_items: List[Dict]) -> str:
    """Generate optimized Digi-Key cart for items to order there"""
    builder = DigiKeyCartBuilder()
    
    for item in digikey_items:
        if "digikey" in item and "pn" in item["digikey"]:
            builder.add_item(item["digikey"]["pn"], item["qty"])
    
    return builder.build_cart_url()


def generate_jlcpcb_bom(jlcpcb_items: List[Dict]) -> str:
    """Generate JLCPCB BOM CSV content"""
    builder = JLCPCBCartBuilder()
    
    for item in jlcpcb_items:
        if "jlcpcb" in item:
            builder.add_item(item)
    
    return builder.generate_bom_csv()


def categorize_sourcing() -> Tuple[List, List]:
    """Categorize items by sourcing strategy"""
    digikey_only = []
    jlcpcb_friendly = []
    
    for item in BOM["items"]:
        has_dk = "digikey" in item and "pn" in item["digikey"]
        has_jlc = "jlcpcb" in item
        
        # Critical parts and unavailable on JLCPCB -> Digi-Key
        if item.get("category") == "critical" or not has_jlc:
            if has_dk:
                digikey_only.append(item)
        elif has_jlc and item["jlcpcb"].get("basic", False):
            # Basic parts -> JLCPCB
            jlcpcb_friendly.append(item)
        elif has_jlc:
            # Extended parts -> Can go either way
            jlcpcb_friendly.append(item)
        else:
            if has_dk:
                digikey_only.append(item)
    
    return digikey_only, jlcpcb_friendly


def main():
    """Main execution"""
    print("=" * 60)
    print("SILENT-001 BOM Cart Generator")
    print("=" * 60)
    print(f"Project: {BOM['project']} v{BOM['version']}")
    print(f"Total Budget: ${BOM['total_budget']:.2f}")
    print()
    
    # Calculate costs
    costs = calculate_costs()
    print("📊 Cost Breakdown:")
    print(f"  Critical:    ${costs['critical']:.2f}")
    print(f"  RF:          ${costs['rf']:.2f}")
    print(f"  Power:       ${costs['power']:.2f}")
    print(f"  Sensors:     ${costs['sensors']:.2f}")
    print(f"  Passive:     ${costs['passive']:.2f}")
    print(f"  Mechanical:  ${costs['mechanical']:.2f}")
    print(f"  Connector:   ${costs['connector']:.2f}")
    print(f"  ─────────────────")
    print(f"  TOTAL:       ${costs['total']:.2f}")
    print(f"  Remaining:   ${BOM['total_budget'] - costs['total']:.2f}")
    print()
    
    # Categorize sourcing
    digikey_items, jlcpcb_items = categorize_sourcing()
    
    print("🛒 Sourcing Strategy:")
    print(f"  Digi-Key items: {len(digikey_items)}")
    print(f"  JLCPCB items:   {len(jlcpcb_items)}")
    print()
    
    # Check critical stock
    stock_status = check_critical_stock()
    print()
    
    # Generate Digi-Key quick links
    print("🔗 Quick Links:")
    print()
    print("  Digi-Key (Critical + Specialty):")
    dk_url = generate_digikey_cart(digikey_items)
    print(f"    Quote Request: {dk_url}")
    print()
    
    # Generate JLCPCB BOM
    print("  JLCPCB (Passives + PCBs):")
    print("    PCB Order: https://cart.jlcpcb.com/quote?from=gerber")
    print("    Parts Library: https://jlcpcb.com/parts")
    print()
    
    # Output JLCPCB BOM to console
    jlc_bom = generate_jlcpcb_bom(jlcpcb_items)
    print("📄 JLCPCB BOM CSV (copy to file):")
    print("-" * 60)
    print(jlc_bom)
    print("-" * 60)
    print()
    
    # Print critical part URLs for manual ordering
    print("⚠️  CRITICAL PARTS - Order First:")
    print("-" * 60)
    for item in BOM["items"]:
        if item.get("category") == "critical":
            dk_info = item.get("digikey", {})
            print(f"  {item['mpn']}")
            print(f"    Qty: {item['qty']} @ ${item['unit_price']:.2f} = ${item['qty'] * item['unit_price']:.2f}")
            if "url" in dk_info:
                print(f"    Link: {dk_info['url']}")
            print()
    
    # Generate affiliate links note
    print("💡 Affiliate Links:")
    print("-" * 60)
    print("  Digi-Key: https://www.digikey.com (Register at https://www.digikey.com/en/resources/affiliate-program)")
    print("  JLCPCB: https://jlcpcb.com (No affiliate program currently)")
    print()
    
    # Save outputs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JLCPCB BOM
    jlc_filename = f"jlcpcb_bom_{timestamp}.csv"
    with open(jlc_filename, "w") as f:
        f.write(jlc_bom)
    print(f"💾 Saved JLCPCB BOM to: {jlc_filename}")
    
    # Save stock status
    stock_filename = f"stock_check_{timestamp}.json"
    with open(stock_filename, "w") as f:
        json.dump(stock_status, f, indent=2)
    print(f"💾 Saved stock check to: {stock_filename}")
    
    print()
    print("✅ Generation complete!")
    
    return {
        "digikey_items": len(digikey_items),
        "jlcpcb_items": len(jlcpcb_items),
        "total_cost": costs["total"],
        "budget": BOM["total_budget"],
        "digikey_url": dk_url,
        "jlcpcb_bom_file": jlc_filename
    }


if __name__ == "__main__":
    result = main()
    print("\n📋 Summary:")
    print(json.dumps(result, indent=2))
