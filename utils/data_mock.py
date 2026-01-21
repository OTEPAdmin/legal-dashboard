import random

def get_dashboard_data(year_str, month_str):
    # 1. Base Multipliers based on Year
    year_int = int(year_str)
    if year_int == 2568: year_mult, trend_base = 1.5, 92
    elif year_int == 2567: year_mult, trend_base = 0.7, 65
    else: year_mult, trend_base = 1.0, 85

    # 2. Seasonal Multipliers
    months = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", 
              "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
    month_idx = months.index(month_str)
    month_mult = 1.0 + (month_idx * 0.02) 

    # Calculations
    cpk_total = int(900000 * year_mult * month_mult)
    cpk_new = int(1200 * year_mult * month_mult)
    cpk_resign = int(800 * (1/year_mult))
    cps_total = int(280000 * year_mult * month_mult)
    rev_total = 45.80 * year_mult * month_mult

    data = {
        "cpk": {
            "total": f"{cpk_total:,}", "new": f"+{cpk_new:,}", "resign": f"-{cpk_resign:,}",
            "apply_vals": [cpk_new, int(cpk_new * 0.2)], 
            "resign_vals": [int(cpk_resign*0.5), int(cpk_resign*0.3), int(cpk_resign*0.1), int(cpk_resign*0.1)],
            "gender": [38 + (year_int%2), 62 - (year_int%2)], 
            "age": [10*year_mult, 35, 30, 25/year_mult] 
        },
        "cps": {
            "total": f"{cps_total:,}", "new": f"+{int(cpk_new*0.4):,}", "resign": f"-{int(cpk_resign*0.4):,}",
            "apply_vals": [int(cpk_new*0.4), int(cpk_new * 0.05)],
            "resign_vals": [int(cpk_resign*0.2), int(cpk_resign*0.2), 50, 50],
            "gender": [42 - (year_int%2), 58 + (year_int%2)],
            "age": [5*year_mult, 25, 45, 25/year_mult]
        },
        "finance": {
            "cpk_trend": [trend_base + (i*0.5*year_mult) for i in range(12)],
            "cps_trend": [trend_base + 2 + (i*0.3*year_mult) for i in range(12)],
            "cpk_paid": f"{trend_base:.2f}%", "cps_paid": f"{trend_base + 1.5:.2f}%"
        },
        "revenue": {
            "total": f"{rev_total:.2f}",
            "users": f"{int(73000 * year_mult):,}",
            "avg": f"{int(627 * month_mult):,}",
            "checkup_stats": [int(50 * year_mult), int(90 * year_mult), int(16000 * year_mult), int(9000 * year_mult)],
            "checkup_rate": (9000/16000) * year_mult,
            "age_dist": [int(1200 * year_mult), int(2100 * year_mult), int(2800 * year_mult), int(1900 * year_mult), int(1100 * year_mult)]
        }
    }
    return data
