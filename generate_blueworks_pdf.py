"""
블루웍스 로봇제어 AI에이전트 소프트웨어 개발자 전용 포트폴리오 PDF 생성기
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ── 한글 폰트 등록 ──────────────────────────────────────────────────────────
FONT_DIR = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")

def reg(name, filename):
    path = os.path.join(FONT_DIR, filename)
    if os.path.exists(path):
        pdfmetrics.registerFont(TTFont(name, path))
        return True
    return False

# Malgun Gothic (맑은 고딕) – Windows 기본 한글 폰트
has_malgun = reg("Malgun", "malgun.ttf") and reg("MalgunBd", "malgunbd.ttf")
if has_malgun:
    FONT_N = "Malgun"
    FONT_B = "MalgunBd"
else:
    FONT_N = "Helvetica"
    FONT_B = "Helvetica-Bold"

# ── 컬러 팔레트 ────────────────────────────────────────────────────────────
C_NAVY   = colors.HexColor("#1A2B4A")   # 헤더 배경
C_BLUE   = colors.HexColor("#2563EB")   # 섹션 라인 / 강조
C_ACCENT = colors.HexColor("#0EA5E9")   # 태그 배경
C_LIGHT  = colors.HexColor("#F1F5F9")   # 행 배경
C_TEXT   = colors.HexColor("#1E293B")   # 본문
C_MUTED  = colors.HexColor("#64748B")   # 부제목

PAGE_W, PAGE_H = A4
ML = 18*mm; MR = 18*mm; MT = 14*mm; MB = 16*mm

# ── 스타일 ─────────────────────────────────────────────────────────────────
def S(name, **kw):
    base = dict(fontName=FONT_N, fontSize=9, leading=13,
                textColor=C_TEXT, spaceAfter=0, spaceBefore=0)
    base.update(kw)
    return ParagraphStyle(name, **base)

sName     = S("name",    fontName=FONT_B, fontSize=22, textColor=colors.white,
              leading=26, alignment=TA_CENTER)
sTitle    = S("title",   fontName=FONT_N, fontSize=11, textColor=colors.HexColor("#BAE6FD"),
              leading=15, alignment=TA_CENTER)
sContact  = S("contact", fontName=FONT_N, fontSize=8,  textColor=colors.HexColor("#CBD5E1"),
              leading=11, alignment=TA_CENTER)

sSec      = S("sec",  fontName=FONT_B, fontSize=12, textColor=C_NAVY, leading=16,
              spaceBefore=10, spaceAfter=2)
sJob      = S("job",  fontName=FONT_B, fontSize=10, textColor=C_NAVY, leading=14)
sSub      = S("sub",  fontName=FONT_N, fontSize=8.5, textColor=C_MUTED, leading=12)
sDate     = S("date", fontName=FONT_N, fontSize=8,  textColor=C_MUTED, leading=12,
              alignment=TA_LEFT)
sBody     = S("body", fontName=FONT_N, fontSize=8.5, textColor=C_TEXT, leading=13,
              alignment=TA_JUSTIFY)
sBullet   = S("bul",  fontName=FONT_N, fontSize=8.5, textColor=C_TEXT, leading=13,
              leftIndent=8, bulletIndent=0)
sTag      = S("tag",  fontName=FONT_B, fontSize=7.5, textColor=C_BLUE, leading=10)
sTableHdr = S("th",   fontName=FONT_B, fontSize=8,  textColor=colors.white, leading=11,
              alignment=TA_CENTER)
sTableCel = S("td",   fontName=FONT_N, fontSize=8,  textColor=C_TEXT, leading=11,
              alignment=TA_CENTER)
sTableCelL= S("tdl",  fontName=FONT_N, fontSize=8,  textColor=C_TEXT, leading=11)
sTableCelB= S("tdb",  fontName=FONT_B, fontSize=8,  textColor=C_TEXT, leading=11)

def HR():
    return HRFlowable(width="100%", thickness=1.5, color=C_BLUE,
                      spaceAfter=4, spaceBefore=2)

def HRThin():
    return HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#CBD5E1"),
                      spaceAfter=3, spaceBefore=3)

def SP(h=4):
    return Spacer(1, h)

def section(title):
    return [SP(6), Paragraph(title, sSec), HR()]

def bullet(text):
    return Paragraph(f"• {text}", sBullet)

def tech_tags(text):
    """기술 스택 태그처럼 보이는 텍스트"""
    return Paragraph(f'<font color="#2563EB"><b>[ {text} ]</b></font>', sTag)

# ── 경험/프로젝트 블록 ─────────────────────────────────────────────────────
def exp_block(company, role, period, desc_lines, last=False):
    items = []
    header_data = [[
        Paragraph(company, sJob),
        Paragraph(period,  sDate)
    ]]
    header_tbl = Table(header_data,
                       colWidths=[PAGE_W - ML - MR - 42*mm, 40*mm])
    header_tbl.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("RIGHTPADDING", (1,0), (1,0), 0),
        ("LEFTPADDING", (0,0), (0,0), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 1),
        ("TOPPADDING", (0,0), (-1,-1), 1),
    ]))
    items.append(header_tbl)
    items.append(Paragraph(role, sSub))
    items.append(SP(3))
    for line in desc_lines:
        if line.startswith("##"):
            items.append(Paragraph(f'<b>{line[2:].strip()}</b>',
                                   S("h3", fontName=FONT_B, fontSize=8.5,
                                     textColor=C_NAVY, leading=13,
                                     spaceBefore=4, spaceAfter=1)))
        elif line.startswith("•"):
            items.append(bullet(line[1:].strip()))
        elif line.startswith("TECH:"):
            items.append(SP(2))
            items.append(tech_tags(line[5:].strip()))
        else:
            items.append(Paragraph(line, sBody))
    if not last:
        items.append(HRThin())
    return KeepTogether(items)

# ── 수상/자격증 테이블 ──────────────────────────────────────────────────────
def make_table(header, rows, col_widths, last_col_bold=False):
    data = [[Paragraph(h, sTableHdr) for h in header]]
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            if i == 1 and last_col_bold:
                cells.append(Paragraph(cell, sTableCelB))
            elif i == 0:
                cells.append(Paragraph(cell, sTableCel))
            else:
                cells.append(Paragraph(cell, sTableCelL))
        data.append(cells)

    tbl = Table(data, colWidths=col_widths)
    style = [
        ("BACKGROUND",    (0,0), (-1,0),  C_NAVY),
        ("TEXTCOLOR",     (0,0), (-1,0),  colors.white),
        ("FONTNAME",      (0,0), (-1,0),  FONT_B),
        ("FONTSIZE",      (0,0), (-1,0),  8),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.white, C_LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
    ]
    tbl.setStyle(TableStyle(style))
    return tbl

# ── 헤더 (이름/타이틀/연락처) ──────────────────────────────────────────────
def build_header():
    name_p    = Paragraph("조윤하  Cho Yun Ha", sName)
    title_p   = Paragraph("산업용 AI 추론 · RAG 에이전트 · 실시간 미들웨어 개발자", sTitle)
    contact_p = Paragraph(
        "jojojo7391@gmail.com  ·  010-5440-5086  ·  "
        "github.com/JoeYunHa  ·  인하대학교 컴퓨터공학과 2026.08 졸업예정",
        sContact
    )
    inner = Table(
        [[name_p], [SP(3)], [title_p], [SP(4)], [contact_p]],
        colWidths=[PAGE_W - ML - MR]
    )
    inner.setStyle(TableStyle([
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING",   (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0), (-1,-1), 0),
    ]))
    outer = Table([[inner]], colWidths=[PAGE_W - ML - MR])
    outer.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), C_NAVY),
        ("LEFTPADDING",  (0,0), (-1,-1), 14),
        ("RIGHTPADDING", (0,0), (-1,-1), 14),
        ("TOPPADDING",   (0,0), (-1,-1), 14),
        ("BOTTOMPADDING",(0,0), (-1,-1), 14),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), 4),
    ]))
    return outer

# ── About ──────────────────────────────────────────────────────────────────
def build_about():
    items = section("■  핵심 역량 요약")
    about_text = (
        "<b>Python · Node.js 중심으로 산업용 AI 추론 파이프라인, IPC 기반 미들웨어, "
        "실시간 데이터 처리 시스템을 구현해온 개발자</b>입니다. "
        "Java/Spring Boot 기반 REST API 연동 경험도 보유하고 있습니다. "
        "원자력 발전소 진동 감시 시스템(RCPVMS)과 산업용 계측 데이터 통합 처리 앱(NIMS I/O Simulator)을 "
        "실제 납품 환경에서 설계·구현했습니다. "
        "LangChain · AWS Bedrock 기반 RAG 에이전트를 서비스에 직접 적용했으며, "
        "Electron/Node.js · Python · C++ N-API를 연동하는 멀티 런타임 아키텍처를 설계합니다."
    )
    items.append(Paragraph(about_text, sBody))
    items.append(SP(6))

    skill_data = [
        [Paragraph("주력 언어", sTableHdr),
         Paragraph("Python · Node.js (JS/TS) · C++   /   Java/Spring Boot (연동 경험)", sTableCelL)],
        [Paragraph("AI / ML", sTableHdr),
         Paragraph("PyTorch · LangChain · AWS Bedrock · XGBoost  (RAG · 이상탐지 · OOD 탐지)", sTableCelL)],
        [Paragraph("실시간 시스템", sTableHdr),
         Paragraph("WebSocket · IPC 프로토콜 설계 · 바이너리 파싱 · Daemon Pool", sTableCelL)],
        [Paragraph("Cloud & Infra", sTableHdr),
         Paragraph("AWS (Lambda · EC2 · RDS · S3 · API GW) · Docker · Nginx · Redis", sTableCelL)],
        [Paragraph("Frameworks", sTableHdr),
         Paragraph("FastAPI · Spring Boot · Electron", sTableCelL)],
    ]
    CW = PAGE_W - ML - MR
    tbl = Table(skill_data, colWidths=[28*mm, CW - 28*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,-1), C_NAVY),
        ("TEXTCOLOR",     (0,0), (0,-1), colors.white),
        ("FONTNAME",      (0,0), (0,-1), FONT_B),
        ("ROWBACKGROUNDS",(1,0), (1,-1), [colors.white, C_LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#E2E8F0")),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
    ]))
    items.append(tbl)
    return items

# ── Experience ─────────────────────────────────────────────────────────────
def build_experience():
    items = section("■  경력")

    items.append(exp_block(
        company="RealGain — 기술 자문 계약직",
        role="AI 추론 엔진 · 산업 제어 소프트웨어 개발",
        period="2026.02 – 2026.06",
        desc_lines=[
            "TECH: Python 3.11 · PyTorch · Electron · Node.js · TypeScript · NumPy · SciPy · Matplotlib",
            "## AI 추론 파이프라인 (산업용 실시간 추론 · 장애 복구)",
            "• 원자력 발전소 RCP 진동 감시 시스템 RCPVMS 단독 설계·구현 — 오프라인 AI 추론 엔진 + Electron 데스크톱 앱",
            "• 3계층 탐지: 앙상블(ResNet18 + OrbitCNN1D) → OOD 탐지(max_conf + TV Distance) → Transformer MAE. 각 계층 독립 Graceful Degradation",
            "• 물리 정보 인코딩: Im(Gxy) 교차 스펙트럼 허수부로 와류 회전 방향을 4채널 스펙트로그램에 명시 인코딩",
            "• XAI: Integrated Gradients(30-step) + GradCAM 히트맵으로 예측 근거 시각화",
            "• Grid Search 가중치 최적화: 목적함수 val_acc * (1 - ood_fp_rate)  [검증 정확도 극대화 + OOD 오탐률 최소화]",
            "## Hot-Standby 추론 서버 (저지연 IPC · self-healing)",
            "• Python Daemon Pool: 모델 사전 적재(콜드 스타트 0), 워커 크래시 자동 재시작, 동적 pool.resize(1~4)",
            "• Node.js IPC ↔ Python inference daemon 간 커스텀 바이너리 프로토콜로 저지연 통신",
        ],
    ))

    items.append(exp_block(
        company="RealGain — 현장실습",
        role="멀티 런타임 산업용 데스크톱 앱 개발",
        period="2026.01 – 2026.02",
        desc_lines=[
            "TECH: Electron 28 · Node.js · React 18 · TypeScript · Python · C++ N-API · NumPy · Canvas 2D",
            "• 원자력 감시 계통(NIMS) 데이터 통합 처리 앱 — LPMS · ALMS · RCPVMS · IVMS 4종 + DMD 포맷 지원. 전체 단독 개발",
            "• Electron/Node.js UI ↔ Python 파싱 엔진 ↔ C++ N-API Addon을 연동한 멀티 런타임 구조 설계",
            "• 커스텀 바이너리 IPC 프로토콜 설계(매직넘버 + 정렬 패딩 + 하이브리드 JSON/Binary): 전송 크기 61% 감소, 역직렬화 218× 향상",
            "• DLL 비스레드 안전 → C++ 단일 전용 워커 스레드 + TSFN 패턴으로 해결",
            "• Canvas 2D 뷰포트 다운샘플 렌더러로 수백만 샘플 파형 고성능 렌더링",
        ],
        last=True,
    ))
    return items

# ── Projects ───────────────────────────────────────────────────────────────
def build_projects():
    items = section("■  프로젝트")

    items.append(exp_block(
        company="kindMap — 교통약자 최적 경로 탐색 서비스",
        role="팀장 | AI 챗봇/RAG · 경로 탐색 엔진 · 시스템 아키텍처 담당",
        period="2025.08 – 2025.11",
        desc_lines=[
            "TECH: Python · FastAPI · AWS · Docker · Nginx · C++ · XGBoost · LangChain · AWS Bedrock · PostgreSQL",
            "## RAG 기반 AI 챗봇 구현 (agentic workflow)",
            "• AWS Bedrock + LangChain 기반 지하철 편의시설 RAG 챗봇 구현 (자연어 질의 → 벡터 검색 → LLM 응답)",
            "• AWS Lambda + RDS 서버리스 아키텍처로 챗봇 백엔드 독립 운영",
            "## 고성능 탐색 엔진 (그래프 탐색 최적화 · 상태공간 pruning)",
            "• 경로 탐색 엔진 단독 설계: Predecessor pointer 경량화, epsilon-pruning, C++ 탐색 엔진, 토폴로지 캐시(O(1) 조회), Marking 전략",
            "• 탐색 시간 19분 → 1초 이내 (서울 지하철 실데이터, t3.medium 기준), RPS 75배 향상 (로컬 부하 테스트 실측)",
            "• XGBoost 서울 지하철 혼잡도 예측 모델 (R² 0.9151)",
        ],
    ))

    items.append(exp_block(
        company="수담(手談) — 실시간 양방향 수어 번역 AI 서비스",
        role="기술 총 책임자 | 백엔드 전체 · AI 파이프라인 · 실시간 통신 담당",
        period="2025.07 – 2025.09",
        desc_lines=[
            "TECH: Python · FastAPI · WebSocket · Redis · AWS · Claude API",
            "• AI I/O Spec 미확정 블로커 → 초기 모델 직접 이식, 선제적 테스트 환경 구축",
            "• 프록시 계층 제거 후 AI 서버 ↔ WebSocket 직접 연결 아키텍처로 재설계",
            "• 정적 데이터 캐시 사전 적재로 불필요한 DB 접근 제거 (O(1) 조회)",
            "• WebSocket 응답 시간 1,000ms → 100ms (로컬 단일 클라이언트 부하 테스트 실측, 90% 이상 감소)",
        ],
        last=True,
    ))
    return items

# ── Education & Awards ─────────────────────────────────────────────────────
def build_edu_awards():
    items = section("■  학력 · 수상 · 자격증 · 활동")

    # 학력
    items.append(Paragraph("<b>학력</b>", S("h4", fontName=FONT_B, fontSize=9,
                                            textColor=C_NAVY, leading=13)))
    items.append(SP(2))
    edu_data = [["학교", "전공", "기간"]]
    edu_data.append(["인하대학교", "컴퓨터공학과", "2020 – 2026.08 (졸업예정)"])
    CW = PAGE_W - ML - MR
    items.append(make_table(
        ["학교", "전공", "기간"],
        [["인하대학교", "컴퓨터공학과", "2020 – 2026.08 (졸업예정)"]],
        [35*mm, 50*mm, CW - 85*mm]
    ))
    items.append(SP(8))

    # 수상
    items.append(Paragraph("<b>수상</b>", S("h4", fontName=FONT_B, fontSize=9,
                                            textColor=C_NAVY, leading=13)))
    items.append(SP(2))
    award_rows = [
        ["2025.06", "Korea Software Empowerment Bootcamp MINI PROJECT 우수 교육생", "정보통신기획평가원"],
        ["2025.08", "K-SoftVation Showcase 우수상", "정보통신기획평가원"],
        ["2025.10", "2025 오픈소스SW 페스티벌 프로젝트 부문 최우수상 (총장상)", "인하대학교 SW중심대학사업단"],
        ["2025.12", "탄소중립 INNOVACATION ACADEMY 대상 (개인역량 강화 부문)", "인하대학교 SW중심대학사업단"],
        ["2025.12", "탄소중립 INNOVACATION ACADEMY 최종 발표회 대상 (팀 프로젝트 부문)", "인하대학교 SW중심대학사업단"],
    ]
    items.append(make_table(
        ["날짜", "수상명", "주관"],
        award_rows,
        [18*mm, CW - 68*mm, 50*mm]
    ))
    items.append(SP(8))

    # 자격증
    items.append(Paragraph("<b>자격증</b>", S("h4", fontName=FONT_B, fontSize=9,
                                              textColor=C_NAVY, leading=13)))
    items.append(SP(2))
    cert_rows = [
        ["2026.03.27", "SQLD (SQL 개발자)", "한국데이터산업진흥원"],
        ["2025.09.11", "AWS Certified Cloud Practitioner (Foundational)", "Amazon Web Services"],
        ["2025.12.31", "탄소중립 SW/AI 엔지니어 인증서  등급: A", "인하대학교 SW중심대학사업단"],
        ["2025.05.24", "TOPCIT 수준 3", "정보통신기획평가원"],
    ]
    items.append(make_table(
        ["취득일", "자격증명", "발급기관"],
        cert_rows,
        [22*mm, CW - 72*mm, 50*mm]
    ))
    items.append(SP(8))

    # 교육·활동
    items.append(Paragraph("<b>교육 및 활동</b>", S("h4", fontName=FONT_B, fontSize=9,
                                                    textColor=C_NAVY, leading=13)))
    items.append(SP(2))
    for act in [
        "2025년 K-Software Empowerment Bootcamp 4기 수료 (2025.01 – 2025.11) — 정보통신기획평가원",
        "2025년 탄소중립 INNOVACATION ACADEMY 4기 수료 (2025.08 – 2025.12) — 인하대학교 SW중심대학사업단",
        "Start-Up K-Shield Jr. 수료 (80H)",
    ]:
        items.append(bullet(act))

    return items

# ── 메인 빌드 ───────────────────────────────────────────────────────────────
def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=ML, rightMargin=MR,
        topMargin=MT, bottomMargin=MB,
        title="조윤하 포트폴리오 — 블루웍스 로봇제어 AI에이전트 개발자",
        author="조윤하 Cho Yun Ha",
    )

    story = []
    story.append(build_header())
    story.append(SP(10))

    story += build_about()
    story += build_experience()
    story += build_projects()
    story += build_edu_awards()

    doc.build(story)
    print(f"[OK] PDF 생성 완료: {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "portfolio_blueworks_조윤하.pdf")
    build_pdf(out)
