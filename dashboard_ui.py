"""Pastel dashboard landing page backed by the app's existing session data."""
from __future__ import annotations

import html
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st


PALETTE = ["#5B9CF6", "#F05278", "#22B98A", "#F4BE3E", "#8B73EF", "#20A7C9"]


def _e(value) -> str:
    return html.escape(str(value or ""))


def _money(value) -> str:
    return f"{float(value or 0):,.0f}원"


def _logo(name: str, code: str, index: int = 0) -> str:
    known = {
        "005930": ("S", "#4A90EE"),
        "000660": ("SK", "#F04464"),
        "035420": ("N", "#20BC83"),
        "035720": ("K", "#F4C53F"),
        "005380": ("H", "#176CB7"),
    }
    mark, color = known.get(str(code), ((_e(name)[:1] or "•").upper(), PALETTE[index % len(PALETTE)]))
    return f'<span class="sd-logo" style="background:{color}">{mark}</span>'


def _stock_rows(state: dict) -> list[dict]:
    rows = []
    for stock in state.get("stocks", [])[:6]:
        report = stock.get("report") or {}
        snapshot = stock.get("price_snapshot") or {}
        rows.append({
            "name": stock.get("name", "종목"),
            "code": stock.get("code", ""),
            "price": report.get("price") or snapshot.get("price"),
        })
    return rows


def _holdings() -> list[dict]:
    snapshot = st.session_state.get("account_snapshot") or {}
    rows = []
    for position in snapshot.get("positions", [])[:6]:
        value = float(position.get("value") or 0)
        pnl = float(position.get("pnl") or 0)
        invested = value - pnl
        rate = (pnl / invested * 100) if invested else None
        rows.append({**position, "return_rate": rate})
    return rows


def _news(state: dict) -> list[dict]:
    notices = []
    for stock in state.get("stocks", []):
        for item in (stock.get("report") or {}).get("disclosures", []):
            notices.append({**item, "company": stock.get("name", "")})
    return sorted(notices, key=lambda item: item.get("date", ""), reverse=True)[:4]


def _overview(holdings: list[dict]) -> tuple[float, float, int]:
    snapshot = st.session_state.get("account_snapshot") or {}
    value = float(snapshot.get("value") or sum(float(row.get("value") or 0) for row in holdings))
    pnl = float(snapshot.get("pnl") or sum(float(row.get("pnl") or 0) for row in holdings))
    return value, pnl, len(holdings)


def render_dashboard(state: dict, sample_mode: bool = False):
    watchlist = _stock_rows(state)
    holdings = _holdings()
    notices = _news(state)
    total_value, total_pnl, count = _overview(holdings)
    invested = total_value - total_pnl
    return_rate = (total_pnl / invested * 100) if invested else None
    now = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y. %m. %d. %H:%M")

    holding_rows = "".join(
        f"""
        <div class="sd-table-row sd-holding-row">
          <div class="sd-stock">{_logo(row.get('name',''), row.get('code',''), i)}<span><b>{_e(row.get('name'))}</b><small>{_e(row.get('code'))}</small></span></div>
          <b>{_money(row.get('value'))}</b>
          <span class="{'sd-up' if (row.get('return_rate') or 0) >= 0 else 'sd-down'}">{row.get('return_rate'):+.1f}%</span>
          <span>{float(row.get('weight') or 0):.1f}%</span>
        </div>"""
        for i, row in enumerate(holdings)
    ) or '<div class="sd-empty">계좌를 연결하면 보유종목과 실제 평가금액이 표시됩니다.</div>'

    watch_rows = "".join(
        f"""
        <div class="sd-table-row sd-watch-row">
          <div class="sd-stock">{_logo(row['name'], row['code'], i)}<span><b>{_e(row['name'])}</b><small>{_e(row['code'])}</small></span></div>
          <b>{_money(row['price']) if row.get('price') else '분석 대기'}</b>
          <span class="sd-muted">공식 데이터</span>
        </div>"""
        for i, row in enumerate(watchlist)
    ) or '<div class="sd-empty">관심종목을 추가하면 이곳에서 한눈에 확인할 수 있습니다.</div>'

    news_rows = "".join(
        f"""<a class="sd-news-row" href="{_e(item.get('url','#'))}" target="_blank">
          <span class="sd-news-thumb">{_e(item.get('company',''))[:2] or '공시'}</span>
          <span><b>{_e(item.get('title','최근 공시'))}</b><small>{_e(item.get('date',''))} · {_e(item.get('company',''))}</small></span>
        </a>"""
        for item in notices
    ) or '<div class="sd-empty">종목 분석 후 최신 공시와 주요 소식이 표시됩니다.</div>'

    value_text = _money(total_value) if holdings else "계좌 연결 대기"
    pnl_text = f"{total_pnl:+,.0f}원" if holdings else "—"
    rate_text = f"{return_rate:+.2f}%" if return_rate is not None else "—"

    st.markdown(
        f"""
<style>
.block-container {{max-width:1540px!important;padding-top:.7rem!important}}
.sd-shell {{color:#172847}}
.sd-topbar {{display:flex;justify-content:space-between;align-items:center;margin:0 0 16px}}
.sd-title {{display:flex;align-items:center;gap:12px;font-size:26px;font-weight:850;letter-spacing:-.05em}}
.sd-bars {{display:flex;align-items:flex-end;gap:3px;height:27px}}
.sd-bars i {{display:block;width:6px;border-radius:4px 4px 1px 1px;background:linear-gradient(#52a9ef,#756af1)}}
.sd-bars i:nth-child(1){{height:10px}} .sd-bars i:nth-child(2){{height:18px}} .sd-bars i:nth-child(3){{height:25px}}
.sd-date {{color:#8a96ad;font-size:12px}}
.sd-grid {{display:grid;grid-template-columns:minmax(0,1.65fr) minmax(420px,1fr);gap:14px}}
.sd-left,.sd-right {{display:grid;gap:14px;align-content:start}}
.sd-card {{background:rgba(255,255,255,.94);border:1px solid #e3e9f3;border-radius:18px;padding:18px 20px;box-shadow:0 10px 32px rgba(69,92,133,.06);overflow:hidden}}
.sd-tint-mint {{background:linear-gradient(135deg,#fff,#f2fffb)}} .sd-tint-peach {{background:linear-gradient(135deg,#fff,#fff7f3)}}
.sd-card-head {{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}}
.sd-card h3 {{margin:0;font-size:18px;letter-spacing:-.035em}} .sd-more {{color:#8d82ed;font-size:12px;font-weight:750}}
.sd-overview {{display:grid;grid-template-columns:1.6fr repeat(3,1fr);gap:0;align-items:center}}
.sd-overview>div {{padding:4px 18px;border-left:1px solid #e6ebf3}} .sd-overview>div:first-child {{border:0;padding-left:0}}
.sd-label {{color:#7d8aa2;font-size:12px;margin-bottom:7px}} .sd-main-value {{font-size:30px;font-weight:850;letter-spacing:-.04em}}
.sd-value {{font-size:18px;font-weight:800}} .sd-up {{color:#0aad83!important;font-weight:750}} .sd-down {{color:#f04d74!important;font-weight:750}} .sd-muted {{color:#8c98ad}}
.sd-indexes {{display:grid;grid-template-columns:repeat(4,1fr);gap:0}} .sd-index {{padding:0 13px;border-left:1px solid #e9edf4}} .sd-index:first-child{{border:0;padding-left:0}}
.sd-index b {{display:block;margin:7px 0;color:#314361}} .sd-spark {{width:100%;height:28px;margin-top:7px}}
.sd-chart-card {{min-height:360px}} .sd-tabs {{display:flex;gap:5px;background:#f3f5fa;border-radius:12px;padding:3px;width:max-content;margin-bottom:12px}}
.sd-tab {{padding:6px 20px;border-radius:10px;font-size:12px;color:#69768e}} .sd-tab.active {{background:linear-gradient(135deg,#8a7cf1,#706ce9);color:white}}
.sd-chart {{height:255px;position:relative;background:repeating-linear-gradient(to bottom,transparent 0,transparent 50px,#edf0f6 51px),repeating-linear-gradient(to right,transparent 0,transparent 145px,#f1f3f8 146px);border-radius:10px}}
.sd-chart svg {{width:100%;height:100%}} .sd-chart-empty {{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#8c98ad;font-size:13px}}
.sd-table-head,.sd-table-row {{display:grid;align-items:center;gap:12px;padding:9px 10px}} .sd-table-head {{background:#f6f8fc;border-radius:9px;color:#78869d;font-size:11px}}
.sd-holding-row,.sd-holdings-head {{grid-template-columns:1.55fr 1fr .75fr .55fr}} .sd-watch-row,.sd-watch-head {{grid-template-columns:1.45fr .8fr .7fr}}
.sd-table-row {{border-bottom:1px solid #eef1f6;font-size:12px}} .sd-table-row:last-child{{border:0}}
.sd-stock {{display:flex;align-items:center;gap:9px;min-width:0}} .sd-stock span:last-child{{display:flex;flex-direction:column;min-width:0}} .sd-stock small,.sd-news-row small {{color:#9aa5b8;font-size:9px;margin-top:2px}}
.sd-logo {{width:29px;height:29px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;flex:none;color:#fff;font-size:10px;font-weight:850}}
.sd-lower {{display:grid;grid-template-columns:1.2fr .8fr;gap:14px}} .sd-empty {{padding:32px 12px;text-align:center;color:#929db0;font-size:12px}}
.sd-ranking-tabs {{display:flex;background:#f4f7fa;border-radius:999px;overflow:hidden;margin-bottom:12px}} .sd-ranking-tabs span {{width:50%;padding:8px;text-align:center;font-size:12px}} .sd-ranking-tabs span:first-child{{background:#e7fbf4;color:#0b9f78;font-weight:800}}
.sd-rank-row {{display:grid;grid-template-columns:24px 1fr auto;gap:8px;padding:11px 4px;border-bottom:1px solid #eff2f6;font-size:12px}}
.sd-news-row {{display:flex;gap:10px;align-items:center;padding:8px 0;border-bottom:1px solid #eff2f6;color:#263754;text-decoration:none}} .sd-news-row:last-child{{border:0}} .sd-news-row>span:last-child{{display:flex;flex-direction:column;font-size:11px}}
.sd-news-thumb {{width:58px;height:38px;border-radius:9px;background:linear-gradient(135deg,#dce9fa,#eee8ff);display:flex;align-items:center;justify-content:center;color:#627391;font-size:11px;font-weight:800;flex:none}}
@media(max-width:1100px){{.sd-grid{{grid-template-columns:1fr}}.sd-right{{grid-template-columns:1fr 1fr}}.sd-right .sd-index-card,.sd-right .sd-watch-card{{grid-column:1/-1}}}}
@media(max-width:760px){{.sd-overview{{grid-template-columns:1fr 1fr}}.sd-overview>div{{border:0;padding:8px}}.sd-indexes{{grid-template-columns:1fr 1fr;gap:15px}}.sd-lower,.sd-right{{grid-template-columns:1fr}}.sd-right>*{{grid-column:auto!important}}.sd-main-value{{font-size:23px}}}}
</style>
<div class="sd-shell">
  <div class="sd-topbar"><div class="sd-title"><span class="sd-bars"><i></i><i></i><i></i></span>주식 대시보드</div><div class="sd-date">{now} KST</div></div>
  <div class="sd-grid">
    <section class="sd-left">
      <article class="sd-card sd-tint-mint">
        <div class="sd-card-head"><h3>총 자산 현황</h3><span class="sd-more">조회 시점 기준</span></div>
        <div class="sd-overview"><div><div class="sd-label">국내주식 평가액</div><div class="sd-main-value">{value_text}</div></div><div><div class="sd-label">보유 종목 수</div><div class="sd-value">{count if holdings else '—'}</div></div><div><div class="sd-label">평가 손익</div><div class="sd-value {'sd-up' if total_pnl >= 0 else 'sd-down'}">{pnl_text}</div></div><div><div class="sd-label">수익률</div><div class="sd-value {'sd-up' if (return_rate or 0) >= 0 else 'sd-down'}">{rate_text}</div></div></div>
      </article>
      <article class="sd-card sd-chart-card"><div class="sd-card-head"><h3>포트폴리오 수익률</h3><span class="sd-more">내 포트폴리오</span></div><div class="sd-tabs"><span class="sd-tab active">1개월</span><span class="sd-tab">3개월</span><span class="sd-tab">6개월</span><span class="sd-tab">1년</span></div><div class="sd-chart"><svg viewBox="0 0 800 250" preserveAspectRatio="none"><defs><linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8275ee" stop-opacity=".20"/><stop offset="1" stop-color="#8275ee" stop-opacity="0"/></linearGradient></defs><path d="M15,210 L95,194 L170,184 L250,164 L330,150 L410,135 L490,112 L570,105 L650,83 L780,62 L780,235 L15,235 Z" fill="url(#area)"/><path d="M15,210 L95,194 L170,184 L250,164 L330,150 L410,135 L490,112 L570,105 L650,83 L780,62" fill="none" stroke="#7f72ed" stroke-width="3"/></svg>{'' if holdings else '<div class="sd-chart-empty">계좌 연결 후 기간별 수익률 이력이 표시됩니다.</div>'}</div></article>
      <div class="sd-lower"><article class="sd-card"><div class="sd-card-head"><h3>▰&nbsp; 보유종목</h3><span class="sd-more">전체보기 ›</span></div><div class="sd-table-head sd-holdings-head"><span>종목</span><span>평가금액</span><span>수익률</span><span>비중</span></div>{holding_rows}</article><article class="sd-card"><div class="sd-card-head"><h3>오늘의 상승/하락 상위</h3></div><div class="sd-ranking-tabs"><span>상승률 상위</span><span>하락률 상위</span></div><div class="sd-empty">시장 순위 API를 연결하면 실시간 상위 종목이 표시됩니다.</div></article></div>
    </section>
    <aside class="sd-right">
      <article class="sd-card sd-tint-peach sd-index-card"><div class="sd-card-head"><h3>주요 지수</h3><span class="sd-more">더보기 ›</span></div><div class="sd-indexes">{''.join(f'<div class="sd-index"><span class="sd-label">{name}</span><b>연결 대기</b><span class="sd-muted">시장 지수 API</span><svg class="sd-spark" viewBox="0 0 100 25"><path d="M2 20 L18 17 L31 19 L45 11 L58 14 L72 8 L98 5" fill="none" stroke="#37c5a3" stroke-width="2"/></svg></div>' for name in ['코스피','코스닥','S&P 500','나스닥'])}</div></article>
      <article class="sd-card sd-watch-card"><div class="sd-card-head"><h3>관심종목</h3><span class="sd-more">더보기 ›</span></div><div class="sd-table-head sd-watch-head"><span>종목명</span><span>현재가</span><span>상태</span></div>{watch_rows}</article>
      <article class="sd-card"><div class="sd-card-head"><h3>주요 뉴스</h3><span class="sd-more">더보기 ›</span></div>{news_rows}</article>
    </aside>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if sample_mode:
        st.caption("현재는 가상 예시 모드입니다. 계좌와 공식 데이터 API를 연결하면 실제 값으로 채워집니다.")
