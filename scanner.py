import json
import os
import datetime
import urllib.request
import xml.etree.ElementTree as ET
import yfinance as yf
import pandas as pd
import numpy as np

os.makedirs("data", exist_ok=True)

TICKERS = [
    "A","AAPL","ABBV","ABNB","ABT","ACGL","ACN","ADBE","ADI","ADM","ADP","ADSK","AEE","AEP","AES","AFL","AIG","AIZ","AJG","AKAM",
    "ALB","ALGN","ALL","ALLE","AMAT","AMCR","AMD","AME","AMGN","AMP","AMT","AMZN","ANET","AON","AOS","APA","APD","APH","APO","APP",
    "APTV","ARE","ARES","ATO","AVB","AVGO","AVY","AWK","AXON","AXP","AZO","BA","BAC","BALL","BAX","BBY","BDX","BE","BEN","BF-B",
    "BG","BIIB","BKNG","BKR","BLDR","BLK","BMY","BNY","BR","BRK-B","BRO","BSX","BX","BXP","C","CAG","CAH","CARR","CASY","CAT",
    "CB","CBOE","CBRE","CCI","CCL","CDNS","CDW","CEG","CF","CFG","CHD","CHRW","CHTR","CI","CIEN","CINF","CL","CLX","CMCSA","CME",
    "CMG","CMI","CMS","CNC","CNP","COF","COHR","COIN","COO","COP","COR","COST","CPAY","CPB","CPRT","CPT","CRL","CRM","CRWD","CSCO",
    "CSGP","CSX","CTAS","CTSH","CVS","CVNA","CVX","D","DAL","DASH","DD","DDOG","DE","DECK","DELL","DG","DGX","DHI","DHR","DIS",
    "DLR","DLTR","DOC","DOV","DOW","DPZ","DRI","DTE","DUK","DVA","DVN","DXCM","EA","EBAY","ECL","ED","EFX","EG","EIX",
    "EL","ELV","EME","EMR","EOG","EPAM","EQIX","EQR","EQT","ERIE","ES","ESS","ETN","ETR","EVRG","EW","EXC","EXE","EXPD","EXPE",
    "EXR","F","FANG","FAST","FCX","FDS","FDX","FE","FERG","FFIV","FICO","FIS","FISV","FITB","FLEX","FIX","FOX","FOXA","FRT",
    "FSLR","FTNT","FTV","GD","GDDY","GE","GEHC","GEN","GEV","GILD","GIS","GL","GLW","GM","GNRC","GOOG","GOOGL","GPC","GPN","GRMN",
    "GS","GWW","HAL","HAS","HBAN","HCA","HD","HIG","HII","HLT","HOLX","HON","HOOD","HPE","HPQ","HRL","HSIC","HST","HSY",
    "HUBB","HUM","HWM","IBM","ICE","IDXX","IEX","IFF","ILMN","INCY","INTC","INTU","INVH","IP","IQV","IR","IRM","ISRG","IT","ITW",
    "IVZ","J","JBHT","JBL","JCI","JKHY","JNJ","JPM","KDP","KEY","KEYS","KHC","KIM","KKR","KLAC","KMB","KMI","KO","KR","L",
    "LDOS","LEN","LH","LHX","LII","LIN","LITE","LLY","LMT","LNT","LOW","LRCX","LULU","LUV","LVS","LW","LYB","LYV","MA","MAA",
    "MAR","MAS","MCD","MCHP","MCK","MCO","MDLZ","MDT","MET","META","MGM","MHK","MKC","MLM","MMM","MNST","MO","MOH","MOS","MPC",
    "MPWR","MRK","MRNA","MRVL","MRSH","MS","MSCI","MSFT","MSI","MTB","MTCH","MTD","MU","NCLH","NDAQ","NDSN","NEE","NEM","NFLX","NI",
    "NKE","NOC","NOW","NRG","NSC","NTAP","NTRS","NUE","NVDA","NVR","NWS","NWSA","NXPI","O","ODFL","OKE","OMC","ON","ORCL","ORLY",
    "OTIS","OXY","PANW","PAYC","PAYX","PCAR","PCG","PEG","PEP","PFE","PFG","PG","PGR","PH","PHM","PKG","PLD","PLTR","PM",
    "PNC","PNR","PNW","PODD","POOL","PPG","PPL","PRU","PSA","PSX","PTC","PWR","PYPL","QCOM","QRVO","RCL","REG","REGN","RF","RJF",
    "RL","RMD","ROK","ROL","ROP","ROST","RSG","RTX","RVTY","SBAC","SBUX","SCHW","SHW","SJM","SLB","SMCI","SNA","SNDK","SNPS",
    "SO","SOLV","SPG","SPGI","SRE","STE","STLD","STT","STX","STZ","SWK","SWKS","SYF","SYK","SYY","T","TAP","TDG","TDY","TECH",
    "TEL","TER","TFC","TGT","TJX","TKO","TMO","TMUS","TPR","TRGP","TRMB","TROW","TRV","TSCO","TSLA","TSN","TT","TTWO","TWLO","TXN",
    "TXT","TYL","UAL","UBER","UDR","UHS","ULTA","UNH","UNP","UPS","URI","USB","V","VEEV","VICI","VLO","VLTO","VMC","VRSK",
    "VRSN","VRT","VRTX","VST","VTR","VTRS","VZ","WAB","WAT","WDAY","WDC","WEC","WELL","WFC","WM","WMB","WMT","WRB","WSM",
    "WST","WTW","WY","WYNN","XEL","XOM","XYL","XYZ","YUM","ZBH","ZBRA","ZTS"
]

INDICES = ["SPY", "QQQ", "DIA", "IWM", "^VIX"]
SECTOR_ETFS = {
    "XLK": "Technology", "XLF": "Financials", "XLV": "Health Care", "XLE": "Energy",
    "XLY": "Consumer Disc.", "XLC": "Communication", "XLI": "Industrials",
    "XLP": "Consumer Staples", "XLB": "Materials", "XLRE": "Real Estate", "XLU": "Utilities"
}

def strat_bar(curr, prev):
    if prev is None:
        return {
            "t": "1",
            "c": "up" if curr["Close"] >= curr["Open"] else "down",
            "o": round(float(curr["Open"]), 2),
            "hi": round(float(curr["High"]), 2),
            "lo": round(float(curr["Low"]), 2)
        }
    hi_brk = curr["High"] > prev["High"]
    lo_brk = curr["Low"] < prev["Low"]
    t = "3" if (hi_brk and lo_brk) else ("2U" if hi_brk else ("2D" if lo_brk else "1"))
    c = "up" if curr["Close"] > curr["Open"] else ("down" if curr["Close"] < curr["Open"] else "doji")
    br = ""
    if t == "2D" and c == "up":
        br = "up"
    elif t == "2U" and c == "down":
        br = "down"
    ifc = ""
    if curr["Close"] > prev["High"]:
        ifc = "up"
    elif curr["Close"] < prev["Low"]:
        ifc = "down"
    rng = curr["High"] - curr["Low"]
    body = abs(curr["Close"] - curr["Open"])
    sh = "normal"
    if rng > 0:
        if body / rng < 0.12:
            sh = "doji"
        elif (min(curr["Open"], curr["Close"]) - curr["Low"]) / rng > 0.6:
            sh = "hammer"
        elif (curr["High"] - max(curr["Open"], curr["Close"])) / rng > 0.6:
            sh = "shooter"
        elif body / rng > 0.8:
            sh = "marubozu"
    return {
        "t": t, "c": c, "sh": sh, "br": br, "ifc": ifc,
        "o": round(float(curr["Open"]), 2),
        "hi": round(float(curr["High"]), 2),
        "lo": round(float(curr["Low"]), 2)
    }

def calc_rsi(s, period=14):
    delta = s.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    val = 100 - (100 / (1 + rs))
    return round(float(val.iloc[-1]), 1) if pd.notna(val.iloc[-1]) else None

def analyze_df(df):
    if df is None or len(df) < 30:
        return None
    df = df.dropna(subset=["Open", "High", "Low", "Close"])
    if len(df) < 30:
        return None
    d_curr, d_prev = df.iloc[-1], df.iloc[-2]
    d_cell = strat_bar(d_curr, d_prev)

    def resample_strat(rule):
        r = df.resample(rule).agg({"Open": "first", "High": "max", "Low": "min", "Close": "last"}).dropna()
        if len(r) < 2:
            return d_cell
        return strat_bar(r.iloc[-1], r.iloc[-2])

    w_cell = resample_strat("W-FRI")
    m_cell = resample_strat("ME")
    q_cell = resample_strat("QE")
    y_cell = resample_strat("YE")

    dirs = [d_cell["c"], w_cell["c"], m_cell["c"], q_cell["c"], y_cell["c"]]
    ftfc = all(x == "up" for x in dirs) or all(x == "down" for x in dirs)

    px = float(d_curr["Close"])
    prev_c = float(d_prev["Close"])
    chg = round((px - prev_c) / prev_c * 100, 2) if prev_c else 0.0
    gap = round((float(d_curr["Open"]) - prev_c) / prev_c * 100, 2) if prev_c else 0.0

    tr = pd.concat([
        df["High"] - df["Low"],
        (df["High"] - df["Close"].shift()).abs(),
        (df["Low"] - df["Close"].shift()).abs()
    ], axis=1).max(axis=1)
    atr = float(tr.rolling(14).mean().iloc[-1]) if len(df) >= 14 else float(tr.mean())
    atrp = round(atr / px * 100, 2) if px else 0.0

    vol = int(d_curr["Volume"]) if pd.notna(d_curr["Volume"]) else 0
    avol30 = float(df["Volume"].tail(30).mean()) if len(df) >= 30 else float(df["Volume"].mean())
    rvol = round(vol / avol30, 2) if avol30 > 0 else 1.0

    hi52 = float(df["High"].tail(252).max())
    lo52 = float(df["Low"].tail(252).min())
    dhi52 = round((px - hi52) / hi52 * 100, 2) if hi52 else 0.0
    dlo52 = round((px - lo52) / lo52 * 100, 2) if lo52 else 0.0

    dsma = {}
    for p in [10, 20, 50, 100, 150, 200]:
        if len(df) >= p:
            ma = float(df["Close"].rolling(p).mean().iloc[-1])
            dsma[str(p)] = round((px - ma) / ma * 100, 2) if ma else None

    c5 = round((px - float(df["Close"].iloc[-6])) / float(df["Close"].iloc[-6]) * 100, 2) if len(df) >= 6 else chg
    c20 = round((px - float(df["Close"].iloc[-21])) / float(df["Close"].iloc[-21]) * 100, 2) if len(df) >= 21 else chg

    return {
        "px": round(px, 2), "chg": chg, "ao": px >= float(d_curr["Open"]),
        "D": d_cell, "W": w_cell, "M": m_cell, "Q": q_cell, "Y": y_cell, "ftfc": ftfc,
        "tech": {
            "px": round(px, 2), "chg": chg, "rsi": calc_rsi(df["Close"]), "rvol": rvol,
            "vol": vol, "avol30": int(avol30), "atr": round(atr, 2), "atrp": atrp,
            "gap": gap, "dhi52": dhi52, "dlo52": dlo52, "dsma": dsma, "c5": c5, "c20": c20
        }
    }

def main():
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    all_syms = list(set(TICKERS + INDICES + list(SECTOR_ETFS.keys())))
    raw = yf.download(all_syms, period="1y", interval="1d", group_by="ticker", threads=True, progress=False)

    indices_out = []
    vix_obj = None
    for idx in INDICES:
        df = raw[idx] if idx in raw else None
        res = analyze_df(df)
        if res:
            sym_clean = "VIX" if idx == "^VIX" else idx
            if sym_clean == "VIX":
                vix_obj = {"level": res["px"], "chg": res["chg"]}
            else:
                ohlc = [[round(float(r["Open"]),2), round(float(r["High"]),2), round(float(r["Low"]),2), round(float(r["Close"]),2)] for _, r in df.dropna().tail(35).iterrows()]
                indices_out.append({"sym": sym_clean, "price": res["px"], "chg": res["chg"], "D": res["D"], "ohlc": ohlc})

    sectors_out = []
    for etf, name in SECTOR_ETFS.items():
        res = analyze_df(raw[etf] if etf in raw else None)
        if res:
            sectors_out.append({
                "name": name, "etf": etf, "px": res["px"], "chg": res["chg"],
                "chg5d": res["tech"]["c5"], "chg20d": res["tech"]["c20"],
                "above": 1, "total": 1, "stocks": []
            })

    scan_rows = []
    prices_map = {}
    above_cnt, below_cnt = 0, 0
    for sym in TICKERS:
        df = raw[sym] if sym in raw else None
        res = analyze_df(df)
        if not res:
            continue
        clean_sym = sym.replace("-", ".")
        if res["ao"]:
            above_cnt += 1
        else:
            below_cnt += 1
        prices_map[clean_sym] = [res["px"], res["chg"]]
        scan_rows.append({
            "s": clean_sym, "sec": "S&P 500", "ind": "S&P 500", "p": res["px"], "c": res["chg"],
            "sp": True, "D": res["D"], "W": res["W"], "M": res["M"], "Q": res["Q"], "Y": res["Y"],
            "ftfc": res["ftfc"], "tech": res["tech"], "ninja": 75 if res["ftfc"] else 50
        })

    sorted_by_chg = sorted(scan_rows, key=lambda x: x["c"], reverse=True)
    leaders = [{"s": x["s"], "c": x["c"]} for x in sorted_by_chg[:10]]
    laggards = [{"s": x["s"], "c": x["c"]} for x in sorted_by_chg[-10:][::-1]]
    gap_up = [{"s": x["s"], "gp": x["tech"]["gap"], "gd": round(x["p"] * x["tech"]["gap"] / 100, 2), "price": x["p"]} for x in scan_rows if x["tech"]["gap"] >= 2.5][:10]
    gap_dn = [{"s": x["s"], "gp": x["tech"]["gap"], "gd": round(x["p"] * x["tech"]["gap"] / 100, 2), "price": x["p"]} for x in scan_rows if x["tech"]["gap"] <= -2.5][:10]

    sec_sorted = sorted(sectors_out, key=lambda x: x["chg"], reverse=True)
    market_data = {
        "updated": now_iso,
        "indices": indices_out,
        "vix": vix_obj,
        "sectors": sectors_out,
        "breadth": {"above": above_cnt, "below": below_cnt, "total": above_cnt + below_cnt},
        "leaders": leaders,
        "laggards": laggards,
        "sectorLeaders": sec_sorted[:5],
        "sectorLaggards": sec_sorted[-5:][::-1],
        "gappers": {"up": gap_up, "down": gap_dn}
    }

    with open("data/scanner.json", "w", encoding="utf-8") as f:
        json.dump({"updated": now_iso, "rows": scan_rows}, f, separators=(",", ":"))
    with open("data/market.json", "w", encoding="utf-8") as f:
        json.dump(market_data, f, separators=(",", ":"))
    with open("data/prices.json", "w", encoding="utf-8") as f:
        json.dump({"updated": now_iso, "prices": prices_map}, f, separators=(",", ":"))

    cards = []
    try:
        req = urllib.request.Request("https://feeds.finance.yahoo.com/rss/2.0/headline?s=SPY,QQQ,AAPL,NVDA,TSLA&region=US&lang=en-US", headers={"User-Agent": "Mozilla/5.0"})
        xml_data = urllib.request.urlopen(req, timeout=10).read()
        root = ET.fromstring(xml_data)
        for item in root.findall(".//item")[:20]:
            title = item.findtext("title") or ""
            link = item.findtext("link") or "#"
            cards.append({"en": title, "he": title, "url": link, "pub": "Yahoo Finance", "ts": now_iso})
    except Exception:
        pass

    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump({"updated": now_iso, "cards": cards}, f, ensure_ascii=False)

if __name__ == "__main__":
    main()
