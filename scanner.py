import json
import os
import datetime
import urllib.request
import xml.etree.ElementTree as ET
import yfinance as yf
import pandas as pd
import numpy as np

os.makedirs("data", exist_ok=True)

SECTOR_MAP = {
    # Technology
    "AAPL":"Technology","MSFT":"Technology","NVDA":"Technology","AVGO":"Technology","ORCL":"Technology","CRM":"Technology",
    "AMD":"Technology","ADBE":"Technology","CSCO":"Technology","ACN":"Technology","IBM":"Technology","INTU":"Technology",
    "TXN":"Technology","QCOM":"Technology","AMAT":"Technology","NOW":"Technology","PANW":"Technology","ADI":"Technology",
    "LRCX":"Technology","MU":"Technology","KLAC":"Technology","SNPS":"Technology","CDNS":"Technology","CRWD":"Technology",
    "MSI":"Technology","APH":"Technology","NXPI":"Technology","FTNT":"Technology","ADSK":"Technology","ROP":"Technology",
    "PLTR":"Technology","ANET":"Technology","DELL":"Technology","SMCI":"Technology","FICO":"Technology","MPWR":"Technology",
    "TEL":"Technology","CTSH":"Technology","IT":"Technology","HPQ":"Technology","HPE":"Technology","CDW":"Technology",
    "ON":"Technology","GLW":"Technology","KEYS":"Technology","NTAP":"Technology","TYL":"Technology","PTC":"Technology",
    "TER":"Technology","STX":"Technology","WDC":"Technology","ZBRA":"Technology","SWKS":"Technology","QRVO":"Technology",
    "AKAM":"Technology","EPAM":"Technology","FFIV":"Technology","GEN":"Technology","JBL":"Technology","CIEN":"Technology",
    "COHR":"Technology","LITE":"Technology","SNDK":"Technology","APP":"Technology","MCHP":"Technology",

    # Financials
    "BRK-B":"Financials","JPM":"Financials","V":"Financials","MA":"Financials","BAC":"Financials","WFC":"Financials",
    "GS":"Financials","MS":"Financials","SPGI":"Financials","BLK":"Financials","AXP":"Financials","C":"Financials",
    "SCHW":"Financials","PGR":"Financials","CB":"Financials","MMC":"Financials","FI":"Financials","FISV":"Financials",
    "BX":"Financials","ICE":"Financials","CME":"Financials","KKR":"Financials","AON":"Financials","MCO":"Financials",
    "USB":"Financials","PNC":"Financials","AJG":"Financials","TRV":"Financials","APO":"Financials","COF":"Financials",
    "AFL":"Financials","ALL":"Financials","AIG":"Financials","MET":"Financials","PRU":"Financials","BK":"Financials",
    "BNY":"Financials","AMP":"Financials","MSCI":"Financials","COIN":"Financials","HOOD":"Financials","FIS":"Financials",
    "ACGL":"Financials","TFC":"Financials","DFS":"Financials","NDAQ":"Financials","HIG":"Financials","WTW":"Financials",
    "RJF":"Financials","MTB":"Financials","FITB":"Financials","STT":"Financials","BRO":"Financials","HBAN":"Financials",
    "CBOE":"Financials","CINF":"Financials","RF":"Financials","CFG":"Financials","NTRS":"Financials","KEY":"Financials",
    "SYF":"Financials","WRB":"Financials","PFG":"Financials","L":"Financials","TROW":"Financials","FDS":"Financials",
    "EG":"Financials","ERIE":"Financials","AIZ":"Financials","GL":"Financials","IVZ":"Financials","BEN":"Financials",
    "ARES":"Financials","CPAY":"Financials","MRSH":"Financials",

    # Health Care
    "LLY":"Health Care","UNH":"Health Care","JNJ":"Health Care","ABBV":"Health Care","MRK":"Health Care","TMO":"Health Care",
    "ABT":"Health Care","DHR":"Health Care","ISRG":"Health Care","AMGN":"Health Care","PFE":"Health Care","SYK":"Health Care",
    "BSX":"Health Care","VRTX":"Health Care","ELV":"Health Care","MDT":"Health Care","BMY":"Health Care","GILD":"Health Care",
    "REGN":"Health Care","CI":"Health Care","CVS":"Health Care","ZTS":"Health Care","BDX":"Health Care","MCK":"Health Care",
    "HCA":"Health Care","EW":"Health Care","COR":"Health Care","GEHC":"Health Care","IDXX":"Health Care","IQV":"Health Care",
    "RMD":"Health Care","A":"Health Care","CNC":"Health Care","DXCM":"Health Care","MTD":"Health Care","CAH":"Health Care",
    "HUM":"Health Care","BIIB":"Health Care","STE":"Health Care","WAT":"Health Care","ZBH":"Health Care","BAX":"Health Care",
    "HOLX":"Health Care","ALGN":"Health Care","PODD":"Health Care","COO":"Health Care","DGX":"Health Care","LH":"Health Care",
    "MOH":"Health Care","VTRS":"Health Care","INCY":"Health Care","TECH":"Health Care","RVTY":"Health Care","CRL":"Health Care",
    "HSIC":"Health Care","UHS":"Health Care","DVA":"Health Care","SOLV":"Health Care","MRNA":"Health Care","ILMN":"Health Care",
    "VEEV":"Health Care",

    # Consumer Discretionary
    "AMZN":"Consumer Discretionary","TSLA":"Consumer Discretionary","HD":"Consumer Discretionary","MCD":"Consumer Discretionary",
    "LOW":"Consumer Discretionary","BKNG":"Consumer Discretionary","TJX":"Consumer Discretionary","NKE":"Consumer Discretionary",
    "SBUX":"Consumer Discretionary","CMG":"Consumer Discretionary","ORLY":"Consumer Discretionary","MAR":"Consumer Discretionary",
    "ABNB":"Consumer Discretionary","GM":"Consumer Discretionary","AZO":"Consumer Discretionary","HLT":"Consumer Discretionary",
    "F":"Consumer Discretionary","ROST":"Consumer Discretionary","DHI":"Consumer Discretionary","LEN":"Consumer Discretionary",
    "RCL":"Consumer Discretionary","YUM":"Consumer Discretionary","LULU":"Consumer Discretionary","TSCO":"Consumer Discretionary",
    "DECK":"Consumer Discretionary","PHM":"Consumer Discretionary","DRI":"Consumer Discretionary","EBAY":"Consumer Discretionary",
    "GRMN":"Consumer Discretionary","NVR":"Consumer Discretionary","EXPE":"Consumer Discretionary","ULTA":"Consumer Discretionary",
    "DPZ":"Consumer Discretionary","CCL":"Consumer Discretionary","LVS":"Consumer Discretionary","APTV":"Consumer Discretionary",
    "BBY":"Consumer Discretionary","POOL":"Consumer Discretionary","TPR":"Consumer Discretionary","LKQ":"Consumer Discretionary",
    "MGM":"Consumer Discretionary","NCLH":"Consumer Discretionary","WYNN":"Consumer Discretionary","HAS":"Consumer Discretionary",
    "RL":"Consumer Discretionary","MHK":"Consumer Discretionary","DASH":"Consumer Discretionary","CVNA":"Consumer Discretionary",
    "WSM":"Consumer Discretionary","KMX":"Consumer Discretionary","BWA":"Consumer Discretionary",

    # Communication Services
    "META":"Communication Services","GOOGL":"Communication Services","GOOG":"Communication Services","NFLX":"Communication Services",
    "DIS":"Communication Services","CMCSA":"Communication Services","VZ":"Communication Services","T":"Communication Services",
    "TMUS":"Communication Services","CHTR":"Communication Services","EA":"Communication Services","TTWO":"Communication Services",
    "WBD":"Communication Services","OMC":"Communication Services","LYV":"Communication Services","MTCH":"Communication Services",
    "FOXA":"Communication Services","FOX":"Communication Services","NWSA":"Communication Services","NWS":"Communication Services",
    "TKO":"Communication Services","IPG":"Communication Services",

    # Industrials
    "GE":"Industrials","CAT":"Industrials","RTX":"Industrials","UNP":"Industrials","HON":"Industrials","ETN":"Industrials",
    "BA":"Industrials","LMT":"Industrials","ADP":"Industrials","UPS":"Industrials","DE":"Industrials","TT":"Industrials",
    "PH":"Industrials","GD":"Industrials","TDG":"Industrials","WM":"Industrials","CTAS":"Industrials","ITW":"Industrials",
    "NOC":"Industrials","EMR":"Industrials","CSX":"Industrials","FDX":"Industrials","NSC":"Industrials","CARR":"Industrials",
    "PCAR":"Industrials","URI":"Industrials","GWW":"Industrials","JCI":"Industrials","PWR":"Industrials","CMI":"Industrials",
    "RSG":"Industrials","FAST":"Industrials","AME":"Industrials","ODFL":"Industrials","VRSK":"Industrials","LHX":"Industrials",
    "OTIS":"Industrials","IR":"Industrials","GEV":"Industrials","EFX":"Industrials","HWM":"Industrials","ROK":"Industrials",
    "AXON":"Industrials","DAL":"Industrials","UAL":"Industrials","LUV":"Industrials","DOV":"Industrials","XYL":"Industrials",
    "HUBB":"Industrials","FTV":"Industrials","WAB":"Industrials","BR":"Industrials","VLTO":"Industrials","EXPD":"Industrials",
    "CPRT":"Industrials","PAYX":"Industrials","J":"Industrials","LDOS":"Industrials","TXT":"Industrials","MAS":"Industrials",
    "LII":"Industrials","SNA":"Industrials","IEX":"Industrials","NDSN":"Industrials","SWK":"Industrials","CHRW":"Industrials",
    "JBHT":"Industrials","BLDR":"Industrials","ALLE":"Industrials","AOS":"Industrials","HII":"Industrials","GNRC":"Industrials",
    "EME":"Industrials","FERG":"Industrials","FIX":"Industrials","FLEX":"Industrials","VRT":"Industrials","PAYC":"Industrials",
    "CSGP":"Industrials","ROL":"Industrials","UBER":"Industrials","XYZ":"Industrials","TRMB":"Industrials",

    # Consumer Staples
    "PG":"Consumer Staples","COST":"Consumer Staples","WMT":"Consumer Staples","KO":"Consumer Staples","PEP":"Consumer Staples",
    "PM":"Consumer Staples","MDLZ":"Consumer Staples","MO":"Consumer Staples","CL":"Consumer Staples","TGT":"Consumer Staples",
    "KMB":"Consumer Staples","GIS":"Consumer Staples","STZ":"Consumer Staples","SYY":"Consumer Staples","KDP":"Consumer Staples",
    "MNST":"Consumer Staples","KR":"Consumer Staples","HSY":"Consumer Staples","ADM":"Consumer Staples","KHC":"Consumer Staples",
    "EL":"Consumer Staples","CHD":"Consumer Staples","MKC":"Consumer Staples","CLX":"Consumer Staples","TSN":"Consumer Staples",
    "DLTR":"Consumer Staples","DG":"Consumer Staples","CAG":"Consumer Staples","SJM":"Consumer Staples","HRL":"Consumer Staples",
    "TAP":"Consumer Staples","CPB":"Consumer Staples","LW":"Consumer Staples","BG":"Consumer Staples","CASY":"Consumer Staples",
    "BF-B":"Consumer Staples",

    # Energy
    "XOM":"Energy","CVX":"Energy","COP":"Energy","EOG":"Energy","SLB":"Energy","MPC":"Energy","PSX":"Energy","VLO":"Energy",
    "WMB":"Energy","OKE":"Energy","OXY":"Energy","KMI":"Energy","HES":"Energy","HAL":"Energy","BKR":"Energy","DVN":"Energy",
    "FANG":"Energy","TRGP":"Energy","EQT":"Energy","CTRA":"Energy","APA":"Energy","EXE":"Energy",

    # Utilities
    "NEE":"Utilities","SO":"Utilities","DUK":"Utilities","CEG":"Utilities","SRE":"Utilities","AEP":"Utilities","D":"Utilities",
    "PCG":"Utilities","EXC":"Utilities","XEL":"Utilities","PEG":"Utilities","ED":"Utilities","WEC":"Utilities","AWK":"Utilities",
    "EIX":"Utilities","DTE":"Utilities","ETR":"Utilities","FE":"Utilities","ES":"Utilities","PPL":"Utilities","AEE":"Utilities",
    "CMS":"Utilities","CNP":"Utilities","ATO":"Utilities","NRG":"Utilities","LNT":"Utilities","EVRG":"Utilities","NI":"Utilities",
    "PNW":"Utilities","AES":"Utilities","VST":"Utilities",

    # Real Estate
    "PLD":"Real Estate","AMT":"Real Estate","EQIX":"Real Estate","WELL":"Real Estate","SPG":"Real Estate","PSA":"Real Estate",
    "O":"Real Estate","CCI":"Real Estate","DLR":"Real Estate","VICI":"Real Estate","CBRE":"Real Estate","EXR":"Real Estate",
    "AVB":"Real Estate","IRM":"Real Estate","EQR":"Real Estate","SBAC":"Real Estate","WY":"Real Estate","VTR":"Real Estate",
    "ARE":"Real Estate","ESS":"Real Estate","MAA":"Real Estate","INVH":"Real Estate","KIM":"Real Estate","DOC":"Real Estate",
    "UDR":"Real Estate","CPT":"Real Estate","HST":"Real Estate","REG":"Real Estate","BXP":"Real Estate","FRT":"Real Estate",

    # Materials
    "LIN":"Materials","SHW":"Materials","APD":"Materials","FCX":"Materials","ECL":"Materials","NEM":"Materials","CTVA":"Materials",
    "NUE":"Materials","DD":"Materials","DOW":"Materials","VMC":"Materials","MLM":"Materials","PPG":"Materials","IFF":"Materials",
    "LYB":"Materials","STLD":"Materials","BALL":"Materials","AVY":"Materials","PKG":"Materials","IP":"Materials","CF":"Materials",
    "ALB":"Materials","MOS":"Materials","EMN":"Materials","CE":"Materials","AMCR":"Materials","BE":"Materials","SOLV":"Materials",
    "TWLO":"Technology","TTD":"Technology","GDDY":"Technology"
}

TICKERS = list(SECTOR_MAP.keys())

INDICES = ["SPY", "QQQ", "DIA", "IWM", "^VIX"]
SECTOR_ETFS = {
    "XLK": "Technology",
    "XLF": "Financials",
    "XLV": "Health Care",
    "XLE": "Energy",
    "XLY": "Consumer Discretionary",
    "XLC": "Communication Services",
    "XLI": "Industrials",
    "XLP": "Consumer Staples",
    "XLB": "Materials",
    "XLRE": "Real Estate",
    "XLU": "Utilities"
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
    br = "up" if (t == "2D" and c == "up") else ("down" if (t == "2U" and c == "down") else "")
    ifc = "up" if curr["Close"] > prev["High"] else ("down" if curr["Close"] < prev["Low"] else "")
    rng = curr["High"] - curr["Low"]
    body = abs(curr["Close"] - curr["Open"])
    sh = "normal"
    if rng > 0:
        if body / rng < 0.12: sh = "doji"
        elif (min(curr["Open"], curr["Close"]) - curr["Low"]) / rng > 0.6: sh = "hammer"
        elif (curr["High"] - max(curr["Open"], curr["Close"])) / rng > 0.6: sh = "shooter"
        elif body / rng > 0.8: sh = "marubozu"
    return {
        "t": t, "c": c, "sh": sh, "br": br, "ifc": ifc,
        "o": round(float(curr["Open"]), 2),
        "hi": round(float(curr["High"]), 2),
        "lo": round(float(curr["Low"]), 2)
    }

def build_tf_cell(sub_df):
    if sub_df is None or len(sub_df) < 2:
        return None
    cc = strat_bar(sub_df.iloc[-1], sub_df.iloc[-2])
    c1 = strat_bar(sub_df.iloc[-2], sub_df.iloc[-3]) if len(sub_df) >= 3 else None
    c2 = strat_bar(sub_df.iloc[-3], sub_df.iloc[-4]) if len(sub_df) >= 4 else None
    if c1:
        cc["c1"] = {"t": c1["t"], "c": c1["c"], "sh": c1["sh"]}
    if c2:
        cc["c2"] = {"t": c2["t"], "c": c2["c"], "sh": c2["sh"]}
    return cc

def calc_rsi(s, period=14):
    delta = s.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    val = 100 - (100 / (1 + rs))
    return round(float(val.iloc[-1]), 1) if pd.notna(val.iloc[-1]) else None

def calc_mfi(df, period=14):
    tp = (df["High"] + df["Low"] + df["Close"]) / 3.0
    mf = tp * df["Volume"]
    pos = mf.where(tp > tp.shift(1), 0.0).rolling(period).sum()
    neg = mf.where(tp < tp.shift(1), 0.0).rolling(period).sum()
    mfr = pos / neg.replace(0, np.nan)
    val = 100 - (100 / (1 + mfr))
    return round(float(val.iloc[-1]), 1) if pd.notna(val.iloc[-1]) else None

def analyze_df(df):
    if df is None or len(df) < 30:
        return None
    df = df.dropna(subset=["Open", "High", "Low", "Close"])
    if len(df) < 30:
        return None

    d_cell = build_tf_cell(df)

    def resample_strat(rule):
        r = df.resample(rule).agg({"Open": "first", "High": "max", "Low": "min", "Close": "last"}).dropna()
        if len(r) < 2:
            return d_cell
        return build_tf_cell(r)

    w_cell = resample_strat("W-FRI")
    m_cell = resample_strat("ME")
    q_cell = resample_strat("QE")
    y_cell = resample_strat("YE")

    dirs = [d_cell["c"], w_cell["c"], m_cell["c"], q_cell["c"], y_cell["c"]]
    ftfc = all(x == "up" for x in dirs) or all(x == "down" for x in dirs)

    d_curr, d_prev = df.iloc[-1], df.iloc[-2]
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
    above_ma = {}
    for p in [20, 50, 100, 150, 200]:
        if len(df) >= p:
            ma = float(df["Close"].rolling(p).mean().iloc[-1])
            dsma[str(p)] = round((px - ma) / ma * 100, 2) if ma else None
            above_ma[p] = px > ma

    # Bollinger Bands (20, 2)
    bb = None
    if len(df) >= 20:
        sma20 = float(df["Close"].rolling(20).mean().iloc[-1])
        std20 = float(df["Close"].rolling(20).std().iloc[-1])
        if std20 > 0:
            upper = sma20 + 2 * std20
            lower = sma20 - 2 * std20
            pos = round((px - lower) / (upper - lower), 2)
            bw = round((upper - lower) / sma20 * 100, 2)
            bb = {"pos": pos, "bw": bw, "sq": bw < 6.0}

    c5 = round((px - float(df["Close"].iloc[-6])) / float(df["Close"].iloc[-6]) * 100, 2) if len(df) >= 6 else chg
    c20 = round((px - float(df["Close"].iloc[-21])) / float(df["Close"].iloc[-21]) * 100, 2) if len(df) >= 21 else chg

    return {
        "px": round(px, 2), "chg": chg, "ao": px >= float(d_curr["Open"]),
        "D": d_cell, "W": w_cell, "M": m_cell, "Q": q_cell, "Y": y_cell, "ftfc": ftfc,
        "above_ma": above_ma,
        "tech": {
            "px": round(px, 2), "chg": chg, "rsi": calc_rsi(df["Close"]), "mfi": calc_mfi(df),
            "rvol": rvol, "vol": vol, "avol30": int(avol30), "atr": round(atr, 2), "atrp": atrp,
            "gap": gap, "dhi52": dhi52, "dlo52": dlo52, "dsma": dsma, "bb": bb, "c5": c5, "c20": c20
        }
    }

def main():
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    all_syms = list(set(TICKERS + INDICES + list(SECTOR_ETFS.keys())))
    raw = yf.download(all_syms, period="1y", interval="1d", group_by="ticker", threads=True, progress=False)

    mc_map = {}
    ext_map = {}
    try:
        t_objs = yf.Tickers(" ".join(TICKERS))
        for sym in TICKERS:
            clean_s = sym.replace("-", ".")
            try:
                fi = t_objs.tickers[sym].fast_info
                mc = getattr(fi, "market_cap", None)
                if mc and mc > 0:
                    mc_map[clean_s] = round(float(mc) / 1e9, 2)
                last_p = getattr(fi, "last_price", None)
                if last_p and last_p > 0:
                    ext_map[clean_s] = {"px": round(float(last_p), 2)}
            except Exception:
                pass
    except Exception:
        pass

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

    scan_rows = []
    prices_map = {}
    above_cnt, below_cnt = 0, 0
    ma_counts = {20: 0, 50: 0, 100: 0, 150: 0, 200: 0}
    ma_totals = {20: 0, 50: 0, 100: 0, 150: 0, 200: 0}
    sec_stocks = {v: [] for v in SECTOR_ETFS.values()}

    for sym in TICKERS:
        df = raw[sym] if sym in raw else None
        res = analyze_df(df)
        if not res:
            continue
        clean_sym = sym.replace("-", ".")
        if res["ao"]: above_cnt += 1
        else: below_cnt += 1

        for p, is_ab in res["above_ma"].items():
            ma_totals[p] += 1
            if is_ab: ma_counts[p] += 1

        sec_name = SECTOR_MAP.get(sym, "Technology")
        mc_val = mc_map.get(clean_sym, 25.0)
        px_now = ext_map.get(clean_sym, {}).get("px", res["px"])
        prices_map[clean_sym] = [px_now, res["chg"]]

        if sec_name in sec_stocks:
            sec_stocks[sec_name].append({"s": clean_sym, "c": res["chg"], "mc": mc_val, "ao": res["ao"]})

        scan_rows.append({
            "s": clean_sym,
            "sec": sec_name,
            "ind": sec_name,
            "p": px_now,
            "c": res["chg"],
            "mc": mc_val,
            "sp": True,
            "D": res["D"], "W": res["W"], "M": res["M"], "Q": res["Q"], "Y": res["Y"],
            "ftfc": res["ftfc"],
            "tech": res["tech"],
            "ninja": 75 if res["ftfc"] else 50
        })

    sectors_out = []
    for etf, name in SECTOR_ETFS.items():
        res = analyze_df(raw[etf] if etf in raw else None)
        st_list = sorted(sec_stocks.get(name, []), key=lambda x: x["mc"], reverse=True)
        ab_s = sum(1 for x in st_list if x["ao"])
        if res:
            sectors_out.append({
                "name": name, "etf": etf, "px": res["px"], "chg": res["chg"],
                "chg5d": res["tech"]["c5"], "chg20d": res["tech"]["c20"],
                "above": ab_s, "total": max(len(st_list), 1), "stocks": st_list[:30]
            })

    sorted_by_chg = sorted(scan_rows, key=lambda x: x["c"], reverse=True)
    leaders = [{"s": x["s"], "c": x["c"]} for x in sorted_by_chg[:10]]
    laggards = [{"s": x["s"], "c": x["c"]} for x in sorted_by_chg[-10:][::-1]]
    gap_up = [{"s": x["s"], "gp": x["tech"]["gap"], "gd": round(x["p"] * x["tech"]["gap"] / 100, 2), "price": x["p"]} for x in scan_rows if x["tech"]["gap"] >= 2.0][:10]
    gap_dn = [{"s": x["s"], "gp": x["tech"]["gap"], "gd": round(x["p"] * x["tech"]["gap"] / 100, 2), "price": x["p"]} for x in scan_rows if x["tech"]["gap"] <= -2.0][:10]

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

    breadth_hist = {
        "updated": now_iso,
        "sp": {str(p): [round(ma_counts[p] / max(ma_totals[p], 1) * 100, 1)] for p in [20, 50, 100, 150, 200]},
        "nq": {str(p): [round(ma_counts[p] / max(ma_totals[p], 1) * 100, 1)] for p in [20, 50, 100, 150, 200]},
        "dates": [now_iso[:10]]
    }

    with open("data/scanner.json", "w", encoding="utf-8") as f:
        json.dump({"updated": now_iso, "rows": scan_rows}, f, separators=(",", ":"))
    with open("data/market.json", "w", encoding="utf-8") as f:
        json.dump(market_data, f, separators=(",", ":"))
    with open("data/prices.json", "w", encoding="utf-8") as f:
        json.dump({"updated": now_iso, "prices": prices_map}, f, separators=(",", ":"))
    with open("data/breadth.json", "w", encoding="utf-8") as f:
        json.dump(breadth_hist, f, separators=(",", ":"))

    cards = []
    try:
        req = urllib.request.Request("https://feeds.finance.yahoo.com/rss/2.0/headline?s=SPY,QQQ,NVDA,AAPL&region=US&lang=en-US", headers={"User-Agent": "Mozilla/5.0"})
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
