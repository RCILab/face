# FACE 홈페이지 수정 계획 및 연구 프레이밍

기준 자료: `../materials/_2026__ICRA___FACE.pdf`, `../materials/FACE (2).pptx`.
레이아웃 기준: `../contact-aware-learning.github.io/index.html` 및 `static/css/index.css`.

## 먼저 유지해야 할 연구의 의미

- 제목: **Contact-Aware Imitation Learning Through Contact Factorization**.
- FACE: **Force Adaptation through Contact-Factor Estimation**.
- 중심 문장: **Preserve intended task behavior while adapting its physical realization to changing contact conditions.**
- 정책이 학습하는 task behavior와 환경에 따른 contact factors(접촉 법선, 마찰 스케일)를 분리한다.
- 관측과 행동 모두 동일한 contact-factorized 표현을 사용한다. Normal loading은 정해진 작동 한계로 정규화하고, tangential loading은 friction-scaled normal loading에 상대적으로 표현한다.
- 학습된 contact-normal estimator와 online friction estimator가 encoder/decoder 양쪽에 쓰인다. 배포 중 정책 파라미터를 갱신하지 않는다. 운동도 접평면 방향으로 조정되므로 단순 force magnitude scaling으로 축소해서 설명하지 않는다.
- 모든 힘이 일정해진다거나, 정책이 온라인 재학습한다거나, 힘 피드백을 넣는 것만이 기여라고 서술하지 않는다.
- 물체 종류별 nominal instance의 시연 200개로 학습한다. 컵 정책 하나로 달걀·닦기를 모두 수행했다고 주장하지 않는다.
- 비교군은 같은 backbone/data를 쓰는 controlled variants다. 특정 외부 방법의 원본 구현보다 우수하다고 주장하지 않는다.
- 성공률: unseen cup surfaces 29/30 (96.7%), unseen cup deformations 13/20 (65%), unseen egg instances 17/25 (68%). Nominal은 제외한다.
- 닦기는 추가 정성 실험이다. 개별 성공 장면을 성공률로 바꾸지 않는다.
- 마찰 추정은 sliding이 제한될 때 어렵다. 완벽한 일반화·안전 보장은 주장하지 않는다.

## 현재 페이지 구성과 편집 기준

1. 익명 제목과 비활성 Paper / GitHub Code 버튼 유지.
2. 버튼 바로 아래 FACE 컵 6개 조건을 2행 × 3열을 유지하며 Trained surface(회색), Unseen geometry(파란색), Unseen friction(초록색) 배경으로 구분하고 각각의 조건명과 공통 캡션 하나로 제시하며, 캡션(슬로건 두 줄과 화살표)은 영상 그리드 위에 둔다. 캡션은 자료의 두 원문 “FACE factorizes interaction to separate task behavior from friction scale and contact normal.”과 “One fixed policy with online adaptation across unseen contact conditions.”을 분리한다. 두 문장 사이에 크고 선명한 채움형 아래 화살표를 두며, 박스나 볼드체는 사용하지 않는다. Nominal에 training 표기를 붙이지 않으며, 별도의 자동 재생 버튼은 두지 않는다.
3. Abstract → 제공된 전체 영상 `ICRA27_3998_VI_i-2.mp4` → How FACE works → 실험 → 닦기 → Contact factor estimation 순서. 전체 영상은 수동 재생이며 원본 전체 구간·화질·속도를 보존한다.
4. 아래 실험에는 상단 6개 FACE 갤러리를 중복 배치하지 않는다. 컵 방법별 비교와 Egg marking을 보여준다. 컵 비교 탭은 티저 범례와 같은 분류명을 앞에 붙인다: `Nominal surface`, `Unseen friction · Wet plastic shell`, `Unseen geometry · Horizontally wrinkled`.
5. Generalization across contact conditions(사용자 요청으로 원래 제목 유지): 닦기 네 조건 × FACE/Direct force를 한 번에 비교. 조건 선택 버튼은 제거한다.
6. Video 바로 아래 How FACE works에 기존 구조도와, 그 아래 PPT의 세 단계(Contact factorization & reparameterization / Online contact estimation / Hybrid compliance control)를 각 두 문장 안팎으로 둔다(한 문장으로 줄였을 때 사용자가 너무 생략했다고 함). 제목은 PPT·구조도 블록과 같고, 문장은 논문 III-B·III-D·IV-B의 핵심(접촉 좌표계, 접평면 모션 투영, 접촉 판정, 입력 이력, 매 청크 재해석, 법선 feedback·접선 feedforward)을 담는다. 구조도는 논문 캡션과 번호를 제외해 사용한다. 별도 하드웨어 섹션은 두지 않는다. Generalization 배경은 흰색이다.
7. 저자·소속·기관 주소·식별 가능한 인용 정보를 표시하지 않는다. 원본 자료는 보존한다.
8. 미디어 출처는 제공 PDF·PPTX·전체 MP4만 허용한다. manifest의 원본·결과 해시를 유지하며 모바일, 키보드, 새로고침·조건 전환 시 자동 재생, 수동 정지를 검증한다. 명시적인 자동 재생 요청에 따라 reduced motion 및 데이터 절약 설정으로 재생을 중단하지 않는다.
9. 닦기 아래 `Contact factor estimation`(id `estimation`; 논문 용어 contact-factor estimation, Fig. 5 제목과 같은 표현): 통제된 선접촉 미끄럼 실험임을 밝히는 한 줄 요약(IV-B 표현) → 논문 Fig. 5 크롭(6쪽, 캡션·번호 제외, `static/images/contact-estimation.png`) → 세부 표 하나(문장 없이 값·수식만; 형상 행과 추정기 행 사이에 진한 구분선 하나). ① 형상별 높이 h(s)[mm]를 행마다 닫힌 식으로(번들 KaTeX로 TeX 조판; 단면·이동을 나눈 표기는 사용자가 비직관적이라고 해서 쓰지 않음). 볼록 세 행은 같은 식 √(R²−(x₀−s)²)−√(R²−x₀²)을 쓰고, x₀는 초기 접촉점에서 정점까지의 부호 있는 거리다. 그래서 convex A 오르막(x₀ 150)과 내리막(x₀ −37.7)은 같은 면을 반대 방향으로 지나는 것이 x₀ 부호로 드러난다(R 540). concave A(e^{s/λ}−1)(A 8.47, λ 150; 지그 프로파일 z(x′)=20+32.14(e^{−x′/150}−e^{−4/3})를 낮은 끝에서 출발해 전개한 것과 동일), convex B(R 1043.8, x₀ 253.5). 표 위 한 줄로 s(초기 접촉점에서의 수평 이동거리, 0 ≤ s ≲ 150 mm: 등록 결과의 형상별 이동거리 중앙값 130–155 mm)와 x₀만 정의. 추정기 행: 법선은 백본(2-layer GRU, hidden 96)만, 마찰은 scalar Kalman(μ₀ 0.12, 0.3 s 미끄럼 후 첫 갱신). 학습 재질·형상·학습 제외 조건은 그림에 있으므로 넣지 않는다. 손실·증강·입력 채널, 결과 수치, 다른 지표의 내부 수치(α≥0.8 평균 각오차 등), 에피소드 수, 하이퍼파라미터, 코드 경로도 넣지 않는다. 법선 추정기의 자세 입력은 초기 자세 대비 상대 회전(논문 III-D)이며 중력 방향이 아니다.
10. 정렬: 섹션·소제목(h2·h3)과 방법 열 제목은 가운데, 본문 글(섹션 설명, 소제목 설명, 주석)은 왼쪽이며 콘텐츠 폭 전체를 쓴다. Abstract는 레퍼런스처럼 양쪽 정렬, 티저 슬로건 두 줄은 레퍼런스 티저 부제처럼 가운데.
11. 각 제목 아래 설명은 레퍼런스(Nerfies)의 'you can …'처럼 FACE로 무엇이 가능한지 서술하는 1–2문장으로 쓴다. 'We …'로 시작하는 실험 보고체는 쓰지 않는다(원문 그대로인 Abstract는 예외). 논문 사실과 어긋나는 수치·일반화 주장은 넣지 않는다.
12. 페이지 글(설명·주석·표·스크린리더 라벨)에 세미콜론, 콜론, em dash(대시 포함)를 쓰지 않는다. 쉼표·괄호·문장 분리로 대신한다. 예외는 브라우저 탭 제목과 공유 메타 제목의 “FACE: …” 형식과 원문 그대로인 Abstract뿐이다.

## Abstract 원문 유지

Abstract는 제공 PDF의 “Generalizable contact-rich manipulation”부터 “to our setting.”까지 연구 초록 전체를 그대로 사용한다. PDF의 행바꿈·조판용 단어 분할만 정리한다. 익명성 요구 때문에 기관 주소가 포함된 마지막 프로젝트 링크 안내문만 제외하며, 그 밖의 문장 발췌·요약·재작성이나 볼드체는 사용하지 않는다.
