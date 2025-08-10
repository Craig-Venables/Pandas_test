from __future__ import annotations

import os
from typing import Dict, List, Tuple


def generate_preview_report(output_dir: str,
                            on_off_ratio_info_list: List[dict],
                            normalized_area_info_list: List[dict]) -> str:
    """
    Generate a simple HTML report with top-10 ON_OFF and normalized area entries.

    Returns the path to the generated HTML file.
    """
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, 'preview_report.html')

    def rows_for(items: List[dict], prop_key: str) -> str:
        rows = []
        for idx, item in enumerate(items[:10], start=1):
            sample = item.get('sample_key', '')
            section = item.get('section_key', '')
            device = item.get('device_key', '')
            fname = item.get('file_name', '')
            prop = item.get('property_value', '')
            rows.append(f"<tr><td>{idx}</td><td>{sample}</td><td>{section}</td><td>{device}</td><td>{fname}</td><td>{prop}</td></tr>")
        return "\n".join(rows)

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Memristor Preview Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    h1, h2 {{ margin: 10px 0; }}
    table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
    th, td {{ border: 1px solid #ccc; padding: 6px 8px; text-align: left; }}
    th {{ background: #f2f2f2; }}
  </style>
 </head>
 <body>
  <h1>Memristor Preview Report</h1>

  <h2>Top 10 (ON_OFF Ratio)</h2>
  <table>
    <thead>
      <tr><th>#</th><th>Sample</th><th>Section</th><th>Device</th><th>File</th><th>ON_OFF Ratio</th></tr>
    </thead>
    <tbody>
      {rows_for(on_off_ratio_info_list, 'ON_OFF_Ratio')}
    </tbody>
  </table>

  <h2>Top 10 (Normalized Area)</h2>
  <table>
    <thead>
      <tr><th>#</th><th>Sample</th><th>Section</th><th>Device</th><th>File</th><th>Normalized Area</th></tr>
    </thead>
    <tbody>
      {rows_for(normalized_area_info_list, 'normalised_area')}
    </tbody>
  </table>

 </body>
</html>
"""
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return report_path


