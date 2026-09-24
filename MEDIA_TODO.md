# 추가 영상 재료 교체 목록

현재 페이지는 논문 그림과 최종 영상으로 구성되어 있습니다. 개별 영상이 없는 영역은 **최종 영상의 실제 프레임 + Individual clip coming soon**으로 표시합니다. 깨진 링크나 가짜 재생 버튼은 없습니다.

| 위치 | 가져올 재료 | 권장 파일명 | 현재 연결 |
| --- | --- | --- | --- |
| Paper cups | nominal / vertical & horizontal wrinkles / PVC tape / plastic / wet plastic 비교 | `static/videos/cup-comparison.mp4` | 최종 영상 00:48 |
| Eggs | FACE와 네 비교 방법의 egg marking 영상 | `static/videos/egg-comparison.mp4` | 최종 영상 01:24 |
| Surface wiping | nominal / wet / soapy / unseen material & geometry 비교 | `static/videos/wiping-comparison.mp4` | 최종 영상 02:12 |
| Hardware (선택) | handheld demonstration 원본 | `static/videos/handheld-demo.mp4` | 논문 Figure 3 |
| Method (선택) | encoder / decoder / contact estimation 애니메이션 원본 | `static/videos/method.mp4` | 논문 Figure 2 |

## 교체 방법

`index.html`에서 `data-media-slot="cup"`, `"egg"`, `"wiping"`을 찾고 해당 div 안의 이미지와 `.slot-label`을 아래 형태로 바꿉니다. 기존 설명과 전체 영상 링크는 유지해도 됩니다.

```html
<video controls playsinline preload="metadata" poster="static/images/geometry.jpg"
       aria-label="Cup marking comparison">
  <source src="static/videos/cup-comparison.mp4" type="video/mp4">
</video>
```

실제 영상 추가 후 하단의 “Individual experiment clips will be added here” 및 관련 figcaption도 수정합니다. 자동 재생은 상단의 무음 미리보기에만 사용합니다.

## 원본과 출처

- 논문: `_2026__ICRA___FACE (2).pdf` → `static/pdfs/face-paper.pdf` (원본 그대로)
- 최종 영상: `ICRA27_3998_VI_i-2.mp4` → `static/videos/face-final.mp4` (재인코딩 없이 MP4 faststart 처리)
- 상단 미리보기: 최종 영상 00:48–00:58.2, 여섯 Success 표시가 모두 나온 마지막 프레임을 1초 고정한 후 반복하는 음소거 루프
- 각 이미지: `scripts/prepare_assets.py`에 원본 페이지·크롭 좌표·영상 시각 기록
- 수치: 논문 Table I / II. 컵 변형 20회, 표면 변화 30회, 달걀 25회에 대해 nominal 조건을 제외하여 집계
- 익명 저자 표기를 유지했으며, 저자 이름·게재 확정·코드 공개 일정은 추가하지 않았습니다.

본문은 영어이며, 이 파일은 초안 편집을 위한 한국어 메모입니다.
